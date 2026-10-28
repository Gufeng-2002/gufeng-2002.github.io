"""Render presentation-only notebooks. No notebook code is ever executed."""
from pathlib import Path
import argparse,json,shutil,re,runpy
import markdown
R=Path(__file__).resolve().parent
parser=argparse.ArgumentParser();parser.add_argument('--base',default='');args=parser.parse_args()
def render(path):
 n=json.loads(path.read_text());parts=[]
 for c in n['cells']:
  if c['cell_type']!='markdown':raise ValueError(f'{path}: only Markdown cells are allowed; remove code/raw cells.')
  parts.append(''.join(c['source']))
 text='\n\n'.join(parts);math=[]
 def protect(m):
  math.append(m.group());return f'MATHPLACEHOLDER{len(math)-1}END'
 text=re.sub(r'\$\$[\s\S]*?\$\$|(?<!\$)\$(?!\$)[^\n$]+\$',protect,text)
 out=markdown.markdown(text,extensions=['tables','fenced_code'])
 for i,m in enumerate(math):out=out.replace(f'MATHPLACEHOLDER{i}END',m)
 return out
catalog=json.loads((R/'site.json').read_text());records=[]
for p in catalog['projects']:
 slug=p['slug']
 if not re.fullmatch('[a-z0-9]+(?:-[a-z0-9]+)*',slug):raise ValueError('Invalid project slug')
 text=render(R/'projects'/slug/'index.ipynb')
 # Layout supplies the project title.
 text=re.sub(r'^<h1>.*?</h1>','',text,count=1,flags=re.S)
 records.append({**p,'content':text})
home=render(R/'pages/home.ipynb');about=render(R/'pages/about.ipynb')
# Validate inputs before touching generated output.
if (R/'dist').exists():shutil.rmtree(R/'dist')
(R/'dist').mkdir();(R/'content').mkdir(exist_ok=True)
(R/'content/projects.json').write_text(json.dumps(records,ensure_ascii=False))
layout=runpy.run_path(str(R/'template/layout.py'))
page=layout['page'];save=layout['save']
save(Path('index.html'),page('Home',home+'<div class="notice">Illustrative demo projects · A presentation-only notebook website.</div>'+layout['rows']()))
save(Path('about/index.html'),page('About',about,'about'))
for name in ['style.css','site.js']:shutil.copy(R/'template'/name,R/'dist'/name)
for p in records:
 src=R/'projects'/p['slug']/'assets'
 if src.exists():shutil.copytree(src,R/'dist/projects'/p['slug']/'assets',dirs_exist_ok=True)
# A public example of the same Markdown-only project template.
template=render(R/'templates/new-project/index.ipynb')
save(Path('projects/project-template/index.html'),page('Project template',template,'projects',True))
mathjax='''<script>window.MathJax={tex:{inlineMath:[['$','$']],displayMath:[['$$','$$']]}};</script><script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js"></script>'''
for f in (R/'dist').rglob('*.html'):
 text=f.read_text().replace('</head>',mathjax+'</head>')
 if args.base:text=re.sub(r'(href|src)="/(?!/)',lambda m:m.group(1)+'="/'+args.base.strip('/')+'/',text)
 f.write_text(text)
print('Website built in dist/. Markdown only; no notebooks executed. Nothing uploaded.')
