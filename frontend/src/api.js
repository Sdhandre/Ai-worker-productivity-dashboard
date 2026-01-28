const BASE_URL = "http://127.0.0.1:8000";

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
