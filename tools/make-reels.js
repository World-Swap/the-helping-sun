/* Build vertical reels (1080x1920) from the 9:16 masters in reels/src/.
   Add an entry to REELS and run:  node tools/make-reels.js  [slug ...]
   Card text styles: big | body | mono | gold                               */
const { chromium } = require('playwright');
const fs = require('fs'), { execSync } = require('child_process');
const SRC = `file://${process.cwd()}/reels/src`;
const OUT = 'reels';
const TMP = (process.env.SP || '/tmp') + '/frames';
const FPS = 30;

const REELS = [
 { slug:'01-ask-well', dur:11, photos:[{src:'sunrise-lighthouse.jpg'}], cards:[
    [0.3,3.4,[['You don’t have to','big'],['ask <em>well</em>.','big']]],
    [3.7,6.6,[['You just have to ask.','big']]],
    [6.9,9.0,[['Support for people carrying hard things.','body'],['Your head. Your body. Your money.','body']]],
    [9.2,11,[['thehelpingsun.com','mono'],['In crisis? 988','gold']]] ]},

 { slug:'02-light-before-noon', dur:11, photos:[{src:'fire-morning.jpg'}], cards:[
    [0.3,2.6,[['One small thing.','big']]],
    [2.9,6.2,[['Ten to twenty minutes','body'],['of outdoor light.','body'],['Before noon.','big']]],
    [6.5,9.0,[['It is not a cure.','body'],['It measurably helps.','body'],['It costs nothing.','body']]],
    [9.2,11,[['The Helping Sun','mono'],['thehelpingsun.com','gold']]] ]},

 { slug:'03-the-word-is-hardship', dur:12, photos:[{src:'crimson-rivermouth.jpg'}], cards:[
    [0.3,2.8,[['Can’t pay a bill?','big']]],
    [3.1,5.8,[['The word is','body'],['HARDSHIP','gold']]],
    [6.1,9.2,[['Almost every lender has','body'],['a hardship program.','body'],['Almost none will','body'],['mention it first.','body']]],
    [9.5,12,[['You have to say the word.','big'],['thehelpingsun.com','mono']]] ]},

 { slug:'04-when-someone-says', dur:14, photos:[{src:'night-lights.jpg'}], cards:[
    [0.3,3.0,[['If someone tells you','body'],['they want to die:','big']]],
    [3.3,6.6,[['Ask directly.','big'],['“Are you thinking about','body'],['killing yourself?”','body']]],
    [6.9,9.4,[['Asking plainly does not','body'],['plant the idea.','big']]],
    [9.7,12.0,[['Then: “I’m glad you told me.','body'],['I’m not going anywhere.”','body']]],
    [12.2,14,[['988','gold'],['call or text, 24/7','mono']]] ]},

 { slug:'05-sunrise-log', dur:12, photos:[
     {src:'sunrise-lighthouse.jpg',in:0,out:3.6},{src:'golden-coaster.jpg',in:3.2,out:6.4},
     {src:'sun-into-lagoon.jpg',in:6.0,out:9.0},{src:'lavender-dusk.jpg',in:8.6,out:12}], cards:[
    [0.4,3.4,[['Every one of these','big']]],
    [3.7,6.4,[['is a morning','big']]],
    [6.7,9.2,[['I got out of bed.','big']]],
    [9.4,12,[['The photo isn’t the point.','body'],['The proof is.','big']]] ]},

 /* ---- batch two ---- */

 { slug:'06-the-unopened-mail', dur:13, photos:[{src:'pale-dusk.jpg'}], cards:[
    [0.3,3.2,[['There were four envelopes','body'],['on my counter.','big']]],
    [3.5,6.0,[['For eleven weeks.','big']]],
    [6.3,9.4,[['I knew one was from the DMV.','body'],['I knew it was getting worse','body'],['every day I didn’t touch it.','body']]],
    [9.7,13,[['You’re not lazy.','big'],['You need a second person','body'],['in the room.','body']]] ]},

 { slug:'07-the-ghosted-friend', dur:14, photos:[{src:'rocks-dusk.jpg'}], cards:[
    [0.3,3.0,[['Disappeared on someone?','big']]],
    [3.3,7.4,[['Send exactly this:','mono'],['“I disappeared and it','body'],['wasn’t about you. I’ve been','body'],['going through it. I’d like to','body'],['come back around.”','body']]],
    [7.7,10.6,[['Don’t apologise five times.','body'],['Don’t explain six months.','body']]],
    [10.9,14,[['Send it today.','big'],['Don’t draft it for a week.','body']]] ]},

 { slug:'08-call-211', dur:12, photos:[{src:'mackerel-dawn.jpg'}], cards:[
    [0.3,2.8,[['One number almost','body'],['nobody knows.','big']]],
    [3.1,5.6,[['211','gold']]],
    [5.9,9.0,[['Free. 24/7. Every county.','body'],['Rent. Utilities. Food.','body'],['Rides to appointments.','body']]],
    [9.3,12,[['Save it now,','big'],['before you need it.','big']]] ]},

 { slug:'09-sunday-night', dur:13, photos:[{src:'ember-band.jpg'}], cards:[
    [0.3,3.2,[['Sunday, around 7pm,','body'],['the light goes.','big']]],
    [3.5,6.4,[['And something in my','body'],['chest changes.','big']]],
    [6.7,9.4,[['It isn’t about Monday.','big'],['I’ve had it on Sundays with','body'],['nowhere to be on Monday.','body']]],
    [9.7,13,[['It passes by about 9.','big'],['You can wait that out.','body']]] ]},

 { slug:'10-looking-fine', dur:14, photos:[{src:'deep-night.jpg'}], cards:[
    [0.3,3.0,[['I was very good at','body'],['looking fine.','big']]],
    [3.3,6.8,[['Nobody was ignoring me.','body'],['They genuinely could not tell.','body'],['I’d spent a decade','body'],['getting good at it.','body']]],
    [7.1,10.0,[['So if you’re waiting for','body'],['someone to notice —','body'],['they might not.','big']]],
    [10.3,14,[['The first move is yours.','big'],['That’s unfair. It’s also true.','body'],['988','gold']]] ]},
];

