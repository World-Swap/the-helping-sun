const { chromium } = require('playwright');
const fs = require('fs'), path = require('path'), { execSync } = require('child_process');
const IMG = `file://${process.cwd()}/site/img`;
const OUT = 'reels', TMP = process.env.SP + '/frames';
const FPS = 30;

// Each card: [start, end] seconds, then lines. kind: big | body | mono | gold
const REELS = [
 { slug:'01-ask-well', dur:11, photos:[{src:'sunrise-lighthouse-2400.jpg', pos:'36%'}],
   cards:[
    [0.3,3.4,[['You don’t have to','big'],['ask <em>well</em>.','big']]],
    [3.7,6.6,[['You just have to ask.','big']]],
    [6.9,9.0,[['Support for people carrying hard things.','body'],['Your head. Your body. Your money.','body']]],
    [9.2,11,[['thehelpingsun.com','mono'],['In crisis? 988','gold']]],
   ]},
 { slug:'02-light-before-noon', dur:11, photos:[{src:'fire-morning-1600.jpg', pos:'50%'}],
   cards:[
    [0.3,2.6,[['One small thing.','big']]],
    [2.9,6.2,[['Ten to twenty minutes','body'],['of outdoor light.','body'],['Before noon.','big']]],
    [6.5,9.0,[['It is not a cure.','body'],['It measurably helps.','body'],['It costs nothing.','body']]],
    [9.2,11,[['The Helping Sun','mono'],['thehelpingsun.com','gold']]],
   ]},
 { slug:'03-the-word-is-hardship', dur:12, photos:[{src:'crimson-rivermouth-1600.jpg', pos:'50%'}],
   cards:[
    [0.3,2.8,[['Can’t pay a bill?','big']]],
    [3.1,5.8,[['The word is','body'],['HARDSHIP','gold']]],
    [6.1,9.2,[['Almost every lender has','body'],['a hardship program.','body'],['Almost none will','body'],['mention it first.','body']]],
    [9.5,12,[['You have to say the word.','big'],['thehelpingsun.com','mono']]],
   ]},
 { slug:'04-when-someone-says', dur:14, photos:[{src:'night-lights-1600.jpg', pos:'50%'}],
   cards:[
    [0.3,3.0,[['If someone tells you','body'],['they want to die:','big']]],
    [3.3,6.6,[['Ask directly.','big'],['“Are you thinking about','body'],['killing yourself?”','body']]],
    [6.9,9.4,[['Asking plainly does not','body'],['plant the idea.','big']]],
    [9.7,12.0,[['Then: “I’m glad you told me.','body'],['I’m not going anywhere.”','body']]],
    [12.2,14,[['988','gold'],['call or text, 24/7','mono']]],
   ]},
 { slug:'05-sunrise-log', dur:12,
   photos:[{src:'sunrise-lighthouse-2400.jpg',pos:'36%',in:0,out:3.6},
           {src:'golden-coaster-1600.jpg',pos:'50%',in:3.2,out:6.4},
           {src:'sun-into-lagoon-1600.jpg',pos:'50%',in:6.0,out:9.0},
           {src:'lavender-dusk-1600.jpg',pos:'50%',in:8.6,out:12}],
   cards:[
    [0.4,3.4,[['Every one of these','big']]],
    [3.7,6.4,[['is a morning','big']]],
    [6.7,9.2,[['I got out of bed.','big']]],
    [9.4,12,[['The photo isn’t the point.','body'],['The proof is.','big']]],
   ]},
];

