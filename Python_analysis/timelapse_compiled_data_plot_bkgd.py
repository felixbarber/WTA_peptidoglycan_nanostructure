import scipy
import sys
from scipy import io
import numpy as np
import numpy.matlib
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pickle
import seaborn as sns
import pandas as pd
from numpy import matlib
import seaborn as sns
import math
import os
import scipy.optimize
import scipy.io as sio
from scipy import stats
import scipy.ndimage

##################### Experiment specifics
cutoff = None

expt_labels = ['bFB66_Tun_gr', 'bFB69_Tun_gr']
pert=r'0.5 $\mu$g/mL Tunicamycin added'
group_label = r'ponA_WT_bkgd'


linestyles = ['-.', '-', '--', '.']
# out_path='/mnt/d/Documents_D/GitHub/Rojas_lab_drafts/outputs/compiled_data/growth_rate_plots/'
# in_path='/mnt/d/Documents_D/GitHub/Rojas_lab_drafts/outputs/compiled_data/'
# out_path = '/Users/felixbarber/Documents/GitHub/Rojas_lab_drafts/outputs/compiled_data/growth_rate_plots/'
# in_path = '/Users/felixbarber/Documents/GitHub/Rojas_lab_drafts/outputs/compiled_data/'
out_path = '/Users/barber.527/Documents/GitHub/Rojas_lab_drafts/outputs/compiled_data/growth_rate_plots/'
in_path = '/Users/barber.527/Documents/GitHub/Rojas_lab_drafts/outputs/compiled_data/'

plot_labels = []
# expt_label = 'bFB7_Tun_gr'
# expt_label = 'bFB8_Tun_gr'
# expt_label = 'bFB69_Tun_gr'
# expt_label = 'bFB87_Tun_gr'
# expt_label = 'bFB93_Tun_gr'

# loading the experimental parameters
for expt_label in expt_labels:
    temp_path = in_path + expt_label + '_condition_parameters.pkl'
    with open(temp_path, 'rb') as input:
        expt_vals = pickle.load(input)
    plot_labels.append(expt_vals['Celltype'])
vars = expt_vals['vars']  # This part should be conserved across all compiled experiments
normed = ['_normed', '']
# ylabels = {'sgr_l': r'$\frac{1}{L}\frac{dL}{dt}$', 'sgr_sa': r'$\frac{1}{S}\frac{dS}{dt}$', 'width':'Width'}
ylabels = {'sgr_l': r'Growth rate $\lambda_l$', 'sgr_sa': r'Growth rate $\lambda_S$', 'width': 'Width'}
yunits = {'sgr_l': r' $(h^{-1})$', 'sgr_sa': r' ($h^{-1}$)', 'width': r' ($\mu$m)'}
sel_vars = ['sgr_l', 'width']


## Now we do some more compact plots for paper figures

sns.set(font_scale=2.0)
sns.set_style("whitegrid")
for norm in normed:
    for var in sel_vars:
        fig = plt.figure(figsize=[10, 6])
        for ind in range(len(expt_labels)):
            expt=expt_labels[ind]
            xv = np.load(in_path + expt + '_time.npy')
            if not cutoff is None:
                temp_vals = np.nonzero(xv / 60 < cutoff)[0][-1]
            else:
                temp_vals = len(xv) - 1
            xv = xv[:temp_vals]
            yv = np.load(in_path + expt + '_' + var + norm + '.npy')[:, :temp_vals]
            sgr_sa_smoothed = scipy.ndimage.gaussian_filter(np.nanmedian(yv, axis=0), sigma=1)
            err = scipy.ndimage.gaussian_filter(np.nanstd(yv, axis=0), sigma=2)
            if ind == 0:
                plt.plot(xv / 60, sgr_sa_smoothed, label=plot_labels[expt_labels.index(expt)], lw=3.0)
                plt.fill_between(xv / 60, sgr_sa_smoothed - err, sgr_sa_smoothed + err, alpha=0.4)
            else:
                plt.plot(xv / 60, sgr_sa_smoothed, label=plot_labels[expt_labels.index(expt)], lw=3.0, linestyle=linestyles[ind],color='k')
        # if norm==normed[0]:
        # plt.ylim(ymin=0.0,ymax=1.5)

        ax = plt.gca()
        plt.vlines(0, ymin=ax.get_ylim()[0], ymax=ax.get_ylim()[1], label=pert, linestyle=linestyles[0], colors='k')
        # plt.legend(loc=[1.02,0.2])
        plt.legend()
        plt.xlabel('Time (min)')
        temp_lab = ylabels[var]
        if norm == normed[0]:
            temp_lab += ' (Normalized)'
        else:
            temp_lab += yunits[var]
        plt.ylabel(temp_lab)
        plt.show()
        fig.savefig(out_path + group_label + '_' + var + norm + '_compact.png', dpi=300, bbox_inches='tight')
        plt.clf()