const PAGE = (photos) => `
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;1,6..72,400&family=IBM+Plex+Mono:wght@500&display=swap">
<style>
 html,body{margin:0;background:#070B12;overflow:hidden}
 .stage{position:relative;width:1080px;height:1920px;overflow:hidden}
 .ph{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;will-change:transform,opacity}
 .scrim{position:absolute;inset:0;background:linear-gradient(180deg,
   rgba(7,11,18,.60) 0%, rgba(7,11,18,.22) 26%, rgba(7,11,18,.28) 52%, rgba(7,11,18,.88) 100%)}
 .safe{position:absolute;left:90px;right:190px;top:430px;height:1020px}
 .card{position:absolute;left:0;right:0;top:50%;transform:translateY(-50%);
   display:flex;flex-direction:column;gap:14px;will-change:opacity,transform}
 .big{font-family:"Newsreader",Georgia,serif;font-weight:500;font-size:96px;line-height:1.04;
   color:#fff;letter-spacing:-.02em;text-shadow:0 3px 40px rgba(6,10,16,.78)}
 .big em{font-style:italic;color:#F5C774}
 .body{font-family:"Newsreader",Georgia,serif;font-weight:400;font-size:60px;line-height:1.26;
   color:#EDF1F6;text-shadow:0 2px 30px rgba(6,10,16,.85)}
 .mono{font-family:"IBM Plex Mono",monospace;font-size:34px;letter-spacing:.12em;
   text-transform:uppercase;color:rgba(255,255,255,.84);text-shadow:0 2px 20px rgba(6,10,16,.85)}
 .gold{font-family:"IBM Plex Mono",monospace;font-size:72px;letter-spacing:.06em;font-weight:500;
   color:#F5C774;text-shadow:0 2px 30px rgba(6,10,16,.85)}
 .bar{position:absolute;left:90px;bottom:150px;width:96px;height:5px;background:#F5C774;
   border-radius:3px;opacity:.9}
</style>
<div class="stage" id="stage">
 ${photos.map((p,i)=>`<img class="ph" id="ph${i}" src="${SRC}/${p.src}">`).join('')}
 <div class="scrim"></div><div class="safe" id="safe"></div><div class="bar"></div>
</div>`;

