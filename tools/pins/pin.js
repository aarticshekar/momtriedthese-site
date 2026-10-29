const {chromium}=require('playwright');const fs=require('fs');
const S='/tmp/claude-0/-home-claude/e5dc4931-8ec0-508e-88d9-aa0e375c6ba6/scratchpad';const F=S+'/fwt/site/static/fonts',IM=S+'/fwt/images/out',OUT=S+'/pins/out';
const b64=f=>fs.readFileSync(f).toString('base64');
const ff=[['Lora',400,'italic','lora-latin-400-italic'],['Lora',600,'normal','lora-latin-600-normal'],['Inter',400,'normal','inter-latin-400-normal'],['Inter',600,'normal','inter-latin-600-normal']].map(([n,w,s,f])=>`@font-face{font-family:${n};font-weight:${w};font-style:${s};src:url(data:font/woff2;base64,${b64(F+'/'+f+'.woff2')})}`).join('');
const css=ff+`*{margin:0;box-sizing:border-box}body{width:1000px;height:1500px;overflow:hidden;background:#FBF8F3;font-family:Inter;color:#241F1C;position:relative}
.g{position:absolute;left:56px;right:56px;top:56px;height:900px;display:grid;gap:20px}.g.n1{grid-template:1fr/1fr}.g.n2{grid-template:1fr/1fr 1fr}.g.n4{grid-template:1fr 1fr/1fr 1fr}
.t{background:#fff;border-radius:28px;display:flex;align-items:center;justify-content:center;overflow:hidden;box-shadow:0 14px 40px rgba(60,40,20,.08)}.t img{width:88%;height:88%;object-fit:contain}
.c{position:absolute;left:64px;right:64px;top:1000px}.k{font:600 26px Inter;letter-spacing:4px;text-transform:uppercase;color:#C8643F}
h1{font:600 74px/1.08 Lora;margin-top:18px;letter-spacing:-.5px}p{font:400 34px/1.4 Inter;color:#5E5550;margin-top:20px}
.f{position:absolute;left:64px;right:64px;bottom:52px;display:flex;justify-content:space-between;font:600 28px Inter;color:#8A807A}.f b{font:600 32px Lora;color:#241F1C}`;
const D=JSON.parse(fs.readFileSync(S+'/pins/pins.json'));
(async()=>{fs.mkdirSync(OUT,{recursive:true});const br=await chromium.launch();const pg=await br.newPage({viewport:{width:1000,height:1500}});
for(const p of D){const n=p.img.length>=4?4:p.img.length;const tiles=p.img.slice(0,n).map(i=>`<div class="t"><img src="data:image/jpeg;base64,${b64(IM+'/'+i+'.jpg')}"></div>`).join('');
await pg.setContent(`<style>${css}</style><body><div class="g n${n}">${tiles}</div><div class="c"><div class="k">${p.k}</div><h1>${p.t}</h1><p>${p.s}</p></div><div class="f"><b>Mom Tried These</b><span>momtriedthese.com</span></div></body>`);
await pg.evaluate(()=>document.fonts.ready);const h=await pg.evaluate(()=>document.querySelector('.c').getBoundingClientRect().bottom);if(h>1420)console.log('OVERFLOW',p.id,h);
await pg.screenshot({path:`${OUT}/${p.id}.jpg`,type:'jpeg',quality:88});}
await br.close();console.log('done',D.length)})();
