import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from scipy.stats import ttest_ind



path='/Users/felixbarber/Documents/Rojas_Lab/data/'
expt_id='/240606_conA_Tun'
out_path=path+expt_id+'/df_appended'
df=pd.read_pickle(out_path)

df_wt_means={}
for day in df.Date.unique():
    temp=(df.Date==day)*(df.Strain=='WT')*(df.Condition=='Buffer A')
    df_wt_means[day]=df[temp]['R2-A'].mean()

normed_R2=np.zeros(len(df))
for temp_ind in df.index:
    temp_out=df.loc[temp_ind]
#     temp=(df.Date==temp_out.Date)*(df.Strain=='WT')*(df.Condition=='Buffer A')
    normed_R2[temp_ind]=temp_out['R2-A']/df_wt_means[temp_out.Date]
df['R2-A normed']=normed_R2
df['Cond']=df['Strain'] +', '+ df['Condition'] + ''

ax=sns.displot(data=df[(df['R2-A normed']>0)*(df['R2-A normed']<30)],x='R2-A normed', hue='Cond', hue_order=['$\Delta tagO$, Buffer A','$\Delta tagO$, GlpQ', '$\\Delta tagE$, Buffer A'] ,log_scale=True)
fig=ax.figure
fig.savefig('./outputs/compiled_data/staining_plots/conA_tagO_dists.png',dpi=300,bbox_inches='tight')
plt.show()
plt.clf()

ax=sns.displot(data=df[df['R2-A']>0],x='R2-A normed', hue='Cond', hue_order=['WT, Buffer A','WT, GlpQ', '$\\Delta tagE$, Buffer A'] ,log_scale=True)
fig=ax.figure
fig.savefig('./outputs/compiled_data/staining_plots/conA_WT_dists.png',dpi=300,bbox_inches='tight')
plt.show()
plt.clf()

plt.tight_layout()
sns.set(font_scale=2.0)

sns.set_style('whitegrid')
col = sns.color_palette()[0]
fig=plt.figure()
order=['WT, Buffer A','WT, GlpQ', '$\\Delta tagO$, Buffer A', '$\\Delta tagO$, GlpQ', '$\\Delta tagE$, Buffer A']
sns.barplot(data=df,x='Cond',y='R2-A normed', order=order, estimator='mean', color=col,capsize=0.3,
            edgecolor="black", errcolor="black")
plt.xticks(rotation=90)
plt.ylabel('Mean ConA stain (norm)')
plt.xlabel('Condition')
fig.savefig('./outputs/compiled_data/staining_plots/conA_compilation_mean_no_tun.png', dpi=300,bbox_inches='tight')
fig.savefig('./outputs/compiled_data/staining_plots/conA_compilation_mean_no_tun.eps',bbox_inches='tight')
plt.show()
plt.clf()

fig=plt.figure()
order=['WT, Buffer A','WT, GlpQ','$\\Delta tagO$, Buffer A', '$\\Delta tagO$, GlpQ', '$\\Delta tagE$, Buffer A']
sns.barplot(data=df,x='Cond',y='R2-A normed', order=order, estimator='median', color=col,capsize=0.3,
            edgecolor="black", errcolor="black")
plt.xticks(rotation=90)
plt.ylabel('Median ConA stain (norm)')
plt.xlabel('Condition')
fig.savefig('./outputs/compiled_data/staining_plots/conA_compilation_med_no_tun.png', dpi=300,bbox_inches='tight')
fig.savefig('./outputs/compiled_data/staining_plots/conA_compilation_med_no_tun.eps',bbox_inches='tight')
plt.show()
plt.clf()

sns.set(font_scale=2.0)
sns.set_style('whitegrid')
fig=plt.figure()
order=['WT, Buffer A','WT, GlpQ', 'WT, Untreated', 'WT, Tunicamycin','$\\Delta tagO$, Buffer A', '$\\Delta tagO$, GlpQ', '$\\Delta tagE$, Buffer A']
sns.barplot(data=df,x='Cond',y='R2-A normed', order=order, estimator='mean', color=col,capsize=0.3,
            edgecolor="black", errcolor="black")
plt.xticks(rotation=90)
plt.ylabel('Mean ConA stain (norm)')
plt.xlabel('Condition')
fig.savefig('./outputs/compiled_data/staining_plots/conA_compilation_mean.png', dpi=300,bbox_inches='tight')
fig.savefig('./outputs/compiled_data/staining_plots/conA_compilation_mean.eps',bbox_inches='tight')
plt.show()
plt.clf()

fig=plt.figure()
order=['WT, Buffer A','WT, GlpQ', 'WT, Untreated', 'WT, Tunicamycin','$\\Delta tagO$, Buffer A', '$\\Delta tagO$, GlpQ', '$\\Delta tagE$, Buffer A']
sns.barplot(data=df,x='Cond',y='R2-A normed', order=order, estimator='median', color=col,capsize=0.3,
            edgecolor="black", errcolor="black")
plt.xticks(rotation=90)
plt.ylabel('Median ConA stain (norm)')
plt.xlabel('Condition')
fig.savefig('./outputs/compiled_data/staining_plots/conA_compilation_med.png', dpi=300,bbox_inches='tight')
fig.savefig('./outputs/compiled_data/staining_plots/conA_compilation_med.eps',bbox_inches='tight')
plt.show()
plt.clf()

sns.set(font_scale=2.0)
col=sns.color_palette()[0]
sns.set_style('whitegrid')
fig=plt.figure()
order=['WT, Buffer A','WT, GlpQ', 'WT, Untreated', 'WT, Tunicamycin','$\\Delta tagO$, Buffer A', '$\\Delta tagO$, GlpQ', '$\\Delta tagE$, Buffer A']
sns.barplot(data=df,x='Date',y='R2-A normed', hue_order=order, estimator='mean', hue='Cond',
            edgecolor="black", errcolor="black")
# plt.xticks(rotation=90)
plt.ylabel('Mean ConA stain (norm)')
plt.xlabel('Condition')
plt.legend(loc=[1.05,0.05])
fig.savefig('./outputs/compiled_data/staining_plots/conA_compilation_mean_dated.png', dpi=300,bbox_inches='tight')
fig.savefig('./outputs/compiled_data/staining_plots/conA_compilation_mean_dated.eps',bbox_inches='tight')
plt.show()
plt.clf()

fig=plt.figure()
order=['WT, Buffer A','WT, GlpQ', 'WT, Untreated', 'WT, Tunicamycin','$\\Delta tagO$, Buffer A', '$\\Delta tagO$, GlpQ', '$\\Delta tagE$, Buffer A']
sns.barplot(data=df,x='Date',y='R2-A normed', hue_order=order, estimator='median', hue='Cond',
            edgecolor="black", errcolor="black")
# plt.xticks(rotation=90)
plt.ylabel('Median ConA stain (norm)')
plt.xlabel('Condition')
plt.legend(loc=[1.05,0.05])
fig.savefig('./outputs/compiled_data/staining_plots/conA_compilation_med_dated.png', dpi=300,bbox_inches='tight')
fig.savefig('./outputs/compiled_data/staining_plots/conA_compilation_med_dated.eps',bbox_inches='tight')
plt.show()
plt.clf()