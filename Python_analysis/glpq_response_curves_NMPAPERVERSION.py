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

# expt_labels = ['bFB69_PBS_bufferA_500mMSorb_rec']
# group_label = 'BufferA_treatment_ponA_500mMSorb'
# perts = [r'PBS added', 'PBS removed, 500mM Sorbitol added']

# expt_labels = ['bFB66_PBS_GlpQdenat_rec']
# group_label = 'PBS_treatment'
# perts = [r'PBS+Buffer added', 'PBS+Buffer removed']

# expt_labels = ['bFB69_PBS_Buffer_rec']
# group_label = 'PBS_treatment_ponA'
# perts = [r'PBS+Buffer added', 'PBS+Buffer removed']

# expt_labels = ['bFB66_PBS_GlpQ_rec']
# group_label = 'GlpQ_treatment'
# perts = [r'PBS+GlpQ added', 'PBS+GlpQ removed']

# expt_labels = ['bFB69_PBS_GlpQ_rec']
# group_label = 'GlpQ_treatment_ponA'
# perts = [r'PBS+GlpQ added', 'PBS+GlpQ removed']

expt_labels = ['bFB69_PBS_GlpQ_500mMSorb_rec']
group_label = 'GlpQ_treatment_ponA_500mMSorb'
perts = [r'PBS+GlpQ added', 'PBS+GlpQ removed, 500mM Sorbitol added']

####

linestyles = ['-', '--', '-.', '.']

# out_path = '/Users/felixbarber/Documents/GitHub/Rojas_lab_drafts/outputs/compiled_data/growth_rate_plots/'
# in_path = '/Users/felixbarber/Documents/GitHub/Rojas_lab_drafts/outputs/compiled_data/'

out_path = '/Users/barber.527/Documents/GitHub/Rojas_lab_drafts/outputs/compiled_data/growth_rate_plots/'
in_path = '/Users/barber.527/Documents/GitHub/Rojas_lab_drafts/outputs/compiled_data/'

plot_labels = []

# loading the experimental parameters
for expt_label in expt_labels:
    temp_path = in_path + expt_label + '_condition_parameters.pkl'
    with open(temp_path, 'rb') as input:
        expt_vals = pickle.load(input)
    plot_labels.append(expt_vals['Celltype'])
vars = expt_vals['vars']  # This part should be conserved across all compiled experiments
# ylabels = {'sgr_l': r'$\frac{1}{L}\frac{dL}{dt}$', 'sgr_sa': r'$\frac{1}{S}\frac{dS}{dt}$', 'width': 'Width'}
ylabels = {'sgr_l': r'Growth rate $\lambda_l$', 'sgr_sa': r'Growth rate $\lambda_s$', 'width': 'Width'}
yunits = {'sgr_l': r' ($h^{-1}$)', 'sgr_sa': r' ($h^{-1}$)', 'width': r' ($\mu$m)'}
sel_vars = ['sgr_l']
pert_times = [expt_vals['t_pert'][0]-expt_vals['t_pert'][0], expt_vals['t_pert1'][0]-expt_vals['t_pert'][0]]

## Now we do some broad plots for talks
sns.set(font_scale=1.5)
sns.set_style("whitegrid")
for var in sel_vars:
    fig = plt.figure(figsize=[3, 3])
    for expt in expt_labels:
        xv = np.load(in_path + expt + '_time.npy')
        temp_vals = np.nonzero(xv < pert_times[1]+40)[0][-1]
        xv = xv[:temp_vals]
        yv = np.load(in_path + expt + '_' + var + '.npy')[:, :temp_vals]
        sgr_sa_smoothed = scipy.ndimage.gaussian_filter(np.nanmean(yv, axis=0),sigma=1)
        err = scipy.ndimage.gaussian_filter(np.nanstd(yv, axis=0), sigma=1)
        plt.plot(xv / 60, sgr_sa_smoothed, lw=3.0)
        plt.fill_between(xv / 60, sgr_sa_smoothed - err, sgr_sa_smoothed + err, alpha=0.4)
        ax = plt.gca()
        ax.set_xlim(xmin=-5)
    for i0 in range(len(pert_times)):
        time = pert_times[i0]
        plt.vlines(time/60, ymin=ax.get_ylim()[0], ymax=ax.get_ylim()[1], label=perts[i0], linestyle=linestyles[i0],
                   colors='k')
    # plt.legend(loc=[1.02,0.2])
    plt.legend(loc=[0.25,0.68],framealpha=1.0)
    plt.xlabel('Time (min)')
    temp_lab = ylabels[var]
    temp_lab += yunits[var]
    plt.ylabel(temp_lab)
    plt.show()
    fig.savefig(out_path + group_label + '_' + var + '_talk_lineplot.png', dpi=300, bbox_inches='tight')
    plt.clf()



