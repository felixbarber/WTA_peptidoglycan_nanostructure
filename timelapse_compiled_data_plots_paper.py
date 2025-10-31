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
cutoff=None
plot_pert=True

# expt_labels = ['bFB66_s750_tun']
# group_label = 'WT_s750_tun'
# pert = 'Tunicamycin added'
# plot_labels=['WT']
# legend_loc=[1.02,0.2]
# # plot_pert=False

# expt_labels = ['bFB66_long_time_LB']
# group_label = 'WT_LB_long_times'
# pert = ''
# plot_labels=['WT']
# legend_loc=[1.02,0.2]
# plot_pert=False

# expt_labels = ['bFB291_IPTG_induction','bFB293_IPTG_induction','bFB295_IPTG_induction']
# group_label = 'ponA_induction'
# pert = '1mM IPTG added'
# plot_labels=[r'$P_{spac}-ponA$', r'$P_{spac}-ponA$ $\Delta lytE$', r'$P_{spac}-ponA$ $\Delta cwlO$']
# legend_loc=[1.02,0.2]

# legend_loc=[0.25,0.0]

# expt_labels = ['bFB66_PBS_GlpQ_rec', 'bFB66_PBS_GlpQdenat_rec']
# group_label = 'GlpQ_WT_comp'
# pert = 'GlpQ added'
# plot_labels=['GlpQ', 'Buffer']

# expt_labels = ['bFB69_PBS_GlpQ_rec', 'bFB69_PBS_Buffer_rec']
# group_label = 'GlpQ_ponA_comp'
# pert = 'GlpQ added'
# plot_labels=['GlpQ', 'Buffer']

# expt_labels = ['bFB66_PBS_GlpQdenat_rec', 'bFB66_30minPBS_rec_only', 'bFB69_PBS_Buffer_rec']
# group_label = 'PBS_treatment_variables'
# pert = 'PBS added'
# plot_labels=['15min WT', '30min WT', r'15min $\Delta ponA$ ']

# expt_labels = ['bFB66_Tun_gr','bFB7_Tun_gr','bFB8_Tun_gr']
# group_label = 'WT_cwlO_lytE'
# pert = 'Tunicamycin added'
# plot_labels=['WT', r'$\Delta cwlO$', r'$\Delta lytE$']

linestyles = ['-', '-.', '--', '.']
# out_path='/mnt/d/Documents_D/GitHub/Rojas_lab_drafts/outputs/compiled_data/growth_rate_plots/'
# in_path='/mnt/d/Documents_D/GitHub/Rojas_lab_drafts/outputs/compiled_data/'
out_path = '/Users/felixbarber/Documents/GitHub/Rojas_lab_drafts/outputs/compiled_data/growth_rate_plots/'
in_path = '/Users/felixbarber/Documents/GitHub/Rojas_lab_drafts/outputs/compiled_data/'
# plot_labels = []
# expt_label = 'bFB7_Tun_gr'
# expt_label = 'bFB8_Tun_gr'
# expt_label = 'bFB69_Tun_gr'
# expt_label = 'bFB87_Tun_gr'
# expt_label = 'bFB93_Tun_gr'

# loading the experimental parameters
expt_vals=[]
for expt_label in expt_labels:
    temp_path = in_path+expt_label+'_condition_parameters.pkl'
    with open(temp_path, 'rb') as input:
        expt_vals.append(pickle.load(input))
    # plot_labels.append(expt_vals[-1]['Celltype'])
vars = expt_vals[-1]['vars'] # This part should be conserved across all compiled experiments
normed = ['_normed', '']
# ylabels = {'sgr_l': r'$\frac{1}{L}\frac{dL}{dt}$', 'sgr_sa': r'$\frac{1}{S}\frac{dS}{dt}$', 'width':'Width'}
ylabels = {'sgr_l': r'Growth rate $\lambda_l$', 'sgr_sa': r'Growth rate $\lambda_S$', 'width':'Width'}
abbrev_ylabels = {'sgr_l': r'$\lambda_l$', 'sgr_sa': r'$\lambda_S$', 'width':'Width'}
yunits = {'sgr_l': r' $(h^{-1})$', 'sgr_sa': r' ($h^{-1}$)', 'width':r' ($\mu$m)'}
sel_vars=['sgr_l', 'width']


