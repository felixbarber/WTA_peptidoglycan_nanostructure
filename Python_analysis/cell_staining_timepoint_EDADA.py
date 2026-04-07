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
sns.set(font_scale=1.5)
from skimage.morphology import disk
from skimage.morphology import erosion, dilation, opening, closing, white_tophat
import image_toolkit as imkit

#base_path = '/mnt/d/Documents_D/Rojas_lab/data/'
# base_path = '/Users/felixbarber/Documents/Rojas_lab/data/'
# base_path = '/Volumes/data_ssd1/Rojas_Lab/data/'
base_path = '/Volumes/data_ssd2/Rojas_Lab/data/'
thresh_peak=8000
rescale=True
min_thresh=1.0

# Note: Scenes_remove starts counting from 1.

# expt_id, date = '/250616_bFB66_EDADA', '6/16/25'
# conds=["LB", "Tun", "fos", "tun_van","van", "untreated"]
# conditions=["LB", "Tun", "fos", "Tun van","van", "untreated"]
# time_labels=['-5 min', '5 min', '10 min', '15 min', '20 min', '25 min']
# num_scenes=[20,20,12,15,15,10]
# # num_scenes=[1,20,1,1,1,1]
# scenes_remove=[[], [], [],[],[],[]] # scenes to remove from consideration-
# channels, HADA_channel, im_shape=[2], 2, [1500,1500]
# label = 'AF-AF488-azide'
# threshs=[0,0,0,0,0,0] # Assessed based on semilogy plot
# thresh_peak=0.8
# # thresh_peak={"LB":0.3, "Tun":0.3, "fos":0.3, "untreated":0.2, "tun_van":0.2, "van":0.2} # Scaling of spot sensitivity.
# min_thresh=200 #This is to avoid picking spots in scenes with no significant fluorescent signal.
# # Tune based on average fluorescence values

# expt_id, date = '/250613_bFB66_EDADA_tun_full_rep2', '6/13/25 v2'
# conds=["LB", "tun", "fos", "unstained", "tun_van", "LB_van"]
# conditions=["LB", "Tun", "fos", "untreated", "Tun van", "van"]
# time_labels=['-5 min', '5 min', '10 min', '15 min', '20 min', '25 min']
# num_scenes=[20,20,10,6, 20, 20]
# # num_scenes=[3,3,1,1,1,1]
# scenes_remove=[[], [], [], [], [], []] # scenes to remove from consideration-
# channels, HADA_channel, im_shape=[2], 2, [1500,1500]
# label = 'AF-AF488-azide'
# threshs=[0, 0, 0, 0, 0, 0]   # threshold average outline fluorescence to filter out debris
# # thresh_peak=0.3 # Scaling of spot sensitivity.
# # thresh_peak={"LB":0.2, "tun":0.2, "fos":0.2, "unstained":0.2, "tun_van":0.2, "LB_van":0.2} # Scaling of spot sensitivity.
# thresh_peak=0.8
# min_thresh=200 #This is to avoid picking spots in scenes with no significant fluorescent signal.
# # Tune based on average fluorescence values

# expt_id, date = '/250613_bFB66_EDADA_tun_full', '6/13/25'
# conds=["LB", "tun", "fos", "unstained", "tun_van", "LB_van"]
# conditions=["LB", "Tun", "fos", "untreated", "Tun van", "van"]
# time_labels=['-5 min', '5 min', '10 min', '15 min', '20 min', '25 min']
# num_scenes=[20,20,10,10, 20, 20]
# # num_scenes=[2,2,1,1,1,1]
# scenes_remove=[[], [], [],[],[], []] # scenes to remove from consideration-
# channels, HADA_channel, im_shape=[2], 2, [1500,1500]
# label = 'AF-AF488-azide'
# threshs=[0,0,0,0,0, 0]   # threshold average outline fluorescence to filter out debris
# thresh_peak=0.4
# min_thresh=200 #This is to avoid picking spots in scenes with no significant fluorescent signal.
# # Tune based on average fluorescence values

# expt_id, date = '/250612_bFB66_EDADA_tun_full', '6/12/25'
# conds=["LB", "tun_hi", "fos", "untreated", "van"]
# conditions=["LB", "Tun", "fos", "untreated", "van"]
# time_labels=['-5 min', '5 min', '10 min', '15 min', '20 min']
# num_scenes=[20,20,10,10, 20]
# scenes_remove=[[], [], [],[], []] # scenes to remove from consideration-
# channels, HADA_channel, im_shape=[2], 2, [1500,1500]
# label = 'AF-AF488-azide'
# threshs=[0,0,0,0,0]   # threshold average outline fluorescence to filter out debris
# thresh_peak=0.4
# min_thresh=200 #This is to avoid picking spots in scenes with no significant fluorescent signal.
# # Tune based on average fluorescence values

