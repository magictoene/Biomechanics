# generate_muboInput.ipynb

## 📄 Overview

This Jupyter Notebook performs the complete data preparation and processing pipeline required to convert raw 3D kinematic marker data into the necessary input files for the **Multibody Kinematic Analysis Program (MuboKAP)**. The process focuses on creating a planar (2D) multibody model for inverse dynamic analysis.

The notebook executes the following major steps sequentially:

1.  **Data Import & Projection:** Loads raw data files (`.tsv`), converts units from millimeters to meters, and projects the 3D marker coordinates onto the sagittal plane (dropping the $Y$-axis).

2.  **Model Definition:** Defines the 15-point rigid body model, including establishing the trunk origin from the hip and shoulder marker midpoints.

3.  **Filtering:** Applies a second-order, forward-backward Butterworth filter (with a fixed $6\ Hz$ cutoff frequency) to remove high-frequency noise from all kinematic marker data.

4.  **Static Trial Analysis:** Uses the filtered static trial data to calculate average segment lengths, define the **Local Coordinate Systems (LCS)**, and determine **Center of Mass (CoM)** locations based on anthropometric tables.

5.  **Kinematic Calculation:** Calculates the segment-specific joint angles ($\theta$) relative to the global frame for the dynamic trials.

6.  **MuboKAP File Generation:** Formats the calculated segment angles and constraints into the specific input coordinate files and driver files required by MuboKAP.

## 🛠️ Setup: User-Configurable Paths

Before running the notebook, the user **MUST** update the file paths within the initial code cells to point to their specific data files:

| File Type | Variable to Check | Example File Name | Purpose |
| :--- |:------------------|:-----------------------------------------| :--- |
| **Static Trial** | `file_3D_static`  | `'Trial0001_static.tsv'`                 | Used to calculate segment lengths and initial LCS. |
| **Dynamic Trial 1** | `file_3D_gait`    | `'Trial0003_str11.tsv'`                  | Primary dynamic trial for analysis. |
| **Dynamic Trial 2** | `file_3D_plank`   | `'Trial0016_Plank_Leg_arm_raise.tsv'`    | Secondary dynamic trial for analysis. |
| **Output Prefix** | `flag_name`       | `'plank'` or `'gait'`                    | Used as the prefix for all generated output files. |

(The current state of the notebook is set up for the `plank` trial.)


## 📦 Generated Output

The notebook generates several input files for the MuboKAP solver for each dynamic trial (Gait and Plank). The output files are saved based on the defined `flag_name` (e.g., `gait_'i'`).

| Output File                       | File Name                                                             | Content Description                                                                                                                                                                                             | MuboKAP Purpose |
|:----------------------------------|:----------------------------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------| :--- |
| Body and Joint Configuration data | `rev_joints.tsv`; `df_body_config.tsv` and `df_body_config_plank.tsv` | Body configuration stores the initial position for each of the 14 rigid bodies, for each trial. Joint configuration specifies the constant coordinates of the articulation point in the two local reference frames. |  |
| Driver File                       | `gait_'i'.txt` or `plank_'i'.txt`                                     | Defines the constraints and connections of the model                                                                                                                                                            


# MuboKAP Input

The files `PlankAnalysisModel.ipynb` and `GaitAnalysisModel.ipynb` hold the final configuration for MuboKAP. These files are made up of the output files explained above. 