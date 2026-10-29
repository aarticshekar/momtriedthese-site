const {chromium}=require('playwright');const fs=require('fs');
const b64=p=>fs.readFileSync(p).toString('base64');
const P=b64(require('path').join(__dirname,'playfair-700.woff2'));
const OUT=process.argv[3]||'./out';
const css=`@font-face{font-family:P;src:url(data:font/woff2;base64,${P})}*{margin:0;box-sizing:border-box}body{position:relative;font-family:Inter,Arial,sans-serif;color:#1C1918;background:#FAF6F0;overflow:hidden}
.b{position:absolute;width:110px;height:110px;border:0 solid #D2643F}.tl{left:70px;top:70px;border-left-width:10px;border-top-width:10px}.br{right:70px;border-right-width:10px;border-bottom-width:10px}
.e{font:600 28px Inter,Arial;letter-spacing:5px;text-transform:uppercase;color:#6E8A74}h1{font:700 88px/1.08 P;text-wrap:balance}h1 em{font-style:normal;color:#D2643F}
.s{font:500 36px/1.4 Inter,Arial;color:#3A3532;text-wrap:pretty}.f{position:absolute;left:0;right:0;bottom:0;height:150px;background:#D2643F;color:#fff;display:flex;align-items:center;justify-content:space-between;padding:0 80px}.f b{font:700 42px P}.f span{font:500 26px Inter,Arial}
.dark{background:#1C1918;color:#FAF6F0}.dark h1{color:#FAF6F0}.dark .s{color:#E8DFD3}.dark .b{border-color:#C9963B}
ul{list-style:none;display:flex;flex-direction:column;gap:22px}li{font:500 38px/1.3 Inter,Arial;padding-left:44px;position:relative}li:before{content:"";position:absolute;left:0;top:16px;width:20px;height:20px;border-radius:50%;background:#D2643F}`;
const ig=(o,i,n,dark)=>`<style>${css}body{width:1080px;height:1350px}.br{bottom:220px}.c{position:absolute;left:140px;right:140px;top:190px;bottom:290px;display:flex;flex-direction:column;justify-content:center;gap:38px}.n{position:absolute;right:84px;top:84px;font:600 26px Inter,Arial;color:#6E8A74}</style><body class="${dark?'dark':''}"><i class="b tl"></i><i class="b br"></i>${n>1?`<div class=n>${i}/${n}</div>`:''}<div class=c>${o.e?`<div class=e>${o.e}</div>`:''}<h1>${o.t}</h1>${o.s?`<div class=s>${o.s}</div>`:''}${o.l?`<ul>${o.l.map(x=>`<li>${x}</li>`).join('')}</ul>`:''}</div><div class=f><b>Mom Tried These</b><span>${o.foot||'Only the ones I kept'}</span></div></body>`;
const pin=(o)=>`<style>${css}body{width:1000px;height:1500px}.br{bottom:230px}.c{position:absolute;left:120px;right:120px;top:190px;bottom:300px;display:flex;flex-direction:column;justify-content:center;gap:44px}h1{font-size:96px}</style><body class="${o.dark?'dark':''}"><i class="b tl"></i><i class="b br"></i><div class=c><div class=e>${o.e}</div><h1>${o.t}</h1><div class=s>${o.s}</div></div><div class=f><b>momtriedthese.com</b><span>${o.foot||'Only the ones I kept'}</span></div></body>`;
const D=JSON.parse(fs.readFileSync(process.argv[2]));
(async()=>{const b=await chromium.launch();
let p=await b.newPage({viewport:{width:1080,height:1350}});
for(const post of D.ig){const dir=`${OUT}/instagram/${post.id}`;fs.mkdirSync(dir,{recursive:true});
 for(let i=0;i<post.slides.length;i++){await p.setContent(ig(post.slides[i],i+1,post.slides.length,post.dark&&(i==0||post.slides.length==1)));await p.waitForTimeout(80);await p.screenshot({path:`${dir}/${String(i+1).padStart(2,'0')}.jpg`,type:'jpeg',quality:90});}
 fs.writeFileSync(`${dir}/caption.txt`,post.caption);}
p=await b.newPage({viewport:{width:1000,height:1500}});fs.mkdirSync(`${OUT}/pins`,{recursive:true});
for(const x of D.pins){await p.setContent(pin(x));await p.waitForTimeout(80);await p.screenshot({path:`${OUT}/pins/${x.id}.jpg`,type:'jpeg',quality:88});}
await b.close()})();
