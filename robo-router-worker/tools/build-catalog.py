"""Generate server-owned facts from tracked curriculum, never execute page JavaScript."""
import ast,html,json,re,subprocess
from pathlib import Path
from html.parser import HTMLParser
ROOT=Path(__file__).resolve().parents[2]
OUTPUT=ROOT/'robo-router-worker/src/lessons.json'
class Facts(HTMLParser):
 def __init__(self):super().__init__();self.depth=0;self.capture=[];self.chunks=[]
 def handle_starttag(self,tag,attrs):
  attrs=dict(attrs)
  if tag not in ['meta','link','img','br','input','hr','source']:self.depth+=1
  if tag=='title' or attrs.get('id') in ['kp','b1Text','b2Text','c1Text'] or any(c in attrs.get('class','').split() for c in ['key-phrase','key-sentence','key-text','key-eng','grammar-title']):self.capture.append(self.depth)
 def handle_endtag(self,tag):
  if self.capture and self.capture[-1]==self.depth:self.capture.pop()
  self.depth=max(0,self.depth-1)
 def handle_data(self,data):
  if self.capture:self.chunks.append(data)
def context(text):
 values=[]
 for name in ['GB_BOOK','GB_BOOK_TITLE','GB_AUTHOR','GB_KEY_SENTENCE','GB_WEEK','GB_EP','GB_TOPIC']:
  match=re.search(r'var\s+'+name+r'''\s*=\s*((?:'(?:\\.|[^'\\])*')|(?:"(?:\\.|[^"\\])*"))\s*;''',text)
  if match:
   try:value=ast.literal_eval(match.group(1))
   except (ValueError,SyntaxError):continue
   if value and value not in values:values.append(value)
 for match in re.finditer(r"\b(book|d1|d2|d3|grade|week|day)\s*:\s*((?:'(?:\\.|[^'\\])*')|(?:\"(?:\\.|[^\"\\])*\"))",text):
  try:value=ast.literal_eval(match.group(2))
  except (ValueError,SyntaxError):continue
  if value and value not in values:values.append(match.group(1)+': '+value)
 parser=Facts();parser.feed(text)
 values.extend(parser.chunks)
 return re.sub(r'\s+',' ',html.unescape(' | '.join(values))).strip()[:12000]
paths=subprocess.check_output(['git','ls-files','camp-a','camp-b','camp-c','grammar-camp'],cwd=ROOT,text=True).splitlines()
catalog={}
for path in paths:
 if not path.endswith('.html'):continue
 text=(ROOT/path).read_text()
 if 'cec-robo.cecenglishcamp.workers.dev/api/ai/chat/completions' not in text and 'window.CECTutor.request(' not in text:continue
 profile='grammar' if path.startswith('grammar-camp/') else path.split('/')[0]
 facts=context(text)
 if not facts:raise ValueError('Missing facts: '+path)
 catalog['/'+path]={'profile':profile,'context':facts}
OUTPUT.write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+'\n')
print('Catalog lessons:',len(catalog))
