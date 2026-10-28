// Shared shell behavior: persistent light/dark theme toggle across all
// P0001 report pages (sidebar/topbar navigation itself is plain links,
// no JS needed for that).
(function () {
  var KEY = "egobrainmini-theme";
  function apply(t) {
    if (t === "light" || t === "dark") {
      document.documentElement.setAttribute("data-theme", t);
    } else {
      document.documentElement.removeAttribute("data-theme");
    }
  }
  apply(localStorage.getItem(KEY));
  window.addEventListener("DOMContentLoaded", function () {
    var btn = document.getElementById("theme-toggle");
    if (!btn) return;
    btn.addEventListener("click", function () {
      var cur = document.documentElement.getAttribute("data-theme");
      var next = cur === "dark" ? "light" : "dark";
      localStorage.setItem(KEY, next);
      apply(next);
    });
  });
})();
