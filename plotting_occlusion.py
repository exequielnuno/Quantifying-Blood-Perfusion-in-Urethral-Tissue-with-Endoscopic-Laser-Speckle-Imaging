import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt

# Get the directory of the current script, folder with data should be located on the same folder as this script 
script_dir = os.path.dirname(os.path.abspath(__file__))

folder_path = script_dir + r"\occlusion_data"

# Load the processed data from the .csv file
df = pd.read_csv(os.path.join(folder_path, 'occlusion_data.csv'))

# Obtain the mean speckle flow index and mean speckle contrast values
mean_speckle_flows = df['Mean Speckle Flow Index'].values
mean_speckle_contrasts = df['Mean Speckle Contrast'].values

# Time array, experimetn took a total of 6 minutes
fps = 50
times = np.arange(len(mean_speckle_flows)) / fps / 60 # data at 50 fps and 60 seconds per minute

# Create new figure for zoomed in section
plt.rcParams['font.size'] = 12
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.weight'] = 'bold'
fig, ax = plt.subplots(dpi=100, figsize=(12, 5))
plt.fontsize = 20
# plt.rcParams[{"font.family": "Arial"}]
ax.plot(times, mean_speckle_flows)
# ax.set_title('Mean Speckle Flow Index Over Time for Blood Occlusion',
#              fontweight='bold', fontsize=15)
ax.set_xlabel('Time (minutes)', fontweight='bold', fontsize=12)
ax.set_ylabel('SFI (a.u.)', fontweight='bold', fontsize=12)
ax.set_xlim(0, 6)
ax.grid()
ax.set_ylim((0, 29000))
for tick in ax.xaxis.get_major_ticks():
    tick.label1.set_fontweight('bold')
for tick in ax.yaxis.get_major_ticks():
    tick.label1.set_fontweight('bold')

# Define the region to be zoomed in 
zoom1_x_start, zoom1_x_end = 1.1, 1.2
zoom1_y_start, zoom1_y_end = 14400, 17000

# Create the inset axes for the zoom-in window
# The arguments [left, bottom, width, height] define the position and size of the inset axes
axins1 = ax.inset_axes([0.1, 0.7, 0.2, 0.2],
                      xlim=(zoom1_x_start, zoom1_x_end),
                      ylim=(zoom1_y_start, zoom1_y_end),
                      facecolor='lightgoldenrodyellow',
                      alpha=0.7)  # Adjust these values as needed

# Plot the zoomed-in data on the inset axes
axins1.plot(times, mean_speckle_flows, color='red')
axins1.set_title('Baseline', fontsize=12, fontfamily='Arial', fontweight='bold')
axins1.tick_params(labelleft=True, labelbottom=True)

# Define the region to be zoomed in 
zoom2_x_start, zoom2_x_end = 3, 3.1
zoom2_y_start, zoom2_y_end = 3000, 4000

# Create the inset axes for the zoom-in window
# The arguments [left, bottom, width, height] define the position and size of the inset axes
axins2 = ax.inset_axes([0.43, 0.32, 0.2, 0.2],
                      xlim=(zoom2_x_start, zoom2_x_end),
                      ylim=(zoom2_y_start, zoom2_y_end),
                      facecolor='lightgoldenrodyellow',
                      alpha=0.7)  # Adjust these values as needed

# Plot the zoomed-in data on the inset axes
axins2.plot(times, mean_speckle_flows, color='red')
axins2.set_title('Occlusion', fontsize=12, fontfamily='Arial', fontweight='bold')
axins2.tick_params(labelleft=True, labelbottom=True)

# Define the region to be zoomed in 
zoom3_x_start, zoom3_x_end = 5.7, 5.8
zoom3_y_start, zoom3_y_end = 14000, 15200

# Create the inset axes for the zoom-in window
# The arguments [left, bottom, width, height] define the position and size of the inset axes
axins3 = ax.inset_axes([0.78, 0.7, 0.2, 0.2],
                      xlim=(zoom3_x_start, zoom3_x_end),
                      ylim=(zoom3_y_start, zoom3_y_end),
                      facecolor='lightgoldenrodyellow',
                      alpha=0.7)  # Adjust these values as needed

# Plot the zoomed-in data on the inset axes
axins3.plot(times, mean_speckle_flows, color='red')
axins3.set_title('Post-occlusion', fontsize=12, fontfamily='Arial', fontweight='bold')
axins3.tick_params(labelleft=True, labelbottom=True)

# Draw a rectangle on the main plot to indicate the zoomed-in area
ax.indicate_inset_zoom(axins1, edgecolor="black", linewidth=2, alpha=1.0)
ax.indicate_inset_zoom(axins2, edgecolor="black", linewidth=2, alpha=1.0)
ax.indicate_inset_zoom(axins3, edgecolor="black", linewidth=2, alpha=1.0)

plt.axvspan(2, 4.2, color='orange', alpha=0.3, label="Occlusion window")

plt.legend(loc="lower right")

plt.show()