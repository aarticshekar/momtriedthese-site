// Faceless reel renderer. Usage: ROOT=<repo> node tools/social/reel.js <spec.json> <outdir>
// Spec: [{id,hook,sub,items:[[image_slug,name,reason]x5],cta,cap,yt}]. Image slugs = files in images/out/.
const {chromium}=require('playwright');const fs=require('fs');const {execSync}=require('child_process');
const ROOT=process.env.ROOT||process.cwd();const F=ROOT+'/site/static/fonts',IM=ROOT+'/images/out',SPEC=process.argv[2],OUT=process.argv[3];const FPS=30;
const b64=f=>fs.readFileSync(f).toString('base64');const img=s=>`data:image/jpeg;base64,${b64(IM+'/'+s+'.jpg')}`;
const ff=[['Lora',400,'italic','lora-latin-400-italic'],['Lora',600,'normal','lora-latin-600-normal'],['Inter',600,'normal','inter-latin-600-normal'],['Inter',500,'normal','inter-latin-500-normal']].map(([n,w,s,f])=>`@font-face{font-family:${n};font-weight:${w};font-style:${s};src:url(data:font/woff2;base64,${b64(F+'/'+f+'.woff2')})}`).join('');
const css=ff+`*{margin:0;box-sizing:border-box}html,body{width:1080px;height:1920px;overflow:hidden;background:#fff;font-family:Inter;color:#241F1C}
.sc{position:absolute;inset:0;opacity:0;overflow:hidden}.bg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}.ov{position:absolute;inset:0;background:linear-gradient(180deg,rgba(20,16,14,.2),rgba(20,16,14,.35) 40%,rgba(20,16,14,.9))}
.hook{position:absolute;left:80px;right:80px;bottom:380px;color:#fff}.hook h1{font:600 118px/1.04 Lora;letter-spacing:-1px}.hook h1 em{font-style:italic;font-weight:400;color:#F2B48F}.hook p{font:600 46px Inter;margin-top:30px;color:#F3ECE6}
.pi{position:absolute;left:0;right:0;top:330px;height:1150px;display:flex;align-items:center;justify-content:center}.pi img{width:96%;height:96%;object-fit:contain}
.cap{position:absolute;left:70px;right:70px;top:150px}.cap .num{font:400 120px/1 Lora;font-style:italic;color:#C8643F}.cap h2{font:600 84px/1.05 Lora;margin-top:6px}
.rs{position:absolute;left:70px;right:70px;bottom:300px;font:600 58px/1.2 Inter;background:#241F1C;color:#fff;padding:26px 34px;border-radius:24px;display:inline-block}
.end{background:#C8643F}.end .c{position:absolute;left:90px;right:90px;top:0;bottom:0;display:flex;flex-direction:column;justify-content:center;gap:40px;color:#fff}.end h2{font:600 104px/1.06 Lora}.end p{font:600 52px Inter}.end .d{font:500 34px Inter;opacity:.85}
.bar{position:absolute;top:0;left:0;height:12px;background:#C8643F;z-index:9}.brand{position:absolute;bottom:150px;left:80px;right:80px;display:flex;justify-content:space-between;font:600 34px Inter;z-index:8;color:#8A807A}.brand b{font:600 40px Lora}
.in{opacity:0}`;
fs.mkdirSync(OUT,{recursive:true});const R=JSON.parse(fs.readFileSync(SPEC));
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
for(const r of R){const S2=[{d:2.6,kind:'hook',h:`<img class="bg zoom" src="${img(r.items[0][0])}"><div class="ov"></div><div class="hook"><h1 class="in">${r.hook}</h1><p class="in">${r.sub}</p></div>`}]
 .concat(r.items.map(([s,n,why],i)=>({d:2.2,h:`<div class="pi"><img class="zoom" src="${img(s)}"></div><div class="cap"><div class="num in">0${i+1}</div><h2 class="in">${n}</h2></div><div class="rs in">${why}</div>`})))
 .concat([{d:3.2,c:'end',h:`<div class="c"><h2 class="in">${r.cta}</h2><p class="in">Link in bio · momtriedthese.com</p><p class="d in">#ad · I earn from qualifying purchases</p></div>`}]);
 let t=0;S2.forEach(s=>{s.st=t;t+=s.d});const T=t;
 const html=`<style>${css}</style>`+S2.map(s=>`<section class="sc ${s.c||''}" data-st="${s.st}" data-d="${s.d}">${s.h}</section>`).join('')+`<div class="bar" id="bar"></div><div class="brand" id="br"><b>Mom Tried These</b><span>momtriedthese.com</span></div>
<script>const SC=[...document.querySelectorAll('.sc')];const T=${T};window.seek=function(t){document.getElementById('bar').style.width=(t/T*100)+'%';let cur=null;SC.forEach((s,i)=>{const st=+s.dataset.st,d=+s.dataset.d,l=t-st,on=l>=0&&l<d;s.style.opacity=on?Math.min(1,l/0.12,i==SC.length-1?1:(d-l)/0.12):0;if(on)cur=s;[...s.querySelectorAll('.in')].forEach((e,k)=>{const a=Math.max(0,Math.min(1,(l-0.05-k*0.18)/0.25));const ea=1-Math.pow(1-a,3);e.style.opacity=ea;e.style.transform='translateY('+(40*(1-ea))+'px)'});[...s.querySelectorAll('.zoom')].forEach(z=>z.style.transform='scale('+(1.0+0.08*Math.max(0,l)/d)+')')});const br=document.getElementById('br');br.style.display=(cur&&(cur===SC[0]||cur.classList.contains('end')))?'none':'flex'};</script>`;
 await p.setContent(html);await p.evaluate(()=>document.fonts.ready);const fr=OUT+'/fr';fs.rmSync(fr,{recursive:true,force:true});fs.mkdirSync(fr);
 const n=Math.round(T*FPS);for(let f=0;f<n;f++){await p.evaluate(t=>window.seek(t),f/FPS);await p.screenshot({path:fr+'/'+String(f).padStart(5,'0')+'.jpg',type:'jpeg',quality:88});}
 await p.evaluate(t=>window.seek(t),1.8);await p.screenshot({path:`${OUT}/${r.id}-cover.jpg`,type:'jpeg',quality:90});
 execSync(`ffmpeg -y -loglevel error -framerate ${FPS} -i ${fr}/%05d.jpg -f lavfi -i anullsrc=r=44100:cl=stereo -shortest -c:v libx264 -preset veryfast -crf 20 -pix_fmt yuv420p -c:a aac -movflags +faststart ${OUT}/${r.id}.mp4`);
 fs.writeFileSync(`${OUT}/${r.id}-captions.txt`,`INSTAGRAM REEL CAPTION\n${r.cap}\n\nAdd a trending sound in the app (the video is silent).\n\nYOUTUBE SHORTS\nTitle: ${r.yt}\nDescription: ${r.cap.split('\\n\\n')[0]} Full list: https://momtriedthese.com/gifts/christmas/\nAs an Amazon Associate I earn from qualifying purchases.\n`);
 fs.rmSync(fr,{recursive:true,force:true});console.log('ok',r.id,T.toFixed(1));}
await b.close();})();