#
expt_id, date = '/250610_bFB66_tun_EDADA', '6/10/25'
conds=["LB_1", "LB_2", "tun_1", "tun_2"]
conditions=["LB_1", "LB_2", "tun_1", "tun_2"]
time_labels=['-5 min', '5 min', '10 min', '15 min']
num_scenes=[10,10,18,10]
scenes_remove=[[], [], [],[]] # scenes to remove from consideration-
channels, HADA_channel, im_shape=[2], 2, [1500,1500]
label = 'AF-AF488-azide'
threshs=[0,0,0,0] # Assessed based on semilogy plot
thresh_peak=1.5
min_thresh=200

out_dir="./outputs"+expt_id
pval=0.01

if not os.path.exists(out_dir):
    os.mkdir(out_dir)
    os.mkdir(out_dir+'/images')

expt_vals_ls=[]
for i0 in range(len(conds)):
    expt_vals_ls.append({'expt_id':expt_id, 'channels':channels,'im_shape':im_shape,
           'base_path':base_path, 'num_scenes':num_scenes[i0], 'cond':conds[i0], 'HADA_channel':HADA_channel, 'date':date,
           'excl_scenes':scenes_remove[i0],'thresh_peak':thresh_peak, 'min_thresh':min_thresh, 'rescale':rescale})

if not os.path.exists(out_dir+expt_id):
    dfs=[]
    for i0 in range(len(expt_vals_ls)):
        print(i0)
        # expt_vals_ls[i0]['median_vals']=imkit.timepoint_bkgd_fluorescence_calculation(expt_vals_ls[i0])
        # dfs.append(imkit.timepoint_import_data_outline(expt_vals_ls[i0]))
        temp_out,temp_ims=imkit.timepoint_import_data_outline_smart_bkgd(expt_vals_ls[i0])
        for i1 in range(len(temp_ims)):
            fig=plt.figure(figsize=[8,8])
            plt.imshow(temp_ims[i1])
            plt.axis('off')
            fig.savefig(out_dir+'/images'+expt_vals_ls[i0]['expt_id']+'_'+expt_vals_ls[i0]['cond']+'_s{0}.png'.format(i1),dpi=300,bbox_inches='tight')
            plt.clf()
        dfs.append(temp_out)
        dfs[i0]['Condition']=conditions[i0]
        dfs[i0]['Date']=expt_vals_ls[i0]['date']
        
    for i0 in range(len(dfs)):  
        temp_df=dfs[i0].rename(columns={'Average F{0}'.format(expt_vals_ls[i0]['HADA_channel']):'Average '+label,
                            'Integrated F{0}'.format(expt_vals_ls[i0]['HADA_channel']):'Integrated '+label,
                                       'Average outline F{0}'.format(expt_vals_ls[i0]['HADA_channel']):'Average outline '+label,
                            'Integrated outline F{0}'.format(expt_vals_ls[i0]['HADA_channel']):'Integrated outline '+label,
                            'CV outline F{0}'.format(expt_vals_ls[i0]['HADA_channel']):'CV outline '+label,
                            'SD outline F{0}'.format(expt_vals_ls[i0]['HADA_channel']):'SD outline '+label})
        if i0==0:
            df=temp_df.copy()
        else:
            df = df.append(temp_df[[obj for obj in df.columns]])
    print(df.keys())
    df.to_pickle(out_dir+expt_id)
else:
    df=pd.read_pickle(out_dir+expt_id)

# Apply thresholding condition by condition for plotting purposes (this will not be saved in the dataset)
for i0 in range(len(conditions)):
    cond=conditions[i0]
    temp_df=df[df['Condition']==cond]
    temp_df = temp_df[temp_df['Average outline ' + label] > threshs[i0]]  # filtering out debris that isn't fluorescent.
    if i0 == 0:
        temp_df1 = temp_df.copy()
    else:
        temp_df1 = temp_df1.append(temp_df[[obj for obj in df.columns]])

df=temp_df1.copy()