# print(cutoff is None)
sns.set(font_scale=1.5)
sns.set_style("whitegrid")
for norm in normed:
    for var in vars:
        fig=plt.figure(figsize=[10,6])
        for expt_ind in range(len(expt_labels)):
            expt=expt_labels[expt_ind]
            xv=np.load(in_path+expt+'_time.npy')
            if not cutoff is None:
                temp_vals = np.nonzero(xv/60<cutoff)[0][-1]
            else:
                temp_vals = len(xv)-1
            # print(temp_vals)
            # xv=xv[:temp_vals] - expt_vals[expt_ind]['t_pert'][-1]
            xv = xv[:temp_vals]
            yv=np.load(in_path+expt+'_'+var+norm+'.npy')[:,:temp_vals]
            sgr_sa_smoothed=scipy.ndimage.gaussian_filter(np.nanmedian(yv,axis=0),sigma=1)
            err=scipy.ndimage.gaussian_filter(np.nanstd(yv,axis=0),sigma=2)
            plt.plot(xv/60,sgr_sa_smoothed,label=plot_labels[expt_labels.index(expt)],lw=3.0)
            plt.fill_between(xv/60,sgr_sa_smoothed-err,sgr_sa_smoothed+err,alpha=0.4)
        # if norm==normed[0]:
            # plt.ylim(ymin=0.0,ymax=1.5)
        
        ax=plt.gca()
        if plot_pert:
            plt.vlines(0,ymin=ax.get_ylim()[0],ymax=ax.get_ylim()[1],label=pert,linestyle=linestyles[0],colors='k')
        # plt.legend(loc=[1.02,0.2])
        plt.legend()
        plt.xlabel('Time (min)')
        temp_lab = ylabels[var]
        if norm==normed[0]:
            temp_lab+=' (Normalized)'
        else:
            temp_lab+=yunits[var]
        plt.ylabel(temp_lab)
        plt.show()
        fig.savefig(out_path+group_label+ '_'+var+norm+'.png',dpi=300, bbox_inches='tight')
        plt.clf()


## Now we do some more compact plots for paper figures

sns.set(font_scale=2.0)
sns.set_style("white")
for norm in normed:
    for var in sel_vars:
        fig = plt.figure(figsize=[10, 6])
        for expt in expt_labels:
            xv = np.load(in_path + expt + '_time.npy')
            if not cutoff is None:
                temp_vals = np.nonzero(xv/60<cutoff)[0][-1]
            else:
                temp_vals = len(xv)-1
            # xv=xv[:temp_vals] - expt_vals[expt_ind]['t_pert'][-1]
            xv = xv[:temp_vals]
            yv = np.load(in_path + expt + '_' + var + norm + '.npy')[:,:temp_vals]
            sgr_sa_smoothed = scipy.ndimage.gaussian_filter(np.nanmedian(yv, axis=0), sigma=1)
            err = scipy.ndimage.gaussian_filter(np.nanstd(yv, axis=0), sigma=2)
            plt.plot(xv / 60, sgr_sa_smoothed, label=plot_labels[expt_labels.index(expt)], lw=3.0)
            plt.fill_between(xv / 60, sgr_sa_smoothed - err, sgr_sa_smoothed + err, alpha=0.4)
        # if norm==normed[0]:
        # plt.ylim(ymin=0.0,ymax=1.5)

        ax = plt.gca()
        if plot_pert:
            plt.vlines(0, ymin=ax.get_ylim()[0], ymax=ax.get_ylim()[1], label=pert, linestyle=linestyles[0], colors='k')
        # plt.legend(loc=[1.02,0.2])
        plt.legend(loc=legend_loc)
        plt.xlabel('Time (min)')
        temp_lab = ylabels[var]
        if norm == normed[0]:
            temp_lab += ' (Normalized)'
        else:
            temp_lab += yunits[var]
        plt.ylabel(temp_lab)
        plt.show()
        fig.savefig(out_path + group_label + '_' + var + norm + '_compact.png', dpi=300, bbox_inches='tight')
        plt.legend(loc=[1.02,0.2])
        fig.savefig(out_path + group_label + '_' + var + norm + '_compact_legend.png', dpi=300, bbox_inches='tight')
        plt.clf()


