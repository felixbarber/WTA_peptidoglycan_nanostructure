import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import scipy
from scipy.stats import ttest_ind



# path='/Users/felixbarber/Documents/Rojas_Lab/data/'
path='/Users/barber.527/Documents/Rojas_Lab/data/'
expt_id='/240606_conA'
out_path=path+expt_id+'/df_appended_paper'
df=pd.read_pickle(out_path)

df_wt_means={}
for day in df.Date.unique():
    temp=(df.Date==day)*(df.Strain=='WT')*(df.Condition=='Buffer A')
    df_wt_means[day]=df[temp]['R2-A'].mean()

normed_R2=np.zeros(len(df))
for temp_ind in np.arange(len(df)):
    temp_out=df.iloc[temp_ind]
#     temp=(df.Date==temp_out.Date)*(df.Strain=='WT')*(df.Condition=='Buffer A')
    normed_R2[temp_ind]=temp_out['R2-A']/df_wt_means[temp_out.Date]
df['R2-A normed']=normed_R2
df['Cond']=df['Strain'] +', '+ df['Condition'] + ''

ax=sns.displot(data=df[(df['R2-A normed']>0)*(df['R2-A normed']<30)],x='R2-A normed', hue='Cond', hue_order=['$\Delta tagO$, Buffer A','$\Delta tagO$, GlpQ', '$\\Delta tagE$, Buffer A'] ,log_scale=True)
fig=ax.figure
fig.savefig('./outputs/compiled_data/staining_plots/conA_tagO_dists.png',dpi=300,bbox_inches='tight')
plt.show()
plt.clf()

plt.tight_layout()
sns.set(font_scale=2.0)

sns.set_style('whitegrid')
col = sns.color_palette()[0]
fig=plt.figure()
order=['WT, Buffer A','WT, GlpQ', '$\\Delta tagO$, Buffer A', '$\\Delta tagO$, GlpQ', '$\\Delta tagE$, Buffer A']
# sns.barplot(data=df,x='Cond',y='R2-A normed', order=order, estimator='mean', color=col,capsize=0.3,
#             edgecolor="black", errcolor="black")
# sns.boxplot(data=df,x='Cond',y='R2-A normed', order=order, color=col,linecolor="black")
# ax=plt.gca()
# ax.set_yscale('log')

sns.boxplot(data=df,x='Cond',y='R2-A normed', order=order, color=col,linecolor="black",showfliers=False)
ax=plt.gca()

plt.xticks(rotation=90)
plt.ylabel('ConA stain (norm)')
plt.xlabel('Condition')
fig.savefig('./outputs/compiled_data/staining_plots/conA_compilation_mean_pub.png', dpi=300,bbox_inches='tight')
fig.savefig('./outputs/compiled_data/staining_plots/conA_compilation_mean_pub.eps',bbox_inches='tight')
plt.show()
plt.clf()

fig=plt.figure()
order=['WT, Buffer A','WT, GlpQ','$\\Delta tagO$, Buffer A', '$\\Delta tagO$, GlpQ', '$\\Delta tagE$, Buffer A']
sns.barplot(data=df,x='Cond',y='R2-A normed', order=order, estimator='median', color=col,capsize=0.3,
            edgecolor="black", errcolor="black")
plt.xticks(rotation=90)
plt.ylabel('Median ConA stain (norm)')
plt.xlabel('Condition')
fig.savefig('./outputs/compiled_data/staining_plots/conA_compilation_med_pub.png', dpi=300,bbox_inches='tight')
fig.savefig('./outputs/compiled_data/staining_plots/conA_compilation_med_pub.eps',bbox_inches='tight')
plt.show()
plt.clf()


with open('./outputs/compiled_data/staining_plots/conA_compilation.txt', 'w') as f:
    outs_anova = []
    samples = [np.asarray(df[df.Cond == order[i0]]['R2-A normed']) for i0 in range(len(order))]
    print(samples,file=f)
    outs_anova.append(scipy.stats.f_oneway(samples[0], samples[1], samples[2], samples[3], samples[4], axis=0))
    print(outs_anova[-1],file=f)
    if outs_anova[-1][1] < 0.01:
        print(scipy.stats.tukey_hsd(samples[0], samples[1], samples[2], samples[3], samples[4]),file=f)

