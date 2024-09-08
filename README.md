# Welcome to streamlit

Check it out on (https://rajkumarpetrophysicsgui.streamlit.app/)

Project Overview

This project focuses on loading and analyzing well log data from a LAS file. It covers data loading, analysis, formation evaluation, and visualization to aid in subsurface characterization and reservoir evaluation.

Key Steps and Analysis:

Data Loading and Formation Evaluation:

Load LAS (Log ASCII Standard) file data.

Extract header information, curve information, and well information.

Data Analysis:

Perform data statistics to understand the range, mean, and distribution of each log.

Formation Evaluation:

Volume of Shale Calculation: Compute the volume of shale using gamma ray logs or other methods.
Water Saturation Calculation: Apply Archie’s Equation to calculate water saturation in the reservoir.
Density Porosity Calculation: Calculate density porosity from bulk density logs.
Total Porosity Calculation: Compute total porosity using neutron porosity and density porosity.

Data Visualization:

Histogram Plots: Create histograms for each available log to visualize their distribution.
Line Plots: Generate line plots for each log to visualize variations with depth.
Triple Combo Log Plot: Visualize multiple logs (e.g., gamma ray, resistivity, and density) together in a single plot.
Cross Plots: Create cross plots (e.g., Neutron-Density, Resistivity-Porosity) for lithology and fluid type identification.
Reservoir Flagging and NTG Calculation:
Identify reservoir zones based on water saturation, porosity, and volume of shale cut-off values.
Calculate Net-To-Gross (NTG) ratio for reservoir characterization.

Conclusion

This workflow provides a comprehensive method for well log analysis, integrating formation evaluation with robust visualizations to support reservoir evaluation and decision-making.
