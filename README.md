# WTA_peptidoglycan_nanostructure
This repository comprises code from the paper: Wall teichoic acids regulate peptidoglycan synthesis by paving cell wall nanostructure 

This repository contains scripts written in FIJI, MatLab and Python. All python code should be run with python 3.11.13 using the following libraries:
Matplotlib 3.7.1
Numpy 1.24.3
Scipy 1.10.1
Scikit-learn 1.2.2
Scikit-image 0.20.0
Pandas 1.5.3

The general workflow follows using FIJI scripts (*.ijm) to import and build image file structures, using MatLab to segment and track phase contrast images either for single-timepoint staining or timelapse tracking, then using Python for fluorescent quantification, single molecule tracking and plotting.

Examples of script use by figure:

-Fig. 1B, S2A,B,C,D:
Image_process_updated.ijm
Alignment_updated.ijm
Imagealign_felix.m
Eraseimagepart_felix_updated_blurry.m
Bactrack_felix_tester.m
Timelapse_growth_rate_script_truncated_time.py
________
Run the steps above for each individual experiment. Then run the step(s) below to compile data across multiple experiments:
Timelapse_compile_data.py
Timelapse_compiled_data_plots.py


-Fig. S1A (EDA-DA labeling):
Timepoint_imaging_v1.ijm
Timepoint_blur_background_automated_repeat.m
Timepoint_segmentation.m
Cell_staining_timepoint_EDADA.py
Cell_staining_EDADA_reformatting.py
Cell_staining_label_saving.py
________
Run the steps above for each individual experiment. Then run the step(s) below to compile data across multiple experiments:
EDADA_plotting_paper.py 

-Fig. S2E, F (Pad growth):
Image_process_updated.ijm
Alignment_updated.ijm
Imagealign_felix_pad.m
Bactrack_felix_tester.m
Timelapse_growth_rate_script_truncated_time.py
________
Run the steps above for each individual experiment. Then run the step(s) below to compile data across multiple experiments:
Timelapse_compile_data.py
Timelapse_compiled_data_plots.py

-Fig. 1E, S4A (Timepoint imaging):
timepoint_imaging_scenes_single_file.ijm (Fiji)
timepoint_blur_background_automated_repeat.m
timepoint_segmentation.m
cell_staining_timepoint.py
cell_staining_label_saving.py
________
Run the steps above for each individual experiment. Then run the step(s) below to compile data across multiple experiments:
cell_staining_timepoint_compilation_paper.py

Fig. 1C (MreB tracking).
Mreb_tracking_v3_py3.py
