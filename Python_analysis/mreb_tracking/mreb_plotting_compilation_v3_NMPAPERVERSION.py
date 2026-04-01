import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import skimage
from skimage import io
import seaborn as sns
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
import scipy
import pandas as pd
import statsmodels.stats.api as sms

# Note this should be run with python 2!
color_ind=None
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

path='/Volumes/data_ssd1/Rojas_Lab/data/'
num_rep=2
err_style1='se' # default error style

expt_ids = ['/211220_bFB22_Tun_TIRF','/250508_bFB22_tun_TIRF', '/250512_bFB22_tun_TIRF']
lab = 'lytE'
pert='Tunicamycin addition'
path='/Volumes/data_ssd2/Rojas_Lab/data/'
num_rep=1

# expt_ids = ['/250617_bFB2_s750_tun_TIRF', '/250618_bFB2_s750_tun_TIRF']
# lab = 's750'
# pert='Tunicamycin addition'
# path='/Volumes/data_ssd2/Rojas_Lab/data/'
# num_rep=1
# err_style1=None # default error style

# expt_ids = ['/211217_bFB26_Tun_TIRF', '/250509_bFB26_tun_TIRF', '/250514_bFB26_tun_TIRF', '/250516_bFB26_tun_TIRF']
# lab = 'cwlO'
# pert='Tunicamycin addition'
# path='/Volumes/data_ssd2/Rojas_Lab/data/'
# num_rep=2

# expt_ids = ['/240122_bFB12_TIRF_Xylose_depletion', '/240111_bFB12_TIRF_Xylose_depletion_consolidated', '/241204_bFB12_Xylose_depletion_TIRF']
# lab='inductor_depletion'
# pert='Xylose depletion'
# num_rep=2

# expt_ids = ['/240126_bFB10_Tun_TIRF', '/240209_bFB10_Tun_TIRF', '/220211_bFB10_Tun_TIRF']
# lab='fluor_type'
# pert='Tunicamycin addition'
# num_rep=2

# expt_ids = ['/220309_bFB2_Tun_TIRF', '/240124_bFB2_Tun_TIRF', '/240223_bFB2_Tun_TIRF', '/240410_bFB2_Tun_TIRF']
# lab='mbl_paper'
# pert='Tunicamycin addition'
# num_rep=2
# #
# expt_ids = ['/220222_bFB83_Tun_TIRF_Mg', '/230221_bFB83_Tun_TIRF', '/240730_bFB83_10mMMgCl2_Tun_TIRF']
# lab = 'ponA'
# pert='Tunicamycin addition'
# color_ind=0

# This part loads the data for all the experiments listed above
out_path='/Users/barber.527/Documents/GitHub/Rojas_lab_drafts/outputs/compiled_data/rod_complex_plots/'
col = ['Condition', 'Time', 'Activity', 'Speed',]
df = pd.DataFrame()
lscale = 0.0929
for expt_id in expt_ids:
    # first we must open the relevant parameters for this experiment
    temp_path = path+expt_id+expt_id+'_condition_parameters.pkl'
    with open(temp_path, 'rb') as input:
        expt_vals=pickle.load(input)
    # print(expt_vals)
    data=[]
    print(expt_id)
    # Now we load the data for each timepoint (cond) associated with a given experiment
    for cond in expt_vals['conds']:
        for scene_num in range(1,expt_vals['scene_nums'][expt_vals['conds'].index(cond)]+1):
            temp_data = []
            temp_path = path+expt_id+'/'+cond+expt_id+'_'+cond+'_s{0}_crop'.format(str(scene_num).zfill(3))
            background = io.imread(temp_path+'_background.tif')
            cell_area=np.sum(background==0)*lscale**2  # this gives the cell area
            with open(temp_path+'_tracked_filt.pkl', 'rb') as input:
                temp_data+=pickle.load(input)
            temp_df=pd.DataFrame(columns=col)
            temp_df['Activity']=[obj.lin for obj in temp_data]
            temp_df['Activity ball.'] = [obj.ballistic for obj in temp_data]
            temp_df['Density'] = [obj.lin/cell_area for obj in temp_data]
            temp_df['Density ball.'] = [obj.ballistic / cell_area for obj in temp_data]
            temp_df['Speed']=[obj.speed_fit[0] for obj in temp_data]
            temp_df['ballistic'] = [obj.ballistic for obj in temp_data]
            temp_df['full_label'] = expt_vals['condition'][0]
            temp_df['Condition'] = expt_vals['condition'][0]
            temp_df['Time'] = expt_vals['timepoints'][expt_vals['conds'].index(cond)]
            temp_df['Scene'] = scene_num
            temp_df['Expt'] = expt_id
            df=df.append(temp_df)
df['Speed ball.']=df['Speed']*df['ballistic']
df['Percent_act']=df['Activity ball.']*100.0
# exit()

