// Logic checks with a small DOM double; layout and actual browser input need visual QA.
const {test}=require('node:test');
const assert=require('node:assert/strict');
const {readFileSync}=require('node:fs');
const {join}=require('node:path');
const vm=require('node:vm');
const root=join(__dirname,'..');
const template=readFileSync(join(root,'mercy/assets/studio.html'),'utf8');
const sample=readFileSync(join(root,'output-galaxy/mercy-studio.html'),'utf8');
const atlas=JSON.parse(sample.match(/<script type="application\/json" id="atlas-data">([\s\S]*?)<\/script>/)[1]);
function mount(data=atlas,reduced=false){
  class Element{
    constructor(tag='div'){this.tagName=tag;this.children=[];this.attrs={};this.dataset={};this.style={setProperty(){}};this.value='';this.events={};this.className='';this._text='';this.clientWidth=760;this.scrollLeft=0;this.scrollTop=0;this.classList={contains:c=>this.className.split(' ').includes(c),toggle:(c,on)=>{const set=new Set(this.className.split(' ').filter(Boolean));if(on===undefined)on=!set.has(c);if(on)set.add(c);else set.delete(c);this.className=[...set].join(' ')},add:c=>this.classList.toggle(c,true),remove:c=>this.classList.toggle(c,false)};}
    setAttribute(k,v){this.attrs[k]=String(v);if(k==='class')this.className=String(v);if(k.startsWith('data-'))this.dataset[k.slice(5).replace(/-([a-z])/g,(_,c)=>c.toUpperCase())]=String(v)}
    getAttribute(k){return this.attrs[k]}
    get parentElement(){return this.parent}
    removeAttribute(k){delete this.attrs[k]}
    set textContent(t){this._text=String(t);this.children=[]}
    get textContent(){return this._text+this.children.map(x=>typeof x==='string'?x:x.textContent).join('')}
    appendChild(e){e.parent=this;this.children.push(e);return e}
    append(e){this.children.push(e)}
    replaceChildren(){this.children=[];this._text=''}
    addEventListener(type,fn){this.events[type]=fn}
    click(){const e={target:this,preventDefault(){},stopPropagation(){}};this.onclick?.(e);this.events.click?.(e)}
    focus(){document.activeElement=this}
    scrollIntoView(){}
    scrollTo(p){this.scrollLeft=p.left;this.scrollTop=p.top}
    closest(s){return matches(this,s)?this:this.parent?.closest(s)}
    setPointerCapture(){}
    getBoundingClientRect(){return {width:760,height:505}}
    getContext(){return new Proxy({createRadialGradient:()=>({addColorStop(){}})},{get:(o,k)=>k in o?o[k]:()=>{}})}
    querySelectorAll(selector){return this.children.flatMap(x=>typeof x==='string'?[]:[...(matches(x,selector)?[x]:[]),...x.querySelectorAll(selector)])}
  }
  function matches(el,s){if(s[0]==='.')return el.classList.contains(s.slice(1));const m=s.match(/^\[([^=\]]+)(?:="([^"]+)")?\]$/);return m?el.attrs[m[1]]!==undefined&&(m[2]===undefined||el.attrs[m[1]]===m[2]):false}
  const nodes=new Map();
  for(const m of template.matchAll(/<([\w-]+)\b([^>]*\bid="([^"]+)"[^>]*)>/g)){const el=new Element(m[1]);for(const a of m[2].matchAll(/([\w-]+)="([^"]*)"/g))el.setAttribute(a[1],a[2]);nodes.set(m[3],el)}
  const nav=[];for(const m of template.matchAll(/<button([^>]*data-(?:section|go)="[^"]+"[^>]*)>([\s\S]*?)<\/button>/g)){const el=new Element('button');for(const a of m[1].matchAll(/([\w-]+)="([^"]*)"/g))el.setAttribute(a[1],a[2]);el.textContent=m[2].replace(/<[^>]+>/g,'');nav.push(el)}
  const document={documentElement:new Element('html'),getElementById:id=>nodes.get(id),createElement:t=>new Element(t),createElementNS:(_,t)=>new Element(t),addEventListener(){},querySelectorAll:s=>[...nodes.values(),...nav].flatMap(x=>[...(matches(x,s)?[x]:[]),...x.querySelectorAll(s)]),querySelector:s=>document.querySelectorAll(s)[0]};
  nodes.get('atlas-data').textContent=JSON.stringify(data);
  const frames=new Map();let next=0,time=0;
  const context=vm.createContext({document,window:{matchMedia:q=>({matches:q.includes('reduced-motion')?reduced:false,addEventListener(){}}),scrollTo(){},devicePixelRatio:1},ResizeObserver:class{observe(){}},requestAnimationFrame:fn=>{frames.set(++next,fn);return next},performance:{now:()=>time},console});
  const run=code=>vm.runInContext(code,context);
  run(template.match(/<script>([\s\S]*?)<\/script>/)[1]);
  return {run,nodes,document,frames,flush(count=1){for(let i=0;i<count;i++){time+=16;const pending=[...frames.values()];frames.clear();pending.forEach(fn=>fn(time))}}};
}
test('mind map expands subjects into real questions, preserves focus, opens evidence',()=>{
  const ui=mount();ui.run("showSection('keymap')");const svg=ui.nodes.get('knowledge-svg'),category=atlas.questions[0].category;
  assert.equal(svg.querySelectorAll('.mind-node').length,new Set(atlas.questions.map(q=>q.category)).size+1);
  const subject=svg.querySelectorAll('.mind-node').find(x=>x.dataset.mindKey===category);subject.click();
  const expanded=svg.querySelectorAll('.mind-node').find(x=>x.dataset.mindKey===category);assert.equal(expanded.getAttribute('aria-expanded'),'true');assert.equal(ui.document.activeElement,expanded);
  const question=svg.querySelectorAll('.mind-node').find(x=>x.dataset.mindKey===atlas.questions[0].id);question.click();assert.ok(ui.nodes.get('mind-detail').textContent.includes(atlas.questions[0].answer));
  const cited=atlas.questions.find(q=>q.evidence.length);ui.run(`selectMindQuestion(ATLAS.questions.find(q=>q.id===${JSON.stringify(cited.id)}))`);ui.nodes.get('mind-detail').querySelectorAll('.evidence-button')[0].click();assert.equal(ui.run('lastFile'),cited.evidence[0].path);assert.equal(ui.run('currentSection'),'architecture');
  ui.run("showSection('keymap')");ui.nodes.get('mind-reset').click();assert.equal(ui.run('MIND.expanded.size'),0);
});
test('question navigation clears stale categories and text stays inert',()=>{
  const data=structuredClone(atlas);data.questions[0].question='<img src=x onerror=alert(1)>';const ui=mount(data);ui.run("qCategory='missing';renderCategories();renderQuestions();fileDetails(ATLAS.questions.find(q=>q.evidence.length).evidence[0].path)");
  ui.nodes.get('arch-detail').querySelectorAll('.evidence-button').find(x=>x.textContent.startsWith('Q')).click();assert.equal(ui.run('qCategory'),'All');assert.ok(ui.nodes.get('question-list').children.length);
  ui.run('selectMindQuestion(ATLAS.questions[0])');assert.ok(ui.nodes.get('mind-detail').textContent.includes(data.questions[0].question));assert.equal(ui.nodes.get('mind-detail').children.find(x=>x.tagName==='h3').children.length,0);
});
test('empty reports have working empty states without canvas animation',()=>{
  const data=structuredClone(atlas);Object.assign(data,{files:[],clusters:[],edges:[],crossings:[],questions:[],routes:[]});const ui=mount(data);ui.flush();ui.run("showSection('keymap');showSection('architecture');showSection('flow')");assert.ok(ui.nodes.get('flow-canvas').textContent.includes('No scanned files'));
  assert.equal(ui.run('currentSection'),'flow');assert.equal(ui.frames.size,0);
});

test('map zoom, fit and background pan update the scroll surface',()=>{
  const ui=mount();ui.run("showSection('keymap')");const svg=ui.nodes.get('knowledge-svg'),before=Number(svg.getAttribute('width'));ui.nodes.get('mind-in').click();assert.ok(Number(svg.getAttribute('width'))>before);ui.nodes.get('mind-out').click();assert.equal(Number(svg.getAttribute('width')),before);ui.nodes.get('mind-fit').click();assert.ok(Number(svg.getAttribute('width'))<=760);const v=ui.nodes.get('mind-viewport');v.onpointerdown({target:svg,clientX:200,clientY:200,pointerId:1,preventDefault(){}});v.onpointermove({clientX:120,clientY:130});assert.equal(v.scrollLeft,80);assert.equal(v.scrollTop,70);v.onpointerup();
});
test('architecture selection survives pointer capture while dragging does not select',()=>{
  const ui=mount();ui.run("showSection('architecture')");const svg=ui.nodes.get('arch-svg'),file=svg.querySelectorAll('.graph-file')[0],rect=file.children[0];svg.onpointerdown({target:rect,clientX:30,clientY:40,pointerId:1});svg.onpointerup();assert.equal(ui.run('lastFile'),file.dataset.path);ui.run('lastFile=null');svg.onpointerdown({target:rect,clientX:30,clientY:40,pointerId:2});svg.onpointermove({clientX:70,clientY:90});svg.onpointerup();assert.equal(ui.run('lastFile'),null);
});

test('project guide keeps complete answers, source lines and sequential reading',()=>{
  const data=structuredClone(atlas);
  const cited=data.questions.find(q=>q.evidence.length);
  data.questions[0].answer='A project-specific explanation that must survive rendering.';
  const ui=mount(data);
  assert.ok(ui.nodes.get('project-purpose').textContent.includes(data.questions[0].answer));
  assert.ok(ui.nodes.get('guide-reader').textContent.includes(data.questions[0].explain_like_im_10));
  const chapters=ui.nodes.get('guide-contents').querySelectorAll('.chapter-question');
  assert.equal(chapters.length,data.questions.length);
  chapters.find(b=>b.dataset.question===cited.id).click();
  assert.ok(ui.nodes.get('guide-reader').textContent.includes(cited.answer));
  assert.equal(ui.document.activeElement,ui.nodes.get('guide-reader'));
  ui.nodes.get('guide-reader').querySelectorAll('.evidence-button')[0].click();
  assert.ok(ui.nodes.get('arch-detail').textContent.includes(cited.evidence[0].path+':'+cited.evidence[0].line));
  ui.run('readGuide(0)');
  const controls=ui.nodes.get('guide-reader').querySelectorAll('.tiny');
  assert.equal(controls[0].disabled,true);
  controls[1].click();
  assert.equal(ui.run('guideIndex'),1);
  assert.ok(ui.nodes.get('guide-reader').textContent.includes(data.questions[1].answer));
});

test('all gaps and scanner notes stay available, and symbol metadata is visible',()=>{
  const data=structuredClone(atlas);
  data.warnings=Array.from({length:9},(_,i)=>'Scan note '+i);
  const ui=mount(data);
  assert.ok(ui.nodes.get('warnings').textContent.includes('Scan note 8'));
  assert.equal(ui.nodes.get('question-gaps').children.length,data.questions.filter(q=>q.verify_next||q.status==='not_verified').length);
  const file=data.files.find(f=>f.symbols.length);
  ui.run(`fileDetails(${JSON.stringify(file.path)})`);
  assert.ok(ui.nodes.get('arch-detail').textContent.includes(file.symbols[0].name));
  assert.ok(ui.nodes.get('arch-detail').textContent.includes('Heuristic role:'));
});

test('question evidence filter, source search and reveal state work together',()=>{
  const ui=mount();const filter=ui.nodes.get('q-status');
  filter.value='not_verified';filter.events.change();
  assert.equal(ui.nodes.get('question-list').children.length,atlas.questions.filter(q=>q.status==='not_verified').length);
  filter.value='all';const q=atlas.questions.find(q=>q.evidence.length);
  ui.nodes.get('q-search').value=q.evidence[0].path;ui.nodes.get('q-search').events.input();
  assert.ok(ui.nodes.get('question-list').children.length>0);
  const toggle=ui.nodes.get('question-list').querySelectorAll('.tiny')[0];
  assert.equal(toggle.getAttribute('aria-expanded'),'true');toggle.click();
  assert.equal(toggle.getAttribute('aria-expanded'),'false');
  assert.ok(toggle.getAttribute('aria-controls').startsWith('answer-'));
});

test('legacy and empty question banks render without new metadata',()=>{
  const data=structuredClone(atlas);delete data.framework_evidence;
  data.questions=[];const ui=mount(data);
  assert.ok(ui.nodes.get('guide-reader').textContent.includes('No questions'));
  assert.ok(ui.nodes.get('project-purpose').textContent.includes('No project explanation'));
});

test('guided report shows review records without promising correct answers',()=>{
  const data=structuredClone(atlas);
  data.review={state:'needs_review',reviewed:3,total:10};
  const ui=mount(data);const banner=ui.nodes.get('review-state');
  assert.equal(banner.hidden,false);
  assert.ok(banner.textContent.includes('Guided draft'));
  assert.ok(banner.textContent.includes('3/10'));
  assert.ok(banner.textContent.includes('not correctness'));
});