(async () => {
  const only = process.argv.slice(2);
  const list = only.length ? REELS.filter(r => only.includes(r.slug)) : REELS;
  const b = await chromium.launch();
  fs.mkdirSync(OUT, {recursive:true}); fs.mkdirSync(TMP, {recursive:true});
  for (const reel of list) {
    const dir = `${TMP}/${reel.slug}`;
    fs.rmSync(dir, {recursive:true, force:true}); fs.mkdirSync(dir, {recursive:true});
    const ctx = await b.newContext({viewport:{width:1080,height:1920}, deviceScaleFactor:1});
    const page = await ctx.newPage();
    const html = `${TMP}/page-${reel.slug}.html`;
    fs.writeFileSync(html, PAGE(reel.photos));
    // goto, not setContent: file:// subresources never load from an about:blank document
    await page.goto('file://' + html, {waitUntil:'networkidle'});
    const ok = await page.evaluate(() => [...document.images].every(i => i.complete && i.naturalWidth > 0));
    if (!ok) throw new Error('photo failed to load in ' + reel.slug);
    await page.evaluate(() => document.fonts.ready);
    await page.evaluate((r) => {
      document.getElementById('safe').innerHTML = r.cards.map((c,i)=>
        `<div class="card" id="c${i}">${c[2].map(([t,k])=>`<div class="${k}">${t}</div>`).join('')}</div>`).join('');
      window.__r = r;
    }, reel);
    await page.waitForTimeout(400);
    const total = Math.round(reel.dur * FPS);
    for (let f = 0; f < total; f++) {
      await page.evaluate(({f,FPS}) => {
        const r = window.__r, t = f/FPS, FADE = 0.45;
        r.photos.forEach((p,i)=>{
          const el = document.getElementById('ph'+i);
          let op = 1;
          if (p.in !== undefined) {
            const a = Math.min(1, Math.max(0,(t - p.in)/0.6));
            const z = p.out >= r.dur ? 1 : Math.min(1, Math.max(0,(p.out - t)/0.6));
            op = Math.min(a, z);
          }
          el.style.opacity = op;
          el.style.transform = `scale(${1 + 0.085 * (t / r.dur)})`;
        });
        r.cards.forEach((c,i)=>{
          const el = document.getElementById('c'+i);
          const a = Math.min(1, Math.max(0,(t - c[0])/FADE));
          const z = Math.min(1, Math.max(0,(c[1] - t)/FADE));
          el.style.opacity = Math.min(a,z);
          el.style.transform = `translateY(calc(-50% + ${(1-a)*26}px))`;
        });
      }, {f,FPS});
      await page.screenshot({path:`${dir}/${String(f).padStart(5,'0')}.jpg`, type:'jpeg', quality:94});
    }
    await ctx.close();
    execSync(`ffmpeg -y -loglevel error -framerate ${FPS} -i ${dir}/%05d.jpg ` +
      `-f lavfi -i anullsrc=channel_layout=stereo:sample_rate=44100 -shortest ` +
      `-c:v libx264 -preset medium -crf 20 -pix_fmt yuv420p -profile:v high -level 4.0 ` +
      `-c:a aac -b:a 128k -movflags +faststart ${OUT}/${reel.slug}.mp4`);
    fs.rmSync(dir, {recursive:true, force:true});
    console.log('built', reel.slug);
  }
  await b.close();
})();
