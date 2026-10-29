# Reads images/manifest.tsv: slug<TAB>source_url (a product page or a direct image URL)
# Writes images/out/<slug>.jpg (800x800 on cream, centred) and images/log.tsv
import csv, io, os, re, sys, requests
from bs4 import BeautifulSoup
from PIL import Image
UA={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36','Accept-Language':'en-US,en;q=0.9'}
os.makedirs('images/out',exist_ok=True)
log=[]
def find_img(url):
    r=requests.get(url,headers=UA,timeout=25); r.raise_for_status()
    ct=r.headers.get('content-type','')
    if ct.startswith('image/'): return r.content,url
    s=BeautifulSoup(r.text,'html.parser')
    for sel in [('meta',{'property':'og:image'}),('meta',{'name':'og:image'}),('meta',{'name':'twitter:image'}),('meta',{'property':'og:image:secure_url'})]:
        m=s.find(*sel)
        if m and m.get('content'):
            u=requests.compat.urljoin(url,m['content'])
            ir=requests.get(u,headers=UA,timeout=25); ir.raise_for_status(); return ir.content,u
    raise Exception('no og:image')
for row in csv.reader(open('images/manifest.tsv'),delimiter='\t'):
    if not row or row[0].startswith('#'): continue
    slug,url=row[0].strip(),row[1].strip()
    dst=f'images/out/{slug}.jpg'
    if os.path.exists(dst): log.append([slug,'exists',url]); continue
    try:
        b,src=find_img(url)
        im=Image.open(io.BytesIO(b)).convert('RGBA')
        bg=Image.new('RGBA',im.size,(255,255,255,255)); bg.alpha_composite(im); im=bg.convert('RGB')
        im.thumbnail((760,760))
        c=Image.new('RGB',(800,800),(250,246,240)); c.paste(im,((800-im.width)//2,(800-im.height)//2))
        c.save(dst,'JPEG',quality=84,optimize=True); log.append([slug,'ok',src])
    except Exception as e:
        log.append([slug,'fail',f'{url} {e}'[:300]])
with open('images/log.tsv','w') as f:
    for l in log: f.write('\t'.join(l)+'\n')
print(sum(1 for l in log if l[1]=='ok'),'ok',sum(1 for l in log if l[1]=='fail'),'fail')
