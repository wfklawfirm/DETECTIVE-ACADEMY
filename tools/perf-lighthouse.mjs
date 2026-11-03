// Mobile Lighthouse runner (perf+a11y). Not a project dependency: `npm i --no-save lighthouse chrome-launcher`, serve the built app on :3100, then `node tools/perf-lighthouse.mjs /home /cases`.
import lighthouse from "lighthouse"; import * as CL from "chrome-launcher"; import fs from "fs";
import {chromium} from "playwright";
const chrome = await CL.launch({chromePath: chromium.executablePath(), chromeFlags:["--headless=new","--no-sandbox"]});
const routes=process.argv.slice(2); const out=[];
for(const r of routes){
  const res=await lighthouse("http://127.0.0.1:3100"+r,{port:chrome.port,output:"json",onlyCategories:["performance","accessibility"],formFactor:"mobile",extraHeaders:{Cookie:"athar_age=16-17"}});
  const a=res.lhr.audits;
  out.push({route:r,perf:Math.round(res.lhr.categories.performance.score*100),a11y:Math.round(res.lhr.categories.accessibility.score*100),LCP:a["largest-contentful-paint"].displayValue,CLS:a["cumulative-layout-shift"].displayValue,TBT:a["total-blocking-time"].displayValue});
}
console.log(JSON.stringify(out,null,1)); await chrome.kill();
