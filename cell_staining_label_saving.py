import scipy
import skimage
import sys
from skimage import io
import numpy as np
import matplotlib.pyplot as plt
import pickle
import pandas as pd
from numpy import matlib
import seaborn as sns
import math
import os
import scipy.optimize
import scipy.io as sio
from scipy import stats
import scipy.ndimage
# import h5py
sns.set_style("white")
from skimage.morphology import disk
from skimage.morphology import erosion, dilation, opening, closing, white_tophat
import image_toolkit as imkit

sns.set(font_scale=1.5)
sns.set_style("whitegrid")

#Note: celltype will be the hue for plotting later.

# path = '/mnt/d/Documents_D/Rojas_lab/data/'
path = '/Volumes/data_ssd2/Rojas_Lab/data/'
# path = '/Volumes/data_ssd1/Rojas_Lab/data/'
# path = '/Users/felixbarber/Documents/Rojas_Lab/data'

expt_id, date = '/221012_bFB69_Tun_gr_HADA', '10/12/22'
conditions=['120 mins, 0.5ug/mL Tun']
label = 'HADA'
expt = r'$\Delta ponA$ 10/12/22'
celltype=r'$\Delta ponA$'


# expt_id, date = '/220309_bFB69_Tun_gr_HADA', '03/09/22'
# conditions=['60 mins, 0.5ug/mL Tun']
# label = 'HADA'
# expt = r'$\Delta ponA$ 03/09/22'
# celltype=r'$\Delta ponA$'

# expt_id, date = '/221214_bFB7_HADA_Tun', '12/14/22'
# conditions=['LB','5 mins, 0.5ug/mL Tun', '10 mins, 0.5ug/mL Tun',  '15 mins, 0.5ug/mL Tun']
# label = 'HADA'
# celltype = r'$\Delta cwlO$'
# expt = r'$\Delta cwlO$ 12/14'

# expt_id, date = '/220120_bFB7_HADA_Tun', '01/20/21'
# conditions=['LB','5 mins, 0.5ug/mL Tun', '10 mins, 0.5ug/mL Tun',  '15 mins, 0.5ug/mL Tun']
# label = 'HADA'
# celltype = r'$\Delta cwlO$'
# expt = r'$\Delta cwlO$ 1/20'

# expt_id, date = '/220204_bFB69_Tun_gr_HADA', '02/04/22'
# conditions=['45 mins, 0.5ug/mL Tun']
# label = 'HADA'
# expt = r'$\Delta ponA$ 02/04/22'
# celltype=r'$\Delta ponA$'

# expt_id, date = '/220121_bFB66_Tun_gr_HADA', '01/21/22'
# conditions=['45 mins, 0.5ug/mL Tun']
# label = 'HADA'
# expt = 'WT 01/21/22'
# celltype='WT'

# expt_id, date = '/250616_bFB6_xylose_depletion_HADA', '06/16/25'
# conditions=['5 min depletion', '10 min depletion', '25 min depletion', '60 min depletion']
# label = 'HADA'
# expt = r'$P_{Xyl}-TagO$ 6/16'
# celltype=r'$P_{Xyl}-TagO$'

# expt_id, date = '/210506_FB6_inducer_loss', '05/06/21'
# conditions=['LB + 30mM Xylose', '10 min depletion', '25 min depletion', '60 min depletion']
# label = 'HADA'
# expt = r'$P_{Xyl}-TagO$ 5/6'
# celltype=r'$P_{Xyl}-TagO$'

# expt_id, date = '/250610_bFB66_tun_EDADA', '06/10/25'
# conditions=['LB', 'LB']
# label = 'AF-AF488-azide'
# expt = r'WT click 6/10/25'
# celltype= 'WT_EDADA_click'

# expt_id, date = '/250616_bFB66_EDADA', '06/16/25'
# conditions=["LB", "Tun", "fos", "Tun van","van", "untreated"]
# label = 'AF-AF488-azide'
# expt = r'WT click 6/16/25'
# celltype= 'WT_EDADA_click'

