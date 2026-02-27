import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import skimage
from skimage import io
import seaborn as sns
import scipy
from scipy import stats
from skimage import feature
from skimage import measure
from skimage import exposure
from scipy import ndimage as ndi
from skimage.morphology import disk
from skimage.morphology import erosion, dilation, opening, closing, white_tophat
import weakref
from matplotlib import cm
import pickle
from numpy.matlib import repmat
import os
import pandas as pd
import statsmodels.stats.api as sms

class trace(object):  # we will define an object called a trace for each MreB filament.
    trackCount = 0  # total number of tracks

    def __init__(self, parameters):  # parameters = [coords(y,x), frame]
        self.coords = [parameters[0]]
        self.frames = [parameters[1]]
        self.displacement = []
        trace.trackCount += 1
        self.id = trace.trackCount

    def timepoint(self, parameters):  # parameters = [coords(y,x), frame]
        self.coords = self.coords + [parameters[0]]
        self.frames = self.frames + [parameters[1]]
        self.displacement = self.displacement + [parameters[2]]

def save_object(obj, filename):
    # Code taken from:
    # https://stackoverflow.com/questions/4529815/saving-an-object-data-persistence?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa
    with open(filename, 'wb') as output:  # Overwrites any existing file.
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)

consolidations = [['0min', '5min'], ['10min', '15min'], ['20min', '25min'], ['30min', '35min'], ['40min', '45min']]

expt_ids = ['/240111_bFB12_TIRF_Xylose_depletion', '/231120_bFB12_Xylose_depletion_TIRF']
expt_ids_out = [expt_id+'_consolidated' for expt_id in expt_ids]
path='/Volumes/data_ssd1/Rojas_Lab/data/'
consolidate_list=[]
for conds in consolidations:
    consolidate_list.extend(conds)
# print('consolidated list', consolidate_list)
# This part loads, consolidates and renames the data for the experiments listed above
for expt_id in expt_ids:
    expt_id_out=expt_ids_out[expt_ids.index(expt_id)]
    if not (os.path.exists(path + expt_id_out)):
        os.mkdir(path + expt_id_out)
    # first we must open the relevant parameters for this experiment
    temp_path = path+expt_id+expt_id+'_condition_parameters.pkl'
    with open(temp_path, 'rb') as input:
        expt_vals=pickle.load(input)
    data=[]
    # Now we load the data for each timepoint (cond) associated with a given experiment
    new_id=expt_id_out
    new_condition=expt_vals['condition']
    # These parameters need to be adjusted to match the consolidated data
    new_conds = []
    new_scene_nums = []
    new_timepoints = []
    new_thresholds=[]
    for cond in expt_vals['conds']:
        if not (cond in consolidate_list):
            new_conds.append(cond)
            temp_ind = expt_vals['conds'].index(cond)
            new_scene_nums.append(expt_vals['scene_nums'][temp_ind])
            new_timepoints.append(expt_vals['timepoints'][temp_ind])
            new_thresholds.append(expt_vals['thresholds'][temp_ind])
            if not (os.path.exists(path + expt_id_out + '/' + cond)):
                os.mkdir(path + expt_id_out + '/' + cond)
        else:
            temp_ind1 = np.nonzero([cond in temp for temp in consolidations])[0][0]  # gives the index of
            cond_consol = consolidations[temp_ind1][0]
            if not (os.path.exists(path + expt_id_out + '/' + cond_consol)):
                os.mkdir(path + expt_id_out + '/' + cond_consol)
            if not(cond_consol in new_conds): # avoids repeats
                new_conds.append(cond_consol)
                temp_ind2 = expt_vals['conds'].index(cond)
                new_timepoints.append(expt_vals['timepoints'][temp_ind2])
                new_thresholds.append(expt_vals['thresholds'][temp_ind2])
                temp_inds=[expt_vals['conds'].index(temp_conds) for temp_conds in consolidations[temp_ind1]]
                new_scene_nums.append(np.sum([expt_vals['scene_nums'][temp_ind3] for temp_ind3 in temp_inds]))

        for scene_num in range(1,expt_vals['scene_nums'][expt_vals['conds'].index(cond)]+1):
            temp_path = path+expt_id+'/'+cond+expt_id+'_'+cond+'_s{0}_crop'.format(str(scene_num).zfill(3))
            with open(temp_path+'_tracked_filt.pkl', 'rb') as input:
                temp_data=pickle.load(input)
            background = io.imread(temp_path+'_background.tif')
            if not(cond in consolidate_list):
                out_path = path + expt_id_out + '/' + cond + expt_id_out + '_' + cond + '_s{0}_crop'.format(
                    str(scene_num).zfill(3))
                save_object(temp_data, out_path + '_tracked_filt.pkl')
                skimage.io.imsave(out_path+'_background.tif',background)
            else:
                # In this case, we need to consolidate our data.
                # print(cond, np.nonzero([cond in temp for temp in consolidations]))
                temp_out_path = path + expt_id_out + '/' +cond_consol
                # print(os.listdir(temp_out_path))
                out_path=temp_out_path + expt_id_out + '_' + cond_consol + '_s{0}_crop'.format(str(int(len(os.listdir(temp_out_path))/2)+1).zfill(3))
                save_object(temp_data, out_path + '_tracked_filt.pkl')
                skimage.io.imsave(out_path + '_background.tif',background)
            print('Initial: ', temp_path[35:])
            print('Final: ', out_path[35:])
    print(expt_id)
    print('New conditions', new_conds)
    print('New timepoints', new_timepoints)
    print('New Scenes', new_scene_nums)
    print('New thresholds', new_thresholds)
    temp = {id:new_id, 'conds':new_conds, 'scene_nums':new_scene_nums, 'timepoints': new_timepoints, 'condition': new_condition, 'thresholds':new_thresholds}
    temp_path = path+expt_id_out+expt_id_out+'_condition_parameters.pkl'
    with open(temp_path, 'wb') as output:  # Overwrites any existing file.
        pickle.dump(temp, output, pickle.HIGHEST_PROTOCOL)
    print('Old vals: ', expt_vals)
    print('New vals: ', temp)
            # temp_data['']