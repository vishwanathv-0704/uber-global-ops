import pandas as pd
from datetime import datetime, timedelta


data = []

base_time = datetime.now().replace(second=0, microsecond=0)


airport_metrics = {
    "SFO": {
        "completion_rate": 71,
        "average_eta": 18,
        "active_drivers": 145,
        "driver_cancellation_rate": 19,
        "queue_size": 180,
        "surge_multiplier": 1.2,
        "request_volume": 920
    },

    "LAX": {
        "completion_rate": 84,
        "average_eta": 16,
        "active_drivers": 210,
        "driver_cancellation_rate": 13,
        "queue_size": 125,
        "surge_multiplier": 1.1,
        "request_volume": 850
    },

    "JFK": {
        "completion_rate": 86,
        "average_eta": 15,
        "active_drivers": 195,
        "driver_cancellation_rate": 11,
        "queue_size": 110,
        "surge_multiplier": 1.2,
        "request_volume": 780
    }
}


# Generate multiple telemetry snapshots
for i in range(10):

    timestamp = base_time - timedelta(minutes=5 * i)

    for airport, metrics in airport_metrics.items():

        row = {
            "airport_code": airport,
            "completion_rate": metrics["completion_rate"],
            "average_eta": metrics["average_eta"],
            "active_drivers": metrics["active_drivers"],
            "driver_cancellation_rate": metrics["driver_cancellation_rate"],
            "queue_size": metrics["queue_size"],
            "surge_multiplier": metrics["surge_multiplier"],
            "request_volume": metrics["request_volume"],
            "timestamp": timestamp
        }

        data.append(row)


df = pd.DataFrame(data)

df.to_csv(
    "data/airport_metrics.csv",
    index=False
)

print("Airport telemetry generated successfully.")
print(f"Rows created: {len(df)}")
print("\nSample:")
print(df.head())
