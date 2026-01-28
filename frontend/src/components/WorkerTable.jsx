
export default function WorkerTable({ workers }) {
  if (!workers) return <p>Loading workers...</p>;

  return (
    <div style={{ marginBottom: "20px" }}>
      <h2>Workers</h2>
      <table border="1" cellPadding="8">
        <thead>
          <tr>
            <th>Name</th>
            <th>Working (min)</th>
            <th>Idle (min)</th>
            <th>Utilization</th>
            <th>Units</th>
            <th>Units / Hr</th>
          </tr>
        </thead>
        <tbody>
          {workers.map(w => (
            <tr key={w.worker_id}>
              <td>{w.name}</td>
              <td>{(w.working_time_sec / 60).toFixed(1)}</td>
              <td>{(w.idle_time_sec / 60).toFixed(1)}</td>
              <td>{(w.utilization * 100).toFixed(1)}%</td>
              <td>{w.total_units}</td>
              <td>{w.units_per_hour.toFixed(2)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
