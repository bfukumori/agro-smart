const data = window.AGROSMART_DATA;
const COLORS = {"TLH-001":"#1b6b45","TLH-002":"#d78b23","TLH-003":"#557fbd"};
const titles = {
  overview: "Visão geral da fazenda",
  telemetry: "Telemetria dos sensores",
  automation: "Automação inteligente",
  architecture: "Arquitetura integrada",
  "process-mining": "Mineração de processos (Process Mining)",
  devsecops: "DevSecOps & Monitoramento contínuo"
};
const formatTime = value => new Intl.DateTimeFormat("pt-BR",{day:"2-digit",month:"2-digit",hour:"2-digit",minute:"2-digit",timeZone:"UTC"}).format(new Date(value));
const statusClass = value => value.toLowerCase().replace("ç","c");

document.querySelectorAll(".nav-item").forEach(button=>button.addEventListener("click",()=>{
  document.querySelectorAll(".nav-item,.view").forEach(item=>item.classList.remove("active"));
  button.classList.add("active"); document.getElementById(button.dataset.view).classList.add("active");
  document.getElementById("view-title").textContent=titles[button.dataset.view];
  if(button.dataset.view==="overview") requestAnimationFrame(drawChart);
}));

document.getElementById("updated-at").textContent=formatTime(data.generated_at)+" UTC";
document.getElementById("kpi-readings").textContent=data.total_readings;
document.getElementById("kpi-plots").textContent=data.active_plots;
document.getElementById("kpi-alerts").textContent=data.open_alerts;
document.getElementById("kpi-critical").textContent=data.critical_plots;

document.getElementById("plot-status").innerHTML=data.latest.map(row=>`<div class="plot-item"><strong>${row.plot_id}</strong><small>Solo ${row.soil_moisture_pct.toFixed(1)}% · ${row.temperature_c.toFixed(1)} °C</small><span class="status-pill ${statusClass(row.risk_level)}">${row.risk_level}</span></div>`).join("");
document.getElementById("alert-list").innerHTML=data.alerts.slice(0,3).map(a=>`<div class="alert ${statusClass(a.severity)}"><div class="alert-top"><strong>${a.plot_id} · ${a.action_type}</strong><span>score ${a.risk_score}</span></div><p>${a.recommendation}</p></div>`).join("");
document.getElementById("rules-grid").innerHTML=data.rules.map((rule,i)=>`<article class="rule-card"><span>REGRA ${String(i+1).padStart(2,"0")}</span><h3>${rule.condition}</h3><p>${rule.decision}</p></article>`).join("");
document.getElementById("automation-log").innerHTML=data.alerts.map(a=>`<div class="log-row"><span>${formatTime(a.timestamp)}</span><strong>${a.plot_id}</strong><em class="status-pill ${statusClass(a.severity)}">${a.severity}</em><div>${a.recommendation}</div></div>`).join("");

const recent=[...data.series].slice(-12);
document.getElementById("telemetry-table").innerHTML=recent.reverse().map(r=>`<tr><td>${formatTime(r.timestamp)}</td><td><strong>${r.plot_id}</strong></td><td>${r.temperature_c.toFixed(1)} °C</td><td>${r.air_humidity_pct.toFixed(1)}%</td><td>${r.soil_moisture_pct.toFixed(1)}%</td><td>${Math.round(r.luminosity_lux).toLocaleString("pt-BR")} lux</td><td><span class="status-pill ${statusClass(r.risk_level)}">${r.risk_level}</span></td></tr>`).join("");

// Process Mining data binding if available
if(data.process_mining){
  if(document.getElementById("pm-cases")) document.getElementById("pm-cases").textContent=data.process_mining.total_cases_analyzed;
  if(document.getElementById("pm-variants")) document.getElementById("pm-variants").textContent=data.process_mining.distinct_variants;
  if(document.getElementById("pm-leadtime")) document.getElementById("pm-leadtime").textContent=Math.round(data.process_mining.avg_case_lead_time_ms)+" ms";
  if(data.process_mining.variants && document.getElementById("pm-variants-list")){
    document.getElementById("pm-variants-list").innerHTML=data.process_mining.variants.map(v=>`<div class="plot-item"><strong>${v.variant_id} (${v.percentage}%)</strong><small style="word-break:break-all;">${v.trace.split(' -> ').slice(3).join(' → ')}</small><span class="status-pill ${v.percentage > 20 ? 'normal' : 'atencao'}">${v.frequency} ocorrências</span></div>`).join("");
  }
}

