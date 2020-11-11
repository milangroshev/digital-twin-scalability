
import math
import pandas as pd
import sys

df_instances_data = pd.read_csv(sys.argv[1]+"/robot_instances.csv")
df_resources_data = pd.read_csv(sys.argv[1]+"/resource_stats.csv")

# MERGE ALL LOGS IN A SINGLE LINE
df_all_data = pd.DataFrame(columns = ["timestamp", "node", "latency", "action", "cpu", "ram", "tx", "rx", "instances"])

for i in [122, 125, 128, 131, 134, 137, 140, 143, 146, 149, 152]:
  df_node_data = pd.read_csv(sys.argv[1]+"/10.0.1."+str(i)+".csv")
  if df_node_data.size == 0:
    continue

  initial_ts = prev_ts = df_node_data.loc[0]["timestamp"]
  prev_cpu = df_resources_data[df_resources_data["timestamp"] <= initial_ts].iloc[-1]["cpu"]
  prev_ram = df_resources_data[df_resources_data["timestamp"] <= initial_ts].iloc[-1]["ram"]
  prev_tx = df_resources_data[df_resources_data["timestamp"] <= initial_ts].iloc[-1]["tx_bytes"]
  prev_rx = df_resources_data[df_resources_data["timestamp"] <= initial_ts].iloc[-1]["rx_bytes"]


  for index, row in df_node_data[1:].iterrows():
    resources = df_resources_data[(df_resources_data["timestamp"] <= row["timestamp"]) & (df_resources_data["timestamp"] > prev_ts)]
    cpu = resources.mean(axis=0)["cpu"]
    if math.isnan(cpu):
      cpu = prev_cpu
    ram = resources.mean(axis=0)["ram"]
    if math.isnan(ram):
      ram = prev_ram
    tx = resources.max(axis=0)["tx_bytes"]
    if math.isnan(tx):
      tx = prev_tx
    rx = resources.max(axis=0)["rx_bytes"]
    if math.isnan(rx):
      rx = prev_rx
    instances = df_instances_data[df_instances_data["timestamp"] < row["timestamp"]].iloc[-1]["num-instances"]

    df_all_data.loc[-1] = [row["timestamp"], row["node"], row["latency"], row["action"], cpu, ram, tx - prev_tx, rx - prev_rx, instances]

    prev_ts = row['timestamp']
    prev_cpu = cpu
    prev_ram = ram
    prev_tx = tx
    prev_rx = rx

    df_all_data.index = df_all_data.index + 1

df_all_data = df_all_data.sort_values("timestamp", ascending=False)
df_all_data.to_csv(sys.argv[1]+"/digital-twin-dataset.csv", index=False)
