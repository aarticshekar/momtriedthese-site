# manifest.tsv: slug<TAB>source
# source forms:  url:<page or image url>  |  book:<title> by <author>  |  q:<search words>[|<preferred domain>]
# Output: images/out/<slug>.jpg (900x900, product centred on cream), images/log.tsv, images/contact-N.jpg
import csv, io, os, re, json, urllib.parse, requests, time
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw
UA={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36','Accept-Language':'en-US,en;q=0.9','Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'}
BAD=('media-amazon','ssl-images-amazon','images-na.ssl','amazon.','amzn','ebay.','aliexpress','temu.','walmart.com/ip','pinterest.','youtube.','facebook.','instagram.','reddit.','tiktok.')
os.makedirs('images/out',exist_ok=True)
S=requests.Session(); S.headers.update(UA)
def get(u,**k): r=S.get(u,timeout=25,**k); r.raise_for_status(); return r
def og(url):
    r=get(url)
    if r.headers.get('content-type','').startswith('image/'): return r.content,url
    s=BeautifulSoup(r.text,'html.parser')
    for a,v in [('property','og:image'),('name','og:image'),('property','og:image:secure_url'),('name','twitter:image'),('property','twitter:image')]:
        m=s.find('meta',{a:v})
        if m and m.get('content'):
            u=urllib.parse.urljoin(url,m['content'].strip())
            return get(u).content,u
    ld=s.find_all('script',{'type':'application/ld+json'})
    for t in ld:
        try:
            j=json.loads(t.string or '{}'); j=j if isinstance(j,list) else [j]
            for x in j:
                im=x.get('image') if isinstance(x,dict) else None
                if isinstance(im,list): im=im[0]
                if isinstance(im,dict): im=im.get('url')
                if im: u=urllib.parse.urljoin(url,im); return get(u).content,u
        except Exception: pass
    raise Exception('no image meta')
def search(q,dom=None):
    links=[]
    try:
        r=get('https://html.duckduckgo.com/html/',params={'q':q})
        for a in BeautifulSoup(r.text,'html.parser').select('a.result__a'):
            h=a.get('href','')
            if 'uddg=' in h: h=urllib.parse.unquote(h.split('uddg=')[1].split('&')[0])
            links.append(h)
    except Exception: pass
    if not links:
        try:
            r=get('https://www.bing.com/search',params={'q':q})
            links=[a['href'] for a in BeautifulSoup(r.text,'html.parser').select('li.b_algo h2 a') if a.get('href')]
        except Exception: pass
    links=[l for l in links if l.startswith('http') and not any(b in l for b in BAD)]
    if dom:
        pref=[l for l in links if dom in urllib.parse.urlparse(l).netloc]
        links=pref+[l for l in links if l not in pref]
    return links[:4]

def bing_images(q,dom=None):
    r=get('https://www.bing.com/images/async',params={'q':q,'first':'0','count':'35','mmasync':'1','adlt':'strict'},headers={'Referer':'https://www.bing.com/images/search?q='+urllib.parse.quote(q)})
    open('images/debug-bing.html','w').write(r.text[:200000]) if not os.path.exists('images/debug-bing.html') else None
    out=[]
    for a in BeautifulSoup(r.text,'html.parser').select('a.iusc'):
        try: m=json.loads(a.get('m','{}'))
        except Exception: continue
        mu,pu=m.get('murl',''),m.get('purl','')
        if not mu.startswith('http') or any(b in mu or b in pu for b in BAD): continue
        out.append((mu,pu))
    if dom:
        pref=[x for x in out if dom in urllib.parse.urlparse(x[1]).netloc or dom in urllib.parse.urlparse(x[0]).netloc]
        out=pref+[x for x in out if x not in pref]
    return out[:6]
def book(spec):
    t,_,a=spec.partition(' by ')
    j=get('https://openlibrary.org/search.json',params={'title':t,'author':a,'limit':5}).json()
    for d in j.get('docs',[]):
        if d.get('cover_i'):
            u=f"https://covers.openlibrary.org/b/id/{d['cover_i']}-L.jpg"; return get(u).content,u
    raise Exception('no cover')
def fit(b,dst,pad=True):
    im=Image.open(io.BytesIO(b))
    if im.mode in ('P','LA','RGBA'):
        im=im.convert('RGBA'); bg=Image.new('RGBA',im.size,(255,255,255,255)); bg.alpha_composite(im); im=bg
    im=im.convert('RGB')
    if im.width<250 or im.height<250: raise Exception(f'too small {im.size}')
    im.thumbnail((820,820),Image.LANCZOS)
    c=Image.new('RGB',(900,900),(255,255,255)); c.paste(im,((900-im.width)//2,(900-im.height)//2))
    c.save(dst,'JPEG',quality=85,optimize=True)
log=[]
rows=[r for r in csv.reader(open('images/manifest.tsv'),delimiter='\t') if r and not r[0].startswith('#')]
for slug,src in rows:
    dst=f'images/out/{slug}.jpg'
    if os.path.exists(dst): log.append([slug,'exists','']); continue
    try:
        kind,_,val=src.partition(':')
        if kind=='url': b,u=og(val)
        elif kind in ('q','book'):
            if kind=='book':
                try: b,u=book(val); fit(b,dst); log.append([slug,'ok',u]); continue
                except Exception: q,dom=val.replace(' by ',' ')+' book cover',None
            else: q,_,dom=val.partition('|'); dom=dom or None
            err=None; done=False
            for mu,pu in bing_images(q,dom):
                try:
                    b=get(mu,headers={'Referer':pu}).content; fit(b,dst); log.append([slug,'ok',mu+' | '+pu]); done=True; break
                except Exception as e: err=e
            if not done:
                for l in search(q,dom):
                    try: b,u=og(l); fit(b,dst); log.append([slug,'ok',u+' | '+l]); done=True; break
                    except Exception as e: err=e
            if not done: raise Exception(f'all sources failed {err}')
            time.sleep(0.8); continue
        fit(b,dst); log.append([slug,'ok',u])
    except Exception as e:
        log.append([slug,'fail',f'{src} :: {e}'[:300]])
    time.sleep(0.6)
with open('images/log.tsv','w') as f:
    for l in log: f.write('\t'.join(l)+'\n')
# contact sheets for review
ok=sorted(f[:-4] for f in os.listdir('images/out') if f.endswith('.jpg'))
for n in range(0,len(ok),48):
    part=ok[n:n+48]; cols=8; rws=(len(part)+cols-1)//cols
    sheet=Image.new('RGB',(cols*200,rws*230),(240,236,230)); d=ImageDraw.Draw(sheet)
    for i,s in enumerate(part):
        t=Image.open(f'images/out/{s}.jpg'); t.thumbnail((190,190)); x,y=(i%cols)*200+5,(i//cols)*230+5
        sheet.paste(t,(x,y)); d.text((x,y+195),s[:30],fill=(20,20,20))
    sheet.save(f'images/contact-{n//48+1}.jpg',quality=80)
print(sum(1 for l in log if l[1]=='ok'),'ok',sum(1 for l in log if l[1]=='fail'),'fail')
