"""Readable evaluator questions. Evidence and uncertainty travel with every answer."""
from __future__ import annotations
from pathlib import Path


def _loc(hits, limit=3):
    return [{'path': e['path'], 'line': e['line']} for e in (hits or [])[:limit]]


GUIDE_TOPICS = [
    ('PURPOSE', 'Start here', 'What does this project do, and for whom?', 'readme project purpose'),
    ('ENTRY', 'Start here', 'How is this project started, and where does execution begin?', 'main cli manage app package pyproject'),
    ('DEPENDENCIES', 'Architecture', 'Which dependencies matter, and where are they used?', 'requirements package pyproject imports'),
    ('MODULES', 'Architecture', 'What are the important modules and their responsibilities?', 'src service core engine app'),
    ('WORKFLOW', 'Architecture', 'Trace one source-supported path from input to output.', 'main route handler process render'),
    ('VALIDATION', 'Data', 'How are inputs validated before use?', 'validate schema form input request'),
    ('STORAGE', 'Data', 'What is stored or loaded, and where?', 'storage model database file save load'),
    ('ERRORS', 'Quality', 'What happens when an operation fails?', 'error exception handler retry'),
    ('INTEGRATIONS', 'Architecture', 'Which external integrations exist, and what remains unverified?', 'client api provider llm integration'),
    ('LIMITS', 'Quality', 'What are the source-supported limits and verification gaps?', 'test limit warning safety'),
]


def make_guided_questions() -> list[dict]:
    return [{'id':'GUIDE_'+topic, 'category':category, 'difficulty':'beginner',
             'question':question, 'answer':'Not reviewed. Inspect source for this topic.',
             'explain_like_im_10':'Not reviewed. Add a plain-language explanation.',
             'status':'not_verified', 'evidence':[],
             'verify_next':'Inspect the suggested files; record exact citations or a concrete evidence gap.'}
            for topic,category,question,_ in GUIDE_TOPICS]


