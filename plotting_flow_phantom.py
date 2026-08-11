import pandas as pd
# import matplotlib
# matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import re
import numpy as np

# Get the directory of the current script, folder with data should be located on the same folder as this script 
script_dir = os.path.dirname(os.path.abspath(__file__))

# # Selecting the parent folder
parent_folder = script_dir + r"\flow phantom data"

# getting the folders in which data is stored
subfolders = [f for f in os.listdir(parent_folder) if os.path.isdir(os.path.join(parent_folder, f))
               and re.match(r'^\d+', f)]

# Initialize dictionaries to store the mean SC and SFI values per folder 
Mean_SCvals_perfolder, Mean_SFIvals_perfolder = {}, {}

# Iterating through each folder to load the mean SC and SFI values (on .csv files)
for folder in subfolders:
    if os.path.isfile(os.path.join(parent_folder, folder, 'Mean_SC_perflow.csv')) and os.path.isfile(os.path.join(parent_folder, folder, 'Mean_SFI_perflow.csv')):
        Mean_SC_perflow = pd.read_csv(os.path.join(parent_folder, folder, 'Mean_SC_perflow.csv'), index_col=0).to_dict(orient='list')
        Mean_SFI_perflow = pd.read_csv(os.path.join(parent_folder, folder, 'Mean_SFI_perflow.csv'), index_col=0).to_dict(orient='list')
        Mean_SFI_perflow = {k: Mean_SFI_perflow[k] for k in sorted(Mean_SFI_perflow.keys(), key=lambda s: int(s))}
        Mean_SCvals_perfolder[folder] = Mean_SC_perflow
        Mean_SFIvals_perfolder[folder] = Mean_SFI_perflow

# Getting the data from one subset of the data I got - only getting 10 or 15 db data
db = 15
working_keys = [f'10_22_25', f'10_23_25', f'11_20_25_1mm', f'11_20_25_3mm', f'10_16_25']

# Comment this if you want to usee all data
Mean_SFIvals_perfolder = {key: Mean_SFIvals_perfolder[key] for key in working_keys}
# Mean_SFIvals_perfolder

# Word formatting
plt.rcParams['font.size'] = 12
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.weight'] = 'bold'

# print(list(Mean_SFIvals_perfolder.keys()))
plt.figure(dpi=100, figsize=(11, 3))
plt.rcParams.update({'font.size': 13})
Plotting_means = []

# Colors for the different trials
color_list = ['red', 'blue', 'green', 'orange', 'purple', 'brown', 'black']
shapes = ['D', '*', '^', 'P', 's', 'v', 'o']

# Labels for the different trials
abs_legends = [f"Trial {i + 1}" for i in range(len(color_list))]

for (key, value), color, shape, legendss in zip(Mean_SFIvals_perfolder.items(), color_list, shapes, abs_legends):
    meanSFIs = [np.nanmean(v) for v in value.values()]
    Plotting_means.append(meanSFIs)
    # plt.figure()
    plt.scatter(list(value.keys()), meanSFIs, marker=shape, label=legendss, color=color, linewidths=0.5, s=60) # label=f'Date: {key}'
    # plt.errorbar(list(value.keys()), meanSFIs, yerr=[np.std(v) for v in value.values()], fmt='o', capsize=3, color=color) # Optional: Add error bars for standard deviation
    plt.xlabel('Flow Speed (mm/s)', fontsize=13, fontweight='bold', fontfamily='Arial')
    plt.ylabel('SFI (a.u.)', fontsize=13, fontweight='bold', fontfamily='Arial')

# Adding sensitive band region
plt.axvspan(-0.5, 5.5, color='orange', alpha=0.3, label="Sensitive band")
plt.legend(fontsize=11, loc='lower right')
plt.ylim(0,1500)
plt.xlim(-0.5,10.5)
plt.rcParams["legend.loc"] = 'lower right'
plt.grid()
# output_path = os.path.join(script_dir, 'flow_phantom_plot.png')
# plt.savefig(output_path, dpi=300, bbox_inches='tight')
# print(f"Saved flow phantom plot to {output_path}")
plt.show()