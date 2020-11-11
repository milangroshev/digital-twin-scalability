import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd

import os
import sys

df_all_data = pd.DataFrame()
df_avg_data = pd.DataFrame()

def parse_file(filename):
  df = pd.read_csv(filename)

  initial_ts = df.iloc[0]['timestamp']

  entries = []
  avg = []
  t = 0
  for index, row in df.iterrows():
    entries.append(((row['timestamp'] - initial_ts) / 1000000000.0, row['latency']))
    t = t + row['latency']
    if index % 20 == 0:
      if index == 0:
        avg.append(((row['timestamp'] - initial_ts) / 1000000000.0, row['latency']))
        continue
      avg.append(((row['timestamp'] - initial_ts) / 1000000000.0, t / 20))
      t = 0

  ts, val = zip(*entries)
  df_all_data['timestamp'] = ts
  df_all_data['latency'] = val 

  ts, val = zip(*avg)
  df_avg_data['timestamp'] = ts
  df_avg_data['latency'] = val 
  print("Finished file: %s" % filename)


for i in range(1, len(sys.argv)):
  parse_file(sys.argv[i])


plt.style.use('seaborn-whitegrid')

fig = plt.figure()
fig.set_size_inches(5,4)
ax = plt.gca()
ax.set_ylabel('Lantecy (ms)')
ax.set_xlabel('Time (s)')

plt.plot(df_all_data['timestamp'], df_all_data['latency'], markersize=5, markeredgewidth=1.5, label="All points")
plt.plot(df_avg_data['timestamp'], df_avg_data['latency'], markersize=5, markeredgewidth=1.5, label="Average 20 entries")

fig.legend(loc='upper center',
           ncol=3, frameon=True, shadow=True)

#for i in range(1, 12, 1):
#  ax.axvline(x=3600*i, linestyle = ":", alpha = 0.5, color = "black")
    
fig.savefig('latency.png', bbox_inches='tight', pad_inches=0.3)
fig.savefig('latency.pdf', bbox_inches='tight', pad_inches=0.3)
plt.close()
