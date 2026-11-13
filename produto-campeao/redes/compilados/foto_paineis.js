// node foto_paineis.js paineis.html pasta largura altura  -> painel0.png, painel1.png...
const {chromium}=require('playwright');
(async()=>{const [h,dir,w,a]=process.argv.slice(2);const b=await chromium.launch();
const p=await b.newPage({viewport:{width:+w,height:+a},deviceScaleFactor:1});
await p.goto('file://'+h);await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(300);
const els=await p.$$('.p');for(let i=0;i<els.length;i++) await els[i].screenshot({path:`${dir}/painel${i}.png`});
console.log(els.length);await b.close();})();
