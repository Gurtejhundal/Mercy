"""Reviewed study aids reject broken references without losing legacy notes."""
import copy
import json
from pathlib import Path
import tempfile
import unittest

from mercy.agent import validate_questions
from mercy.questions import make_questions
from mercy.scanner import scan_project
from mercy.studio import build_atlas


class StudyFormatTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        root = Path(self.temp.name)
        (root/'web').mkdir()
        (root/'web/app.py').write_text('from helper import answer\n')
        (root/'helper.py').write_text('def answer(): return 42\n')
        self.report = scan_project(root)
        self.q = make_questions(self.report)[0]
        self.ref = {'path':'web/app.py','line':1}
        self.q.update(viva_question='What does it do?', viva_answer='It asks a helper for an answer.',
                      components=[{'id':'screen','name':'Screen','description':'Accepts a request.',
                                   'files':['web/app.py'],'evidence':[self.ref]},
                                  {'id':'logic','name':'Logic','description':'Returns the answer.',
                                   'files':['helper.py'],'evidence':[{'path':'helper.py','line':1}]}],
                      directories=[{'path':'web','description':'Contains the interface code.','evidence':[self.ref]}],
                      demonstration=[{'action':'Inspect the app import.','expected':'It references the helper.','evidence':[self.ref]}],
                      flow={'nodes':[{'id':'start','label':'Ask for an answer','kind':'start','evidence':[self.ref]},
                                     {'id':'end','label':'Receive answer','kind':'end','evidence':[self.ref]}],
                            'edges':[{'source':'start','target':'end','evidence':[self.ref]}]})

    def test_component_connections_are_aggregated_from_real_imports_only(self):
        validate_questions(self.report,[self.q])
        atlas = build_atlas(self.report,[self.q])
        self.assertEqual(len(atlas['components']),2)
        self.assertEqual(len(atlas['component_edges']),1)
        edge = atlas['component_edges'][0]
        self.assertEqual((edge['source'],edge['target']),('screen','logic'))
        self.assertEqual(edge['imports'][0]['line'],1)
        self.assertEqual(atlas['flows'][0]['nodes'],self.q['flow']['nodes'])
        self.assertEqual(atlas['demonstrations'][0]['steps'],self.q['demonstration'])
        self.assertNotIn('heuristic',atlas['components'][0])

    def test_invalid_study_aids_are_rejected(self):
        variants=[]
        def variant(edit):
            q=copy.deepcopy(self.q);edit(q);variants.append(q)
        variant(lambda q:q.update(viva_answer='word '*46))
        variant(lambda q:q.update(viva_question='word '*15))
        variant(lambda q:q['components'][0].update(files=['missing.py']))
        variant(lambda q:q['components'][0]['evidence'][0].update(line=True))
        variant(lambda q:q['components'][1].update(id='screen'))
        variant(lambda q:q['components'][1].update(files=['web/app.py']))
        variant(lambda q:q['directories'][0].update(path='../web'))
        variant(lambda q:q['directories'][0].update(path='missing'))
        variant(lambda q:q['demonstration'][0].update(evidence=[]))
        variant(lambda q:q['flow']['edges'][0].update(target='missing'))
        variant(lambda q:q['flow']['edges'][0].update(source=[]))
        variant(lambda q:q['flow']['nodes'][0].update(kind='decision'))
        variant(lambda q:q['flow']['nodes'].append({'id':'orphan','kind':'action','label':'Orphan','evidence':[self.ref]}))
        variant(lambda q:q['flow'].update(edges=[]))
        for q in variants:
            with self.subTest(q=q),self.assertRaises(ValueError):validate_questions(self.report,[q])

    def test_decisions_need_labels_and_a_path_to_an_end(self):
        flow=self.q['flow']
        flow['nodes'].append({'id':'check','kind':'decision','label':'Valid?','evidence':[self.ref]})
        flow['edges']=[{'source':a,'target':b,'evidence':[self.ref],**({'label':label} if label else {})}
                       for a,b,label in [('start','check',None),('check','end','Yes'),('check','start','No')]]
        validate_questions(self.report,[self.q])
        del flow['edges'][1]['label']
        with self.assertRaisesRegex(ValueError,'branches need labels'):validate_questions(self.report,[self.q])

    def test_technology_sources_and_file_explanations_validate_and_survive_export(self):
        self.q['stack']=[{'id':'model','kind':'model','name':'Example model',
            'description':'Loads existing weights.', 'origin':'A named upstream project.',
            'logo':'huggingface', 'paths':['web','helper.py'], 'evidence':[self.ref],
            'resources':[{'label':'Model card','url':'https://huggingface.co/example/model'}]}]
        self.q['file_notes']=[{'path':'helper.py','description':'Returns the fixed answer.','evidence':[{'path':'helper.py','line':1}]}]
        validate_questions(self.report,[self.q]);atlas=build_atlas(self.report,[self.q])
        self.assertEqual(atlas['stack'],self.q['stack'])
        self.assertEqual(atlas['file_notes'],self.q['file_notes'])
        variants=[]
        def variant(edit):
            q=copy.deepcopy(self.q);edit(q);variants.append(q)
        for url in ['javascript:alert(1)','data:text/html,hello','file:///private','https://user:password@example.com','https://example.com/has space','https://example.com/\\evil']:
            variant(lambda q,url=url:q['stack'][0]['resources'][0].update(url=url))
        variant(lambda q:q['stack'][0].update(kind=[]))
        variant(lambda q:q['stack'][0].update(logo=[]))
        variant(lambda q:q['stack'][0].update(logo='unknown'))
        variant(lambda q:q['stack'][0].update(paths=['../web']))
        variant(lambda q:q['stack'][0].update(paths=['not-scanned']))
        variant(lambda q:q['stack'][0].update(evidence=[]))
        variant(lambda q:q['file_notes'][0].update(path='not-scanned.py'))
        variant(lambda q:q['file_notes'][0].update(description='word '*46))
        variant(lambda q:q['file_notes'].append(copy.deepcopy(q['file_notes'][0])))
        variant(lambda q:q['stack'].append(copy.deepcopy(q['stack'][0])))
        for q in variants:
            with self.subTest(q=q),self.assertRaises(ValueError):validate_questions(self.report,[q])

    def test_components_cannot_overlap_across_questions(self):
        second=copy.deepcopy(self.q);second['id']='SECOND'
        with self.assertRaisesRegex(ValueError,'IDs must be unique across'):
            validate_questions(self.report,[self.q,second])
        for c in second['components']:c['id']='other_'+c['id']
        with self.assertRaisesRegex(ValueError,'only one component'):
            validate_questions(self.report,[self.q,second])

    def test_component_markdown_and_text_companion_keep_reviewed_aids(self):
        from mercy.renderer import export_architecture, export_markdown
        out=Path(self.temp.name)/'architecture.md'
        export_architecture(self.report,out,[self.q])
        text=out.read_text()
        self.assertIn('N0["Screen"]',text)
        self.assertIn('N0 --> N1',text)
        self.assertNotIn('N0["web/app.py"]',text)
        export_markdown(self.report,[self.q],out)
        text=out.read_text()
        self.assertIn(self.q['viva_answer'],text)
        self.assertIn(self.q['answer'],text)
        self.assertIn('Inspect the app import.',text)
        self.assertIn('Ask for an answer → Receive answer',text)

    def test_legacy_questions_keep_full_answers_and_get_no_fabricated_flow(self):
        q=make_questions(self.report)
        atlas=build_atlas(self.report,q)
        self.assertTrue(all(c['heuristic'] for c in atlas['components']))
        self.assertEqual(atlas['flows'],[])
        self.assertEqual(atlas['demonstrations'],[])
        self.assertEqual(atlas['questions'],q)
        validate_questions(self.report,json.loads(json.dumps(q)))
