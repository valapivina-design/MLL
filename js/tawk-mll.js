/**
 * Mike Levy Law — Tawk.to embed (native widget button only)
 */
(function () {
  if (window.__MLL_TAWK_BOOT__) return;
  window.__MLL_TAWK_BOOT__ = true;

  var PROPERTY = "6ae76fff7ef3933c394c3c57";
  var WIDGET = "1k6c0r03d";

  window.Tawk_API = window.Tawk_API || {};
  window.Tawk_LoadStart = new Date();
  window.Tawk_API.customStyle = { zIndex: "45" };

  function boot() {
    if (document.querySelector('script[src*="embed.tawk.to/' + PROPERTY + '"]')) return;
    var s1 = document.createElement("script");
    var s0 = document.getElementsByTagName("script")[0];
    s1.async = true;
    s1.src = "https://embed.tawk.to/" + PROPERTY + "/" + WIDGET;
    s1.charset = "UTF-8";
    s1.setAttribute("crossorigin", "*");
    if (s0 && s0.parentNode) s0.parentNode.insertBefore(s1, s0);
    else document.head.appendChild(s1);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
