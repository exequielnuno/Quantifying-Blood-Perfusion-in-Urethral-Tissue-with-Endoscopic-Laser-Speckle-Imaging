import numpy as np 
import pandas as pd 
from scipy import stats 
import matplotlib.pyplot as plt 
import os 
from statsmodels.stats.multitest import multipletests
plt.rcParams['font.weight'] = 'bold'

# Get the directory of the current script, folder with data should be located on the same folder as this script 
script_dir = os.path.dirname(os.path.abspath(__file__))

print(script_dir)

# Loading the data for the 4 rabbits and create a dictionary 
# that holds the data. Data is found on .csv files 
pFolderPath = script_dir + r'\rabbit_data'

# folders within the parent folder (each folder contains the data for each rabbit)
subfolders = [ f.path for f in os.scandir(pFolderPath) if f.is_dir() ]

# The median value for each SFI map (400 - 1000 per region) were saved on .csv files, need to extract the filepaths for each 
rabbitsDPath = {
    os.path.basename(folder): [
        os.path.join(root, file_name)
        for root, dirs, files in os.walk(folder)    # Getting the files on the subfolder 
        for file_name in files                      
        if "median" in file_name.lower()            # Checking if median is part of the name of the file
    ]
    for folder in subfolders
}

# Plotting rabbit 3 
rab3 = rabbitsDPath['rabbit3']
rab3_nonoc, rab3_oc = pd.read_csv(rab3[0]), pd.read_csv(rab3[1])

def plotting_rabbit(rab_oc, rab_nonoc):
    # Extract lists of data for each region (column)
    deg_data = [rab_nonoc[col].dropna().tolist() for col in rab3_nonoc.columns]
    post_data = [rab_oc[col].dropna().tolist() for col in rab3_oc.columns]
    region_labels = list(rab3_nonoc.columns)

    num_regions = len(deg_data)

    # Compute medians + IQR asymmetry for error bars
    def median_iqr(arr):
        med = np.nanmedian(arr)
        q1, q3 = np.nanpercentile(arr, [25, 75])
        return med, med - q1, q3 - med

    med_deg, low_deg, high_deg = [], [], []
    med_post, low_post, high_post = [], [], []

    for r in range(num_regions):
        m, l, h = median_iqr(deg_data[r])
        med_deg.append(m); low_deg.append(l); high_deg.append(h)

        m, l, h = median_iqr(post_data[r])
        med_post.append(m); low_post.append(l); high_post.append(h)

    # Setup Plot Figure & Styles
    plt.rcParams['font.family'] = 'Arial'
    fig, ax = plt.subplots(figsize=(12, 4), dpi=100)

    x = np.arange(num_regions)
    width = 0.35

    # Plot bars with matching grayscale color palettes & thin black error caps
    ax.bar(x - width/2, med_deg, width,
        yerr=[low_deg, high_deg], capsize=3, error_kw={'lw': 1, 'ecolor': '#404040'},
        label="Non-occluded", color="#B8B8B8") 

    ax.bar(x + width/2, med_post, width,
        yerr=[low_post, high_post], capsize=3, error_kw={'lw': 1, 'ecolor': '#404040'},
        label="Occluded", color="#606060") 

    # 4. Labels, Axis Limits & Figure Panel Text
    ax.set_xticks(x)
    ax.set_xticklabels(region_labels, fontsize=11, fontweight='bold')
    ax.set_xlabel("Region", fontsize=12, fontweight='bold')
    ax.set_ylabel("SFI (a.u.)", fontsize=12, fontweight='bold')
    ax.set_title("Non-occluded vs occluded (Median ± IQR)", fontweight='bold', fontsize=13)

    # Add the panel sub-label at the top left corner
    ax.text(-0.07, 1.02, "D)", transform=ax.transAxes, fontsize=16, fontweight='bold', va='top', ha='right')

    # Y-axis range 
    ax.set_ylim(0, 10000)
    ax.tick_params(axis='both', labelsize=11, width=1.2)

    #Legend Customization
    leg = ax.legend(fontsize=10, loc='upper right')
    frame = leg.get_frame()
    frame.set_edgecolor('black')
    frame.set_linewidth(0.8)

    plt.tight_layout()



