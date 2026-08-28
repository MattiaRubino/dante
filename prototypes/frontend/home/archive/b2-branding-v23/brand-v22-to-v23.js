/* DANTE Home B2 v23 — approved brand alignment layer
 * Applies identically to B2 v22 FULL and PARTIAL reconstructed outputs.
 * Scope: topbar brand + AI identity only. No layout, timeline, stage, rail,
 * palette or background changes.
 */
(function(){
  'use strict';

  const SYMBOL =
    'https://raw.githubusercontent.com/MattiaRubino/dante/db02da603f3779d8c7fcb1d7601f6f66f8a23241/assets/brand/logo/master/dante-symbol-master-v0.svg';
  const WORDMARK =
    'https://raw.githubusercontent.com/MattiaRubino/dante/db02da603f3779d8c7fcb1d7601f6f66f8a23241/assets/brand/wordmark/master/dante-wordmark-master-v0.svg';

  const STYLE_ID = 'dante-brand-pass-v23-style';

  function installStyle(){
    if(document.getElementById(STYLE_ID)) return;
    const style = document.createElement('style');
    style.id = STYLE_ID;
    style.textContent = `
      .tb-brand-lockup.dante-brand-lockup{
        min-width:205px!important;
        display:flex!important;
        align-items:center!important;
        gap:14px!important;
      }
      .dante-topbar-symbol{
        display:block;
        width:39px;
        height:39px;
        flex:0 0 39px;
      }
      .dante-topbar-symbol>svg{
        display:block;
        width:39px;
        height:39px;
      }
      .dante-topbar-wordmark{
        display:block;
        width:auto;
        height:18px;
        flex:0 0 auto;
      }
      .dante-topbar-wordmark>svg{
        display:block;
        width:auto;
        height:18px;
      }
      .ai-chat-identity{
        display:flex!important;
        align-items:center!important;
        gap:0!important;
      }
      .dante-ai-symbol-only{
        display:block;
        width:25px;
        height:25px;
        flex:0 0 25px;
      }
      .dante-ai-symbol-only>svg{
        display:block;
        width:25px;
        height:25px;
      }
      .ai-chat-identity .ai-head-label{
        display:none!important;
      }
      @media(max-width:900px){
        .tb-brand-lockup.dante-brand-lockup{
          min-width:auto!important;
          gap:11px!important;
        }
        .dante-topbar-symbol,
        .dante-topbar-symbol>svg{
          width:35px;
          height:35px;
        }
        .dante-topbar-wordmark,
        .dante-topbar-wordmark>svg{
          height:16px;
        }
      }
    `;
    document.head.appendChild(style);
  }

  function apply(symbolSvg, wordmarkSvg){
    installStyle();

    const lockup = document.querySelector('.tb-brand-lockup');
    if(lockup && !lockup.classList.contains('dante-brand-lockup')){
      const whiteWordmark = wordmarkSvg.replaceAll('#222F37', '#FFFFFF');
      lockup.classList.add('dante-brand-lockup');
      lockup.setAttribute('aria-label','DANTE');
      lockup.innerHTML =
        '<span class="dante-topbar-symbol" aria-hidden="true">' +
          symbolSvg +
        '</span>' +
        '<span class="dante-topbar-wordmark" aria-hidden="true">' +
          whiteWordmark +
        '</span>';
    }

    const aiIdentity = document.querySelector('.ai-chat-identity');
    if(aiIdentity){
      aiIdentity.setAttribute('aria-label','Assistente');

      const oldOrb = aiIdentity.querySelector('.ai-chat-orb');
      if(oldOrb && !aiIdentity.querySelector('.dante-ai-symbol-only')){
        const holder = document.createElement('span');
        holder.className = 'dante-ai-symbol-only';
        holder.setAttribute('aria-hidden','true');
        holder.innerHTML = symbolSvg;
        oldOrb.replaceWith(holder);
      }

      const oldLabel = aiIdentity.querySelector('.ai-head-label');
      if(oldLabel) oldLabel.remove();
    }
  }

  Promise.all([
    fetch(SYMBOL, {cache:'force-cache'}).then(function(r){
      if(!r.ok) throw new Error('DANTE symbol HTTP ' + r.status);
      return r.text();
    }),
    fetch(WORDMARK, {cache:'force-cache'}).then(function(r){
      if(!r.ok) throw new Error('DANTE wordmark HTTP ' + r.status);
      return r.text();
    })
  ]).then(function(parts){
    apply(parts[0], parts[1]);
  }).catch(function(err){
    console.error('DANTE Home B2 v23 branding:', err);
  });
})();