# expt_id, date = '/250613_bFB66_EDADA_tun_full_rep2', '06/13/25 v2'
# conditions=["LB", "Tun", "fos", "untreated", "Tun van", "van"]
# label = 'AF-AF488-azide'
# expt = r'WT click 6/13/25 v2'
# celltype= 'WT_EDADA_click'
#
# expt_id, date = '/250613_bFB66_EDADA_tun_full', '06/13/25'
# conditions=["LB", "Tun", "fos", "untreated", "Tun van", "van"]
# label = 'AF-AF488-azide'
# expt = r'WT click 6/13/25'
# celltype= 'WT_EDADA_click'
#
# expt_id, date = '/250612_bFB66_EDADA_tun_full', '06/12/25'
# conditions=["LB", "Tun", "fos", "untreated", "van"]
# label = 'AF-AF488-azide'
# expt = r'WT click 6/12/25'
# celltype= 'WT_EDADA_click'

# expt_id, date = '/241129_bFB69_GlpQ_antibody_staining_pads', '11/29/24'
# conditions=['Buffer', 'GlpQ', 'Control']
# label = 'anti-His-AF488'
# expt = r'$\Delta$ponA his 11/29/24'
# celltype= 'ponA_pads_his_control_v1'

# expt_id, date = '/241126_bFB69_GlpQ_antibody_staining_pads', '11/26/24'
# conditions=['Buffer', 'GlpQ']
# label = 'anti-His-AF488'
# expt = r'$\Delta$ponA his 11/26/24'
# celltype= 'ponA_pads_his_control'

# expt_id, date = '/241121_bFB69_GlpQ_antibody_staining', '11/21/24'
# conditions=['Buffer', 'GlpQ']
# label = 'anti-His-AF488'
# expt = r'$\Delta$ponA his 11/21/24'
# celltype= 'ponA_chip_his_control'

# expt_id, date = '/241115_bFB69_LB_Van_control', '11/15/24'
# conditions=['LB', '10min']
# label = 'Vancomycin-Bodipy'
# expt = r'$\Delta$ponA Van 11/15/24'
# celltype= 'ponA_bulk_van_LB_control'


# expt_id, date = '/241114_bFB69_Tun_Van_pads', '11/14/24'
# conditions=['Tun', 'LB']
# label = 'Vancomycin-Bodipy'
# expt = r'$\Delta$ponA Van 11/14/24'
# celltype= 'ponA_bulk_van_Tun'

# expt_id, date = '/241114_bFB66_GlpQ_Van_pads', '11/14/24'
# conditions=['GlpQ', 'Buffer']
# label = 'Vancomycin-Bodipy'
# expt = 'WT Van 11/14/24'
# celltype= 'WT_bulk_van_GlpQ'

# expt_id, date = '/241113_bFB66_GlpQ_Van_pads_v1', '11/13/24'
# conditions=['GlpQ', 'Buffer']
# label = 'Vancomycin-Bodipy'
# expt = 'WT Van 11/13/24'
# celltype= 'WT_bulk_van_GlpQ'

# expt_id, date = '/241113_bFB69_Tun_HADA', '11/13/24'
# conditions=['LB', '0 mins, 0.5ug/mL Tun','5 mins, 0.5ug/mL Tun', '10 mins, 0.5ug/mL Tun']
# label = 'HADA'
# expt = r'$\Delta ponA$ 11/13/24'
# celltype=r'$\Delta ponA$'

# expt_id, date = '/241113_bFB69_Tun_Van_pads_v2', '11/13/24 v2'
# conditions=['Tun', 'LB']
# label = 'Vancomycin-Bodipy'
# expt = r'$\Delta$ponA Van 11/13/24 v2'
# celltype= 'ponA_bulk_van_Tun'

# expt_id, date = '/241113_bFB69_Tun_Van_pads_v1', '11/13/24'
# conditions=['Tun', 'LB']
# label = 'Vancomycin-Bodipy'
# expt = r'$\Delta$ponA Van 11/13/24'
# celltype= 'ponA_bulk_van_Tun'

# expt_id, date = '/241112_bFB66_GlpQ_Van_pads', '11/12/24'
# conditions=['GlpQ', 'Buffer']
# label = 'Vancomycin-Bodipy'
# expt = 'WT Van 11/12/24'
# celltype= 'WT_bulk_van_GlpQ'

# expt_id, date = '/241112_bFB66_Tun_WGA_pads', '11/12/24'
# conditions=['Tun', 'LB']
# label = 'WGA-AF488'
# expt = 'WT WGA 11/12/24'
# celltype= 'WT_bulk'

# expt_id, date = '/241112_bFB66_Tun_Van_pads', '11/12/24'
# conditions=['Tun', 'LB']
# label = 'Vancomycin-Bodipy'
# expt = 'WT Van 11/12/24'
# celltype= 'WT_bulk_van_Tun'

