const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const html = path.join(__dirname, 'welcome10.html');
const frames = path.join(__dirname, 'frames_welcome10');
fs.rmSync(frames, { recursive: true, force: true });
fs.mkdirSync(frames, { recursive: true });

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 720, height: 1280 }, deviceScaleFactor: 1 });
  await page.goto('file://' + html, { waitUntil: 'load' });
  const fps = 60;
  const duration = 20;
  const total = fps * duration;
  for (let i = 0; i < total; i++) {
    const t = i / fps;
    await page.evaluate((time) => window.__setFrame(time), t);
    await page.screenshot({ path: path.join(frames, `frame_${String(i).padStart(4, '0')}.jpg`), type: 'jpeg', quality: 92 });
    if (i % 120 === 0) console.log(`rendered ${i}/${total}`);
  }
  await browser.close();
})();