function drawChart(){
  const canvas=document.getElementById("soil-chart"), rect=canvas.getBoundingClientRect(), scale=window.devicePixelRatio||1;
  canvas.width=rect.width*scale; canvas.height=285*scale; const ctx=canvas.getContext("2d"); ctx.scale(scale,scale);
  const w=rect.width,h=285,p={l:42,r:15,t:14,b:28}; ctx.clearRect(0,0,w,h);
  ctx.font="10px Segoe UI";ctx.fillStyle="#7a8881";ctx.strokeStyle="#e3e9e5";ctx.lineWidth=1;
  [0,20,40,60].forEach(v=>{const y=p.t+(60-v)/60*(h-p.t-p.b);ctx.beginPath();ctx.moveTo(p.l,y);ctx.lineTo(w-p.r,y);ctx.stroke();ctx.fillText(v+"%",7,y+3)});
  const byPlot={}; data.series.filter(r=>new Date(r.timestamp)>=new Date(data.series[data.series.length-1].timestamp)-24*3600000).forEach(r=>(byPlot[r.plot_id]??=[]).push(r));
  Object.entries(byPlot).forEach(([plot,rows])=>{ctx.beginPath();ctx.strokeStyle=COLORS[plot];ctx.lineWidth=2.5;rows.forEach((r,i)=>{const x=p.l+i/(rows.length-1)*(w-p.l-p.r),y=p.t+(60-r.soil_moisture_pct)/60*(h-p.t-p.b);i?ctx.lineTo(x,y):ctx.moveTo(x,y)});ctx.stroke()});
  ctx.fillStyle="#7a8881";ctx.fillText("24h atrás",p.l,h-7);ctx.fillText("agora",w-p.r-30,h-7);
}
document.getElementById("chart-legend").innerHTML=Object.entries(COLORS).map(([plot,c])=>`<span style="--c:${c}">${plot}</span>`).join("");
window.addEventListener("resize",drawChart); drawChart();

let timer=null, simIndex=Math.max(0,data.series.length-15);
function showReading(r){
  document.getElementById("sensor-temp").textContent=r.temperature_c.toFixed(1)+" °C";
  document.getElementById("sensor-air").textContent=r.air_humidity_pct.toFixed(1)+" %";
  document.getElementById("sensor-soil").textContent=r.soil_moisture_pct.toFixed(1)+" %";
  document.getElementById("sensor-light").textContent=Math.round(r.luminosity_lux).toLocaleString("pt-BR")+" lx";
  document.getElementById("sim-plot").textContent=r.plot_id+" · leitura recebida"; document.getElementById("sim-time").textContent=formatTime(r.timestamp)+" UTC";
  document.getElementById("board-led").classList.toggle("on");
  const output=document.getElementById("serial-output"); output.textContent+=`\n[${r.timestamp}] ${r.plot_id} | temp=${r.temperature_c}C | ar=${r.air_humidity_pct}% | solo=${r.soil_moisture_pct}% | luz=${r.luminosity_lux}lx | risco=${r.risk_level}`; output.scrollTop=output.scrollHeight;
}
document.getElementById("play-simulation").addEventListener("click",event=>{
  if(timer){clearInterval(timer);timer=null;event.currentTarget.textContent="Continuar simulação";return}
  event.currentTarget.textContent="Pausar simulação";showReading(data.series[simIndex]);
  timer=setInterval(()=>{simIndex=(simIndex+1)%data.series.length;showReading(data.series[simIndex])},1200);
});

showReading(data.series[simIndex]);

// Alternância entre visualização vetorial e imagem do mapa de processos
const btnSvg = document.getElementById("btn-show-svg");
const btnImg = document.getElementById("btn-show-img");
const viewSvg = document.getElementById("dfg-vector-view");
const viewImg = document.getElementById("dfg-image-view");
if (btnSvg && btnImg && viewSvg && viewImg) {
  btnSvg.addEventListener("click", () => {
    viewSvg.style.display = "block";
    viewImg.style.display = "none";
    btnSvg.style.background = "#1b6b45";
    btnImg.style.background = "#203a2f";
  });
  btnImg.addEventListener("click", () => {
    viewSvg.style.display = "none";
    viewImg.style.display = "block";
    btnSvg.style.background = "#203a2f";
    btnImg.style.background = "#1b6b45";
  });
}

const initialView=location.hash.slice(1);
if(titles[initialView]) document.querySelector(`.nav-item[data-view="${initialView}"]`).click();