def iter_plotting(df, temp_var,temp_out_name,temp_ylab,temp_iter,temp_xlabel,plot_points=True,showfliers=True, temp_hue=None, style="white"):
    # fig=plt.figure(figsize=[6,4])
    sns.set_style(style)
    fig = plt.figure()
    ax=plt.subplot(1,1,1)
    if temp_hue is None:
        plot=sns.boxplot(x=temp_iter,y=temp_var,data=df,fliersize=0,showfliers=showfliers)
        if plot_points:
            plot=sns.stripplot(x=temp_iter,y=temp_var,dodge=True,data=df,color='k',edgecolor='black',linewidth=1,alpha=0.1)
    else:
        plot = sns.boxplot(x=temp_iter, y=temp_var, data=df, fliersize=0, showfliers=showfliers, hue=temp_hue)
        if plot_points:
            plot = sns.stripplot(x=temp_iter, y=temp_var, dodge=True, data=df, color='k', edgecolor='black',
                                 linewidth=1, alpha=0.1, hue=temp_hue)
    plot.set(xlabel=temp_xlabel,ylabel=temp_ylab)
    plt.xticks(rotation = 90)
    
    print('Statistical significances for ', temp_var)
    temp_iter_vals=df[temp_iter].unique()
    print(temp_iter_vals)
    for i0 in range(len(temp_iter_vals)):
        cond1=temp_iter_vals[i0]
        for cond2 in temp_iter_vals[i0:]:
            if cond1!=cond2:
                x1=df[df[temp_iter]==cond1][temp_var]
                x2=df[df[temp_iter]==cond2][temp_var]
                print('Condition 1: '+cond1+',','Condition 2: '+cond2+':', scipy.stats.ttest_ind(x2, x1, axis=0, equal_var=False, nan_policy='propagate')[1] < pval)

    return fig,ax
print(df.Scene[:10])
# Now we plot the results and save the figures

sys.stdout = open(out_dir+expt_id+'_outputs.txt', "w")

# HADA average length density of puncta
temp_var, temp_out_name, temp_ylab='Cell spots/length', 'cell_spots_length', r'Cellular puncta/$\mu$m'
temp_iter,temp_xlabel='Condition','Condition'
fig,ax=iter_plotting(df, temp_var,temp_out_name,temp_ylab,temp_iter,temp_xlabel,showfliers=False)
# ax.set_ylim(ymax=1000)
fig.savefig(out_dir+expt_id+'_'+temp_out_name+'.png',dpi=300,bbox_inches='tight')
plt.clf()

# HADA average length density of wall puncta
temp_var, temp_out_name, temp_ylab='Wall spots/length', 'wall_spots_length', r'Peripheral puncta/$\mu$m'
temp_iter,temp_xlabel='Condition','Condition'
fig,ax=iter_plotting(df, temp_var,temp_out_name,temp_ylab,temp_iter,temp_xlabel,showfliers=False)
# ax.set_ylim(ymax=1000)
fig.savefig(out_dir+expt_id+'_'+temp_out_name+'.png',dpi=300,bbox_inches='tight')
plt.clf()



# HADA average number of puncta
temp_var, temp_out_name, temp_ylab='Cell spots', 'cell_spots', 'Cellular puncta'
temp_iter,temp_xlabel='Condition','Condition'
fig,ax=iter_plotting(df, temp_var,temp_out_name,temp_ylab,temp_iter,temp_xlabel,showfliers=False)
# ax.set_ylim(ymax=1000)
fig.savefig(out_dir+expt_id+'_'+temp_out_name+'.png',dpi=300,bbox_inches='tight')
plt.clf()

# HADA average number of puncta
temp_var, temp_out_name, temp_ylab='Wall spots', 'wall_spots', 'Peripheral puncta'
temp_iter,temp_xlabel='Condition','Condition'
fig,ax=iter_plotting(df, temp_var,temp_out_name,temp_ylab,temp_iter,temp_xlabel,showfliers=False)
# ax.set_ylim(ymax=1000)
fig.savefig(out_dir+expt_id+'_'+temp_out_name+'.png',dpi=300,bbox_inches='tight')
plt.clf()

# HADA outline average values
temp_var, temp_out_name, temp_ylab='Average outline '+label, 'av_outline_fl', 'Average outline fluorescence'
temp_iter,temp_xlabel='Condition','Condition'
fig,ax=iter_plotting(df, temp_var,temp_out_name,temp_ylab,temp_iter,temp_xlabel,showfliers=False)
# ax.set_ylim(ymax=1000)
fig.savefig(out_dir+expt_id+'_'+temp_out_name+'.png',dpi=300,bbox_inches='tight')
plt.clf()

# HADA outline average values
temp_var, temp_out_name, temp_ylab='Average outline '+label, 'av_outline_fl', 'Average outline fluorescence'
temp_iter,temp_xlabel='Condition','Condition'
fig,ax=iter_plotting(df, temp_var,temp_out_name,temp_ylab,temp_iter,temp_xlabel,showfliers=False,style='whitegrid')
ax.set_yscale('log')
fig.savefig(out_dir+expt_id+'_'+temp_out_name+'_semilogy.png',dpi=300,bbox_inches='tight')
plt.clf()

# HADA outline average values
temp_var, temp_out_name, temp_ylab='Average '+label, 'av_area_fl', 'Average area fluorescence'
temp_iter,temp_xlabel='Condition','Condition'
fig,ax=iter_plotting(df, temp_var,temp_out_name,temp_ylab,temp_iter,temp_xlabel,showfliers=False)
# ax.set_ylim(ymax=1000)
fig.savefig(out_dir+expt_id+'_'+temp_out_name+'.png',dpi=300,bbox_inches='tight')
plt.clf()