def make_questions(r: dict) -> list[dict]:
    s = r['signals']; fs = r['frameworks']; summary = r['summary']
    questions = []
    def add(category, level, q, answer, simple, proof=None, check=None):
        proof = proof or []
        questions.append({'id': f'Q{len(questions)+1:02}', 'category': category,
            'difficulty': level, 'question': q, 'answer': answer, 'explain_like_im_10': simple,
            'evidence': proof, 'status': 'supported' if proof else 'not_verified',
            'verify_next': check or ('' if proof else 'Ask the project owner and check README, deployment, or external services.')})
    def evidence(tag, limit=3):
        return _loc(s.get(tag, []), limit)
    tech = ', '.join(sorted(fs)) or 'No framework confirmed'
    tech_proof = []
    for k in sorted(fs)[:5]: tech_proof += _loc(fs[k], 1)
    files = [f['path'] for f in r['files'] if f['lines']]
    entry = [f['path'] for f in r['files'] if f['lines'] and (Path(f['path']).name.lower() in {'app.py','main.py','server.py','index.js','server.js','app.js','manage.py','package.json','pyproject.toml'} or f['path'].startswith('src/app/'))]
    entries = ', '.join(entry[:5]) if entry else 'No obvious entry point found'
    routes = [(f['path'], x) for f in r['files'] for x in f['routes']]
    route_proof = [{'path': p, 'line': x['line']} for p,x in routes[:3]]
    rname = r['project']
    add('Start here','Basic','What is this project?',
        f'The repository is called {rname}. The exact business goal must be confirmed from the owner or documentation; the code scan alone does not prove user outcomes.',
        'First explain the problem it solves, then who uses it, then what happens when they click a button.',
        check='Write a one-sentence problem statement and demonstrate the main feature.')
    add('Start here','Basic','What is your project tech stack?',
        f'Found these technology signals: {tech}. A detected import does not prove a service is configured or used in production.',
        'A tech stack is your toolbox: what builds the screen, what handles requests, and where data lives.', tech_proof,
        'Verify versions and running services in package manifests and deployment.')
    add('Start here','Basic','Show me where the application starts.',
        f'Likely starting files: {entries}. Confirm the start command before claiming any one is the actual entry point.',
        'An entry point is the front door. It is the first file started when the app runs.',
        [{'path': p, 'line': 1} for p in entry[:3]], 'Check README scripts or package.json and run the project.')
    add('Start here','Basic','Show the frontend and backend directories.',
        ('Files include: ' + ', '.join(files[:9]) + '. A folder name alone cannot prove which part runs on the server.'),
        'Frontend is what users see. Backend is what responds to requests and talks to data.',
        [{'path': f, 'line': 1} for f in files[:3]], 'Trace one UI request to one server handler.')
    add('Start here','Basic','Explain your project workflow from opening the app to getting a result.',
        f'Observed {summary["routes_found"]} route declarations and {summary["module_links"]} local module links. A full end-to-end workflow is not verified by static analysis alone.',
        'Tell the story: user -> screen -> request -> server -> database/model -> answer -> screen.', route_proof,
        'Run the app, click the main feature and watch its network requests.')
    add('Architecture','Basic','Show your software architecture.',
        f'Likely technology components are {tech}. Use the import map and actual route handlers to draw confirmed arrows.',
        'Architecture is a map of the rooms in your application and the doors between them.', tech_proof,
        'Trace at least one complete user action and draw only confirmed connections.')
    add('Architecture','Intermediate','Which module calls which other module?',
        ('Local references found: ' + '; '.join(f'{e["source"]} -> {e["target"]}' for e in r['edges'][:5])) if r['edges'] else 'No local imports could be resolved automatically.',
        'An import means one file can use code from another. That is not always a runtime call.',
        [{'path': e['source'], 'line': e['line']} for e in r['edges'][:3]],
        'Follow the imported function in the actual call sites.')
    add('Architecture','Intermediate','What are your API endpoints?',
        ('Found routes: ' + '; '.join(f'{x["path"]} in {p}' for p,x in routes[:8])) if routes else 'No HTTP route declaration was confidently located.',
        'An endpoint is a door the frontend knocks on to ask the server for something.', route_proof,
        'Inspect router registration and use a real HTTP request to verify these routes.')
    add('Architecture','Intermediate','What happens when the frontend sends a request?',
        ('Found HTTP handlers in ' + ', '.join(sorted({p for p,_ in routes})[:6])) if routes else 'No confirmed server handlers from this scan.',
        'A request is like ordering food: the screen asks, the server prepares, then sends a response.', route_proof,
        'Open browser DevTools Network and trace one request to the backend.')
    add('Architecture','Intermediate','What is the difference between frontend and backend?',
        'Frontend builds the screens that people use. Backend handles server-side logic, data and API requests. Your exact code split still requires tracing.',
        'Frontend = shop counter; backend = kitchen.', check='Identify two files from each side, if both exist.')
    add('Architecture','Intermediate','Where are business rules written?',
        'Look for functions that validate inputs, calculate values, or decide outcomes. Static import names cannot prove which functions contain the core rules.',
        'Business logic is the rulebook, not the paint on the screen.',
        [{'path': x['path'], 'line': x['symbols'][0]['line']} for x in r['files'] if x['symbols']][:3],
        'Follow one important function from input to return value.')
    add('Architecture','Advanced','What breaks if a service is down?',
        'Failure handling and deployed dependencies are not confirmed by static scanning.',
        'If the kitchen is closed, the shop should tell the customer instead of crashing.',
        check='Disconnect the API or database in a test environment and record the result.')
    add('Data','Basic','Where is your database?',
        ('Database-related code signals found in ' + ', '.join(sorted({x['path'] for x in s['database']})[:5])) if s.get('database') else 'No database connection was proven in the inspected code.',
        'A database is the app’s organized notebook. An SDK import is not the same as a running database.', evidence('database'),
        'Locate connection config, schema, migrations and deployment provider.')
    add('Data','Intermediate','Show your database tables or collections.',
        'The scanner does not execute migrations or query databases, so it cannot establish the live schema.',
        'Tables are like named pages in a notebook; columns are the headings.',
        check='Open migrations/schema and compare with the actual database.')
    add('Data','Intermediate','How does data travel through your system?',
        f'The scan located {summary["routes_found"]} routes, {len(r["datasets"])} data-shaped files and {summary["module_links"]} module links. These are clues, not a verified complete data pipeline.',
        'Follow one piece of data from where it enters until you see the result.', route_proof,
        'Trace and document one real input all the way through.')
    add('Data','Intermediate','How do you validate user input?',
        'Input validation is not established by a basic repository scan.',
        'Validation is checking a form before accepting it, like rejecting an impossible age.',
        check='Show the exact schema or condition and test invalid input.')
    add('Data','Intermediate','How do you handle errors and bad requests?',
        'Error handling must be checked in actual route handlers and through tests.',
        'When something fails, the program should say what went wrong instead of dying.',
        check='Try missing fields, invalid IDs and unavailable services.')
    add('Data','Advanced','How do you prevent SQL injection?',
        'The audit does not certify that queries are parameterized or safe.',
        'Never glue untrusted user text into a database command.',
        check='Inspect query construction and verify parameterized queries or safe ORM calls.')
    add('AI/ML','Basic','Did you train the model yourself?',
        ('I found possible training operations, but their presence alone does not prove a completed model was trained.' if s.get('training') else
         'I did not find direct model-training steps in the inspected code. Do not claim the model was trained here.'),
        'Calling an AI API is like using someone else’s already-trained calculator. Training means teaching a model with data.', evidence('training'),
        'Find actual training script, data split, trained weights and run logs if claiming training.')
    add('AI/ML','Basic','Where did you get the dataset? Show it.',
        ('Data-shaped files: ' + ', '.join(d['path'] for d in r['datasets'][:7]) + '. Their actual role is not confirmed.' if r['datasets'] else
         'No local dataset file was found in the inspected files. It might be remote, generated or absent; verify before answering.'),
        'A dataset is examples a model learns from or looks things up in. One CSV file does not automatically mean training.',
        ([{'path': x['path'], 'line': 1} for x in r['datasets'][:3]] + evidence('dataset_loader',2)),
        'Identify the precise dataset source, license, sample rows and where it is loaded.')
    add('AI/ML','Intermediate','Where is the model saved?',
        'Static inspection did not verify a trained model checkpoint or the hosted model behind any API.',
        'A model file is like a saved brain; an API can use a brain hosted on someone else’s computer.',
        check='Find a real model checkpoint, model name or provider configuration.')
    add('AI/ML','Basic','What is an AI model?',
        'An AI model is a program whose behaviour is shaped by learned patterns or parameters, rather than only hard-coded rules.',
        'Think of a model like a student who learned from many examples.')
    add('AI/ML','Basic','Are you using an AI API or your own ML model?',
        (('Found API/SDK usage in ' + ', '.join(sorted({x['path'] for x in s['llm_api']})[:5]) + '. This suggests externally provided model access, not proof of self-training.') if s.get('llm_api') else
         'No clear AI API call was identified. This does not prove there is no model: look for wrappers and external services.'),
        'API = you send a question to someone else’s service. Local model = the model runs in your own system.', evidence('llm_api'),
        'Check model initialization and where inference actually executes.')
    add('AI/ML','Intermediate','What is inference?',
        'Inference means using an already-prepared model to produce a prediction or response.',
        'Training is studying; inference is answering the exam.')
    add('AI/ML','Intermediate','What is RAG? Does your project use it?',
        ('Retrieval-related code detected. It may be a RAG system; confirm that retrieved text is actually passed to a generative model.' if s.get('rag') else
         'RAG was not established from this repository scan. Do not claim RAG simply because an LLM is present.'),
        'RAG = look up relevant notes first, then ask an AI to answer using those notes.', evidence('rag'),
        'Show a retrieval step AND where its results enter the model prompt.')
    add('AI/ML','Intermediate','Explain a RAG pipeline step by step.',
        'A typical RAG flow is: load documents -> split text -> create embeddings -> store vectors -> retrieve useful chunks -> include chunks in a prompt -> generate an answer. Actual steps depend on the project.',
        'It is an open-book test: find pages, read them, then answer. Do not call this your implemented flow until you prove each step.', evidence('rag')+evidence('embeddings',1),
        'Locate the exact implementation of each stage or mark it not implemented.')
    add('AI/ML','Intermediate','What are embeddings?',
        ('Embedding-related code markers exist; check where vectors are generated and stored.' if s.get('embeddings') else
         'No embedding pipeline was confirmed.'),
        'An embedding turns text into a list of numbers so similar meanings can be compared.', evidence('embeddings'),
        'Find the exact embedding model and vector dimension if used.')
    add('AI/ML','Intermediate','What is a vector database? Do you use one?',
        ('Retrieval/vector-storage clues were found; their presence alone does not confirm a working vector database.' if s.get('rag') else
         'No vector store was proven by this scan.'),
        'A vector database is a special library shelf that finds meaning-similar notes.', evidence('rag'),
        'Name the actual store, collection, persistence and retrieval call.')
    add('AI/ML','Intermediate','What is chunking and why use it?',
        ('Chunking configuration or calls were found.' if s.get('chunking') else
         'No explicit document chunking step was confirmed.'),
        'Chunking means cutting a long book into smaller pages, so finding the right part is easier.', evidence('chunking'),
        'Show chunk size, overlap, and why these values were chosen.')
    add('AI/ML','Advanced','How do you reduce hallucinations in the AI answer?',
        'No reliability evaluation was verified. RAG and citations can help grounding but do not guarantee correct answers.',
        'A hallucination is when AI confidently makes something up. Make it show the source.', evidence('rag',1),
        'Test a set of answerable and unanswerable questions and measure grounded correctness.')
    add('AI/ML','Advanced','How do you evaluate model accuracy?',
        ('Evaluation metric calls were detected, but a measured score or test dataset is not verified.' if s.get('metrics') else
         'No evaluation metrics were located. Do not invent accuracy percentages.'),
        'Accuracy asks: out of many known-answer questions, how many answers were right?', evidence('metrics'),
        'Provide a held-out test set, metric definition and reproducible result.')
    add('AI/ML','Advanced','What is overfitting?',
        'Overfitting happens when a model learns the training examples too specifically and performs worse on new examples.',
        'Like memorizing exam answers but not understanding the subject.')
    add('AI/ML','Advanced','What is fine-tuning versus prompting?',
        'Prompting changes the instructions sent to a model. Fine-tuning updates model parameters through training. Neither is confirmed without evidence.',
        'Prompting tells the student what to do; fine-tuning gives the student extra lessons.')
    add('Security','Intermediate','Where is authentication implemented?',
        ('Auth-related code clues found in ' + ', '.join(sorted({x['path'] for x in s['auth']})[:5]) + '; actual login protection must be tested.' if s.get('auth') else
         'No clear authentication implementation was confirmed.'),
        'Authentication checks who you are. Authorization checks what you may access.', evidence('auth'),
        'Show login, token/session validation and a protected endpoint.')
    add('Security','Intermediate','Where are secrets and API keys stored?',
        ('Environment variable names found: ' + ', '.join(r['environment_variables'][:10]) if r['environment_variables'] else
         'No environment variable names detected in scanned source; secrets were not read.'),
        'Secrets are house keys. Do not put them in a public repository or a viva PDF.',
        check='Verify secrets are server-side and not checked into version control.')
    add('Security','Advanced','Can one user read another user’s data?',
        'Object-level authorization cannot be proven without tracing identity checks at each data-access route.',
        'Knowing the house address does not mean someone should get the key.',
        check='Test access to another user’s ID in a controlled test environment.')
    add('Security','Advanced','What happens if an attacker sends malicious input?',
        'No penetration test was run by Mercy. Treat security as unverified until tested.',
        'Bad input should be rejected or treated as plain text, not followed as instructions.',
        check='Review input boundaries and test with safe invalid inputs.')
    add('Quality','Basic','How many tests does this project have?',
        f'Found {summary["tests_found"]} files with test-like names. This is not a test pass result or a coverage percentage.',
        'Tests are practice questions for your software. Counting them does not tell you if it passed.',
        [{'path': f['path'], 'line': 1} for f in r['files'] if f['lines'] and 'test' in f['path'].lower()][:3],
        'Run the project test command and save the result.')
    add('Quality','Intermediate','What are the limitations of your project?',
        'Known verification gaps: ' + '; '.join(r['warnings'][:3]) + '. There may be other runtime limitations not visible in code.',
        'A limitation is something your current project cannot reliably do yet.',
        check='Write down three issues observed in real usage, not guesses.')
    add('Quality','Intermediate','How do you handle performance or high traffic?',
        'No load or latency benchmark was run. Architecture alone does not prove scaling ability.',
        'Can the kitchen handle 100 orders at once? Measure instead of guessing.',
        check='Run a small controlled load test and record latency, error rate and resource use.')
    add('Deployment','Basic','Where is the project deployed?',
        ('Deployment-related code found, but the actual live URL and running infrastructure are not verified.' if s.get('deployment') else
         'No deployed service was confirmed.'),
        'Deployment means putting the app on a computer/server where others can open it.', evidence('deployment'),
        'Show the real deployed URL, hosting dashboard and production start command.')
    add('Deployment','Intermediate','How does a new change reach production?',
        'No confirmed deployment pipeline was executed. Check CI configuration and actual production settings.',
        'A deployment pipeline is the delivery route from your laptop to a live website.', evidence('deployment',1),
        'Walk through an actual commit, build, test and deploy log.')
    add('Deployment','Advanced','What would you improve next?',
        'Prioritize measured limitations, missing tests and unclear architecture before adding unnecessary features.',
        'Fix broken doors before building another floor.',
        check='Pick a real observed limitation and explain how you would verify the fix.')
    add('Defense','Intermediate','Which part did you personally implement?',
        'Personal contribution cannot be established from repository code or Git history alone.',
        'Say what you wrote, what a tool generated, and what you tested. Do not claim someone else’s work.',
        check='Select two pieces of code you can explain line by line.')
    add('Defense','Advanced','If you remove the LLM, what still works?',
        'This requires a runtime dependency test; any detected AI SDK only gives a clue.',
        'Pretend the AI service is offline. What parts of the app still work?', evidence('llm_api',1),
        'Disable external AI access in a local test and observe which features fail.')
    add('Defense','Advanced','Can you change one feature now and show exactly where?',
        'Use the dependency map to locate the responsible function, then explain how it is called and tested.',
        'Showing a real small change proves you understand the project better than memorizing a speech.',
        [{'path': x['path'], 'line': x['symbols'][0]['line']} for x in r['files'] if x['symbols']][:3],
        'Pick a small input/label/validation rule and practice modifying it safely.')
    for path, route in routes[:6]:
        filename = next((f for f in r['files'] if f['path']==path), {})
        handler = next((symbol for symbol in filename.get('symbols',[])
                        if route['line'] < symbol['line'] <= route['line']+4), None)
        name = handler['name'] if handler else 'the route handler'
        proof = [{'path':path,'line':route['line']}]
        if handler: proof.append({'path':path,'line':handler['line']})
        add('Code-specific follow-ups','Intermediate',
            f'Where is endpoint {route["path"]} implemented, and what does it do?',
            f'{route["path"]} is declared in {path}:{route["line"]}; the likely handler is {name}. Its full behavior still requires reading the function body.',
            'An endpoint is a door. Find the person standing behind that door and ask what happens next.',
            proof, 'Follow calls inside the handler and verify the real response.')
    for e in r['edges'][:6]:
        add('Code-specific follow-ups','Intermediate',
            f'Why does {e["source"]} import {e["target"]}?',
            f'{e["source"]}:{e["line"]} imports {e["via"]}, which resolves to {e["target"]}. This proves a reference, not that every exported function is called.',
            'One file borrows a tool from another file. Point at the borrowing line and find where the tool is actually used.',
            [{'path':e['source'],'line':e['line']}],
            'Find the exact call site and show the input and output.')
    return questions


