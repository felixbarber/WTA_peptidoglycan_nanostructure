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
sns.set_style("whitegrid")
from skimage.morphology import disk
from skimage.morphology import erosion, dilation, opening, closing, white_tophat
import image_toolkit as imkit

expt_ids = ['/250610_bFB66_tun_EDADA', '/250612_bFB66_EDADA_tun_full', '/250613_bFB66_EDADA_tun_full','/250613_bFB66_EDADA_tun_full_rep2','/250616_bFB66_EDADA']
group_id = 'WT_EDADA_click_no_van'
label = 'AF-AF488-azide'
norm_cond = 'LB'  # Setting this here since this is the standard normalization condition
thresh=0
plotting_conds=['LB', 'Tun',"van", "Tun van", 'fos', 'untreated']
hue=None
plot_points=False

output_dir = './outputs/compiled_data/staining_plots/'
path = '/Volumes/data_ssd2/Rojas_Lab/data/'

# This assumes that cell_staining_timepoint.py has already been run
out_name=output_dir+group_id+'_public_share.pkl'
if not os.path.exists(out_name):
    print('loading data and saving for the first time')
    for ind in range(len(expt_ids)):
        temp_df1 = pd.DataFrame()
        expt_id =expt_ids[ind]
        temp_path = path + expt_id + expt_id + '_condition_parameters.pkl'
        with open(temp_path, 'rb') as input:
            expt_vals = pickle.load(input)
        data_dir = "./outputs" + expt_id
        temp_df = pd.read_pickle(data_dir + expt_id)
        temp_df['Celltype'] = expt_vals['Celltype']
        temp_df['expt'] = expt_vals['expt']
        temp_df['Date'] = expt_vals['Date']
        temp_df['Plot'] = [obj in plotting_conds for obj in temp_df.Condition]
        temp_df = temp_df[temp_df.Plot == 1]
        temp_df = temp_df[temp_df['Average outline ' + label] > thresh]  # filtering out debris that isn't fluorescent.
        temp_df['Normalized Average outline ' + label] = temp_df['Average outline ' + label] / \
                                                         temp_df[temp_df.Condition == norm_cond][
                                                             'Average outline ' + label].mean()
        # temp_df['Conditions']=expt_vals['Conditions']
        if ind == 0:
            df = pd.DataFrame(columns=temp_df.columns)
        df = df.append(temp_df)
    with open(out_name, 'wb') as output:  # Overwrites any existing file.
        pickle.dump(df, output, pickle.HIGHEST_PROTOCOL)
else:
    df = pd.read_pickle(out_name)
    print('loading pre-prepared data')


# Now we plot the results and save the figures
# These are iterable
temp_vars = ['Average outline ' + label, 'Average ' + label, 'Normalized Average outline ' + label, 'Cell spots/length']
# temp_vars=['Average outline '+label, 'Average outline '+label, 'Average '+label, 'Normalized Average outline '+label]
temp_out_names = ['av_outline_fl', 'av_area_fl', 'normed_av_outline_fl', 'cell_spots_length']
temp_ylabs = ['Fluorescence', 'Area fluorescence', 'Staining (norm)', r'Puncta/$\mu$m']


# Now we generate paper quality figures

def iter_plotting(df, temp_var, temp_out_name, temp_ylab, temp_iter, temp_xlabel, temp_hue=None, plot_points=True):
    fig = plt.figure(figsize=[2.5, 2])
    sns.set(font_scale=0.9)
    sns.set_style("whitegrid")
    ax = plt.subplot(1, 1, 1)
    if not temp_hue is None:
        plot = sns.barplot(x=temp_iter, y=temp_var, data=df, estimator=np.mean,capsize=0.4, hue=temp_hue)
    else:
        plot = sns.barplot(x=temp_iter, y=temp_var, data=df, estimator=np.mean, capsize=0.4,color=sns.color_palette()[0],
                           order=plotting_conds)
    plot.set(xlabel=temp_xlabel, ylabel=temp_ylab)
    return fig, ax

