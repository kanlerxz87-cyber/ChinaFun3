// Minimal progressive enhancement: mobile nav toggle.
(function () {
  "use strict";
  var toggle = document.getElementById("navToggle");
  var nav = document.getElementById("nav");
  if (!toggle || !nav) return;
  toggle.addEventListener("click", function () {
    var open = nav.classList.toggle("open");
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
  });
})();
