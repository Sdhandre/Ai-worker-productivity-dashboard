export default function FactorySummary({ data }) {
  if (!data) return <p>Loading factory metrics...</p>;

  return (
    <div style={{ marginBottom: "20px" }}>
      <h2>Factory Summary</h2>
      <ul>
        <li>Total Productive Time: {(data.total_productive_time_sec / 60).toFixed(1)} min</li>
        <li>Total Units Produced: {data.total_units_produced}</li>
        <li>Average Utilization: {(data.average_utilization * 100).toFixed(1)}%</li>
        <li>
          Avg Production Rate:{" "}
          {data.average_production_rate_units_per_hour.toFixed(2)} units/hr
        </li>
      </ul>
    </div>
  );
}