sns.set(font_scale=2.0)
sns.set_style("whitegrid")
for var in sel_vars:
    fig = plt.figure(figsize=[10, 6])
    for expt in expt_labels:
        xv = np.load(in_path + expt + '_time.npy')
        if not cutoff is None:
            temp_vals = np.nonzero(xv / 60 < cutoff)[0][-1]
        else:
            temp_vals = len(xv) - 1
        xv = xv[:temp_vals]
        yv = np.load(in_path + expt + '_' + var + '.npy')[:, :temp_vals]

        for i0 in range(yv.shape[0]):
            yv1 = yv[i0, :]
            xv1 = xv[:]
            if i0 == 0:
                yv_out = yv1
                xv_out = xv1
            else:
                yv_out = np.concatenate([yv1, yv_out])
                xv_out = np.concatenate([xv1, xv_out])
        x_min,x_max,y_min,y_max=np.amin(xv_out/60), np.amax(xv_out/60),-0.5,3
        plt.xlim(left=x_min, right=x_max)
        plt.ylim(bottom=y_min, top=y_max)
        # Plotting and normalization
        hb=plt.hexbin(xv_out/60, yv_out, cmap='plasma',gridsize=60,extent=[x_min, x_max, y_min, y_max])
        xvals1=[v[0] for v in hb.get_offsets()]
        counts1=[v for v in hb.get_array()]
        counts=[]
        offsets=hb.get_offsets()
        for x in xvals1:
            counts.append(np.sum([counts1[ind] for ind in np.nonzero([temp==x for temp in xvals1])[0]]))
        hb1=plt.hexbin(offsets[:, 0], offsets[:, 1],C=hb.get_array()/np.array(counts), cmap='plasma',gridsize=60,extent=[x_min, x_max, y_min, y_max])
        # plt.plot(xv / 60, sgr_sa_smoothed, label=plot_labels[expt_labels.index(expt)], lw=3.0)
        ax = plt.gca()
    for i0 in range(len(pert_times)):
        time = pert_times[i0]
        plt.vlines(time/60, ymin=ax.get_ylim()[0], ymax=ax.get_ylim()[1], label=perts[i0], linestyle=linestyles[i0], colors='w')
    # plt.legend(loc=[1.02,0.2])
    plt.legend(loc=1)
    plt.xlabel('Time (min)')
    temp_lab = ylabels[var]
    temp_lab += yunits[var]
    plt.ylabel(temp_lab)
    plt.show()
    fig.savefig(out_path + group_label + '_' + var + '_talk_heatmap_normed.png', dpi=300, bbox_inches='tight')
    plt.clf()


## Now we do some compact plots for paper figures

sns.set(font_scale=0.8)
sns.set_style("whitegrid")
num_hex=15
for var in sel_vars:
    fig = plt.figure(figsize=[2.5, 2])
    for expt in expt_labels:
        xv = np.load(in_path + expt + '_time.npy')
        if not cutoff is None:
            temp_vals = np.nonzero(xv / 60 < cutoff)[0][-1]
        else:
            temp_vals = len(xv) - 1
        xv = xv[:temp_vals]
        yv = np.load(in_path + expt + '_' + var + '.npy')[:, :temp_vals]

        for i0 in range(yv.shape[0]):
            yv1 = yv[i0, :]
            xv1 = xv[:]
            if i0 == 0:
                yv_out = yv1
                xv_out = xv1
            else:
                yv_out = np.concatenate([yv1, yv_out])
                xv_out = np.concatenate([xv1, xv_out])
        x_min,x_max,y_min,y_max=np.amin(xv_out/60), np.amax(xv_out/60),-0.5,3
        plt.xlim(left=x_min, right=x_max)
        plt.ylim(bottom=y_min, top=y_max)
        # plt.hexbin(xv_out/60, yv_out, cmap='BuPu',gridsize=[int(np.sqrt(3))*num_hex,num_hex],extent=[x_min, x_max, y_min, y_max])
        ############
        hb=plt.hexbin(xv_out / 60, yv_out, cmap='plasma', gridsize=num_hex,
                   extent=[x_min, x_max, y_min, y_max])
        # plt.plot(xv / 60, sgr_sa_smoothed, label=plot_labels[expt_labels.index(expt)], lw=3.0)
        ax = plt.gca()
    for i0 in range(len(pert_times)):
        time = pert_times[i0]
        plt.vlines(time/60, ymin=ax.get_ylim()[0], ymax=ax.get_ylim()[1], label=perts[i0], linestyle=linestyles[i0], colors='w')
    # plt.legend(loc=[1.02,0.2])
    # plt.legend(loc=1)
    plt.xlabel('Time (min)')

    temp_lab = ylabels[var]
    temp_lab += yunits[var]
    plt.ylabel(temp_lab)
    plt.tight_layout()
    plt.show()
    fig.savefig(out_path + group_label + '_' + var + '_compact_heatmap.png', dpi=300, bbox_inches='tight')
    fig.savefig(out_path + group_label + '_' + var + '_compact_heatmap.pdf', bbox_inches='tight')
    plt.clf()

