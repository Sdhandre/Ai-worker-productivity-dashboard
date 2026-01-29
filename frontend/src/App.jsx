import { useEffect, useState } from "react";
import {
  getFactoryMetrics,
  getWorkerMetrics,
  getStationMetrics
} from "./api";

import FactorySummary from "./components/FactorySummary";
import WorkerTable from "./components/WorkerTable";
import StationTable from "./components/StationTable";

export default function App() {
  const [factory, setFactory] = useState(null);
  const [workers, setWorkers] = useState(null);
  const [stations, setStations] = useState(null);
  const [selectedWorker, setSelectedWorker] = useState("ALL");
  const [selectedStation, setSelectedStation] = useState("ALL");



  useEffect(() => {
    getFactoryMetrics().then(setFactory);
    getWorkerMetrics().then(setWorkers);
    getStationMetrics().then(setStations);
  }, []);

  const filteredWorkers =
  selectedWorker === "ALL"
    ? workers
    : workers?.filter(w => w.worker_id === selectedWorker);


  const filteredStations =
  selectedStation === "ALL"
    ? stations
    : stations?.filter(s => s.station_id === selectedStation);



  return (
    <div style={{ padding: "20px" }}>
      <h1>AI Worker Productivity Dashboard(Please wait for 2-3 minutes, the backend might be loading)</h1>

      <FactorySummary data={factory} />
      <h2>Filter by Worker</h2>

<select
  value={selectedWorker}
  onChange={(e) => setSelectedWorker(e.target.value)}
  style={{ marginBottom: "20px" }}
>
  <option value="ALL">All Workers</option>

  {workers &&
    workers.map(w => (
      <option key={w.worker_id} value={w.worker_id}>
        {w.name}
      </option>
    ))}
</select>

<WorkerTable workers={filteredWorkers} />

      <h2>Filter by Workstation</h2>

<select
  value={selectedStation}
  onChange={(e) => setSelectedStation(e.target.value)}
  style={{ marginBottom: "20px" }}
>
  <option value="ALL">All Workstations</option>

  {stations &&
    stations.map(s => (
      <option key={s.station_id} value={s.station_id}>
        {s.name}
      </option>
    ))}
</select>

<StationTable stations={filteredStations} />

    </div>
  );
}