# expt_id, date = '/241108_bFB66_Tun_van', '11/08/24'
# conditions=['Tun', 'LB']
# label = 'Vancomycin-Bodipy'
# expt = 'WT Van 11/08/24'
# celltype= 'WT_bulk_van_Tun'

# expt_id, date = '/241105_bFB66_Tun_van', '11/05/24'
# conditions=['Tun', 'LB']
# label = 'Vancomycin-Bodipy'
# expt = 'WT Van 11/05/24'
# celltype= 'WT_bulk_van_Tun'

# expt_id, date = '/241025_bFB66_Tun_WGA_pads', '10/25/24'
# conditions=['Tun', 'LB', 'Tun rep']
# label = 'WGA-AF488'
# expt = 'WT WGA 10/25/24'
# celltype= 'WT_bulk'

# expt_id, date = '/241024_bFB69_GlpQ_WGA_pads', '10/24/24'
# conditions=['GlpQ', 'Buffer', 'GlpQ rep']
# label = 'WGA-AF488'
# expt = 'ponA GlpQ WGA 10/24/24'
# celltype= 'ponA_bulk_GlpQ'

# expt_id, date = '/241024_bFB66_Tun_WGA_pads', '10/24/24'
# conditions=['Tun', 'LB']
# label = 'WGA-AF488'
# expt = 'WT WGA 10/24/24'
# celltype= 'WT_bulk'

# expt_id, date = '/241023_bFB69_Tun_WGA_pads', '10/23/24'
# conditions=['Tun', 'LB', 'LB repeat']
# label = 'WGA-AF488'
# expt = 'ponA WGA 10/23/24'
# celltype= 'ponA_bulk'


# expt_id, date = '/241018_bFB69_WGA_LB_pads', '10/18/24'
# conditions=['Tun', 'LB']
# label = 'WGA-AF488'
# expt = 'ponA WGA 10/18/24'
# celltype= 'ponA_bulk'
#
# expt_id, date = '/241022_bFB69_Tun_WGA_pads_LB', '10/22/24'
# conditions=['Tun', 'LB']
# label = 'WGA-AF488'
# expt = 'ponA WGA 10/22/24'
# celltype= 'ponA_bulk'

# expt_id, date = '/241015_bFB69_Tun_WGA', '10/15/24'
# conditions=['Tun', 'LB']
# label = 'WGA-AF488'
# expt = 'ponA WGA 10/15/24'
# celltype= 'ponA'

# expt_id, date = '/241008_bFB69_Tun_WGA', '10/08/24'
# conditions=['Tun', 'LB']
# label = 'WGA-AF488'
# expt = 'ponA WGA 10/08/24'
# celltype= 'ponA'

# expt_id, date = '/241011_bFB69_Tun_WGA', '10/11/24'
# conditions=['Tun', 'LB']
# label = 'WGA-AF488'
# expt = 'ponA WGA 10/11/24'
# celltype= 'ponA'

# expt_id, date = '/240913_bFB66_GlpQ_FLVan', '09/13/24'
# conditions=['GlpQ', 'PBS']
# label = 'Vancomycin'
# expt = 'WT GlpQ  9/13/24'
# celltype= 'WT'

# expt_id, date = '/240912_bFB66_GlpQ_FLVan', '09/12/24'
# conditions=['GlpQ', 'PBS']
# label = 'Vancomycin'
# expt = 'WT GlpQ  9/12/24'
# celltype= 'WT'


# expt_id, date = '/240911_bFB66_FLVan', '09/11/24'
# conditions=['GlpQ', 'PBS']
# label = 'Vancomycin'
# expt = 'WT GlpQ  9/11/24'
# celltype= 'WT'

# expt_id, date = '/240202_bFB205_Tun_HADA', '02/02/24'
# conditions=['LB', '5 min, 0.5ug/mL Tun', '15 min, 0.5ug/mL Tun']
# label = 'HADA'
# expt = r'$\Delta 4$  2/2/24'
# celltype= r'$\Delta 4$'

# expt_id, date = '/240202_bFB69_Tun_HADA', '02/02/24'
# conditions=['LB', '5 min, 0.5ug/mL Tun', '15 min, 0.5ug/mL Tun', '25 min, 0.5ug/mL Tun']
# label = 'HADA'
# expt = r'$\Delta ponA$ 2/2/24'
# celltype=r'$\Delta ponA$'

