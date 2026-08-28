/*
 * B2 Home Infrastructure Color v27
 * Deterministic prototype-layer transform over the accepted v26 Home string.
 * Scope: generic Home/Today chrome color only; no geometry, stage semantics,
 * event/category colors, backend/API/domain semantics or persistence changes.
 */
(function (root) {
  'use strict';

  function mustReplace(source, needle, replacement, label) {
    if (!source.includes(needle)) {
      throw new Error('B2 v27 transform: missing ' + label);
    }
    return source.replace(needle, replacement);
  }

  function applyHomeInfrastructureColorV27(home) {
    if (typeof home !== 'string' || !home.length) {
      throw new TypeError('B2 v27 transform expects the accepted v26 Home HTML string');
    }

    var chromeScript = `
<script id="dante-home-infrastructure-color-v27">
(function(){
'use strict';
const O='#EA5C12', OT='#F0A06F', OS='rgba(234,92,18,.11)', OB='rgba(234,92,18,.38)', N='#AEB9BD', NB='rgba(159,177,184,.14)';
function f(e,p,v){if(e)e.style.setProperty(p,v,'important')}
function orange(e,filled){if(!e)return;f(e,'color',filled?'#fff':OT);f(e,'border-color',OB);f(e,'background',filled?O:OS);f(e,'box-shadow','none')}
function neutral(e){if(!e)return;f(e,'color',N);f(e,'border-color',NB);f(e,'box-shadow','none')}
function exact(root,t){t=String(t).trim().toLowerCase();return Array.from(root.querySelectorAll('*')).find(e=>(e.textContent||'').trim().toLowerCase()===t)||null}
function card(label){let e=label;while(e&&e.parentElement){const r=e.getBoundingClientRect(),txt=(e.textContent||'').trim();if(r.width>=230&&r.height>=100&&txt.length>=30)return e;e=e.parentElement}return label&&label.parentElement}
function purpleSample(cs){const s=(cs.color+' '+cs.backgroundColor+' '+cs.borderTopColor+' '+cs.boxShadow);return /(?:137, 101, 255|124, 92, 255|139, 101, 255|142, 103, 255|151, 124, 255|122, 88, 255|149, 116, 255|168, 148, 255)/.test(s)}
function smallPurple(scope){if(!scope)return;scope.querySelectorAll('*').forEach(e=>{const r=e.getBoundingClientRect(),cs=getComputedStyle(e);if(r.width<=42&&r.height<=42&&purpleSample(cs)){f(e,'color',OT);f(e,'border-color',OB);if(cs.backgroundColor!=='rgba(0, 0, 0, 0)')f(e,'background-color',OS);f(e,'box-shadow','none')}})}
function temporal(root){
 const now=root.querySelector('#goNow');if(now){orange(now,false);now.querySelectorAll('*').forEach(e=>{const r=e.getBoundingClientRect();if(r.width<=10&&r.height<=10){f(e,'background',O);f(e,'color',O)}else f(e,'color',OT)})}
 const week=root.querySelector('#weekStrip');if(week)week.querySelectorAll('button').forEach(b=>{const a=b.classList.contains('is-viewing')||b.classList.contains('is-today')||b.classList.contains('active')||b.getAttribute('aria-selected')==='true';a?orange(b,false):neutral(b);if(a)b.querySelectorAll('*').forEach(e=>{const r=e.getBoundingClientRect();if(r.width<=10&&r.height<=10){f(e,'background',O);f(e,'color',O)}else f(e,'color',OT)})});
 const line=root.querySelector('.tl-nowline');if(line){f(line,'background','linear-gradient(90deg,#EA5C12,rgba(234,92,18,.60),transparent)');const s=line.querySelector('span');if(s){f(s,'background','#C94B0E');f(s,'color','#fff')}}
}
function capture(root){const l=exact(root,'Cattura'),c=card(l);if(!c)return;c.querySelectorAll('button,[role="button"]').forEach(b=>{const t=(b.textContent||'').trim().toLowerCase(),m=[b.getAttribute('aria-label')||'',b.getAttribute('title')||'',String(b.className||'')].join(' ').toLowerCase();(t==='+'||/\\b(send|invia|submit|capture|cattura|registra)\\b/.test(m))?orange(b,false):neutral(b)});Array.from(c.querySelectorAll('*')).filter(e=>(e.textContent||'').trim().toLowerCase()==='registrato').forEach(reg=>{const row=reg.parentElement;if(row)row.querySelectorAll('*').forEach(d=>{if(d===reg)return;const r=d.getBoundingClientRect();if(r.width<=12&&r.height<=12){f(d,'background',O);f(d,'color',O);f(d,'border-color',OB);f(d,'box-shadow','none')}})});smallPurple(c)}
function resolution(root){const l=exact(root,'Da risolvere'),c=card(l);if(c){c.querySelectorAll('button,[role="button"]').forEach(b=>neutral(b));smallPurple(c)}const confirm=exact(root,'Conferma');if(confirm)orange(confirm.closest('button,[role="button"]')||confirm,false)}
function apply(){const h=document.querySelector('lifeos-today'),r=h&&h.shadowRoot;if(!r)return false;temporal(r);capture(r);resolution(r);return true}
let ob=null;function bind(){const h=document.querySelector('lifeos-today'),r=h&&h.shadowRoot;if(!r)return false;if(!ob){ob=new MutationObserver(()=>requestAnimationFrame(apply));ob.observe(r,{subtree:true,childList:true,attributes:true,attributeFilter:['class','aria-selected','aria-pressed','aria-expanded']})}return true}
let n=0,t=setInterval(()=>{n++;apply();bind();if(n>=100)clearInterval(t)},80);if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',apply,{once:true});else apply();window.addEventListener('resize',apply,{passive:true});
})();
</script>`;

    home = mustReplace(home, '</body>', chromeScript + '\n</body>', 'body close');
    return home;
  }

  root.applyHomeInfrastructureColorV27 = applyHomeInfrastructureColorV27;
  if (typeof module !== 'undefined' && module.exports) {
    module.exports = { applyHomeInfrastructureColorV27: applyHomeInfrastructureColorV27 };
  }
})(typeof globalThis !== 'undefined' ? globalThis : this);
