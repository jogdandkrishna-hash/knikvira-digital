/*
 * Knikvira AI — webchat launcher branding
 * Botpress webchat v5 has no `launchButtonIcon` config key (verified against
 * cdn.botpress.cloud/webchat/v5.0/inject.js), and the default FAB glyph is an
 * inline SVG masked via `-webkit-mask` on `.bpFabIcon` — so a background-image
 * on that element would be clipped to the glyph. Instead we hide `.bpFabIcon`
 * and append an <img> using Botpress's own `.bpFabImage` rules.
 * Also swaps the configured botAvatar (apple-touch-icon.png) in the chat panel.
 */
(function () {
  "use strict";

  var LOGO = "/img/bot-avatar.png";
  var MARK = "data-kv-logo"; /* our launcher image */
  var AMARK = "data-kv-av"; /* a swapped avatar image */

  function patchFab(root) {
    var changed = 0;
    if (!root || !root.querySelectorAll) return 0;

    // .bpFabContainer is the painted, rounded box; only fall back to .bpFab
    // (its parent) when no container exists, so we never insert twice.
    var containers = root.querySelectorAll(".bpFabContainer");
    if (!containers.length) containers = root.querySelectorAll(".bpFab");
    for (var i = 0; i < containers.length; i++) {
      var box = containers[i];
      if (box.querySelector(":scope > img[" + MARK + "]")) continue;
      var glyph = box.querySelector(".bpFabIcon");
      if (glyph) glyph.style.display = "none";
      box.style.setProperty("background", "transparent", "important");
      var img = document.createElement("img");
      img.src = LOGO;
      img.alt = "Knikvira AI";
      img.className = "bpFabImage";
      img.setAttribute(MARK, "1");
      img.setAttribute(
        "style",
        "width:100%;height:100%;display:block;border-radius:50%;object-fit:cover;background:#4f46e5"
      );
      box.appendChild(img);
      changed++;
    }
    return changed;
  }

  function patchAvatars(root) {
    var n = 0;
    if (!root || !root.querySelectorAll) return 0;
    var imgs = root.querySelectorAll('img[src*="apple-touch-icon"]');
    for (var i = 0; i < imgs.length; i++) {
      if (imgs[i].getAttribute(AMARK) === "1") continue;
      imgs[i].setAttribute(AMARK, "1");
      imgs[i].src = LOGO;
      n++;
    }
    return n;
  }

  function walk(root) {
    var hits = patchFab(root) + patchAvatars(root);
    if (root.querySelectorAll) {
      var all = root.querySelectorAll("*");
      for (var i = 0; i < all.length; i++) {
        if (all[i].shadowRoot) hits += walk(all[i].shadowRoot);
      }
    }
    return hits;
  }

  function run() {
    try {
      walk(document);
    } catch (e) {
      /* branding must never break the page */
    }
  }

  var scheduled = false;
  function schedule() {
    if (scheduled) return;
    scheduled = true;
    setTimeout(function () {
      scheduled = false;
      run();
    }, 0);
  }

  if (window.MutationObserver) {
    new MutationObserver(schedule).observe(document.documentElement, {
      childList: true,
      subtree: true,
      attributes: true,
      attributeFilter: ["src", "class", "style"],
    });
  }
  // The panel (and its header avatar) is built lazily on open/toggle.
  document.addEventListener(
    "click",
    function () {
      setTimeout(run, 150);
      setTimeout(run, 700);
    },
    true
  );
  run();
})();
