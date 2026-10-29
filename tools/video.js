// Renders brand kinetic-typography vertical videos (1080x1920) frame by frame, then ffmpeg -> mp4.
const {chromium}=require('playwright');const fs=require('fs');const {execSync}=require('child_process');
const P=fs.readFileSync(require('path').join(__dirname,'playfair-700.woff2')).toString('base64');
const FPS=24;
const css=`@font-face{font-family:P;src:url(data:font/woff2;base64,${P})}*{margin:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;overflow:hidden;background:#FAF6F0;font-family:Inter,Arial,sans-serif;color:#1C1918}
.scene{position:absolute;inset:0;opacity:0;display:flex;flex-direction:column;justify-content:center;padding:0 110px;gap:44px}
.dark{background:#1C1918;color:#FAF6F0}.sun{background:#D2643F;color:#fff}
.k{font:600 34px Inter,Arial;letter-spacing:6px;text-transform:uppercase;color:#6E8A74}.dark .k{color:#C9963B}.sun .k{color:#FCE9DF}
h1{font:700 118px/1.04 P;text-wrap:balance}h2{font:700 92px/1.06 P;text-wrap:balance}h1 em,h2 em{font-style:normal;color:#D2643F}.sun h1 em,.sun h2 em{color:#1C1918}
p{font:500 48px/1.35 Inter,Arial;text-wrap:pretty}.dark p{color:#E8DFD3}
.num{font:700 230px/0.9 P;color:#D2643F}.card{background:#fff;border-radius:40px;padding:60px 64px;box-shadow:0 30px 80px rgba(60,40,20,.12);display:flex;flex-direction:column;gap:28px}
.tag{align-self:flex-start;font:600 30px Inter;padding:10px 22px;border-radius:99px;background:#DDE7DF;color:#2F4A36}.tag.r{background:#ECE6F2;color:#4A3C5E}
.bar{position:absolute;top:0;left:0;height:14px;background:#C9963B;z-index:9}
.brand{position:absolute;bottom:110px;left:110px;right:110px;display:flex;justify-content:space-between;font:600 34px Inter;opacity:.8;z-index:8}
.brand b{font:700 40px P}
.br1,.br2{position:absolute;width:120px;height:120px;border:0 solid #D2643F;z-index:7}.br1{left:70px;top:90px;border-left-width:12px;border-top-width:12px}.br2{right:70px;bottom:200px;border-right-width:12px;border-bottom-width:12px}
.in{opacity:0;transform:translateY(60px)}`;
function page(v){
 let t=0;const scenes=v.scenes.map((s,i)=>{const st=t;t+=s.d;return {...s,st,i}});
 const total=t;
 const html=`<style>${css}</style><div class=bar id=bar></div><i class=br1></i><i class=br2></i>`+scenes.map(s=>`<section class="scene ${s.c||''}" data-st="${s.st}" data-d="${s.d}">${s.h}</section>`).join('')+`<div class=brand><b>Mom Tried These</b><span>${v.foot||'momtriedthese.com'}</span></div>
<script>
const S=[...document.querySelectorAll('.scene')];const T=${total};
window.seek=function(t){document.getElementById('bar').style.width=(t/T*100)+'%';
S.forEach(s=>{const st=+s.dataset.st,d=+s.dataset.d,l=t-st;const on=l>=0&&l<d;s.style.opacity=on?Math.min(1,l/0.25,(d-l)/0.25+ (s===S[S.length-1]?9:0)):0;
 [...s.querySelectorAll('.in')].forEach((e,k)=>{const a=Math.max(0,Math.min(1,(l-0.15-k*0.35)/0.4));const ea=1-Math.pow(1-a,3);e.style.opacity=ea;e.style.transform='translateY('+(60*(1-ea))+'px)'});
 const z=s.querySelector('.zoom');if(z){z.style.transform='scale('+(1+0.04*Math.max(0,l)/d)+')'}});};
</script>`;
 return {html,total};
}
(async()=>{
 const V=JSON.parse(fs.readFileSync(process.argv[2]));const out=process.argv[3];fs.mkdirSync(out,{recursive:true});
 const b=await chromium.launch();
 for(const v of V){const pg=await b.newPage({viewport:{width:1080,height:1920}});const {html,total}=page(v);await pg.setContent(html);await pg.waitForTimeout(200);
  const dir=require('os').tmpdir()+'/mttframes/'+v.id;fs.rmSync(dir,{recursive:true,force:true});fs.mkdirSync(dir,{recursive:true});
  const n=Math.round(total*FPS);for(let f=0;f<n;f++){await pg.evaluate(t=>window.seek(t),f/FPS);await pg.screenshot({path:`${dir}/${String(f).padStart(5,'0')}.jpg`,type:'jpeg',quality:88});}
  execSync(`ffmpeg -y -loglevel error -framerate ${FPS} -i ${dir}/%05d.jpg -f lavfi -i anullsrc=r=44100:cl=stereo -shortest -c:v libx264 -preset veryfast -crf 20 -pix_fmt yuv420p -c:a aac -movflags +faststart ${out}/${v.id}.mp4`);
  await pg.evaluate(t=>window.seek(t),Math.min(2.2,total-0.1));await pg.screenshot({path:`${out}/${v.id}-cover.jpg`,type:'jpeg',quality:88});
  fs.rmSync(dir,{recursive:true,force:true});await pg.close();console.log(v.id,total+"s");}
 await b.close();})();