sns.set(font_scale=1.5)
sns.set_style("white")
fig=plt.figure(figsize=[12, 8])
sns.pointplot(x='Time', y='Activity', hue='Condition', estimator=np.mean, data=df, capsize=0.2,join=1)
plt.ylabel('Rod Complex Activity')
plt.xlabel('Time post ' + pert +' (mins)')
fig.savefig(out_path+lab+'_activity.png',dpi=300, bbox_inches='tight')
plt.clf()

sns.set(font_scale=1.5)
sns.set_style("white")
fig=plt.figure(figsize=[12, 8])
sns.pointplot(x='Time', y='Activity ball.', hue='Condition', estimator=np.mean, data=df, capsize=0.2,join=1)
plt.ylabel('Frac. ballistic tracks')
plt.xlabel('Time post ' + pert +' (mins)')
fig.savefig(out_path+lab+'_activity_ball.png',dpi=300, bbox_inches='tight')
plt.clf()

fig=plt.figure(figsize=[12, 8])
sns.pointplot(x='Time', y='Speed', hue='Condition', data=df[df.Activity == 1], estimator=np.median, capsize=0.5)
plt.ylabel(r'Rod Complex Speed  ($\mu m/s$)')
plt.xlabel('Time post ' + pert +' (mins)')
fig.savefig(out_path+lab+'_speed.png',dpi=300, bbox_inches='tight')
plt.clf()

fig=plt.figure(figsize=[12, 8])
sns.pointplot(x='Time', y='Speed ball.', hue='Condition', data=df[df.Activity == 1], estimator=np.median, capsize=0.5)
plt.ylabel(r'Ballistic Filament Speed ($\mu m/s$)')
plt.xlabel('Time post ' + pert +' (mins)')
fig.savefig(out_path+lab+'_speed_ball.png',dpi=300, bbox_inches='tight')
plt.clf()

# Calculating spatial filament density
temp1=df.groupby(['Expt', 'Condition', 'Time','Scene'])['Density'].sum()
temp2=temp1.groupby(['Expt', 'Condition', 'Time'])
df1=pd.DataFrame(temp2.mean()).reset_index()

fig=plt.figure(figsize=[12, 8])
sns.pointplot(data=df1,x='Time',y='Density', hue='Condition', capsize=0.2, join=1)
plt.ylabel(r'Rod Complex Filament Density ($1/\mu m^2$)')
plt.xlabel('Time post ' + pert +' (mins)')
fig.savefig(out_path+lab+'_density.png',dpi=300, bbox_inches='tight')
plt.clf()

temp1=df.groupby(['Expt', 'Condition', 'Time','Scene'])['Density ball.'].sum()
temp2=temp1.groupby(['Expt', 'Condition', 'Time'])
df2=pd.DataFrame(temp2.mean()).reset_index()

fig=plt.figure(figsize=[12, 8])
sns.pointplot(x='Time', y='Density ball.', hue='Condition', estimator=np.sum, data=df, capsize=0.2, join=1)
plt.ylabel(r'Ballistic Filament Density ($1/\mu m^2$)')
plt.xlabel('Time post ' + pert +' (mins)')
fig.savefig(out_path+lab+'_density_ball.png',dpi=300, bbox_inches='tight')
plt.clf()


# Paper plots
# Now we selectively isolate the timepoints where the required number of replicates overlap (i.e. # > num_rep), ignoring those where they
# don't, so that our data consistently has enough experimental coverage.

tmp_conds=df.Condition.unique()
tmp_timepoints=np.asarray(df.Time.unique())
timepoints=[]
for cond in tmp_conds:
    timepoints.append(df[df.Condition==cond].Time.unique())
print(timepoints)
numreps=[]
for time in tmp_timepoints:
    numreps.append(np.sum([time in temp for temp in timepoints]))
print(tmp_timepoints, numreps)
sel_times=tmp_timepoints[np.nonzero(np.asarray(numreps)>num_rep)] # change this
print(sel_times)
df['tmp']=[val in sel_times for val in df['Time']]
print(numreps)
print(tmp_timepoints)





df2=df[df.tmp==1].groupby(['Condition','Time'])['Percent_act'].describe()
sns.set(font_scale=1.0)
sns.set_style("ticks")
colors=sns.color_palette()
fig=plt.figure(figsize=[2, 1.5])
if not(color_ind is None):
    sns.lineplot(x='Time', y='mean', data=df2, err_style='bars', errorbar=err_style1, err_kws={'capsize': 2}, markers=None,color=colors[color_ind])
    sns.scatterplot(data=df2, x='Time', y='mean', alpha=0.5,color=colors[color_ind])
else:
    sns.lineplot(x='Time',y='mean',data=df2,err_style='bars',errorbar=err_style1,err_kws={'capsize':2},markers=None)
    sns.scatterplot(data=df2, x='Time', y='mean', alpha=0.5)