sns.set(font_scale=0.8)
sns.set_style("whitegrid")
num_hex=15
for var in sel_vars:
    fig = plt.figure(figsize=[2.5, 2])
    for expt in expt_labels:
        xv = np.load(in_path + expt + '_time.npy')
        if not cutoff is None:
            temp_vals = np.nonzero(xv / 60 < cutoff)[0][-1]
        else:
            temp_vals = len(xv) - 1
        xv = xv[:temp_vals]
        yv = np.load(in_path + expt + '_' + var + '.npy')[:, :temp_vals]

        for i0 in range(yv.shape[0]):
            yv1 = yv[i0, :]
            xv1 = xv[:]
            if i0 == 0:
                yv_out = yv1
                xv_out = xv1
            else:
                yv_out = np.concatenate([yv1, yv_out])
                xv_out = np.concatenate([xv1, xv_out])
        x_min,x_max,y_min,y_max=np.amin(xv_out/60), np.amax(xv_out/60),-0.5,3
        plt.xlim(left=x_min, right=x_max)
        plt.ylim(bottom=y_min, top=y_max)
        # plt.hexbin(xv_out/60, yv_out, cmap='BuPu',gridsize=[int(np.sqrt(3))*num_hex,num_hex],extent=[x_min, x_max, y_min, y_max])
        ############
        hb=plt.hexbin(xv_out / 60, yv_out, cmap='plasma', gridsize=num_hex,
                   extent=[x_min, x_max, y_min, y_max]) # previously cmap='BuPu'

        # plotting and normalization
        xvals1 = [v[0] for v in hb.get_offsets()]
        counts1 = [v for v in hb.get_array()]
        counts = []
        offsets = hb.get_offsets()
        for x in xvals1:
            counts.append(np.sum([counts1[ind] for ind in np.nonzero([temp == x for temp in xvals1])[0]]))
        hb1 = plt.hexbin(offsets[:, 0], offsets[:, 1], C=hb.get_array() / np.array(counts), cmap='plasma',
                         gridsize=num_hex, extent=[x_min, x_max, y_min, y_max])
        # plt.plot(xv / 60, sgr_sa_smoothed, label=plot_labels[expt_labels.index(expt)], lw=3.0)
        ax = plt.gca()
    for i0 in range(len(pert_times)):
        time = pert_times[i0]
        plt.vlines(time/60, ymin=ax.get_ylim()[0], ymax=ax.get_ylim()[1], label=perts[i0], linestyle=linestyles[i0], colors='w')
    # plt.legend(loc=[1.02,0.2])
    # plt.legend(loc=1)
    plt.xlabel('Time (min)')

    temp_lab = ylabels[var]
    temp_lab += yunits[var]
    plt.ylabel(temp_lab)
    plt.tight_layout()
    plt.show()
    fig.savefig(out_path + group_label + '_' + var + '_compact_heatmap_normed.png', dpi=300, bbox_inches='tight')
    fig.savefig(out_path + group_label + '_' + var + '_compact_heatmap_normed.pdf', bbox_inches='tight')
    plt.clf()


