const BASE_URL = "https://ai-worker-productivity-dashboard-g2ji.onrender.com";

export async function getFactoryMetrics() {
  const res = await fetch(`${BASE_URL}/metrics/factory`);
  return res.json();
}

export async function getWorkerMetrics() {
  const res = await fetch(`${BASE_URL}/metrics/workers`);
  return res.json();
}

export async function getStationMetrics() {
  const res = await fetch(`${BASE_URL}/metrics/workstations`);
  return res.json();
}
