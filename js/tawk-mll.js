/**
 * Mike Levy Law — quiet Tawk.to embed
 * - Brand launcher (navy / tan), no flashy default bubble on load
 * - Widget stays hidden until support or visitor messages (or launcher click)
 * - Set widget chrome colors in Tawk dashboard to #1a2a4a / #a68b6d
 */
(function () {
  if (window.__MLL_TAWK_BOOT__) return;
  window.__MLL_TAWK_BOOT__ = true;

  var PROPERTY = "6ae76fff7ef3933c394c3c57";
  var WIDGET = "1k6c0r03d";
  var NAVY = "#1a2a4a";
  var TAN = "#a68b6d";
  var CREAM = "#fcfaf5";

  var Tawk_API = (window.Tawk_API = window.Tawk_API || {});
  window.Tawk_LoadStart = new Date();
  Tawk_API.customStyle = { zIndex: "45" };

  var state = { active: false, unread: 0 };

  function $(id) {
    return document.getElementById(id);
  }

  function injectStyles() {
    if ($("mll-tawk-styles")) return;
    var css =
      "#mll-chat-launch{position:fixed;right:20px;bottom:20px;z-index:44;" +
      "display:inline-flex;align-items:center;gap:8px;padding:11px 16px;" +
      "border:1px solid rgba(26,42,74,.14);border-radius:999px;" +
      "background:" +
      NAVY +
      ";color:" +
      CREAM +
      ";font:500 13px/1 Lato,system-ui,sans-serif;letter-spacing:.02em;" +
      "cursor:pointer;box-shadow:0 8px 24px rgba(18,32,56,.18);" +
      "opacity:.92;transition:opacity .2s ease,transform .2s ease,background .2s ease,box-shadow .2s ease;" +
      "-webkit-tap-highlight-color:transparent}" +
      "#mll-chat-launch:hover{opacity:1;background:#122038}" +
      "#mll-chat-launch:focus-visible{outline:2px solid " +
      TAN +
      ";outline-offset:3px}" +
      "#mll-chat-launch svg{width:15px;height:15px;flex:0 0 auto}" +
      "#mll-chat-launch .mll-chat-dot{display:none;width:8px;height:8px;border-radius:50%;" +
      "background:" +
      TAN +
      ";box-shadow:0 0 0 3px rgba(166,139,109,.28)}" +
      "#mll-chat-launch[data-active='1']{background:" +
      NAVY +
      ";box-shadow:0 10px 28px rgba(18,32,56,.22)}" +
      "#mll-chat-launch[data-unread='1'] .mll-chat-dot{display:block}" +
      "#mll-chat-launch[data-unread='1']{border-color:" +
      TAN +
      "}" +
      "@media (max-width:640px){#mll-chat-launch{right:14px;bottom:14px;padding:10px 14px;font-size:12px}}" +
      /* Keep default Tawk bubble quiet while our launcher owns the idle state */
      "body:not(.mll-tawk-live) iframe[title*='chat widget' i]," +
      "body:not(.mll-tawk-live) div[id^='tawk'] > iframe{opacity:0!important;pointer-events:none!important}";
    var style = document.createElement("style");
    style.id = "mll-tawk-styles";
    style.textContent = css;
    document.head.appendChild(style);
  }

  function ensureLauncher() {
    if ($("mll-chat-launch")) return;
    var btn = document.createElement("button");
    btn.type = "button";
    btn.id = "mll-chat-launch";
    btn.setAttribute("aria-label", "Chat with Mike Levy Law");
    btn.innerHTML =
      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true">' +
      '<path d="M4 6.5A2.5 2.5 0 0 1 6.5 4h11A2.5 2.5 0 0 1 20 6.5v7A2.5 2.5 0 0 1 17.5 16H9l-4 3.2V6.5z"/>' +
      "</svg><span>Chat</span><span class='mll-chat-dot' aria-hidden='true'></span>";
    btn.addEventListener("click", function () {
      openChat(true);
    });
    document.body.appendChild(btn);
  }

  function setLive(on) {
    state.active = !!on;
    document.body.classList.toggle("mll-tawk-live", !!on);
    var btn = $("mll-chat-launch");
    if (btn) btn.setAttribute("data-active", on ? "1" : "0");
  }

  function setUnread(n) {
    state.unread = n || 0;
    var btn = $("mll-chat-launch");
    if (btn) btn.setAttribute("data-unread", state.unread > 0 ? "1" : "0");
  }

  function revealBubble() {
    setLive(true);
    try {
      if (typeof Tawk_API.showWidget === "function") Tawk_API.showWidget();
    } catch (e) {}
  }

  function openChat(maximize) {
    revealBubble();
    try {
      if (typeof Tawk_API.start === "function") {
        Tawk_API.start({ showWidget: true });
      }
    } catch (e) {}
    try {
      if (maximize && typeof Tawk_API.maximize === "function") Tawk_API.maximize();
    } catch (e2) {}
    setUnread(0);
  }

  function hushDefaultBubble() {
    setLive(false);
    try {
      if (typeof Tawk_API.hideWidget === "function") Tawk_API.hideWidget();
      if (typeof Tawk_API.minimize === "function") Tawk_API.minimize();
    } catch (e) {}
  }

  Tawk_API.onLoad = function () {
    hushDefaultBubble();
  };

  Tawk_API.onChatMessageAgent = function () {
    revealBubble();
    setUnread((state.unread || 0) + 1);
    try {
      if (typeof Tawk_API.showWidget === "function") Tawk_API.showWidget();
    } catch (e) {}
  };

  Tawk_API.onChatMessageVisitor = function () {
    revealBubble();
  };

  Tawk_API.onChatMessageSystem = function () {
    /* stay quiet for generic system noise unless already live */
  };

  Tawk_API.onChatMaximized = function () {
    setLive(true);
    setUnread(0);
  };

  Tawk_API.onChatMinimized = function () {
    /* After a real conversation, leave the Tawk bubble available; idle stays on our launcher only */
    if (!state.active) hushDefaultBubble();
  };

  function boot() {
    injectStyles();
    ensureLauncher();
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