# Initialize dictionary to hold the data for each rabbit - load the data from the .csv files
rabbitStats = {
    "degNonOcc" : {},
    "degOcc"    : {}
}
# Iterating through each rabbit (subfolder)
for rabbit, paths in rabbitsDPath.items():
    for path in paths:
        # --- Degloved Non-occluded ---
        if "median_SFI" in path and "degloved non-occluded" in path: 
            # .csv contains the region (column) and the median SFI for each frame
            df = pd.read_csv(path).to_dict(orient="list")

            # Initialize empty array 
            medians = []

            # Calculate median for each region (ignoring NaNs if there are any)
            for region_vals in df.values():
                medians.append(np.nanmedian(region_vals))
            # Appending the array to the dictionary
            rabbitStats["degNonOcc"][rabbit] = medians

            # --- Degloved Occluded ---
        if "median_SFI" in path and "degloved occluded" in path: 
            # .csv contains the region (column) and the median SFI for each frame
            df = pd.read_csv(path).to_dict(orient="list")

            # Initialize empty array 
            medians = []

            # Calculate median for each region (ignoring NaNs if there are any)
            for region_vals in df.values():
                medians.append(np.nanmedian(region_vals))
            # Appending the array to the dictionary
            rabbitStats["degOcc"][rabbit] = medians


# Fucntions for plotting 
# new sig brackets whose legs reach all the way to the bottom 
def add_sig_bracket(ax, x1, x2, y, h, text, bar1_top, bar2_top, fontsize=11):
    """
    Draws a significance bracket between bars x1 and x2.
    bar1_top and bar2_top are the actual top heights of the bars (median + IQR).
    """
    # Vertical lines go from bar top → bracket height
    ax.plot([x1, x1], [bar1_top, y], lw=1.2, c='black')
    ax.plot([x2, x2], [bar2_top, y], lw=1.2, c='black')

    # Horizontal line
    ax.plot([x1, x2], [y, y], lw=1.2, c='black')

    # Text
    ax.text((x1+x2)/2, y + h, text, ha='center', va='bottom', fontsize=fontsize)

