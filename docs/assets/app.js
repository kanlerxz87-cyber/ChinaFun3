/* Renders the JSON data files into responsive tables.
   Rule: any empty value is shown as "Unverified" and is never filled in. */
(function () {
  "use strict";

  function esc(s) {
    return String(s)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;").replace(/'/g, "&#39;");
  }

  var URL_RE = /(https?:\/\/[^\s·,;)]+)/g;

  // Turn any URLs inside text into links.
  function linkify(text) {
    return esc(text).replace(URL_RE, function (u) {
      return '<a href="' + u + '" target="_blank" rel="noopener">' + u.replace(/^https?:\/\//, "").slice(0, 48) + "…</a>";
    });
  }

  function isEmpty(v) {
    return v === null || v === undefined || v === "";
  }

  function cellHtml(value, col) {
    if (col.type === "source") {
      if (!value || !value.url) {
        return '<span class="unverified">Unverified — no official source yet</span>';
      }
      return esc(value.label || "Source") + '<br><a href="' + esc(value.url) +
        '" target="_blank" rel="noopener">Open source ↗</a>';
    }
    if (isEmpty(value)) {
      return '<span class="unverified">Unverified</span>';
    }
    if (typeof value === "object") {
      return esc(JSON.stringify(value));
    }
    return linkify(value);
  }

  function renderTable(columns, rows) {
    if (!rows || rows.length === 0) {
      return '<div class="empty">No verified rows yet.</div>';
    }
    var head = columns.map(function (c) { return "<th>" + esc(c.label) + "</th>"; }).join("");
    var body = rows.map(function (r) {
      return "<tr>" + columns.map(function (c) {
        var cls = c.type === "source" ? "" : " cell-text";
        return '<td class="' + cls.trim() + '" data-label="' + esc(c.label) + '">' +
          cellHtml(r[c.key], c) + "</td>";
      }).join("") + "</tr>";
    }).join("");
    return '<div class="table-wrap"><table class="data"><thead><tr>' + head +
      "</tr></thead><tbody>" + body + "</tbody></table></div>";
  }

  // Derive columns from an array of plain objects (used for extra lists).
  function columnsFrom(arr) {
    var keys = [];
    arr.forEach(function (o) {
      Object.keys(o).forEach(function (k) { if (keys.indexOf(k) < 0) keys.push(k); });
    });
    return keys.map(function (k) { return { key: k, label: k.replace(/_/g, " ") }; });
  }

  function renderSection(title, data) {
    return "<h2>" + esc(title) + "</h2>";
  }

  function countUnverified(data) {
    var n = 0;
    (data.rows || []).forEach(function (r) {
      (data.columns || []).forEach(function (c) {
        if (c.type === "source") {
          if (!r[c.key] || !r[c.key].url) n++;
        } else if (isEmpty(r[c.key])) {
          n++;
        }
      });
    });
    return n;
  }

  function renderPage(el, data) {
    var html = "";
    if (data.title) html += "<h1>" + esc(data.title) + "</h1>";
    if (data.intro) html += '<p class="lead">' + esc(data.intro) + "</p>";

    if (data.summary) {
      html += '<div class="card"><h3>Summary</h3><ul class="plain">' +
        data.summary.map(function (s) { return "<li>" + linkify(s) + "</li>"; }).join("") + "</ul></div>";
    }
    if (data.repo_facts) {
      html += '<h2>Repository facts</h2>' + renderTable(columnsFrom(data.repo_facts), data.repo_facts);
    }
    if (data.requirements) {
      html += '<div class="card"><h3>Requirements</h3><ul class="plain">' +
        data.requirements.map(function (s) { return "<li>" + esc(s) + "</li>"; }).join("") + "</ul></div>";
    }
    if (data.columns && data.rows) {
      html += renderTable(data.columns, data.rows);
    }
    if (data.checks) {
      html += "<h2>Checks</h2>" + renderTable(columnsFrom(data.checks), data.checks);
    }
    if (data.leads) {
      html += "<h2>Leads (not verified)</h2>" + renderTable(columnsFrom(data.leads), data.leads);
    }
    el.innerHTML = html;
  }

  function init() {
    var els = document.querySelectorAll("[data-src]");
    Array.prototype.forEach.call(els, function (el) {
      fetch(el.getAttribute("data-src"), { cache: "no-cache" })
        .then(function (r) {
          if (!r.ok) throw new Error(r.status);
          return r.json();
        })
        .then(function (data) { renderPage(el, data); })
        .catch(function (e) {
          el.innerHTML = '<div class="flag">Could not load data (' + esc(e.message) +
            '). Open the site from its published URL, not from a file.</div>';
        });
    });

    // Dashboard counts
    var stats = document.querySelectorAll("[data-count-src]");
    Array.prototype.forEach.call(stats, function (el) {
      fetch(el.getAttribute("data-count-src"), { cache: "no-cache" })
        .then(function (r) { return r.json(); })
        .then(function (data) {
          var rows = (data.rows || []).length;
          var unv = countUnverified(data);
          el.textContent = rows + " rows · " + unv + " unverified cells";
        })
        .catch(function () { el.textContent = "data unavailable"; });
    });
  }

  window.ChinaFun3 = { renderTable: renderTable, countUnverified: countUnverified };
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
