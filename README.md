# WTA_peptidoglycan_nanostructure
This repository comprises code from the paper: Wall teichoic acids regulate peptidoglycan synthesis by paving cell wall nanostructure 

Datasets intended to be run with this code are located at: https://doi.org/10.6084/m9.figshare.c.8406249

This repository contains scripts written in FIJI, MatLab and Python. All python code should be run with python 3.11.13 using the following libraries:
Matplotlib 3.7.1
Numpy 1.24.3
Scipy 1.10.1
Scikit-learn 1.2.2
Scikit-image 0.20.0
Pandas 1.5.3
Seaborn 0.13.2

The general workflow uses FIJI scripts (*.ijm) to import and build image file structures, uses MatLab to segment and track phase contrast images either for single-timepoint staining or timelapse tracking, and applies Python scripts for fluorescent quantification, single molecule tracking and plotting. 

Examples of script workflows for different applications:

## Single-cell growth rate and width tracking (e.g. Figures 1A, 2A, S5A-D, ED2A-H):
- Image_process_updated.ijm
- Alignment_updated.ijm
- Imagealign_barber.m
- Eraseimagepart_barber.m
- BacTrack_barber.m
- Timelapse_growth_rate_script_truncated_time.py
### Run the steps above for each individual experiment. Then run the step(s) below to compile data across multiple experiments:
- timelapse_compile_data_NMPAPERVERSION.py
- timelapse_compiled_data_plots_paper_one_pert_NMPAPERVERSION.py
- timelapse_compiled_data_plot_bkgd.py
- glpq_response_curves_NMPAPERVERSION.py (for heatmap growth rate plots, e.g. Figs. 3D-F, S4A-C) 
### Timelapse significance tests performed with:
- Signficance_test_timelapse_WT_ponA_NMPAPERVERSION.ipynb
- Signficance_test_timelapse_hydrolases_NMPAPERVERSION.ipynb
- Signficance_test_timelapse_hydrolases_ponA_NMPAPERVERSION.ipynb

## Transmission Electron Microscopy (Figures 3G,H):
- TEM_width_plotting-paper_Rod_relative_change_NMPAPERVERSION.ipynb

## EDA-DA labeling (Figs. ED1A, ED4B):
- Timepoint_imaging_v1.ijm
- timepoint_blur_background_automated_repeat_barber.m
- Cell_staining_timepoint_EDADA.py
- Cell_staining_EDADA_reformatting.py
- Cell_staining_label_saving.py
### Run the steps above for each individual experiment. Then run the step(s) below to compile data across multiple experiments:
- EDADA_plotting_paper_NMPAPERVERSION.py

## Single-cell growth rate and width tracking on pads (Figs. ED2E,F):
- Image_process_updated.ijm
- Alignment_updated.ijm
- Imagealign_barber_pad.m
- BacTrack_barber.m
- Timelapse_growth_rate_script_truncated_time.py
### Run the steps above for each individual experiment. Then run the step(s) below to compile data across multiple experiments:
- timelapse_compile_data_NMPAPERVERSION.py
- timelapse_compiled_data_plots_paper_one_pert_NMPAPERVERSION.py

  
## FDAA staining imaging (Figs. 1E, ED4A):
- timepoint_imaging_scenes_single_file.ijm (Fiji)
- timepoint_blur_background_automated_repeat_barber.m
- cell_staining_timepoint.py
- cell_staining_label_saving.py
### Run the steps above for each individual experiment. Then run the step(s) below to compile data across multiple experiments:
- cell_staining_timepoint_compilation_paper_NMPAPERVERSION.py

## MreB tracking (Figures 1C, 2F, S5E-J, ED3A-B,D-L, ED8A-C,E-G):
- tirf_processing.ijm
- Mreb_tracking_v3_py3.py
- Mreb_consolidate_timepoints.py (needed to combine finer time-resolution points into coarser timepoints for some experiments)
### Run the steps above for each individual experiment. Then run the step(s) below to compile data across multiple experiments:
- mreb_plotting_compilation_v3_NMPAPERVERSION.py
- mreb_plotting_compilation_py3_glpQ_NMPAPERVERSION.py

## Single Molecule Tracking (Figs. 2D, ED6D)
- tirf_processing.ijm
- single_molecule_tracking_v1.py
- pbp1_tracking_compilation_NMPAPERVERSION.ipynb

## Bulk growth curve data (Figs. 2C, ED1B,C, ED6A, ED10A)
- growth_curves_plate_reader.py
## Run the above for each experiment, then generate saturating OD600 plots using:
- Growth data plotting-ponA_idr-compiled-stats_NMPAPERCOPY.ipynb
- Growth data plotting-ponA_s750_NMPAPERVERSION.ipynb
- Growth data plotting-tun_sens-compiled-stats_NMPAPERCOPY.ipynb
- Growth data plotting-hydrolases_NMPAPERCOPY.ipynb

## Lysis microscopy data (Fig. 2B)
- lysis_annotation_lysed_cells_updated.ijm
- lysis_annotation_plain_cells_updated.ijm
- cell_lysis_timelapse_compiled.py
- lysis_stat_tests.ipynb (to calculate statistical significance)

## Permeability assay — see dedicated ReadMe file.

## PBP1-HADA colocalization (Fig. ED6E)
- FDAA_PBP1_cross_correlation_NMPAPERVERSION.ipynb

## Wheat Germ agglutinin staining (Fig. ED7C)
- WGA_staining_NMPAPERVERSION.py

## Flow Cytometry Data (Fig. S3A)
- cytek_plotting_NMPAPERVERSION.py

## Western and SDS-PAGE plotting (Figs. 2E, ED6G-I)
- bocillin_plotting_NMPAPERVERSION.ipynb
- western_plotting_NMPAPERVERSION.ipynb
- western_plotting-sigInull.ipynb

## HPLC plots (Figs. 1E, ED5A-C)
- HPLC_plots_NMPAPERVERSION.ipynb