def import_user_pyqs(path: str, existing: list[dict]) -> list[dict]:
    """Add externally provided questions without pretending they are authenticated PYQs."""
    import re
    from pathlib import Path
    source=Path(path)
    if source.suffix.lower() not in {'.md','.txt'}:
        raise ValueError('PYQ input must be .txt or .md plain text.')
    if source.stat().st_size > 100_000:
        raise ValueError('PYQ file is too large; limit is 100 KB.')
    raw=source.read_text(encoding='utf-8')
    prompts=[]
    for line in raw.splitlines():
        prefix = re.match(r'^\s*(?:[-*]\s+|Q(?:uestion)?\s*\d*\s*[:.)-]\s*|\d+[.)-]\s*)',line, flags=re.IGNORECASE)
        text = line[prefix.end():].strip() if prefix else line.strip()
        if text and (prefix or text.endswith('?')) and len(text)<500:
            prompts.append(text)
        if len(prompts)>=75:
            break
    additions=[]
    for question in prompts:
        matched=next((q for q in existing if q['question'].strip().casefold()==question.casefold()),None)
        additions.append({'id':f'PYQ{len(additions)+1:02}', 'category':'User-supplied past questions',
            'difficulty':matched['difficulty'] if matched else 'Needs review',
            'question':question,
            'answer':matched['answer'] if matched else 'This question was supplied by the user. Mercy cannot confirm the answer from this wording alone; trace the relevant source code before presenting an answer.',
            'explain_like_im_10':matched['explain_like_im_10'] if matched else 'Find the file that does this job, show the input, describe the steps, and say what comes out.',
            'evidence':matched['evidence'] if matched else [],
            'status':matched['status'] if matched else 'not_verified',
            'verify_next':'Question authenticity and any unmatched answer need checking; student supplied this file.'})
    return additions