def plot_two_conditions(deg, post,
                        rabbit_labels=None,
                        figsize=(12,5),
                        title="Deg vs Deg-occluded per Rabbit (Median ± IQR)",
                        y_label="Median SFI",
                        fontsize=14):

    num_rabbits = len(deg)
    if rabbit_labels is None:
        rabbit_labels = [f"Rabbit {i+1}" for i in range(num_rabbits)]

    # Compute medians + IQR helper function
    def median_iqr(arr):
        med = np.nanmedian(arr)
        q1, q3 = np.nanpercentile(arr, [25, 75])
        return med, med - q1, q3 - med

    med_deg, low_deg, high_deg = [], [], []
    med_post, low_post, high_post = [], [], []

    # Getting the vlaues for the Interquartile Range
    for r in range(num_rabbits):
        m, l, h = median_iqr(deg[r])
        med_deg.append(m); low_deg.append(l); high_deg.append(h)

        m, l, h = median_iqr(post[r])
        med_post.append(m); low_post.append(l); high_post.append(h)

    # Mann–Whitney per rabbit
    pvals = []
    for r in range(num_rabbits):
        stat, p = stats.ttest_ind(deg[r], post[r])
        pvals.append(p)

    # Remanant for when this function was doing multiple comparisons 
    # reject, p_adj, _, _ = multipletests(pvals, method='holm')

    # Plot
    x = np.arange(num_rabbits)
    width = 0.35

    fig, ax = plt.subplots(figsize=figsize, dpi=300)

    ax.bar(x - width/2, med_deg, width,
           yerr=[low_deg, high_deg], capsize=5,
           label="Non-occluded", color="#B0B0B0") #color="#DD8452"

    ax.bar(x + width/2, med_post, width,
           yerr=[low_post, high_post], capsize=5,
           label="Occluded", color="#737373") # color="#55A868"

    ax.set_xticks(x)
    ax.set_xticklabels(rabbit_labels, fontweight='bold', fontsize=fontsize)
    ax.set_ylabel(y_label, fontsize=fontsize + 2, fontweight='bold', color='black')
    ax.set_title(title, color="black", fontweight='bold', fontsize=fontsize + 2)
    leg = ax.legend(fontsize=fontsize) # Legend 
    ax.tick_params(axis='both', colors='black', labelsize=fontsize, width=1.5)
    for text in leg.get_texts(): # Changing legend text
        text.set_color('black')
        text.set_fontweight('bold')
        text.set_fontsize(fontsize)
    frame = leg.get_frame()
    frame.set_edgecolor('black')
    frame.set_linewidth(1)
    plt.rcParams['font.size'] = fontsize
    plt.rcParams['font.family'] = 'Arial'
    plt.rcParams['font.weight'] = 'bold'

    # Significance brackets
    # Compute true maximum height including error bars
    true_ymax = max(
        max(np.array(med_deg)  + np.array(high_deg)),
        max(np.array(med_post) + np.array(high_post))
    )
    padding = true_ymax * 0.05
    h = true_ymax * 0.05  # vertical spacing

    m = 0.05
    for r in range(num_rabbits):
        # How far do the legs of the bar reach
        bar1_top = med_deg[r]  + high_deg[r] + true_ymax * m
        bar2_top = med_post[r] + high_post[r] + true_ymax * m

        y = max(bar1_top, bar2_top) + padding   # bracket sits above tallest bar

        if pvals[r] < 0.01:
            text = "**"
        elif pvals[r] < 0.05:
            text = "*"
        else:
            text = "ns"

        x1, x2 = r - width/2, r + width/2

        max_bracket_y = max(0, y)

        add_sig_bracket(ax, x1, x2, y, h*0.3, text, bar1_top, bar2_top, fontsize=fontsize + 1)

    ax.set_ylim(0, max_bracket_y + true_ymax * 0.4)
    # plt.ylim(0,180)
    plt.tight_layout()

    return pvals


# Getting data back to array form - the previous was done so that we can keep track on each rabbit 
dgoC = [rabbitStats['degOcc'][rabbit] for rabbit in rabbitStats['degOcc'].keys()]
deg = [rabbitStats['degNonOcc'][rabbit] for rabbit in rabbitStats["degNonOcc"].keys()]

# Normalizing values to non-occluded median values 
div_median = [np.median(vals) for vals in deg]
valid_deg = [vals/np.median(vals) * 100 for vals in deg]
valid_dgoC = [vals / md * 100 for vals, md in zip(dgoC, div_median)]

print("\nShapiro on non-occluded, rabbits 1-4")
for j, data in enumerate(valid_deg):
    print(f"Rabbit {j + 1} shapiro: ", stats.shapiro(data))

print("Shapiro on occluded, rabbits 1-4") 
for k, data in enumerate(valid_dgoC):
    print(f"Rabbit {k + 1}: ", stats.shapiro(data))

# calculating median 
dgoC_medians = [np.median(row) for row in dgoC]
deg_medians = [np.median(row) for row in deg]

# Plotting rabbit 3 
plotting_rabbit(rab3_oc, rab3_nonoc)

# print(deg)
# plot_two_conditions(deg_medians, dgoC_medians)
pvals = plot_two_conditions(valid_deg, valid_dgoC,
                     title="Non-occluded vs occluded per rabbit (Percentage median ± IQR)",
                     y_label="Normalized SFI (%)",
                     figsize=(5, 2),
                     fontsize=5)

# Printing the p-value
print("\n P-values")
rabbit_string = ["Rabbit 1", "Rabbit 2", "Rabbit 3", "Rabbit 4"]
for k in range(len(pvals)):
    print(rabbit_string[k] + "Non-occluded vs Occluded Mann-Whitney U p-value: ", pvals[k])


# plt.figure()
# plt.bar(rabbitStats['degOcc'].keys(), deg_medians)
plt.show()


# plt.hist(dgoC[2], bins=4)
# plt.show()