# Paper-style figures.
sns.set(font_scale=0.9)
sns.set_style("white")
for norm in normed:
    for var in sel_vars:
        fig = plt.figure(figsize=[2.5, 2])
        for expt in expt_labels:
            xv = np.load(in_path + expt + '_time.npy')
            if not cutoff is None:
                temp_vals = np.nonzero(xv/60<cutoff)[0][-1]
            else:
                temp_vals = len(xv)-1
            # xv=xv[:temp_vals] - expt_vals[expt_ind]['t_pert'][-1]
            xv = xv[:temp_vals]
            yv = np.load(in_path + expt + '_' + var + norm + '.npy')[:,:temp_vals]
            sgr_sa_smoothed = scipy.ndimage.gaussian_filter(np.nanmedian(yv, axis=0), sigma=1)
            err = scipy.ndimage.gaussian_filter(np.nanstd(yv, axis=0), sigma=2)
            plt.plot(xv / 60, sgr_sa_smoothed, label=plot_labels[expt_labels.index(expt)], lw=0.5)
            plt.fill_between(xv / 60, sgr_sa_smoothed - err, sgr_sa_smoothed + err, alpha=0.4)
        # if norm==normed[0]:
        # plt.ylim(ymin=0.0,ymax=1.5)

        ax = plt.gca()
        if plot_pert:
            plt.vlines(0, ymin=ax.get_ylim()[0], ymax=ax.get_ylim()[1], linestyle=linestyles[0], colors='k',lw=0.5)
        # plt.legend(loc=[1.02,0.2])
        # plt.legend()
        plt.xlabel('Time (min)')
        temp_lab = ylabels[var]
        if norm == normed[0]:
            temp_lab += ' (Normalized)'
        else:
            temp_lab += yunits[var]
        plt.ylabel(temp_lab)
        plt.show()
        fig.savefig(out_path + group_label + '_' + var + norm + '_compact.pdf', bbox_inches='tight')
        plt.legend(loc=legend_loc)
        fig.savefig(out_path + group_label + '_' + var + norm + '_compact_legend.pdf', dpi=300, bbox_inches='tight')
        plt.clf()