def iter_plotting_boxplot(df, temp_var, temp_out_name, temp_ylab, temp_iter, temp_xlabel, temp_hue=None, plot_points=True):
    fig = plt.figure(figsize=[2.5, 2])
    sns.set(font_scale=0.9)
    sns.set_style("white")
    ax = plt.subplot(1, 1, 1)
    if not temp_hue is None:
        plot = sns.boxplot(x=temp_iter, y=temp_var, data=df, showfliers=False, hue=temp_hue)
        if plot_points:
            temp_ymin,temp_ymax=plt.gca().get_ylim()
            plot = sns.stripplot(x=temp_iter, y=temp_var, jitter=True,dodge=True, data=df, edgecolor='black', linewidth=0.5,
                                 alpha=0.1, hue=temp_hue,label=None)
            ax.set_ylim(bottom=temp_ymin, top=temp_ymax)
    else:
        plot = sns.boxplot(x=temp_iter, y=temp_var, data=df, showfliers=False,color=sns.color_palette()[0],order=plotting_conds,linecolor='black',linewidth=1)
        # sns.stripplot(x=temp_iter, y=temp_var, data=df, color=sns.color_palette()[0],
        #                    order=plotting_conds,alpha=0.1,linewidth=1)
        # plot = sns.violinplot(x=temp_iter, y=temp_var, data=df, color=sns.color_palette()[0],
        #                    order=plotting_conds)
        # plt.yscale('log')

    plot.set(xlabel=temp_xlabel, ylabel=temp_ylab)
    return fig, ax
# # print([temp in plotting_conds for temp in df.Condition])
# print(df.Condition.unique())
# df=df[np.nonzero([temp in plotting_conds for temp in df.Condition])[0]]
print(df.head())
temp_xlabel = ''
temp_iter = 'Condition'
pval = 0.01
print('I got here')
for i0 in range(len(temp_vars)):
    temp_var, temp_out_name, temp_ylab = temp_vars[i0], temp_out_names[i0], temp_ylabs[i0]
    fig, ax = iter_plotting(df, temp_var, temp_out_name, temp_ylab, temp_iter, temp_xlabel, temp_hue=hue)
    # plt.legend(loc=[0.92,0.7])
    fig.savefig(output_dir + group_id + '_' + temp_out_name + '_barplot_compact.eps', dpi=300, bbox_inches='tight')
    fig.savefig(output_dir + group_id + '_' + temp_out_name + '_barplot_compact.png', dpi=300, bbox_inches='tight')
    plt.clf()
    print('Finished plot {0}'.format(i0))
for i0 in range(len(temp_vars)):
    temp_var, temp_out_name, temp_ylab = temp_vars[i0], temp_out_names[i0], temp_ylabs[i0]
    fig, ax = iter_plotting_boxplot(df, temp_var, temp_out_name, temp_ylab, temp_iter, temp_xlabel, temp_hue=hue,plot_points=plot_points)
    # plt.legend(loc=[0.75, 0.7])
    fig.savefig(output_dir + group_id + '_' + temp_out_name + '_boxplot_compact.pdf', dpi=300, bbox_inches='tight')
    fig.savefig(output_dir + group_id + '_' + temp_out_name + '_boxplot_compact.png', dpi=300, bbox_inches='tight')
    plt.clf()
    print('Finished plot {0}'.format(i0))



with open(output_dir + group_id + '_' + temp_out_name + '.txt', 'w') as f:
    for celltype in df.Celltype.unique():
        # print(df.groupby(['Condition', 'Date']).describe(), file=f)  # Python 3.x
        print(df.groupby(['Condition']).describe(), file=f)  # Python 3.x
        for temp_var in temp_vars:
            print('For celltype ='+celltype+', variable='+temp_var, file=f)
            temp_df=df[df.Celltype==celltype ]
            conds=list(temp_df.Condition.unique())
            for condition in conds:
                for condition1 in conds[conds.index(condition)+1:]:
                    temp_v1=temp_df[temp_df.Condition == condition][temp_var]
                    temp_v2 = temp_df[temp_df.Condition == condition1][temp_var]

                    out=scipy.stats.ttest_ind(temp_v1, temp_v2)
                    print('Conditions = ', condition, condition1, file=f)
                    print('T-test result: statistic, pvalue, df', file=f)
                    print(out, file=f)
            temp_vecs=[]
            print(conds,file=f)
            for condition in conds:
                temp_vecs.append(temp_df[temp_df.Condition==condition][temp_var])
            temp_v1=temp_vecs[0]
            temp_v2=temp_vecs[1]
            temp_v3 = temp_vecs[2]
            temp_v4 = temp_vecs[3]
            temp_v5 = temp_vecs[4]
            temp_v6 = temp_vecs[5]
            print(scipy.stats.f_oneway(*temp_vecs), file=f)
            print(scipy.stats.tukey_hsd(*temp_vecs), file=f)
            print(scipy.stats.tukey_hsd(*temp_vecs).pvalue, file=f)


# Now we make our spot plots