/*
 * B2 Home Edge Attachment v26
 * Deterministic prototype-layer transform over the accepted v25 Home string.
 * No backend/API/domain semantics are introduced here.
 */
(function (root) {
  'use strict';

  function mustReplace(source, needle, replacement, label) {
    if (!source.includes(needle)) {
      throw new Error('B2 v26 transform: missing ' + label);
    }
    return source.replace(needle, replacement);
  }

  function applyHomeEdgeAttachmentV26(home) {
    if (typeof home !== 'string' || !home.length) {
      throw new TypeError('B2 v26 transform expects the accepted v25 Home HTML string');
    }

    var edgeCss = `
<style id="dante-home-edge-attachment-v26">
.app{
  width:100%!important;
  max-width:none!important;
  margin-left:0!important;
  margin-right:0!important;
}

/* Expanded AI: keep parent geometry, attach only the visible card to the left edge. */
#lifeosHero.home-vnext-test .hero-left-panel{
  overflow:visible!important;
}
#lifeosHero.home-vnext-test .hero-left-panel .ai-card.ai-chat-pro{
  margin-left:calc(0px - var(--hv-outer))!important;
  width:calc(100% + var(--hv-outer))!important;
  border-radius:0 20px 20px 0!important;
}

/* Collapsed AI: target the exact rail created by the Home structure layer. */
#lifeosHero.home-vnext-test.ai-collapsed .home-ai-rail{
  left:0!important;
  border-radius:0 18px 18px 0!important;
}
</style>`;

    var edgeScript = `
<script id="dante-home-timeline-edge-v26">
(function(){
  'use strict';

  function apply(){
    var host = document.querySelector('lifeos-today');
    if(!host || !host.shadowRoot) return false;

    /* Preserve the component's existing right margin; remove only the attached-side margin. */
    host.style.setProperty('margin-left','0px','important');

    var today = host.shadowRoot.querySelector('.today');
    if(!today) return false;

    today.style.setProperty('border-top-left-radius','0px','important');
    today.style.setProperty('border-bottom-left-radius','0px','important');
    return true;
  }

  var attempts = 0;
  var timer = setInterval(function(){
    attempts += 1;
    if(apply() || attempts >= 80) clearInterval(timer);
  },50);

  if(document.readyState === 'loading'){
    document.addEventListener('DOMContentLoaded',apply,{once:true});
  }else{
    apply();
  }

  window.addEventListener('resize',apply,{passive:true});
})();
</script>`;

    home = mustReplace(home, '</head>', edgeCss + '\n</head>', 'head close');
    home = mustReplace(home, '</body>', edgeScript + '\n</body>', 'body close');

    return home;
  }

  root.applyHomeEdgeAttachmentV26 = applyHomeEdgeAttachmentV26;
  if (typeof module !== 'undefined' && module.exports) {
    module.exports = { applyHomeEdgeAttachmentV26: applyHomeEdgeAttachmentV26 };
  }
})(typeof globalThis !== 'undefined' ? globalThis : this);
