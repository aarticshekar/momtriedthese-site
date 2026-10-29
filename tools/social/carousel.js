// Full-page carousel renderer. Usage: ROOT=<repo> node tools/social/carousel.js <posts.json> <outdir>
// posts.json: {posts:[{id,slides:[{k,t,s},{img,t,s,k?}...,{k,t,s}],caption}]}. Product slides need img (slug in images/out/).
const {chromium}=require('playwright');const fs=require('fs');
const ROOT=process.env.ROOT||process.cwd();const F=ROOT+'/site/static/fonts',IM=ROOT+'/images/out',SPEC=process.argv[2],OUT=process.argv[3];
const b64=f=>fs.readFileSync(f).toString('base64');const im=x=>'data:image/jpeg;base64,'+b64(IM+'/'+x+'.jpg');
const ff=[['Lora',400,'italic','lora-latin-400-italic'],['Lora',600,'normal','lora-latin-600-normal'],['Inter',400,'normal','inter-latin-400-normal'],['Inter',500,'normal','inter-latin-500-normal'],['Inter',600,'normal','inter-latin-600-normal']].map(([n,w,s,f])=>`@font-face{font-family:${n};font-weight:${w};font-style:${s};src:url(data:font/woff2;base64,${b64(F+'/'+f+'.woff2')})}`).join('');
const css=ff+`*{margin:0;box-sizing:border-box}body{width:1080px;height:1350px;overflow:hidden;font-family:Inter;color:#241F1C;position:relative;background:#fff}
.bg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.pimg{position:absolute;left:40px;right:40px;top:240px;bottom:270px;display:flex;align-items:center;justify-content:center}.pimg img{max-width:100%;max-height:100%;object-fit:contain;transform:scale(1.25)}
.top{position:absolute;left:72px;right:72px;top:72px}.bot{position:absolute;left:72px;right:72px;bottom:108px}
.k{font:600 26px Inter;letter-spacing:5px;text-transform:uppercase;color:#C8643F}.n{font:400 96px/1 Lora;font-style:italic;color:#C8643F;position:absolute;right:72px;top:56px}
h2{font:600 64px/1.08 Lora;margin-top:12px;max-width:820px}p{font:500 34px/1.38 Inter;color:#4A423D}
.ov{position:absolute;inset:0;background:linear-gradient(180deg,rgba(20,16,14,.15) 0%,rgba(20,16,14,.25) 45%,rgba(20,16,14,.88) 100%)}
.cov .bot{bottom:120px}.cov h1{font:600 96px/1.05 Lora;color:#fff;letter-spacing:-.5px}.cov h1 em,.end h1 em{font-style:italic;font-weight:400;color:#F2B48F}.cov p{color:#F3ECE6;margin-top:22px}.cov .k{color:#F2B48F}
.end{background:#C8643F}.end .c{position:absolute;left:90px;right:90px;top:0;bottom:0;display:flex;flex-direction:column;justify-content:center;gap:34px}.end h1{font:600 92px/1.08 Lora;color:#fff}.end h1 em{color:#241F1C}.end p{color:#fff}.end .k{color:#FDE5D8}
.brand{position:absolute;left:72px;right:72px;bottom:40px;display:flex;justify-content:space-between;font:600 24px Inter;color:#8A807A}.brand b{font:600 28px Lora}.cov .brand,.end .brand{color:rgba(255,255,255,.85)}
.tag{display:inline-block;background:#5F7D66;color:#fff;font:600 22px Inter;letter-spacing:3px;text-transform:uppercase;padding:8px 14px;border-radius:8px;margin-bottom:14px}`;
const srcs=[SPEC];
(async()=>{const br=await chromium.launch();const pg=await br.newPage({viewport:{width:1080,height:1350}});let made=0;
for(const src of srcs){const D=JSON.parse(fs.readFileSync(src));for(const post of D.posts){if(!post.slides.some(s=>s.img))continue;const dir=OUT+'/'+post.id;fs.mkdirSync(dir,{recursive:true});const n=post.slides.length;const first=post.slides.find(s=>s.img).img;
 for(let i=0;i<n;i++){const s=post.slides[i];let html;const brand=`<div class="brand"><b>Mom Tried These</b><span>${i<n-1?'Swipe →':'momtriedthese.com'}</span></div>`;
  if(i===0) html=`<body class="cov"><img class="bg" src="${im(first)}"><div class="ov"></div><div class="bot">${s.k?`<div class="k">${s.k}</div>`:''}<h1 style="margin-top:18px">${s.t}</h1>${s.s?`<p>${s.s}</p>`:''}</div>${brand}</body>`;
  else if(i===n-1) html=`<body class="end"><div class="c"><div class="k">${s.k||''}</div><h1>${s.t}</h1><p>${s.s||''}</p></div>${brand}</body>`;
  else html=`<body><div class="pimg"><img src="${im(s.img)}"></div><div class="top">${s.k?`<span class="tag">${s.k}</span>`:''}<h2>${s.t}</h2></div><div class="n">0${i}</div><div class="bot"><p>${s.s}</p></div>${brand}</body>`;
  await pg.setContent(`<style>${css}</style>${html}`);await pg.evaluate(()=>document.fonts.ready);await pg.waitForTimeout(50);await pg.screenshot({path:`${dir}/${String(i+1).padStart(2,'0')}.jpg`,type:'jpeg',quality:90});}
 fs.writeFileSync(dir+'/caption.txt',post.caption);made++;}}
await br.close();console.log('posts',made)})();
