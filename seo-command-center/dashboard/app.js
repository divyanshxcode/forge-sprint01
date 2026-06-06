/* app.js — SEO Command Center live cockpit. Plain DOM + SSE, no build step. */
const $ = (id) => document.getElementById(id);
let totals = { High: 0, Medium: 0, Low: 0, total: 0 };
let chart = null;

function initChart() {
  const ctx = document.getElementById('issueChart').getContext('2d');
  chart = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: ['High', 'Medium', 'Low'],
      datasets: [{
        data: [0, 0, 0],
        backgroundColor: ['#FF0000', '#e2b53e', '#3a3a42'],
        borderColor: '#242428',
        borderWidth: 2
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false }
      },
      cutout: '70%'
    }
  });
}

function updateChart() {
  if (!chart) return;
  chart.data.datasets[0].data = [totals.High, totals.Medium, totals.Low];
  chart.update();
}

function log(msg) {
  const l = $("log"); if (l.querySelector(".empty")) l.innerHTML = "";
  const d = document.createElement("div"); d.textContent = "› " + msg; l.appendChild(d); l.scrollTop = l.scrollHeight;
}

function addIssue(i) {
  const tb = $("tbody"); if (tb.querySelector(".empty")) tb.innerHTML = "";
  const tr = document.createElement("tr");
  tr.innerHTML = `<td><span class="sev ${i.severity.toLowerCase()}">${i.severity}</span></td>
                  <td>${i.type}</td><td>${i.count}</td>`;
  tb.appendChild(tr);
  totals[i.severity] = (totals[i.severity] || 0) + 1; totals.total++;
  $("c-total").textContent = totals.total; $("c-high").textContent = totals.High;
  $("c-med").textContent = totals.Medium; $("c-low").textContent = totals.Low;
  updateChart();
}

function handle({ event, data }) {
  if (event === "snapshot") {
    if (data.site) { $("meta").textContent = "· " + data.site; $("urls").textContent = (data.urls||0) + " URLs"; }
    (data.issues || []).forEach(addIssue);
  } else if (event === "loaded") {
    $("meta").textContent = "· " + data.site; $("urls").textContent = data.urls + " URLs";
    log(`Loaded ${data.urls} URLs from ${data.site}`); $("tbody").innerHTML = "";
    totals = { High:0, Medium:0, Low:0, total:0 };
    updateChart();
  } else if (event === "issue") { addIssue(data); log(`Found ${data.count} × ${data.type}`); }
  else if (event === "summary") { log(`Audit complete: ${data.total_issues} issue types`); }
  else if (event === "fixes") {
    log(`Fixes ready: ${(data.titles||[]).length} titles, ${(data.redirect_map||[]).length} redirects`);
    $("f-titles").textContent = (data.titles||[]).length;
    $("f-redirs").textContent = (data.redirect_map||[]).length;
    // Note: Meta and H1 fixes aren't explicitly passed in the 'fixes' event in server.py,
    // but we'll track them if the server is updated to emit them.
  }
  else if (event === "exported") { $("export").innerHTML = "<b>report.html written ✓</b><br><span style='color:#c8c5be;font-size:12px'>Open or email outputs/report.html to the client.</span>"; }
  else if (event === "saved") { log("report.json saved"); }
}

initChart();
const es = new EventSource("/events");
es.onmessage = (m) => { try { handle(JSON.parse(m.data)); } catch (e) {} };