# sns.pointplot(x='Time', y='Percent_act', estimator=np.mean, data=df[df.tmp==1], capsize=0.1,join=1, markers='.')
ax = plt.gca()
plt.vlines(0, ymin=ax.get_ylim()[0], ymax=ax.get_ylim()[1], linestyle='-', colors='k', lw=0.5)
# plt.ylabel('Processive filaments (%)')
plt.xlabel('Time (min)')
fig.savefig(out_path+lab+'_activity_percent.pdf', bbox_inches='tight')
fig.savefig(out_path+lab+'_activity_percent.png',dpi=300, bbox_inches='tight')
plt.clf()

df2=df[(df.tmp==1)*(df.ballistic==1)].groupby(['Condition','Time'])['Speed ball.'].describe()

sns.set(font_scale=1.0)
sns.set_style("white")
fig=plt.figure(figsize=[2, 1.5])
sns.lineplot(x='Time',y='mean',data=df2,err_style='bars',errorbar=err_style1,err_kws={'capsize':2},markers=None)
sns.scatterplot(data=df2,x='Time',y='mean',alpha=0.5)
# sns.pointplot(x='Time', y='Percent_act', estimator=np.mean, data=df[df.tmp==1], capsize=0.1,join=1, markers='.')
ax = plt.gca()
# plt.ylim(ymax=1.15, ymin=0.85)
plt.ylim(ymax=0.05, ymin=0.025)
plt.vlines(0, ymin=ax.get_ylim()[0], ymax=ax.get_ylim()[1], linestyle='-', colors='k', lw=0.5)
plt.ylabel(r'Speed ($\mu$m/s)')
plt.xlabel('Time (min)')
fig.savefig(out_path+lab+'_ballistic_speed_cumulative.pdf', bbox_inches='tight')
fig.savefig(out_path+lab+'_ballistic_speed_cumulative.png',dpi=300, bbox_inches='tight')
plt.clf()

df2=df[(df.tmp==1)].groupby(['Condition','Time'])['Speed'].describe()

sns.set(font_scale=1.0)
sns.set_style("white")
fig=plt.figure(figsize=[2, 1.5])
sns.lineplot(x='Time',y='mean',data=df2,err_style='bars',errorbar=err_style1,err_kws={'capsize':2},markers=None)
sns.scatterplot(data=df2,x='Time',y='mean',alpha=0.5)
# sns.pointplot(x='Time', y='Percent_act', estimator=np.mean, data=df[df.tmp==1], capsize=0.1,join=1, markers='.')
ax = plt.gca()
# plt.ylim(ymax=0.9, ymin=0.6)
plt.ylim(ymax=0.03, ymin=0.005)
plt.vlines(0, ymin=ax.get_ylim()[0], ymax=ax.get_ylim()[1], linestyle='-', colors='k', lw=0.5)
plt.ylabel(r'Speed ($\mu$m/s)')
plt.xlabel('Time (min)')
fig.savefig(out_path+lab+'_general_speed_cumulative.pdf', bbox_inches='tight')
fig.savefig(out_path+lab+'_general_speed_cumulative.png',dpi=300, bbox_inches='tight')
plt.clf()

temp1=df[df.tmp==1].groupby(['Expt', 'Condition', 'Time','Scene'])['Density ball.'].sum()
temp2=temp1.groupby(['Expt', 'Condition', 'Time'])
df2=pd.DataFrame(temp2.mean()).reset_index()

# print(df2.head(100))
sns.set(font_scale=1.0)
sns.set_style("white")
fig=plt.figure(figsize=[2, 1.5])
sns.lineplot(x='Time',y='Density ball.',data=df2,err_style='bars',errorbar=err_style1,err_kws={'capsize':2},markers=None)
sns.scatterplot(data=df2,x='Time',y='Density ball.',alpha=0.5)
# sns.pointplot(x='Time', y='Percent_act', estimator=np.mean, data=df[df.tmp==1], capsize=0.1,join=1, markers='.')
ax = plt.gca()
plt.vlines(0, ymin=ax.get_ylim()[0], ymax=ax.get_ylim()[1], linestyle='-', colors='k', lw=0.5)
plt.ylabel(r'Density ($1/\mu m^2$)')
plt.xlabel('Time (min)')
fig.savefig(out_path+lab+'_ballistic_density_cumulative.pdf', bbox_inches='tight')
fig.savefig(out_path+lab+'_ballistic_density_cumulative.png',dpi=300, bbox_inches='tight')
plt.clf()

with open(out_path + lab+'.txt', 'w') as f:
    print('Ballistic filaments:', np.sum(df[df.tmp==1]['ballistic']), file=f)  # Python 3.x
    print('Total filaments:', len(df[df.tmp==1]), file=f)  # Python 3.x