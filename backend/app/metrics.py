from datetime import datetime
from collections import defaultdict

def infer_state_durations(events, end_time=None):
    """
    events: list of Event objects (already sorted by timestamp)
    end_time: datetime (optional, defaults to now)
    """

    if not events:
        return {}

    if end_time is None:
        end_time = datetime.utcnow()

    durations = defaultdict(float)

    for i in range(len(events) - 1):
        current_event = events[i]
        next_event = events[i + 1]

        delta = (next_event.timestamp - current_event.timestamp).total_seconds()

        if current_event.event_type in ["working", "idle", "absent"]:
            durations[current_event.event_type] += delta

    # Handle last event
    last_event = events[-1]
    delta = (end_time - last_event.timestamp).total_seconds()

    if last_event.event_type in ["working", "idle", "absent"]:
        durations[last_event.event_type] += max(delta, 0)

    return durations
def compute_worker_metrics(events):
    """
    events: list of Event objects for ONE worker
    """

    durations = infer_state_durations(events)

    working_time = durations.get("working", 0)
    idle_time = durations.get("idle", 0)

    # Utilization definition
    utilization = 0
    if (working_time + idle_time) > 0:
        utilization = working_time / (working_time + idle_time)

    # Production aggregation
    total_units = sum(
        e.count for e in events
        if e.event_type == "product_count" and e.count
    )

    units_per_hour = 0
    if working_time > 0:
        units_per_hour = total_units / (working_time / 3600)

    return {
        "working_time_sec": working_time,
        "idle_time_sec": idle_time,
        "utilization": utilization,
        "total_units": total_units,
        "units_per_hour": units_per_hour
    }
    
def compute_workstation_metrics(events):
    """
    events: list of Event objects for ONE workstation
    """

    durations = infer_state_durations(events)

    occupancy_time = durations.get("working", 0)
    idle_time = durations.get("idle", 0)

    utilization = 0
    if (occupancy_time + idle_time) > 0:
        utilization = occupancy_time / (occupancy_time + idle_time)

    total_units = sum(
        e.count for e in events
        if e.event_type == "product_count" and e.count
    )

    throughput = 0
    if occupancy_time > 0:
        throughput = total_units / (occupancy_time / 3600)

    return {
        "occupancy_time_sec": occupancy_time,
        "utilization": utilization,
        "total_units": total_units,
        "throughput_units_per_hour": throughput
    }