# Paper-style figures.
sns.set(font_scale=1.0)
sns.set_style("whitegrid")
cutoff=50
for norm in normed:
    for var in sel_vars:
        fig = plt.figure(figsize=[2.5, 2])
        for expt in expt_labels:
            xv = np.load(in_path + expt + '_time.npy')
            if not cutoff is None:
                temp_vals = np.nonzero((xv-expt_vals[expt_labels.index(expt)]['t_pert1'][0]+\
                 expt_vals[expt_labels.index(expt)]['t_pert'][0])/60<cutoff)[0][-1]
            else:
                temp_vals = len(xv)-1
            # xv=xv[:temp_vals] - expt_vals[expt_ind]['t_pert'][-1]
            # print(xv/60, expt_vals[expt_labels.index(expt)]['t_pert'][0], expt_vals[expt_labels.index(expt)]['t_pert1'][0])
            xv = (xv[:temp_vals]-expt_vals[expt_labels.index(expt)]['t_pert1'][0]+\
                 expt_vals[expt_labels.index(expt)]['t_pert'][0])/60.0
            yv = np.load(in_path + expt + '_' + var + norm + '.npy')[:,:temp_vals]
            # sgr_sa_smoothed = scipy.ndimage.gaussian_filter(np.nanmean(yv, axis=0), sigma=1)
            # err = scipy.ndimage.gaussian_filter(np.nanstd(yv, axis=0)/np.sqrt(np.nansum(np.isnan(yv)==0,axis=0)), sigma=2)
            sgr_sa_smoothed = np.nanmean(yv, axis=0)
            err = np.nanstd(yv, axis=0) / np.sqrt(np.nansum(np.isnan(yv) == 0, axis=0))
            plt.plot(xv , sgr_sa_smoothed, label=plot_labels[expt_labels.index(expt)], lw=1)
            plt.fill_between(xv, sgr_sa_smoothed - err, sgr_sa_smoothed + err, alpha=0.4, lw=0.0)
        # if norm==normed[0]:
        # plt.ylim(ymin=0.0,ymax=1.5)

        ax = plt.gca()
        if plot_pert:
            plt.vlines(0, ymin=ax.get_ylim()[0], ymax=ax.get_ylim()[1], linestyle=linestyles[2], colors='k',lw=2.0)
        plt.xlim(xmin=-5)
        plt.legend(loc=[1.02,0.2])
        # plt.legend(loc=legend_loc)
        plt.xlabel('Time (min)')
        temp_lab = ylabels[var]
        if norm == normed[0]:
            temp_lab += ' (Normalized)'
        else:
            temp_lab += yunits[var]
        plt.ylabel(temp_lab)
        plt.show()
        fig.savefig(out_path + group_label + '_' + var + norm + '_compact_sem.pdf', bbox_inches='tight')
        fig.savefig(out_path + group_label + '_' + var + norm + '_compact_sem.png', bbox_inches='tight')
        plt.clf()

