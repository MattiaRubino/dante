/*
 * B2 Home Shell & Timeline v25
 * Deterministic prototype-layer transform over the accepted v24 Home string.
 * No backend/API/domain semantics are introduced here.
 */
(function (root) {
  'use strict';

  function mustReplace(source, needle, replacement, label) {
    if (!source.includes(needle)) {
      throw new Error('B2 v25 transform: missing ' + label);
    }
    return source.replace(needle, replacement);
  }

  function applyHomeShellTimelineV25(home) {
    if (typeof home !== 'string' || !home.length) {
      throw new TypeError('B2 v25 transform expects the accepted v24 Home HTML string');
    }

    /* ---------- global app bar ---------- */
    var createMatch = home.match(/<button class="tb-create tb-create-main"[\s\S]*?<\/button>/);
    var searchMatch = home.match(/<button class="tb-search tb-search-right"[\s\S]*?<\/button>/);
    if (!createMatch || !searchMatch) {
      throw new Error('B2 v25 transform: topbar controls not found');
    }

    var createHtml = createMatch[0];
    var searchHtml = searchMatch[0];
    home = home.replace(createHtml, '');
    home = home.replace(searchHtml, '');

    var leftPattern = /(<div class="tb-left-a">[\s\S]*?)(\s*<\/div>\s*<nav class="tb-nav tb-nav-a")/;
    if (!leftPattern.test(home)) {
      throw new Error('B2 v25 transform: left topbar group not found');
    }
    home = home.replace(leftPattern, '$1\n    ' + searchHtml + '$2');

    var reviewMarker = '<button class="tb-review"';
    home = mustReplace(
      home,
      reviewMarker,
      createHtml + '\n\n    ' + reviewMarker,
      'review anchor'
    );

    var shellCss = `
<style id="dante-home-shell-v25">
.app{padding-top:0!important}
.topbar.tb-a{
  position:sticky!important;top:0!important;z-index:900!important;
  width:100vw!important;max-width:none!important;margin-left:calc(50% - 50vw)!important;
  height:64px!important;padding:0 24px!important;
  border:0!important;border-bottom:1px solid rgba(159,177,184,.13)!important;border-radius:0!important;
  background:rgba(14,20,23,.955)!important;
  -webkit-backdrop-filter:blur(20px) saturate(125%)!important;
  backdrop-filter:blur(20px) saturate(125%)!important;
  box-shadow:0 1px 0 rgba(255,255,255,.018) inset,0 10px 30px rgba(0,0,0,.20)!important;
}
.tb-left-a{min-width:0!important;display:flex!important;align-items:center!important;gap:24px!important}
.tb-left-a .tb-brand{min-width:0!important;flex:0 0 auto!important}
.tb-left-a .tb-search-right{
  width:220px!important;min-width:220px!important;height:38px!important;padding:0 11px!important;
  display:flex!important;align-items:center!important;justify-content:flex-start!important;gap:8px!important;
  border:1px solid rgba(159,177,184,.12)!important;border-radius:10px!important;
  background:rgba(255,255,255,.028)!important;color:var(--f-text-2,#B2BDC1)!important;box-shadow:none!important;
}
.tb-left-a .tb-search-right kbd{margin-left:auto!important;font:600 9px ui-monospace,monospace!important;color:var(--f-muted,#7D8A90)!important;border:0!important;background:transparent!important}
.tb-nav-a{
  position:absolute!important;left:50%!important;top:50%!important;transform:translate(-50%,-50%)!important;
  height:44px!important;display:flex!important;align-items:center!important;gap:2px!important;padding:3px!important;
  border:1px solid rgba(159,177,184,.115)!important;border-radius:13px!important;background:rgba(255,255,255,.025)!important;box-shadow:none!important;
}
.tb-nav-a button{height:36px!important;padding:0 13px!important;border-radius:10px!important}
.tb-utility-a{
  position:absolute!important;right:24px!important;top:50%!important;transform:translateY(-50%)!important;
  width:max-content!important;min-width:0!important;max-width:none!important;flex:0 0 auto!important;
  margin:0!important;padding:0!important;display:flex!important;align-items:center!important;justify-content:flex-end!important;gap:11px!important;
}
.tb-utility-a .tb-create-main{
  width:auto!important;min-width:92px!important;height:40px!important;padding:0 15px 0 13px!important;
  display:flex!important;align-items:center!important;justify-content:center!important;gap:8px!important;flex:0 0 auto!important;border-radius:11px!important;
}
.tb-utility-a .tb-review,.tb-utility-a .tb-grid-launcher,.tb-utility-a .tb-avatar{height:40px!important}
.tb-utility-a .tb-avatar{margin-right:0!important}
.tb-search-pop{top:72px!important;left:24px!important;right:auto!important}
.tb-create-pop{top:72px!important;left:auto!important;right:24px!important}
.hero{border-left:0!important;border-right:0!important}
@media(max-width:1240px){
  .tb-left-a{gap:14px!important}
  .tb-left-a .tb-search-right{width:42px!important;min-width:42px!important;padding:0!important;justify-content:center!important}
  .tb-left-a .tb-search-right .tb-search-label,.tb-left-a .tb-search-right kbd{display:none!important}
}
@media(max-width:980px){
  .tb-utility-a .tb-create-main{min-width:42px!important;width:42px!important;padding:0!important}
  .tb-utility-a .tb-create-main span{display:none!important}
}
</style>`;
    home = mustReplace(home, '</head>', shellCss + '\n</head>', 'head close');

    /* ---------- timeline contextual add ---------- */
    var calZonePattern = /(<div class="cal-zone">\s*)(<button class="cal-trigger" id="calTrigger")/;
    if (!calZonePattern.test(home)) {
      throw new Error('B2 v25 transform: cal-zone markup not found');
    }
    home = home.replace(
      calZonePattern,
      '$1<button class="tl-quick-add-v25" id="tlQuickAddV25" type="button" aria-label="Aggiungi alla timeline" title="Aggiungi alla timeline">+</button>\n          $2'
    );

    home = mustReplace(
      home,
      'grid-template-columns:auto auto minmax(330px,1fr) auto !important;',
      'grid-template-columns:56px auto auto minmax(330px,1fr) auto !important;',
      'desktop temporal grid columns'
    );
    home = mustReplace(
      home,
      'grid-template-areas:"month now week actions" !important;',
      'grid-template-areas:"add month now week actions" !important;',
      'temporal grid areas'
    );
    home = mustReplace(
      home,
      'grid-template-columns:auto auto minmax(300px,1fr) auto !important;gap:8px !important',
      'grid-template-columns:56px auto auto minmax(300px,1fr) auto !important;gap:10px !important',
      'responsive temporal grid columns'
    );

    var monthRuleRe = /(\s*\.cal-trigger\{\s*\n\s*grid-area:month !important;justify-self:start !important;)/;
    var addRule = `      .tl-quick-add-v25{
        grid-area:add !important;justify-self:start !important;align-self:center !important;
        width:42px !important;min-width:42px !important;height:42px !important;padding:0 !important;margin:0 !important;
        border:1px solid rgba(234,92,18,.34) !important;border-radius:14px !important;
        background:linear-gradient(180deg,rgba(18,27,40,.96),rgba(11,18,29,.98)) !important;color:#F06A1A !important;
        box-shadow:inset 0 1px 0 rgba(255,255,255,.04),0 10px 24px rgba(0,0,0,.18) !important;
        display:grid !important;place-items:center !important;font-size:24px !important;font-weight:500 !important;line-height:1 !important;cursor:pointer !important;
      }
      .tl-quick-add-v25:hover{background:linear-gradient(180deg,rgba(27,39,55,.98),rgba(14,23,35,.99)) !important;border-color:rgba(234,92,18,.52) !important;box-shadow:inset 0 1px 0 rgba(255,255,255,.05),0 12px 26px rgba(0,0,0,.22) !important}
      .tl-quick-add-v25:focus-visible{outline:2px solid rgba(234,92,18,.42) !important;outline-offset:2px !important}
`;
    if (!monthRuleRe.test(home)) {
      throw new Error('B2 v25 transform: missing calendar toolbar rule');
    }
    home = home.replace(monthRuleRe, addRule + '$1');

    var bindMarker = '  bind(){\n    const r=this.root;';
    home = mustReplace(
      home,
      bindMarker,
      bindMarker + "\n    const quickAddV25=r.getElementById('tlQuickAddV25');\n    if(quickAddV25)quickAddV25.onclick=()=>{const create=document.querySelector('.tb-create-main');if(create)create.click()};",
      'timeline bind()'
    );

    return home;
  }

  root.applyHomeShellTimelineV25 = applyHomeShellTimelineV25;
  if (typeof module !== 'undefined' && module.exports) {
    module.exports = { applyHomeShellTimelineV25: applyHomeShellTimelineV25 };
  }
})(typeof globalThis !== 'undefined' ? globalThis : this);
