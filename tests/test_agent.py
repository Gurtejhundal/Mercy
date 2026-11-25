"""Native-agent tool checks; run with the Python standard library."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from mercy.agent import apply_review, source_context, validate_questions, next_question, review_progress
from mercy.questions import make_questions, make_guided_questions
from mercy.scanner import scan_project


class AgentToolsTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='mercy-agent-test-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)/'project'
        self.root.mkdir()
        (self.root/'main.py').write_text('from helper import answer\n\ndef main():\n    return answer()\n')
        (self.root/'helper.py').write_text('def answer():\n    return 42\n')
        self.out = Path(self.temp.name)/'output'
        self.out.mkdir()
        self.report = scan_project(self.root)
        self.questions = make_questions(self.report)
        self.source = self.out/'mercy-evidence.json'
        self.source.write_text(json.dumps({'report':self.report,'questions':self.questions}))
        self.review = self.out/'review.json'

    def question(self, id='SOURCE01'):
        return {'id':id,'category':'Architecture','difficulty':'Basic',
                'question':'What does main return?', 'answer':'It returns the helper result.',
                'explain_like_im_10':'It asks a helper for the answer.', 'status':'supported',
                'evidence':[{'path':'main.py','line':4}], 'verify_next':'Runtime remains untested.'}

    def patch(self, questions):
        self.review.write_text(json.dumps({'questions':questions}))

    def test_context_returns_numbered_source_without_executing_or_exposing_secrets(self):
        (self.root/'main.py').write_text('raise RuntimeError("DO_NOT_EXECUTE")\npassword="HIDDEN_VALUE"\n')
        (self.root/'.env').write_text('PRIVATE_ENV=KEEP_PRIVATE\n')
        data=source_context(self.root,path='main.py',start=1)
        self.assertEqual(data['matches'][0]['lines'][0]['line'],1)
        self.assertIn('DO_NOT_EXECUTE',data['matches'][0]['lines'][0]['text'])
        self.assertNotIn('HIDDEN_VALUE',json.dumps(data))
        self.assertNotIn('KEEP_PRIVATE',json.dumps(data))
        with self.assertRaises(ValueError): source_context(self.root,path='.env')

    def test_context_blocks_symlinks_traversal_and_nonindexed_paths(self):
        exterior=Path(self.temp.name)/'outside.py';exterior.write_text('NEVER_READ')
        (self.root/'link.py').symlink_to(exterior)
        directory=Path(self.temp.name)/'outside';directory.mkdir()
        (directory/'private.py').write_text('NEVER_READ_DIRECTORY')
        (self.root/'linked').symlink_to(directory,target_is_directory=True)
        for path in ['../outside.py',str(exterior),'link.py','linked/private.py','missing.py']:
            with self.subTest(path=path), self.assertRaises(ValueError):
                source_context(self.root,path=path)

    def test_context_search_and_bounds(self):
        result=source_context(self.root,query='answer',limit=1)
        self.assertEqual(len(result['matches']),1)
        self.assertEqual(source_context(self.root,query='unfindable_xyz')['matches'],[])
        excerpt=source_context(self.root,path='main.py',start=4)['matches'][0]
        self.assertEqual(excerpt['start'],4)
        self.assertEqual(excerpt['lines'][0]['text'],'    return answer()')
        for args in [{'query':'x','limit':0},{'query':'x','limit':13},{'path':'main.py','start':99},
                     {'query':'x','path':'main.py'},{'query':'the and'}]:
            with self.subTest(args=args),self.assertRaises(ValueError):source_context(self.root,**args)

    def test_review_replaces_and_adds_without_changing_snapshot(self):
        replacement=self.question(self.questions[0]['id']);new=self.question()
        self.patch([replacement,new])
        self.assertEqual(apply_review(self.source,self.review,self.root),2)
        result=json.loads(self.source.read_text())
        self.assertEqual(result['report'],self.report)
        self.assertEqual(result['questions'][0],replacement)
        self.assertEqual(result['questions'][-1],new)
        self.assertFalse(list(self.out.glob('.mercy-review-*')))

    def test_invalid_reviews_never_mutate_the_evidence_file(self):
        original=self.source.read_bytes()
        variants=[]
        q=self.question();q['evidence'][0]['line']=True;variants.append([q])
        q=self.question();q['evidence'][0]['path']='missing.py';variants.append([q])
        q=self.question();q['evidence'][0]['line']=999;variants.append([q])
        q=self.question();q['evidence']=[];variants.append([q])
        q=self.question();q['status']='verified';variants.append([q])
        variants.append([self.question(),self.question()])
        for questions in variants:
            self.patch(questions)
            with self.subTest(questions=questions),self.assertRaises(ValueError):
                apply_review(self.source,self.review,self.root)
            self.assertEqual(self.source.read_bytes(),original)
        self.review.write_text(json.dumps({'questions':[],'report':{}}))
        with self.assertRaises(ValueError):apply_review(self.source,self.review,self.root)
        self.assertEqual(self.source.read_bytes(),original)

    def test_failed_atomic_replace_keeps_original_and_cleans_temporary_file(self):
        self.patch([self.question()]);original=self.source.read_bytes()
        with patch('mercy.agent.os.replace',side_effect=OSError('simulated disk failure')):
            with self.assertRaises(OSError):apply_review(self.source,self.review,self.root)
        self.assertEqual(self.source.read_bytes(),original)
        self.assertFalse(list(self.out.glob('.mercy-review-*')))

    def test_same_length_source_change_and_new_files_invalidate_snapshot(self):
        self.patch([self.question()])
        helper=self.root/'helper.py';original=helper.read_text();helper.write_text(original.replace('42','43'))
        with self.assertRaisesRegex(ValueError,'Source changed'):apply_review(self.source,self.review,self.root)
        helper.write_text(original)
        (self.root/'added.py').write_text('print("new")\n')
        with self.assertRaisesRegex(ValueError,'inventory changed'):apply_review(self.source,self.review,self.root)

    def test_legacy_snapshot_requires_refresh_and_symlink_output_is_rejected(self):
        self.patch([self.question()])
        legacy=copy.deepcopy(self.report)
        for file in legacy['files']:file.pop('sha256')
        self.source.write_text(json.dumps({'report':legacy,'questions':self.questions}))
        with self.assertRaisesRegex(ValueError,'predates'):apply_review(self.source,self.review,self.root)
        link=self.out/'link.json';link.symlink_to(self.source)
        with self.assertRaisesRegex(ValueError,'symbolic'):apply_review(link,self.review,self.root)

    def test_cli_context_review_render_end_to_end(self):
        def run(*args):
            p=subprocess.run([sys.executable,'-m','mercy',*args],capture_output=True,text=True)
            self.assertEqual(p.returncode,0,p.stderr)
            return p
        context=json.loads(run('context','--project',str(self.root),'--path','main.py').stdout)
        question=self.question();question['evidence'][0]['line']=context['matches'][0]['lines'][-1]['line']
        self.patch([question])
        run('review','--project',str(self.root),'--input',str(self.source),'--review',str(self.review))
        run('render','--input',str(self.source))
        html=(self.out/'mercy-studio.html').read_text()
        self.assertIn(question['answer'],html)
        self.assertNotIn('<canvas',html)
        self.assertNotIn('Planetary Atlas',html)
        self.assertIn('id="knowledge-svg"',html)

    def test_empty_source_is_not_a_fabricated_line_one_citation(self):
        (self.root/'main.py').write_text('')
        report=scan_project(self.root)
        validate_questions(report,make_questions(report))
        q=self.question();q['evidence'][0]['line']=1
        with self.assertRaises(ValueError):validate_questions(report,[q])
        with self.assertRaisesRegex(ValueError,'no source lines'):
            source_context(self.root,path='main.py')

    def test_render_uses_same_proof_validation_as_review(self):
        question=self.question();question['evidence'][0]['line']=False
        self.source.write_text(json.dumps({'report':self.report,'questions':[question]}))
        result=subprocess.run([sys.executable,'-m','mercy','render','--input',str(self.source)],capture_output=True,text=True)
        self.assertNotEqual(result.returncode,0)
        self.assertFalse((self.out/'mercy-studio.html').exists())

    def guided(self):
        self.questions=make_guided_questions()
        self.source.write_text(json.dumps({'report':self.report,'questions':self.questions,
            'workflow':{'kind':'guided-v1','reviewed':{}}}))

    def test_guided_tasks_are_bounded_and_untouched_starters_cannot_pass(self):
        self.guided();task=next_question(self.source,self.root)
        self.assertFalse(task['ready_to_render'])
        self.assertEqual(task['progress']['reviewed'],0)
        self.assertEqual(len(task['review_template']['questions']),1)
        self.assertLessEqual(len(task['source_excerpts']),2)
        self.assertTrue(all(len(e['lines'])<=40 for e in task['source_excerpts']))
        returns=[line['text'] for e in task['source_excerpts'] for line in e['lines']
                 if line['text'].lstrip().startswith('return ')]
        self.assertTrue(returns)
        self.assertTrue(all(line.startswith('    ') for line in returns))
        self.assertEqual(len(task['progress']['pending']),10)
        original=self.source.read_bytes();self.patch(self.questions[:1])
        with self.assertRaisesRegex(ValueError,'starter explanations'):
            apply_review(self.source,self.review,self.root)
        self.assertEqual(self.source.read_bytes(),original)

    def test_guided_completion_tracks_edits_and_preserves_unknowns_and_missing_topics(self):
        self.guided()
        for q in self.questions:
            q['answer']='Inspected main.py and helper.py only; this fixture does not establish this topic.'
            q['explain_like_im_10']='Two small files do not give enough information for this question.'
            q['verify_next']='Inspect the implementation relevant to '+q['question']
        self.patch(self.questions);apply_review(self.source,self.review,self.root)
        task=next_question(self.source,self.root)
        self.assertTrue(task['ready_to_render'])
        self.assertEqual(task['progress']['not_verified'],10)
        data=json.loads(self.source.read_text())
        data['questions'][0]['answer']='A human has edited this explanation.'
        data['questions'].pop()
        self.source.write_text(json.dumps(data))
        progress=review_progress(data)
        self.assertEqual(progress['reviewed'],8)
        self.assertEqual(progress['total'],10)
        self.assertIn(self.questions[0]['id'],progress['pending'])
        self.assertIn(self.questions[-1]['id'],progress['pending'])
        (self.root/'helper.py').write_text('def answer():\n    return 43\n')
        with self.assertRaisesRegex(ValueError,'Source changed'):
            next_question(self.source,self.root)

    def test_guided_cli_next_and_human_edit_render_preserve_tracking(self):
        self.guided()
        command=[sys.executable,'-m','mercy']
        result=subprocess.run(command+['next','--input',str(self.source),'--project',str(self.root)],capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertEqual(json.loads(result.stdout)['progress']['state'],'needs_review')
        data=json.loads(self.source.read_text());data['questions'][0]['answer']='An editable answer survives regeneration.'
        self.source.write_text(json.dumps(data))
        rendered=subprocess.run(command+['render','--input',str(self.source)],capture_output=True,text=True)
        self.assertEqual(rendered.returncode,0,rendered.stderr)
        self.assertEqual(json.loads(self.source.read_text())['workflow'],data['workflow'])
        self.assertIn(data['questions'][0]['answer'],(self.out/'mercy-studio.html').read_text())
        refused=subprocess.run(command+['prepare','--guided','--project',str(self.root),'--out',str(self.out)],capture_output=True,text=True)
        self.assertNotEqual(refused.returncode,0)
        self.assertIn('already exists',refused.stderr)

    def test_review_respects_the_original_scan_budget(self):
        report=scan_project(self.root,max_files=1)
        questions=make_questions(report)
        self.source.write_text(json.dumps({'report':report,'questions':questions}))
        question=self.question();question['evidence']=[{'path':report['files'][0]['path'],'line':1}]
        self.patch([question])
        self.assertEqual(apply_review(self.source,self.review,self.root),1)


if __name__=='__main__': unittest.main()