# Plotting a hexbin version of specific cell growth rates
#
# xv=time
# fig=plt.figure(figsize=[8,5])
# yv_out = np.array([])
# for i0 in range(sgr.shape[0]):
#     yv=sgr[i0,:]
#     xv1 = xv[:]
#     if i0 ==0:
#         yv_out=yv
#         xv_out=xv1
#     else:
#         yv_out=np.concatenate([yv,yv_out])
#         xv_out = np.concatenate([xv1, xv_out])
# plt.xlim(left=0.0,right=np.amax(xv_out))
# plt.hexbin(xv_out,yv_out,cmap ='plasma')
# yv=scipy.ndimage.gaussian_filter(np.nanmedian(sgr,axis=0),sigma=1)
# plt.plot(xv,yv,label= 'Smoothed median',color='g',lw=3.0)
# # plt.ylim(ymin=np.nanmedian(sgrmed)-4*np.nanmedian(sgrstd),ymax=np.nanmedian(sgrmed)+6*np.nanmedian(sgrstd))
# ax=plt.gca()
# for i0 in range(len(t_pert)):
#     plt.vlines(t_pert[i0],ymin=ax.get_ylim()[0],ymax=ax.get_ylim()[1],label=labels[i0],linestyle=linestyles[i0],color='y')
# plt.legend(loc=[0.5,0.6])
# plt.xlabel('Time (s)')
# plt.ylabel(r'$\frac{1}{l}\frac{dl}{dt}$ ($s^{-1}$)')
# fig.savefig('./outputs/'+expt_id+expt_id+'_sgr_hexbin.png',bbox_inches='tight',dpi=150)
# plt.clf()



# now we look at the initial and final growth rates, to see if there's a significant difference.
for var in sel_vars:
    for expt in expt_labels:
        xv = np.load(in_path + expt + '_time.npy')
        if not cutoff is None:
            temp_vals = np.nonzero(xv / 60 < cutoff)[0][-1]
        else:
            temp_vals = len(xv) - 1
        xv = xv[:temp_vals]
        yv = np.load(in_path + expt + '_' + var + '.npy')[:, :temp_vals]

    init_cutoff = np.nonzero(xv<pert_times[0])[0][-1]
    print(len(xv), init_cutoff, pert_times[0]/60.0)
    init_grs=np.nanmean(yv[:,:init_cutoff],axis=1)
    init_grs=init_grs[np.nonzero(~np.isnan(init_grs))]
    final_cutoff = np.nonzero(xv<pert_times[-1]+10.0)[0][-1] # Wait 10 mins after re-adding LB to confirm which cells
    # recover
    print(final_cutoff, pert_times[-1]//60.0)
    final_grs=np.nanmean(yv[:,final_cutoff:],axis=1)
    final_grs = final_grs[np.nonzero(~np.isnan(final_grs))]
    out_val=scipy.stats.ttest_ind(init_grs, final_grs, equal_var=False)
    with open(out_path + group_label + '.txt', 'w') as f:
        print('Cell number:', yv.shape[0], file=f)  # Python 3.x
        print('Data shape (samples x timepoints)', yv.shape, file=f)
        print('T-test outputs', out_val, file=f)
        cutoff_gr=np.mean(init_grs)*0.5
        print('Percentage of cells that recover to 0.5x the initial growth rate:. ',100.0*np.mean(final_grs>cutoff_gr), file=f)
        print('SEM for percentage of cells that recover to 0.5x the initial growth rate:. ',
              100.0*np.std(final_grs > cutoff_gr)/np.sqrt(len(final_grs)), file=f)

    cols=['Time', r'Growth Rate $\lambda_l$ ($h^{-1}$)']
    grs=pd.DataFrame(columns=cols)
    for item in init_grs:
        temp_grs=pd.DataFrame(columns=cols,data=[['Initial', item]])
        grs=pd.concat([grs,temp_grs])
    for item in final_grs:
        temp_grs = pd.DataFrame(columns=cols, data=[['Final', item]])
        grs = pd.concat([grs, temp_grs])
    #
    # av_grs=[np.nanmean(arr) for arr in temp_grs]
    # sd_grs=[np.nanstd(arr)/np.sqrt(np.sum(np.nonzero(~np.isnan(arr)))) for arr in temp_grs]
    # print([[np.sum(np.nonzero(~np.isnan(arr))),len(arr)] for arr in temp_grs])
    sns.set(font_scale=0.8)
    sns.set_style("whitegrid")
    fig = plt.figure(figsize=[1.5, 2.0])
    col = sns.color_palette()[0]
    sns.barplot(data=grs,x='Time', y=r'Growth Rate $\lambda_l$ ($h^{-1}$)',estimator=np.mean,color=col,capsize=0.4,edgecolor="black",errcolor="black")
    plt.tight_layout()
    plt.show()
    fig.savefig(out_path + group_label + '_' + var + '_compact_barplot.png', dpi=300, bbox_inches='tight')
    fig.savefig(out_path + group_label + '_' + var + '_compact_barplot.pdf', bbox_inches='tight')