const PAGE = (photos) => `
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;1,6..72,400&family=IBM+Plex+Mono:wght@500&display=swap">
<style>
 html,body{margin:0;background:#070B12;overflow:hidden}
 .stage{position:relative;width:1080px;height:1920px;overflow:hidden}
 .ph{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;will-change:transform,opacity}
 .scrim{position:absolute;inset:0;background:linear-gradient(180deg,
   rgba(7,11,18,.62) 0%, rgba(7,11,18,.26) 26%, rgba(7,11,18,.30) 54%, rgba(7,11,18,.86) 100%)}
 .safe{position:absolute;left:90px;right:190px;top:430px;height:1020px;
   display:flex;flex-direction:column;justify-content:center;gap:0}
 .card{position:absolute;left:0;right:0;top:50%;transform:translateY(-50%);
   display:flex;flex-direction:column;gap:14px;will-change:opacity,transform}
 .big{font-family:"Newsreader",Georgia,serif;font-weight:500;font-size:96px;line-height:1.04;
   color:#fff;letter-spacing:-.02em;text-shadow:0 3px 40px rgba(6,10,16,.72)}
 .big em{font-style:italic;color:#F5C774}
 .body{font-family:"Newsreader",Georgia,serif;font-weight:400;font-size:62px;line-height:1.26;
   color:#EDF1F6;text-shadow:0 2px 30px rgba(6,10,16,.8)}
 .mono{font-family:"IBM Plex Mono",monospace;font-size:34px;letter-spacing:.12em;
   text-transform:uppercase;color:rgba(255,255,255,.84);text-shadow:0 2px 20px rgba(6,10,16,.8)}
 .gold{font-family:"IBM Plex Mono",monospace;font-size:72px;letter-spacing:.06em;font-weight:500;
   color:#F5C774;text-shadow:0 2px 30px rgba(6,10,16,.8)}
 .bar{position:absolute;left:90px;bottom:150px;width:96px;height:5px;background:#F5C774;
   border-radius:3px;opacity:.9}
</style>
<div class="stage" id="stage">
 ${photos.map((p,i)=>`<img class="ph" id="ph${i}" src="${IMG}/${p.src}" style="object-position:${p.pos} 50%">`).join('')}
 <div class="scrim"></div>
 <div class="safe" id="safe"></div>
 <div class="bar"></div>
</div>`;

(async () => {
  const b = await chromium.launch();
  fs.mkdirSync(OUT, {recursive:true});
  for (const reel of REELS) {
    const dir = `${TMP}/${reel.slug}`;
    fs.rmSync(dir, {recursive:true, force:true}); fs.mkdirSync(dir, {recursive:true});
    const ctx = await b.newContext({viewport:{width:1080,height:1920}, deviceScaleFactor:1});
    const page = await ctx.newPage();
    const html = `${process.env.SP}/page-${reel.slug}.html`;
    fs.writeFileSync(html, PAGE(reel.photos));
    await page.goto('file://' + html, {waitUntil:'networkidle'});
    const okImgs = await page.evaluate(() => [...document.images].every(i => i.complete && i.naturalWidth > 0));
    if (!okImgs) throw new Error('PHOTO FAILED TO LOAD in ' + reel.slug);
    await page.evaluate(() => document.fonts.ready);
    await page.evaluate((r) => {
      const safe = document.getElementById('safe');
      safe.innerHTML = r.cards.map((c,i)=>
        `<div class="card" id="c${i}">${c[2].map(([t,k])=>`<div class="${k}">${t}</div>`).join('')}</div>`).join('');
      window.__r = r;
    }, reel);
    await page.waitForTimeout(400);
    const total = Math.round(reel.dur * 30);
    for (let f = 0; f < total; f++) {
      await page.evaluate((f) => {
        const r = window.__r, t = f/30, FADE = 0.45;
        (r.photos||[]).forEach((p,i)=>{
          const el = document.getElementById('ph'+i);
          const z = 1 + 0.085 * (t / r.dur);
          let op = 1;
          if (p.in !== undefined) {
            const a = Math.min(1, Math.max(0,(t - p.in)/0.6));
            const bo = p.out >= r.dur ? 1 : Math.min(1, Math.max(0,(p.out - t)/0.6));
            op = Math.min(a, bo);
          }
          el.style.opacity = op;
          el.style.transform = `scale(${z})`;
        });
        r.cards.forEach((c,i)=>{
          const el = document.getElementById('c'+i);
          const [t0,t1] = c;
          const a = Math.min(1, Math.max(0,(t - t0)/FADE));
          const bo = Math.min(1, Math.max(0,(t1 - t)/FADE));
          const o = Math.min(a,bo);
          el.style.opacity = o;
          el.style.transform = `translateY(calc(-50% + ${(1-a)*26}px))`;
        });
      }, f);
      await page.screenshot({path:`${dir}/${String(f).padStart(5,'0')}.jpg`, type:'jpeg', quality:94});
    }
    await ctx.close();
    execSync(`ffmpeg -y -loglevel error -framerate 30 -i ${dir}/%05d.jpg ` +
      `-f lavfi -i anullsrc=channel_layout=stereo:sample_rate=44100 -shortest ` +
      `-c:v libx264 -preset medium -crf 20 -pix_fmt yuv420p -profile:v high -level 4.0 ` +
      `-c:a aac -b:a 128k -movflags +faststart ${OUT}/${reel.slug}.mp4`);
    fs.rmSync(dir, {recursive:true, force:true});
    console.log('built', reel.slug, total, 'frames');
  }
  await b.close();
})();