# HADA outline average values
temp_var, temp_out_name, temp_ylab='Average outline '+label, 'av_outline_fl', 'Average outline fluorescence'
temp_iter,temp_xlabel='Condition','Condition'
fig,ax=iter_plotting(df, temp_var,temp_out_name,temp_ylab,temp_iter,temp_xlabel,plot_points=False,showfliers=False)
# ax.set_ylim(ymax=1000)
fig.savefig(out_dir+expt_id+'_'+temp_out_name+'_no_data.png',dpi=300,bbox_inches='tight')
plt.clf()

# HADA area average values
temp_var, temp_out_name, temp_ylab='Average '+label, 'av_area_fl', 'Average area fluorescence'
temp_iter,temp_xlabel='Condition','Condition'
fig,ax=iter_plotting(df, temp_var,temp_out_name,temp_ylab,temp_iter,temp_xlabel,plot_points=False,showfliers=False)
# ax.set_ylim(ymax=1000)
fig.savefig(out_dir+expt_id+'_'+temp_out_name+'_no_data.png',dpi=300,bbox_inches='tight')
plt.clf()

# HADA outline integrated values
temp_var, temp_out_name, temp_ylab='Integrated outline '+label, 'int_outline_fl', 'Integrated outline fluorescence'
temp_iter,temp_xlabel='Condition','Condition'
fig,ax=iter_plotting(df, temp_var,temp_out_name,temp_ylab,temp_iter,temp_xlabel)
fig.savefig(out_dir+expt_id+'_'+temp_out_name+'.png',dpi=300,bbox_inches='tight')
plt.clf()

# HADA outline integrated values
temp_var, temp_out_name, temp_ylab='Average outline '+label, 'av_outline_fl', 'Average outline fluorescence'
temp_iter,temp_xlabel='Condition','Condition'
fig,ax=iter_plotting(df, temp_var,temp_out_name,temp_ylab,temp_iter,temp_xlabel,temp_hue='Scene')
plt.legend(loc=[1.05,0.0])
fig.savefig(out_dir+expt_id+'_'+temp_out_name+'_by_scene.png',dpi=300,bbox_inches='tight')
plt.clf()

# HADA outline integrated values
temp_var, temp_out_name, temp_ylab='Integrated outline '+label, 'int_outline_fl', 'Integrated outline fluorescence'
temp_iter,temp_xlabel='Condition','Condition'
fig,ax=iter_plotting(df, temp_var,temp_out_name,temp_ylab,temp_iter,temp_xlabel,temp_hue='Scene')
plt.legend(loc=[1.05,0.0])
fig.savefig(out_dir+expt_id+'_'+temp_out_name+'_by_scene.png',dpi=300,bbox_inches='tight')
plt.clf()

# HADA area integrated values
temp_var, temp_out_name, temp_ylab='Integrated '+label, 'int_area_fl', 'Integrated area fluorescence'
temp_iter,temp_xlabel='Condition','Condition'
fig,ax=iter_plotting(df, temp_var,temp_out_name,temp_ylab,temp_iter,temp_xlabel)
fig.savefig(out_dir+expt_id+'_'+temp_out_name+'.png',dpi=300,bbox_inches='tight')
plt.clf()

# HADA outline CV values
temp_var, temp_out_name, temp_ylab='CV outline '+label, 'cv_outline_fl', 'CV outline fluorescence'
temp_iter,temp_xlabel='Condition','Condition'
fig,ax=iter_plotting(df, temp_var,temp_out_name,temp_ylab,temp_iter,temp_xlabel)
fig.savefig(out_dir+expt_id+'_'+temp_out_name+'.png',dpi=300,bbox_inches='tight')
plt.clf()

# HADA outline SD values
temp_var, temp_out_name, temp_ylab='SD outline '+label, 'sd_outline_fl', 'SD outline fluorescence'
temp_iter,temp_xlabel='Condition','Condition'
fig,ax=iter_plotting(df, temp_var,temp_out_name,temp_ylab,temp_iter,temp_xlabel)
fig.savefig(out_dir+expt_id+'_'+temp_out_name+'.png',dpi=300,bbox_inches='tight')
plt.clf()

# HADA outline CV values
temp_var, temp_out_name, temp_ylab='CV outline '+label, 'cv_outline_fl', 'CV outline fluorescence'
temp_iter,temp_xlabel='Condition','Condition'
fig,ax=iter_plotting(df, temp_var,temp_out_name,temp_ylab,temp_iter,temp_xlabel,plot_points=False,showfliers=False)
plt.ylim(ymax=2.5)
fig.savefig(out_dir+expt_id+'_'+temp_out_name+'_nopoints.png',dpi=300,bbox_inches='tight')
plt.clf()
sys.stdout.close()
