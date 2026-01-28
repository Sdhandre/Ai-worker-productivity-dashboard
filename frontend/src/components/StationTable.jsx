export default function StationTable({ stations }) {
  if (!stations) return <p>Loading workstations...</p>;

  return (
    <div style={{ marginBottom: "20px" }}>
      <h2>Workstations</h2>
      <table border="1" cellPadding="8">
        <thead>
          <tr>
            <th>Name</th>
            <th>Occupied (min)</th>
            <th>Utilization</th>
            <th>Units</th>
            <th>Throughput (units/hr)</th>
          </tr>
        </thead>
        <tbody>
          {stations.map(s => (
            <tr key={s.station_id}>
              <td>{s.name}</td>
              <td>{(s.occupancy_time_sec / 60).toFixed(1)}</td>
              <td>{(s.utilization * 100).toFixed(1)}%</td>
              <td>{s.total_units}</td>
              <td>{s.throughput_units_per_hour.toFixed(2)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