# Now we work with conservative plots that only include timepoints covered by all three datasets
sns.set(font_scale=0.9)
sns.set_style("ticks")
yv1s = []
colors=sns.color_palette()
with open(out_path + group_label + '.txt', 'w') as f:
    for norm in normed:
        for var in sel_vars:
            fig = plt.figure(figsize=[2.5, 2])
            for ind in range(len(expt_labels)):
                expt = expt_labels[ind]
                xv = np.load(in_path + expt + '_time_conservative.npy')
                if not cutoff is None:
                    temp_vals = np.nonzero(xv / 60 < cutoff)[0][-1]
                else:
                    temp_vals = len(xv) - 1
                xv = xv[:temp_vals]
                yv1 = np.load(in_path + expt + '_' + var + norm + '_conservative.npy')[:, :temp_vals]
                yv1s.append(yv1)

                ind1 = sel_vars.index(var)
                print('Conservative cell tracks, ', var, expt_labels.index(expt), ' :',
                      np.sum(np.sum(np.isnan(yv1s[ind]), axis=1) != yv1s[ind1].shape[1]), file=f)  # Python 3.x
                sgr_sa_smoothed = scipy.ndimage.gaussian_filter(np.nanmedian(yv1, axis=0), sigma=1)
                err = scipy.ndimage.gaussian_filter(np.nanstd(yv1, axis=0), sigma=2)
                if ind == 1:
                    plt.plot(xv / 60, sgr_sa_smoothed, label=plot_labels[expt_labels.index(expt)], lw=1.0)
                    plt.fill_between(xv / 60, sgr_sa_smoothed - err, sgr_sa_smoothed + err, alpha=0.4,color=colors[ind])
                else:
                    plt.plot(xv / 60, sgr_sa_smoothed, label=plot_labels[expt_labels.index(expt)], lw=1.0)
            # if norm==normed[0]:
            # plt.ylim(ymin=0.0,ymax=1.5)

            ax = plt.gca()
            plt.vlines(0, ymin=ax.get_ylim()[0], ymax=ax.get_ylim()[1], linestyle='-', colors='k', lw=0.5)
            plt.xlabel('Time (min)')
            temp_lab = ylabels[var]
            if norm == normed[0]:
                temp_lab += ' (norm)'
            else:
                temp_lab += yunits[var]
            plt.ylabel(temp_lab)
            plt.show()
            fig.savefig(out_path + group_label + '_' + var + norm + '_compact_conservative.pdf', bbox_inches='tight')
            plt.legend(loc=[0.49,0.68])
            plt.show()
            fig.savefig(out_path + group_label + '_' + var + norm + '_compact_conservative_legend.pdf', bbox_inches='tight')
            plt.clf()



# Now let's plot the initial growth rates and the initial widths

for var in sel_vars:
    df = pd.DataFrame(columns=['Genotype', var])
    for expt in expt_labels:
        xv = np.load(in_path + expt + '_time_conservative.npy')
        temp_vals = np.nonzero(xv < 0)[0][-1]
        xv = xv[:temp_vals]
        yv1 = np.load(in_path + expt + '_' + var + '_conservative.npy')[:, :temp_vals]
        yvs = np.nanmean(yv1, axis=1)
        yvs = yvs[~np.isnan(yvs)]

        for i0 in range(len(yvs)):
            temp_df = pd.DataFrame(columns=['Genotype', var], data=[[plot_labels[expt_labels.index(expt)], yvs[i0]]])
            df = pd.concat([df, temp_df])
    sns.set(font_scale=1.5)
    sns.set_style("whitegrid")
    fig = plt.figure(figsize=[2.5, 2])
    sns.boxplot(data=df, x='Genotype', y=var, showfliers=False)
    plt.xticks(rotation=90)
    fig.savefig(out_path + group_label + '_' + var + 'boxplot_initial.pdf', bbox_inches='tight')
    plt.clf()
    sns.set(font_scale=1.5)
    sns.set_style("whitegrid")
    fig = plt.figure(figsize=[2.5, 2])
    sns.barplot(data=df, x='Genotype', y=var, estimator=np.mean)
    plt.xticks(rotation=90)
    fig.savefig(out_path + group_label + '_' + var + 'mean_initial.pdf', bbox_inches='tight')
    plt.clf()
    sns.set(font_scale=1.5)
    sns.set_style("whitegrid")
    fig = plt.figure(figsize=[2.5, 2])
    sns.barplot(data=df, x='Genotype', y=var, estimator=np.median)
    plt.xticks(rotation=90)
    fig.savefig(out_path + group_label + '_' + var + 'med_initial.pdf', bbox_inches='tight')
    plt.clf()