// usage: node shot.mjs <url> <out.png> [width=390] [height=844] [full=0] [dpr=2] [waitMs=2500] [scrollToSelector]
import { spawn } from 'node:child_process';
import { writeFileSync } from 'node:fs';
const [url,out,W='390',H='844',FULL='0',DPR='2',WAIT='2500',SEL='']=process.argv.slice(2);
const PORT=9560+Math.floor(Math.random()*30);
const chrome=spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',['--headless=new',`--remote-debugging-port=${PORT}`,`--user-data-dir=/tmp/shot-${PORT}`,'--hide-scrollbars','about:blank'],{stdio:'ignore'});
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
let tgt;for(let i=0;i<60&&!tgt;i++){try{tgt=await(await fetch(`http://127.0.0.1:${PORT}/json/new?about:blank`,{method:'PUT'})).json()}catch{await sleep(250)}}
const ws=new WebSocket(tgt.webSocketDebuggerUrl);await new Promise(r=>ws.addEventListener('open',r,{once:true}));
let id=0;const pend=new Map();ws.addEventListener('message',e=>{const m=JSON.parse(e.data);if(m.id&&pend.has(m.id)){pend.get(m.id)(m);pend.delete(m.id)}});
const cdp=(method,params={},ms=40000)=>new Promise((r)=>{const i=++id;const to=setTimeout(()=>{console.error('CDP timeout',method);chrome.kill();process.exit(3)},ms);pend.set(i,m=>{clearTimeout(to);r(m)});ws.send(JSON.stringify({id:i,method,params}))});
const ev=async expr=>(await cdp('Runtime.evaluate',{expression:expr,returnByValue:true})).result?.result?.value;
await cdp('Emulation.setDeviceMetricsOverride',{width:+W,height:+H,deviceScaleFactor:+DPR,mobile:+W<800});
await cdp('Page.navigate',{url});await sleep(+WAIT);
await ev(`document.querySelectorAll('.rv,[data-wire],[data-tl],[data-app],[data-ad],.lx-rv').forEach(e=>e.classList.add('in'));window.scrollTo(0,0);1`);
if(SEL){await ev(`(function(){var e=document.querySelector(${JSON.stringify(SEL)});if(e){window.scrollTo(0,e.getBoundingClientRect().top+window.scrollY-64)};document.querySelectorAll('.rv').forEach(x=>x.classList.add('in'));return 1})()`);await sleep(1500);}
await sleep(600);
if(FULL==='1'){await ev(`(function(){var st=document.createElement('style');st.textContent='.site-hd{position:absolute!important}.lx-sbar,.lx-pv-badge{display:none!important}';document.head.appendChild(st);return 1})()`);
  const h=Math.min(20000,Math.ceil(await ev('document.documentElement.scrollHeight')));const parts=[];
  for(let y=0;y<h;y+=+H){await ev(`window.scrollTo(0,${y});document.querySelectorAll('.rv,.lx-rv').forEach(e=>e.classList.add('in'));1`);await sleep(350);
    const sc=await cdp('Page.captureScreenshot',{format:'png'},30000);const real=await ev('window.scrollY');parts.push({y:real,data:sc.result.data});}
  writeFileSync(out+'.json',JSON.stringify(parts.map(p=>({y:p.y}))));parts.forEach((p,i)=>writeFileSync(out.replace(/\.png$/,'')+'_part'+i+'.png',Buffer.from(p.data,'base64')));
}else{const shot=await cdp('Page.captureScreenshot',{format:'png'});writeFileSync(out,Buffer.from(shot.result.data,'base64'));}
console.log('saved',out,'innerWidth x scrollWidth x scrollHeight =',await ev('[innerWidth,document.documentElement.scrollWidth,document.documentElement.scrollHeight].join("x")'));
ws.close();chrome.kill();process.exit(0);
