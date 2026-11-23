/* =====================================================================
   Vinho Verde · sitio de resultados
   Lee window.WINE (generado por src/exportar_web.py) y construye todo.
   ===================================================================== */
(function () {
  "use strict";

  const W = window.WINE;
  if (!W) {
    document.body.innerHTML = '<div style="padding:4rem;font-family:sans-serif">' +
      'No se encontró <code>web/data/resultados.js</code>. Ejecuta <code>python src/main.py</code> primero.</div>';
    return;
  }

  /* ---------- utilidades ---------- */
  const $ = (s) => document.querySelector(s);
  const css = getComputedStyle(document.documentElement);
  const C = {
    text: css.getPropertyValue("--text").trim(),
    muted: css.getPropertyValue("--muted").trim(),
    wine: css.getPropertyValue("--wine").trim(),
    wine2: css.getPropertyValue("--wine-2").trim(),
    gold: css.getPropertyValue("--gold").trim(),
    tinto: css.getPropertyValue("--tinto").trim(),
    blanco: css.getPropertyValue("--blanco").trim(),
    grid: "rgba(74,24,42,.07)",
    card: css.getPropertyValue("--card").trim(),
    card2: css.getPropertyValue("--card-2").trim(),
    font: "Plus Jakarta Sans, system-ui, sans-serif",
    ok: css.getPropertyValue("--ok").trim(),
  };
  const TIPO_COLOR = { tinto: C.tinto, blanco: C.blanco };
  const ETQ = Object.fromEntries(W.variables.map((v) => [v.key, v.etiqueta]));
  const FEATURES = W.variables.filter((v) => v.key !== "quality").map((v) => v.key);

  const fmt = (x, d = 3) => (x === null || x === undefined || Number.isNaN(x) ? "—" :
    Number(x).toLocaleString("es-MX", { minimumFractionDigits: d, maximumFractionDigits: d }));
  const fmtInt = (x) => Number(x).toLocaleString("es-MX");
  const fmtP = (p) => (p === null || p === undefined ? "—" : p < 0.001 ? "< 0.001" : fmt(p, 3));
  const el = (tag, attrs = {}, html = "") => {
    const e = document.createElement(tag);
    Object.entries(attrs).forEach(([k, v]) => (k === "class" ? (e.className = v) : e.setAttribute(k, v)));
    e.innerHTML = html;
    return e;
  };

  const baseLayout = (extra = {}) => ({
    paper_bgcolor: "rgba(0,0,0,0)",
    plot_bgcolor: "rgba(0,0,0,0)",
    font: { family: C.font, color: C.muted, size: 12 },
    margin: { l: 50, r: 20, t: 20, b: 45 },
    xaxis: { gridcolor: C.grid, zerolinecolor: C.grid, linecolor: C.grid },
    yaxis: { gridcolor: C.grid, zerolinecolor: C.grid, linecolor: C.grid },
    legend: { orientation: "h", y: 1.1, x: 0, font: { color: C.text } },
    hoverlabel: { bgcolor: C.card, bordercolor: C.wine2, font: { color: C.text, family: C.font } },
    ...extra,
  });
  // Interpola valores numéricos a colores entre C.wine y C.gold (evita colores numéricos en Plotly)
  const escala = (vals) => {
    const hex = (h) => { h = h.replace("#", ""); if (h.length === 3) h = [...h].map((c) => c + c).join(""); return [0, 2, 4].map((i) => parseInt(h.slice(i, i + 2), 16)); };
    const a = hex(C.wine), b = hex(C.gold);
    const lo = Math.min(...vals), hi = Math.max(...vals), span = hi - lo || 1;
    return vals.map((v) => { const t = (v - lo) / span; return `rgb(${a.map((x, i) => Math.round(x + (b[i] - x) * t)).join(",")})`; });
  };
  const CFG = { displayModeBar: false, responsive: true };
  const plot = (id, data, layout) => Plotly.newPlot(id, data, baseLayout(layout), CFG);

  const tabla = (id, cols, filas) => {
    const t = $(id);
    t.innerHTML = "<thead><tr>" + cols.map((c) => `<th class="${c.num ? "num" : ""}">${c.t}</th>`).join("") +
      "</tr></thead><tbody>" + filas.map((f) => `<tr class="${f._clase || ""}">` + cols.map((c) =>
        `<td class="${c.num ? "num" : ""}">${c.f ? c.f(f[c.k], f) : f[c.k] ?? "—"}</td>`).join("") + "</tr>").join("") +
      "</tbody>";
  };

  /* ---------- HERO ---------- */
  const M = W.meta;
  const D = W.datos;
  const n = D.quality.length;
  const mediaCal = D.quality.reduce((a, b) => a + b, 0) / n;
  $("#hero-materia").textContent = `${M.materia} · Proyecto final`;
  $("#hero-titulo").textContent = M.titulo;
  [
    [fmtInt(n), "muestras analizadas"],
    ["11", "variables fisicoquímicas"],
    [fmtInt(W.limpieza.duplicados ?? 0), "duplicados eliminados"],
    [fmt(mediaCal, 2), "calidad promedio (0–10)"],
  ].forEach(([v, l]) => $("#hero-kpis").append(el("div", { class: "kpi" }, `<div class="kpi-val">${v}</div><div class="kpi-lbl">${l}</div>`)));
  $("#hero-team").append(el("span", { class: "lider" }, `★ ${M.lider}`));
  M.integrantes.forEach((i) => $("#hero-team").append(el("span", {}, i)));
  $("#footer-inst").textContent = `${M.institucion} · ${M.materia}`;
  $("#alpha").textContent = `α = ${M.alpha}`;

  /* ---------- 01 DATASET ---------- */
  $("#cita").textContent = M.cita;
  plot("chart-tipos", [{
    type: "pie", hole: .62, labels: ["Tinto", "Blanco"], values: [M.n_tinto, M.n_blanco],
    marker: { colors: [C.tinto, C.blanco], line: { color: C.card, width: 3 } },
    textinfo: "label+percent", textfont: { color: [C.card, C.text], size: 13 },
    hovertemplate: "%{label}: %{value:,} muestras<extra></extra>", sort: false,
  }], {
    showlegend: false, margin: { l: 10, r: 10, t: 10, b: 10 },
    annotations: [{ text: `<b style="font-size:26px">${fmtInt(n)}</b><br>muestras`, showarrow: false, font: { color: C.text, family: C.font, size: 14 } }],
  });
  tabla("#tabla-variables", [
    { t: "Variable", k: "etiqueta" },
    { t: "Columna", k: "key", f: (v) => `<code>${v}</code>` },
    { t: "Unidad", k: "unidad" },
    { t: "Descripción", k: "descripcion", f: (v) => `<span class="desc">${v}</span>` },
  ], W.variables);

  /* ---------- 02 TRATAMIENTO ---------- */
  const L = W.limpieza;
  [
    [fmtInt(L.filas_originales), "registros originales", false],
    [fmtInt(L.nulos), "valores nulos", false],
    [`−${fmtInt(L.duplicados)}`, "duplicados eliminados", false],
    [fmtInt(L.filas_finales), "registros finales", true],
  ].forEach(([v, l, hl]) => $("#flow-limpieza").append(el("div", { class: "flow-step" + (hl ? " hl" : "") },
    `<div class="flow-val">${v}</div><div class="flow-lbl">${l}</div>`)));
  const out = [...L.outliers].sort((a, b) => a.pct_IQR - b.pct_IQR);
  plot("chart-outliers", [{
    type: "bar", orientation: "h", y: out.map((o) => ETQ[o.variable]), x: out.map((o) => o.pct_IQR),
    marker: { color: escala(out.map((o) => o.pct_IQR)) },
    text: out.map((o) => `${fmt(o.pct_IQR, 1)}%`), textposition: "outside", textfont: { color: C.text },
    customdata: out.map((o) => o.outliers_IQR),
    hovertemplate: "%{y}: %{customdata:,} registros (%{x:.2f}%)<extra></extra>",
  }], { margin: { l: 120, r: 50, t: 10, b: 40 }, xaxis: { gridcolor: C.grid, ticksuffix: "%" } });

  /* ---------- 03 DESCRIPTIVA ---------- */
  const califs = [...new Set(D.quality)].sort((a, b) => a - b);
  const conteo = (tipo) => califs.map((q) => D.quality.filter((x, i) => x === q && D.tipo[i] === tipo).length);
  plot("chart-calidad", ["tinto", "blanco"].map((t) => ({
    type: "bar", name: t[0].toUpperCase() + t.slice(1), x: califs, y: conteo(t),
    marker: { color: TIPO_COLOR[t] }, hovertemplate: "Calidad %{x}: %{y:,}<extra>" + t + "</extra>",
  })), { barmode: "group", bargap: .25, xaxis: { title: "Calidad", dtick: 1, gridcolor: C.grid }, yaxis: { title: "Frecuencia", gridcolor: C.grid } });

  const pintaVariable = (key) => {
    document.querySelectorAll(".chip").forEach((c) => c.classList.toggle("active", c.dataset.key === key));
    plot("chart-hist", ["tinto", "blanco"].map((t) => ({
      type: "histogram", name: t[0].toUpperCase() + t.slice(1), x: D[key].filter((_, i) => D.tipo[i] === t),
      histnorm: "probability density", opacity: .7, nbinsx: 40, marker: { color: TIPO_COLOR[t] },
    })), { barmode: "overlay", xaxis: { title: ETQ[key], gridcolor: C.grid }, yaxis: { title: "Densidad", gridcolor: C.grid } });
    plot("chart-box", ["tinto", "blanco"].map((t) => ({
      type: "box", name: t[0].toUpperCase() + t.slice(1),
      x: D.calidad_cat.filter((_, i) => D.tipo[i] === t), y: D[key].filter((_, i) => D.tipo[i] === t),
      marker: { color: TIPO_COLOR[t], size: 3 }, line: { width: 1.5 }, boxpoints: false,
    })), {
      boxmode: "group",
      xaxis: { title: "Categoría de calidad", categoryorder: "array", categoryarray: ["baja", "media", "alta"], gridcolor: C.grid },
      yaxis: { title: ETQ[key], gridcolor: C.grid },
    });
  };
  FEATURES.forEach((k) => {
    const b = el("button", { class: "chip", "data-key": k }, ETQ[k]);
    b.onclick = () => pintaVariable(k);
    $("#chips-variables").append(b);
  });
  pintaVariable("alcohol");

  const fmtV = (v, r) => fmt(v, r.key === "density" ? 5 : 3);
  tabla("#tabla-descriptiva", [
    { t: "Variable", k: "variable" },
    { t: "Media", k: "mean", num: 1, f: fmtV },
    { t: "Mediana", k: "mediana", num: 1, f: fmtV },
    { t: "Desv. est.", k: "std", num: 1, f: fmtV },
    { t: "Mín", k: "min", num: 1, f: fmtV },
    { t: "Máx", k: "max", num: 1, f: fmtV },
    { t: "CV %", k: "cv", num: 1, f: (v) => fmt(v, 1) },
    { t: "Asimetría", k: "asimetria", num: 1, f: (v) => fmt(v, 2) },
    { t: "Curtosis", k: "curtosis", num: 1, f: (v) => fmt(v, 2) },
  ], W.descriptiva);

  /* ---------- 04 CORRELACION ---------- */
  const R = W.correlacion;
  plot("chart-heatmap", [{
    type: "heatmap", z: R.matriz, x: R.labels, y: R.labels, zmin: -1, zmax: 1,
    colorscale: [[0, "#3f7ea6"], [.5, "#ffffff"], [1, C.wine2]],
    text: R.matriz.map((r) => r.map((v) => v.toFixed(2))), texttemplate: "%{text}",
    textfont: { size: 10 }, hovertemplate: "%{y} × %{x}: %{z:.3f}<extra></extra>",
    colorbar: { thickness: 10, outlinewidth: 0, tickfont: { color: C.muted } },
  }], { margin: { l: 110, r: 10, t: 10, b: 110 }, xaxis: { tickangle: -45 }, yaxis: { autorange: "reversed" } });

  const h2 = [...W.hipotesis.find((h) => h.id === "H2").tabla].sort((a, b) => a.spearman_rho - b.spearman_rho);
  plot("chart-corr-calidad", [{
    type: "bar", orientation: "h", y: h2.map((r) => r.variable), x: h2.map((r) => r.spearman_rho),
    marker: { color: h2.map((r) => (r.spearman_rho >= 0 ? C.wine2 : "#3f7ea6")) },
    text: h2.map((r) => r.spearman_rho.toFixed(2)), textposition: "outside", textfont: { color: C.text },
    customdata: h2.map((r) => fmtP(r.p_spearman)),
    hovertemplate: "%{y}<br>ρ = %{x:.3f}<br>p = %{customdata}<extra></extra>",
  }], { margin: { l: 110, r: 40, t: 10, b: 40 }, xaxis: { range: [-1, 1], gridcolor: C.grid, zerolinecolor: C.muted } });

  /* ---------- 05 HIPOTESIS ---------- */
  const detalle = $("#hip-detalle");
  const columnasDetalle = {
    H1: [{ t: "Variable", k: "variable" }, { t: "K²", k: "DAgostino_K2", num: 1, f: (v) => fmt(v, 2) }, { t: "p", k: "p_K2", num: 1, f: fmtP }, { t: "KS", k: "KS", num: 1, f: (v) => fmt(v) }, { t: "Normal", k: "normal" }],
    H2: [{ t: "Variable", k: "variable" }, { t: "Pearson r", k: "pearson_r", num: 1, f: (v) => fmt(v) }, { t: "p", k: "p_pearson", num: 1, f: fmtP }, { t: "Spearman ρ", k: "spearman_rho", num: 1, f: (v) => fmt(v) }, { t: "p", k: "p_spearman", num: 1, f: fmtP }, { t: "Decisión", k: "decision" }],
    H4: [{ t: "Grupo 1", k: "group1" }, { t: "Grupo 2", k: "group2" }, { t: "Dif. medias", k: "meandiff", num: 1, f: (v) => fmt(+v) }, { t: "p ajust.", k: "p-adj", num: 1, f: (v) => fmtP(+v) }, { t: "Rechaza", k: "reject", f: (v) => (v === "True" ? "Sí" : "No") }],
    H5: null,
    H6: [{ t: "Variable", k: "variable" }, { t: "β", k: "coef", num: 1, f: (v) => fmt(v, 4) }, { t: "p", k: "p", num: 1, f: fmtP }],
  };

  const muestraDetalle = (h, card) => {
    const activo = card.classList.contains("active");
    document.querySelectorAll(".hip").forEach((c) => c.classList.remove("active"));
    if (activo) { detalle.classList.add("hidden"); return; }
    card.classList.add("active");
    detalle.classList.remove("hidden");
    detalle.innerHTML = `<h3>${h.id} · ${h.titulo} <span class="badge ${h.rechaza ? "si" : "no"}">${h.decision}</span></h3>
      <div class="det-grid"><div class="det-meta">
        <p><span class="k">Hipótesis nula (H0)</span>${h.h0}</p>
        <p><span class="k">Hipótesis alternativa (H1)</span>${h.h1}</p>
        <p><span class="k">Prueba</span>${h.prueba}</p>
        ${h.estadistico !== null ? `<p><span class="k">Estadístico</span>${h.estadistico_nombre} = ${fmt(h.estadistico)} · p ${fmtP(h.p).startsWith("<") ? fmtP(h.p) : "= " + fmtP(h.p)}</p>` : ""}
        <div class="det-interp">${h.interpretacion}</div>
      </div><div id="det-visual"></div></div>`;
    const vis = $("#det-visual");
    if (h.id === "H3" || h.id === "H4") {
      vis.append(el("div", { id: "chart-det", class: "chart" }));
      if (h.id === "H3") {
        plot("chart-det", ["tinto", "blanco"].map((t) => ({
          type: "violin", name: t[0].toUpperCase() + t.slice(1), y: D.quality.filter((_, i) => D.tipo[i] === t),
          line: { color: TIPO_COLOR[t] }, fillcolor: TIPO_COLOR[t] + "55", meanline: { visible: true }, box: { visible: true }, points: false,
        })), { showlegend: false, yaxis: { title: "Calidad", gridcolor: C.grid } });
      } else {
        plot("chart-det", ["baja", "media", "alta"].map((c, j) => ({
          type: "box", name: c, y: D.alcohol.filter((_, i) => D.calidad_cat[i] === c),
          marker: { color: [C.wine, C.wine2, C.gold][j] }, boxmean: true, boxpoints: false,
        })), { showlegend: false, yaxis: { title: "Alcohol (% vol)", gridcolor: C.grid }, xaxis: { title: "Categoría de calidad" } });
        vis.append(el("div", { class: "table-wrap mt" }, '<table id="tabla-det"></table>'));
        tabla("#tabla-det", columnasDetalle.H4, h.tabla);
      }
    } else if (h.id === "H5") {
      const cats = ["baja", "media", "alta"];
      vis.append(el("div", { class: "table-wrap" }, '<table id="tabla-det"></table>'));
      tabla("#tabla-det", [{ t: "Tipo", k: "tipo" }, ...cats.map((c) => ({ t: c, k: c, num: 1, f: (v) => fmtInt(v) }))], h.tabla);
    } else if (columnasDetalle[h.id]) {
      vis.append(el("div", { class: "table-wrap" }, '<table id="tabla-det"></table>'));
      tabla("#tabla-det", columnasDetalle[h.id], h.tabla);
    }
    detalle.scrollIntoView({ behavior: "smooth", block: "nearest" });
  };

  W.hipotesis.forEach((h) => {
    const card = el("div", { class: "hip", tabindex: "0", role: "button" }, `
      <div class="hip-top"><span class="hip-id">${h.id}</span><span class="badge ${h.rechaza ? "si" : "no"}">${h.decision}</span></div>
      <h4>${h.titulo}</h4>
      <p class="hip-h"><b>H0:</b> ${h.h0}</p>
      <div class="hip-stats">
        ${h.estadistico !== null ? `<div class="hip-stat"><span>${h.estadistico_nombre.split(" ")[0]}</span><strong>${fmt(h.estadistico, 2)}</strong></div>` : ""}
        <div class="hip-stat"><span>p-valor</span><strong>${fmtP(h.p)}</strong></div>
      </div>`);
    card.onclick = () => muestraDetalle(h, card);
    card.onkeydown = (e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); muestraDetalle(h, card); } };
    $("#hip-grid").append(card);
  });

  /* ---------- 06 MODELO ---------- */
  const mejor = (arr, k, menor = false) => arr.reduce((a, b) => ((menor ? b[k] < a[k] : b[k] > a[k]) ? b : a));
  const reg = W.modelo.regresion.map((r) => ({ ...r }));
  mejor(reg, "R2")._clase = "best";
  tabla("#tabla-reg", [
    { t: "Modelo", k: "modelo" }, { t: "RMSE", k: "RMSE", num: 1, f: (v) => fmt(v) }, { t: "MAE", k: "MAE", num: 1, f: (v) => fmt(v) },
    { t: "R²", k: "R2", num: 1, f: (v) => fmt(v) }, { t: "Acierto exacto", k: "exactitud_redondeo", num: 1, f: (v) => fmt(v * 100, 1) + "%" },
  ], reg);
  const clf = W.modelo.clasificacion.map((r) => ({ ...r }));
  mejor(clf, "F1")._clase = "best";
  const pct = (v) => fmt(v * 100, 1) + "%";
  tabla("#tabla-clf", [
    { t: "Modelo", k: "modelo" }, { t: "Accuracy", k: "accuracy", num: 1, f: pct }, { t: "Precision", k: "precision", num: 1, f: pct },
    { t: "Recall", k: "recall", num: 1, f: pct }, { t: "F1", k: "F1", num: 1, f: pct }, { t: "ROC-AUC", k: "ROC_AUC", num: 1, f: (v) => fmt(v) },
  ], clf);

  const imp = W.modelo.importancia;
  const impIdx = imp.valores.map((_, i) => i).reverse();
  plot("chart-importancia", [{
    type: "bar", orientation: "h", y: impIdx.map((i) => imp.variables[i]), x: impIdx.map((i) => imp.valores[i]),
    marker: { color: escala(impIdx.map((i) => imp.valores[i])) },
    hovertemplate: "%{y}: %{x:.3f}<extra></extra>",
  }], { margin: { l: 120, r: 20, t: 10, b: 40 }, xaxis: { gridcolor: C.grid } });

  const cm = W.modelo.matriz_confusion;
  plot("chart-cm", [{
    type: "heatmap", z: cm, x: ["No bueno", "Bueno"], y: ["No bueno", "Bueno"],
    colorscale: [[0, C.card2], [1, C.wine2]], showscale: false,
    text: cm.map((r) => r.map((v) => fmtInt(v))), texttemplate: "%{text}", textfont: { size: 22, family: C.font },
    hovertemplate: "Real %{y} · Predicho %{x}: %{z}<extra></extra>",
  }], { margin: { l: 90, r: 20, t: 10, b: 60 }, xaxis: { title: "Predicho", side: "bottom" }, yaxis: { title: "Real", autorange: "reversed" } });

  /* ---------- 07 SIMULADOR ---------- */
  const S = W.simulador;
  let tipo = "tinto";
  const valores = {};
  const dec = (k) => { const r = S.rangos[k].max - S.rangos[k].min; return r < 0.1 ? 4 : r < 2 ? 3 : r < 20 ? 2 : 1; };

  FEATURES.forEach((k) => {
    const r = S.rangos[k];
    const paso = (r.max - r.min) / 200;
    const fila = el("div", { class: "slider" }, `
      <label for="sl-${k}">${ETQ[k]}</label>
      <input type="range" id="sl-${k}" min="${r.min}" max="${r.max}" step="${paso}">
      <output id="out-${k}"></output>`);
    $("#sim-sliders").append(fila);
    fila.querySelector("input").addEventListener("input", (e) => { valores[k] = +e.target.value; actualizaSim(); });
  });

  const cargaMedianas = () => {
    FEATURES.forEach((k) => { valores[k] = S.rangos[k][tipo]; $(`#sl-${k}`).value = valores[k]; });
    actualizaSim();
  };

  const predice = () => {
    const x = S.columnas.map((c) => (c === "tipo_num" ? (tipo === "tinto" ? 1 : 0) : valores[c]));
    const z = x.map((v, i) => (v - S.media[i]) / S.escala[i]);
    const lin = S.lineal.intercepto + z.reduce((a, v, i) => a + v * S.lineal.coef[i], 0);
    const logit = S.logistica.intercepto + z.reduce((a, v, i) => a + v * S.logistica.coef[i], 0);
    return { calidad: Math.min(10, Math.max(0, lin)), prob: 1 / (1 + Math.exp(-logit)) };
  };

  let gaugeListo = false;
  const actualizaSim = () => {
    FEATURES.forEach((k) => ($(`#out-${k}`).textContent = fmt(valores[k], dec(k))));
    const { calidad, prob } = predice();
    const gauge = [{
      type: "indicator", mode: "gauge+number", value: calidad,
      number: { valueformat: ".2f", font: { family: C.font, size: 52, color: C.text } },
      title: { text: "Calidad estimada", font: { color: C.muted, size: 14 } },
      gauge: {
        axis: { range: [0, 10], tickcolor: C.muted, tickfont: { color: C.muted } },
        bar: { color: C.wine2, thickness: .28 }, bgcolor: C.card2, borderwidth: 0,
        steps: [{ range: [0, 5], color: "#f3ebe9" }, { range: [5, 7], color: "#f0e2e2" }, { range: [7, 10], color: "#f7ead2" }],
        threshold: { line: { color: C.gold, width: 3 }, thickness: .8, value: S.umbral },
      },
    }];
    const lay = baseLayout({ margin: { l: 30, r: 30, t: 50, b: 10 } });
    gaugeListo ? Plotly.react("chart-gauge", gauge, lay, CFG) : Plotly.newPlot("chart-gauge", gauge, lay, CFG);
    gaugeListo = true;
    $("#sim-prob-val").textContent = fmt(prob * 100, 1) + "%";
    $("#sim-prob-bar").style.width = (prob * 100).toFixed(1) + "%";
    $("#sim-veredicto").textContent = calidad >= 7 ? "🍷 Vino de calidad alta" : calidad >= 6 ? "Vino de calidad media" : "Vino de calidad baja";
  };

  document.querySelectorAll("#sim-tipo button").forEach((b) => b.addEventListener("click", () => {
    tipo = b.dataset.tipo;
    document.querySelectorAll("#sim-tipo button").forEach((x) => x.classList.toggle("active", x === b));
    cargaMedianas();
  }));
  $("#sim-reset").onclick = cargaMedianas;
  cargaMedianas();

  /* ---------- 08 SPSS ---------- */
  const capturados = W.spss.filter((r) => r.spss !== null && r.spss !== undefined).length;
  tabla("#tabla-spss", [
    { t: "Prueba", k: "prueba" },
    { t: "Python", k: "python", num: 1, f: (v, r) => (r.id.endsWith("_p") ? fmtP(v) : fmt(v, 4)) },
    { t: "SPSS", k: "spss", num: 1, f: (v, r) => (v === null || v === undefined ? '<span class="pend">pendiente</span>' : r.id.endsWith("_p") ? fmtP(v) : fmt(v, 4)) },
    { t: "Diferencia", k: "python", num: 1, f: (v, r) => (r.spss === null || r.spss === undefined ? "—" : fmt(Math.abs(v - r.spss), 4)) },
    { t: "Coincide", k: "python", f: (v, r) => {
      if (r.spss === null || r.spss === undefined) return '<span class="pend">—</span>';
      const tol = r.id.endsWith("_p") ? 0.001 : Math.max(0.01, Math.abs(v) * 0.01);
      return Math.abs(v - r.spss) <= tol ? '<span class="ok">✓ Sí</span>' : '<span class="dif">Revisar</span>';
    } },
  ], W.spss);
  $("#spss-nota").innerHTML = capturados === 0
    ? "Capturen los valores del visor de SPSS en <code>spss/resultados_spss.json</code> y vuelvan a ejecutar <code>python src/main.py</code>."
    : `${capturados} de ${W.spss.length} valores de SPSS capturados. Diferencias pequeñas se deben a redondeo o a la versión de la prueba (p. ej. t de Welch vs t clásica).`;

  /* ---------- 09 CONCLUSIONES ---------- */
  const K = W.conclusiones;
  const H = Object.fromEntries(W.hipotesis.map((h) => [h.id, h]));
  [
    `Las variables con mayor peso en la calidad son <strong>${K.top_variables.join(", ")}</strong>, según el modelo Random Forest.`,
    `${H.H2.interpretacion} En total, <strong>${H.H2.decision.replace("significativas", "variables")}</strong> tienen correlación significativa con la calidad (Spearman, α = ${M.alpha}).`,
    `${H.H4.rechaza ? "El grado de alcohol <strong>sí difiere</strong>" : "El grado de alcohol <strong>no difiere</strong>"} entre vinos de calidad baja, media y alta (ANOVA, p ${fmtP(H.H4.p).startsWith("<") ? fmtP(H.H4.p) : "= " + fmtP(H.H4.p)}).`,
    `La regresión lineal múltiple explica el <strong>${fmt(K.r2 * 100, 1)}%</strong> de la variación de la calidad: las propiedades químicas influyen, pero la percepción sensorial tiene factores que no se miden en laboratorio.`,
    `Para identificar <strong>buenos vinos</strong> (≥ 7), el mejor clasificador fue <strong>${K.mejor_clf.modelo}</strong> con F1 = ${pct(K.mejor_clf.F1)} y ROC-AUC = ${fmt(K.mejor_clf.ROC_AUC)}.`,
    `Python y SPSS se complementan: Python automatiza el tratamiento, la visualización y el modelado; SPSS valida las pruebas estadísticas con salidas estándar.`,
  ].forEach((t, i) => $("#lista-conclusiones").append(el("div", { class: "concl reveal" }, `<span class="concl-n">${i + 1}</span><p>${t}</p>`)));

  /* ---------- navegación y animaciones ---------- */
  // Menú lateral en celular: abrir/cerrar
  const menuBtn = $("#menu-btn");
  const setMenu = (open) => { document.body.classList.toggle("menu-open", open); menuBtn.setAttribute("aria-expanded", open); };
  menuBtn.addEventListener("click", () => setMenu(!document.body.classList.contains("menu-open")));
  $("#side-overlay").addEventListener("click", () => setMenu(false));
  document.addEventListener("keydown", (e) => e.key === "Escape" && setMenu(false));
  document.querySelectorAll(".side a").forEach((a) => a.addEventListener("click", () => setMenu(false)));
  $("#side-materia").textContent = M.materia;
  $("#side-inst").textContent = M.institucion;

  const links = [...document.querySelectorAll(".side-links a")];
  const secciones = links.map((a) => $(a.getAttribute("href")));
  const spy = new IntersectionObserver((entries) => entries.forEach((e) => {
    if (e.isIntersecting) links.forEach((a) => a.classList.toggle("active", a.getAttribute("href") === "#" + e.target.id));
  }), { rootMargin: "-45% 0px -50% 0px" });
  secciones.forEach((s) => s && spy.observe(s));

  document.querySelectorAll(".section-head, .card, .hip, .flow-step, .kpi").forEach((e) => e.classList.add("reveal"));
  const rev = new IntersectionObserver((entries) => entries.forEach((e) => {
    if (e.isIntersecting) { e.target.classList.add("visible"); rev.unobserve(e.target); }
  }), { threshold: 0.08 });
  document.querySelectorAll(".reveal").forEach((e) => rev.observe(e));
})();