# now we look at the initial and final growth rates, to see if there's a significant difference.
with open(out_path + group_label+'.txt', 'w') as f:
    for norm in normed:
        for var in sel_vars:
            cols = ['Time', r'Growth Rate $\lambda_l$ ($h^{-1}$)', 'Condition']
            grs = pd.DataFrame(columns=cols)
            for expt in expt_labels:
                xv = np.load(in_path + expt + '_time.npy')
                if not cutoff is None:
                    temp_vals = np.nonzero((xv - expt_vals[expt_labels.index(expt)]['t_pert1'][0] + \
                                            expt_vals[expt_labels.index(expt)]['t_pert'][0]) / 60 < cutoff)[0][-1]
                else:
                    temp_vals = len(xv) - 1
                xv = xv[:temp_vals]
                yv = np.load(in_path + expt + '_' + var + norm + '.npy')[:,:temp_vals]
                init_cutoff = np.nonzero(xv<0)[0][-1]
                init_grs=np.nanmean(yv[:,:init_cutoff],axis=1)
                init_grs=init_grs[np.nonzero(~np.isnan(init_grs))]
                final_grs=np.nanmean(yv[:,-init_cutoff:],axis=1)
                final_grs = final_grs[np.nonzero(~np.isnan(final_grs))]
                out_val=scipy.stats.ttest_ind(init_grs, final_grs, equal_var=False)

                print('Cell type:', plot_labels[expt_labels.index(expt)], file=f)
                print('Cell number:', yv.shape[0], file=f)  # Python 3.x
                print('Data shape (samples x timepoints)', yv.shape, file=f)
                print('T-test outputs', out_val, file=f)
                for item in init_grs:
                    temp_grs=pd.DataFrame(columns=cols,data=[['Initial', item, plot_labels[expt_labels.index(expt)]]])
                    grs=pd.concat([grs,temp_grs])
                for item in final_grs:
                    temp_grs = pd.DataFrame(columns=cols, data=[['Final', item, plot_labels[expt_labels.index(expt)]]])
                    grs = pd.concat([grs, temp_grs])
            #
            # av_grs=[np.nanmean(arr) for arr in temp_grs]
            # sd_grs=[np.nanstd(arr)/np.sqrt(np.sum(np.nonzero(~np.isnan(arr)))) for arr in temp_grs]
            # print([[np.sum(np.nonzero(~np.isnan(arr))),len(arr)] for arr in temp_grs])
            sns.set(font_scale=0.8)
            sns.set_style("whitegrid")
            fig = plt.figure(figsize=[3.0, 2.0])
            col = sns.color_palette()[0]
            sns.barplot(data=grs,x='Condition', y=r'Growth Rate $\lambda_l$ ($h^{-1}$)',estimator=np.mean,color=col,capsize=0.3,
                        edgecolor="black",errcolor="black",hue='Time')
            plt.tight_layout()
            plt.show()
            fig.savefig(out_path + group_label + '_' + var +norm+ '_compact_barplot.png', dpi=300, bbox_inches='tight')
            fig.savefig(out_path + group_label + '_' + var +norm+ '_compact_barplot.pdf', bbox_inches='tight')

    # inset Paper-style figures.
    sns.set(font_scale=1.0)
    sns.set_style("whitegrid")
    cutoff=50
    for norm in normed:
        for var in sel_vars:
            fig = plt.figure(figsize=[1.0, 1.0])
            for expt in expt_labels:
                xv = np.load(in_path + expt + '_time.npy')
                if not cutoff is None:
                    temp_vals = np.nonzero(xv/60<cutoff)[0][-1]
                else:
                    temp_vals = len(xv)-1
                # xv=xv[:temp_vals] - expt_vals[expt_ind]['t_pert'][-1]
                xv = xv[:temp_vals]
                yv = np.load(in_path + expt + '_' + var + norm + '.npy')[:,:temp_vals]
                # sgr_sa_smoothed = scipy.ndimage.gaussian_filter(np.nanmean(yv, axis=0), sigma=1)
                # err = scipy.ndimage.gaussian_filter(np.nanstd(yv, axis=0)/np.sqrt(np.nansum(np.isnan(yv)==0,axis=0)), sigma=2)
                sgr_sa_smoothed = np.nanmean(yv, axis=0)
                err = np.nanstd(yv, axis=0) / np.sqrt(np.nansum(np.isnan(yv) == 0, axis=0))
                plt.plot(xv / 60, sgr_sa_smoothed, label=plot_labels[expt_labels.index(expt)], lw=1)
                plt.fill_between(xv / 60, sgr_sa_smoothed - err, sgr_sa_smoothed + err, alpha=0.4, lw=0.0)
            # if norm==normed[0]:
            # plt.ylim(ymin=0.0,ymax=1.5)

            ax = plt.gca()
            plt.vlines(0, ymin=ax.get_ylim()[0], ymax=ax.get_ylim()[1], linestyle=linestyles[2], colors='k',lw=2.0)
            plt.xlim(xmin=-5)
            # plt.legend(loc=[1.02,0.2])
            # plt.legend(loc=4)
            # plt.xlabel('Time (min)')
            temp_lab = abbrev_ylabels[var]
            if norm == normed[0]:
                temp_lab += ' (Normalized)'
            else:
                temp_lab += yunits[var]
            # plt.ylabel(temp_lab)
            plt.show()
            fig.savefig(out_path + group_label + '_' + var + norm + '_compact_sem_inset.pdf', bbox_inches='tight')
            plt.clf()


    # Abbreviated paper-style figures.
    cutoff=50
    sns.set(font_scale=0.9)
    sns.set_style("whitegrid")
    yvs=[]
    for norm in normed:
        for var in sel_vars:
            fig = plt.figure(figsize=[2.5,2])
            for expt in expt_labels:
                xv = np.load(in_path + expt + '_time.npy')
                if not cutoff is None:
                    temp_vals = np.nonzero(xv/60<cutoff)[0][-1]
                else:
                    temp_vals = len(xv)-1
                # xv=xv[:temp_vals] - expt_vals[expt_ind]['t_pert'][-1]
                xv = xv[:temp_vals]
                yv = np.load(in_path + expt + '_' + var + norm + '.npy')[:,:temp_vals]
                yvs.append(yv)
                sgr_sa_smoothed = scipy.ndimage.gaussian_filter(np.nanmedian(yv, axis=0), sigma=1)
                err = scipy.ndimage.gaussian_filter(np.nanstd(yv, axis=0), sigma=2)
                plt.plot(xv / 60, sgr_sa_smoothed, label=plot_labels[expt_labels.index(expt)], lw=0.5)
                plt.fill_between(xv / 60, sgr_sa_smoothed - err, sgr_sa_smoothed + err, alpha=0.4)
            # if norm==normed[0]:
            # plt.ylim(ymin=0.0,ymax=1.5)

            ax = plt.gca()
            if plot_pert:
                plt.vlines(0, ymin=ax.get_ylim()[0], ymax=ax.get_ylim()[1], linestyle=linestyles[0], colors='k',lw=0.5)
            # plt.legend(loc=[1.02,0.2])
            # plt.legend()
            plt.xlabel('Time (min)')
            temp_lab = ylabels[var]
            if norm == normed[0]:
                temp_lab += ' (Normalized)'
            else:
                temp_lab += yunits[var]
            plt.ylabel(temp_lab)
            plt.show()
            fig.savefig(out_path + group_label + '_' + var + norm + '_compact_abbreviated.pdf', bbox_inches='tight')
            plt.clf()

    # Now we work with conservative plots that only include timepoints covered by all three datasets
    sns.set(font_scale=0.9)
    sns.set_style("whitegrid")
    yv1s=[]
    for norm in normed:
        for var in sel_vars:
            fig = plt.figure(figsize=[2.5, 2])
            for expt in expt_labels:
                xv = np.load(in_path + expt + '_time_conservative.npy')
                if not cutoff is None:
                    temp_vals = np.nonzero(xv/60<cutoff)[0][-1]
                else:
                    temp_vals = len(xv)-1
                # xv=xv[:temp_vals] - expt_vals[expt_ind]['t_pert'][-1]
                xv = xv[:temp_vals]
                yv1 = np.load(in_path + expt + '_' + var + norm + '_conservative.npy')[:,:temp_vals]
                yv1s.append(yv1)
                sgr_sa_smoothed = scipy.ndimage.gaussian_filter(np.nanmedian(yv1, axis=0), sigma=1)
                err = scipy.ndimage.gaussian_filter(np.nanstd(yv1, axis=0), sigma=2)
                plt.plot(xv / 60, sgr_sa_smoothed, label=plot_labels[expt_labels.index(expt)], lw=0.5)
                plt.fill_between(xv / 60, sgr_sa_smoothed - err, sgr_sa_smoothed + err, alpha=0.4)
            # if norm==normed[0]:
            # plt.ylim(ymin=0.0,ymax=1.5)

            ax = plt.gca()
            if plot_pert:
                plt.vlines(0, ymin=ax.get_ylim()[0], ymax=ax.get_ylim()[1], linestyle=linestyles[0], colors='k',lw=0.5)
            # plt.legend(loc=[1.02,0.2])
            plt.legend(loc=legend_loc)
            plt.xlabel('Time (min)')
            temp_lab = ylabels[var]
            if norm == normed[0]:
                temp_lab += ' (Normalized)'
            else:
                temp_lab += yunits[var]
            plt.ylabel(temp_lab)
            plt.show()
            fig.savefig(out_path + group_label + '_' + var + norm + '_compact_conservative.pdf', bbox_inches='tight')
            plt.clf()


    for var in sel_vars:
        ind=sel_vars.index(var)
        print('Generous cell tracks, ', var, ' :', np.sum(np.sum(np.isnan(yvs[ind]),axis=1)!=yvs[ind].shape[1]),
              file=f)  # Python 3.x
        print('Conservative cell tracks, ', var, ' :', np.sum(np.sum(np.isnan(yv1s[ind]),axis=1)!=yv1s[ind].shape[1]),
              file=f)  # Python 3.x