# expt_id, date = '/240131_bFB205_Tun_HADA', '01/31/24'
# conditions=['LB', '0 min, 0.5ug/mL Tun', '5 min, 0.5ug/mL Tun', '15 min, 0.5ug/mL Tun']
# label = 'HADA'
# expt = r'$\Delta 4$  1/31/24'
# celltype= r'$\Delta 4$'

# expt_id, date = '/240126_bFB66_Tun_HADA', '01/26/24'
# conditions=['LB', '0 min, 0.5ug/mL Tun', '5 min, 0.5ug/mL Tun', '10 min, 0.5ug/mL Tun']
# label = 'HADA'
# expt = r'WT'
# celltype=r'WT'


# expt_id, date = '/210416_FB2_HADA_Staining', '04/16/21'
# conditions=['LB', '5 min 0.5ug/mL Tun', '10 min 0.5ug/mL Tun', '15 min 0.5ug/mL Tun',
#             '25 min 0.5ug/mL Tun']
# label = 'HADA'
# celltype='WT'
# expt = r'WT PY79 4/16'

# expt_id, date = '/220104_bFB66_Tun_HADA', '01/04/21'
# conditions=['LB', '0 mins, 0.5ug/mL Tun', '5 mins, 0.5ug/mL Tun', '10 mins, 0.5ug/mL Tun']
# label = 'HADA'
# celltype = 'WT'
# expt = r'WT PY79 1/4'

# expt_id, date = '/220104_bFB79_Tun_HADA', '01/4/22'
# conditions=['LB', '0 mins, 0.5ug/mL Tun', '5 mins, 0.5ug/mL Tun', '10 mins, 0.5ug/mL Tun']
# label = 'HADA'
# celltype=r'$\Delta dacA$'
# expt = r'$\Delta dacA$ 1/4/22'


# expt_id, date = '/220111_bFB79_HADA_Tun', '01/11/22'
# conditions=['LB', '0 mins, 0.5ug/mL Tun', '5 mins, 0.5ug/mL Tun', '10 mins, 0.5ug/mL Tun']
# label = 'HADA'
# celltype=r'$\Delta dacA$'
# expt = r'$\Delta dacA$ 1/11/22'

# expt_id, date = '/220113_bFB79_HADA_Tun', '01/13/22'
# conditions=['LB','5 mins, 0.5ug/mL Tun', '10 mins, 0.5ug/mL Tun',  '15 mins, 0.5ug/mL Tun']
# label = 'HADA'
# celltype=r'$\Delta dacA$'
# expt = r'$\Delta dacA$ 1/13/22'

# expt_id, date = '/220202_bFB8_Tun_HADA', '02/02/22'
# conditions=['LB','5 mins, 0.5ug/mL Tun', '10 mins, 0.5ug/mL Tun',  '15 mins, 0.5ug/mL Tun']
# label = 'HADA'
# celltype = r'$\Delta lytE$'
# expt = r'$\Delta lytE$ 2/2'

# expt_id, date = '/220207_bFB69_Tun_HADA', '02/02/22'
# conditions=['LB','5 mins, 0.5ug/mL Tun', '10 mins, 0.5ug/mL Tun',  '15 mins, 0.5ug/mL Tun']
# label = 'HADA'
# celltype=r'$\Delta ponA$'
# expt = r'$\Delta ponA$ 2/2'

# expt_id, date = '/230203_bFB107_HADA_Tun', '02/03/23'
# conditions=['LB', '5 min, 0.5ug/mL Tun']
# label = 'HADA'
# expt = r'trpC2 $\Delta pbpA$ 2/3'
# celltype=r'trpC2 $\Delta pbpA$ 2/3'

# expt_id, date = '/230203_bFB108_HADA_Tun', '02/03/23'
# conditions=['LB', '5 min, 0.5ug/mL Tun']
# label = 'HADA'
# expt = r'trpC2 $\Delta pbpH$ 2/3'
# celltype=r'trpC2 $\Delta pbpH$ 2/3'

# expt_id, date = '/230206_bFB1_HADA_Tun', '02/06/23'
# conditions=['LB', '5 min, 0.5ug/mL Tun']
# label = 'HADA'
# expt = r'trpC2 WT 2/3'
# celltype=r'trpC2 WT 2/3'


temp = {'id':expt_id, 'Conditions':conditions, 'Date':date, 'Celltype':celltype, 'Label':label, 'expt':expt}
temp_path = path+expt_id+expt_id+'_condition_parameters.pkl'
with open(temp_path, 'wb') as output:  # Overwrites any existing file.
    pickle.dump(temp, output, pickle.HIGHEST_PROTOCOL)