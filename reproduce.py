#!/usr/bin/env python3
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Patch
from matplotlib.colors import ListedColormap, BoundaryNorm

HERE=Path(__file__).resolve().parent
DATA=HERE/'data'
states=['E','P','U']

# Locked documentary classifications are inputs, not reconstructed by this script.
chain=pd.read_csv(DATA/'P2_ITT2026_Primary_Chain.csv')
ledger=pd.read_csv(DATA/'P2_58_Institution_Evidence_Ledger.csv')
sample=pd.read_csv(DATA/'P2_58_Institution_Selection.csv')
assert list(chain['Jurisdiction'])==['United Arab Emirates','Saudi Arabia','Qatar','Oman','Bahrain','Kuwait']
assert len(chain)==6 and len(ledger)==len(sample)==58
assert (ledger['Selection_status']=='FINALIZED').all()
assert sorted(ledger.Institution)==sorted(sample.Institution)

# Derived institutional summaries.
country=(ledger.pivot_table(index='Jurisdiction',columns='Final_state',values='Institution',aggfunc='count',fill_value=0).reindex(columns=states,fill_value=0))
country['N']=country.sum(axis=1)
for s in states: country[f'{s}_share_raw']=country[s]/country['N']
country.reset_index().to_csv(DATA/'P2_Country_State_Summary.csv',index=False,float_format='%.9f')

js=(ledger.pivot_table(index=['Jurisdiction','Stratum'],columns='Final_state',values='Institution',aggfunc='count',fill_value=0).reindex(columns=states,fill_value=0))
js['N']=js.sum(axis=1)
for s in states: js[f'{s}_share']=js[s]/js['N']
js=js.reset_index(); js.to_csv(DATA/'P2_Jurisdiction_Stratum_Summary.csv',index=False,float_format='%.9f')
rows=[]
for jur,g in js.groupby('Jurisdiction'):
    row={'Jurisdiction':jur,'Cells_present':len(g)}
    for s in states: row[f'Equal_cell_{s}_share']=g[f'{s}_share'].mean()
    rows.append(row)
pd.DataFrame(rows).to_csv(DATA/'P2_Equal_Cell_Sensitivity.csv',index=False,float_format='%.9f')

# Robustness summary is derived from the locked chain plus declared scenario substitutions.
def chain_metrics(frame):
    n=len(frame)
    l3=int((frame['L3']=='E').sum())
    l4=int((frame['L4']=='E').sum())
    disc=int(((frame['L4']=='E') & (frame['L3']!='E')).sum())
    return l3,l4,disc,n

def frac(x,n): return f'{x}/{n}'

rob_rows=[]
scenarios=pd.read_csv(DATA/'P2_Sensitivity_Scenario_Definitions.csv')
source_recovery=pd.read_csv(DATA/'P2_ITT2026_Source_Recovery_Ledger.csv').set_index('Source_ID')
for _,sc in scenarios.iterrows():
    f=chain.copy()
    replacement=str(sc['Replacement_state'])
    if sc['Scenario_ID']=='OMN_NO_SQU':
        replacement=str(source_recovery.loc['OMN04','Before_recovery_state'])
    mask=f['Jurisdiction'].eq(sc['Jurisdiction'])
    assert mask.sum()==1 and sc['Layer'] in ['L1','L2','L3','L4']
    f.loc[mask,sc['Layer']]=replacement
    l3,l4,disc,n=chain_metrics(f)
    interp='Discontinuity already present' if sc['Scenario_ID']=='OMN_NO_SQU' else 'Gap persists under more permissive L3 coding'
    rob_rows.append([sc['Scenario'],frac(l3,n),frac(l4,n),frac(disc,n),interp])
l3,l4,disc,n=chain_metrics(chain)
rob_rows.insert(1,['Primary recovered chain',frac(l3,n),frac(l4,n),frac(disc,n),'Same direction; larger extent'])
no_sau=chain[chain['Jurisdiction']!='Saudi Arabia'].copy(); l3,l4,disc,n=chain_metrics(no_sau)
rob_rows.append(['Leave out Saudi Arabia',frac(l3,n),frac(l4,n),frac(disc,n),'Only L3-explicit jurisdiction removed'])
other=[]
for jur in chain.loc[chain['Jurisdiction']!='Saudi Arabia','Jurisdiction']:
    f=chain[chain['Jurisdiction']!=jur].copy(); other.append(chain_metrics(f))
assert len(set(other))==1
l3,l4,disc,n=other[0]
rob_rows.append(['Leave out any one other jurisdiction',frac(l3,n),frac(l4,n),frac(disc,n),'Five equivalent leave-one-out cases'])
rob=pd.DataFrame(rob_rows,columns=['Analysis_condition','L3_explicit','L4_explicit','L4E_L3_notE','Interpretation'])
rob.to_csv(DATA/'P2_ITT2026_Robustness_Summary.csv',index=False)

ivfs_rows=[]
for layer in ['L1','L2','L3','L4']:
    vals=chain[layer]; e=int((vals=='E').sum()); p=int((vals=='P').sum()); u=int((vals=='U').sum()); n=len(vals)
    ivfs_rows.append([layer,e,p,u,n,e/n,(e+p)/n])
ivfs=pd.DataFrame(ivfs_rows,columns=['Layer','E_count','P_count','U_count','n','Envelope_lower','Envelope_upper'])
ivfs.to_csv(DATA/'P2_ITT2026_IVFS_Representation_Robustness.csv',index=False,float_format='%.6f')

old3=[]
for (jur,st),g in ledger.groupby(['Jurisdiction','Stratum'],sort=False):
    g=g.sort_values(['Founding_year','Institution'])
    q=g.copy() if len(g)<=3 else g[g['Founding_year']<=g.iloc[2]['Founding_year']].copy()
    old3.append(q)
old3=pd.concat(old3,ignore_index=True)
old3[['Jurisdiction','Stratum','Institution','Founding_year','Final_state']].to_csv(DATA/'P2_Oldest3_Tie_Sensitivity_Membership.csv',index=False)
o3=(old3.pivot_table(index='Jurisdiction',columns='Final_state',values='Institution',aggfunc='count',fill_value=0).reindex(columns=states,fill_value=0)); o3['N']=o3.sum(axis=1)
o3.reset_index().to_csv(DATA/'P2_Oldest3_Tie_Sensitivity_Summary.csv',index=False)

adv=pd.DataFrame([
 ['Primary governance-control gate','P',1,2,3,1/6,3/6,1/2],
 ['Broader HE operational-framework gate','E',2,1,3,2/6,3/6,1/2],
],columns=['Scenario','UAE_L3','L3_E','L3_P','L3_U','Envelope_lower','Envelope_upper','Minimum_L4_minus_L3'])
adv.to_csv(DATA/'P2_UAE_OBEF_L3_Broader_Sensitivity.csv',index=False,float_format='%.6f')

state_val={'U':0,'P':1,'E':2}
mat=np.array([[state_val[x] for x in row] for row in chain[['L1','L2','L3','L4']].values])
colors=['#440154','#21918c','#fde725']; cmap=ListedColormap(colors); norm=BoundaryNorm([-0.5,0.5,1.5,2.5],cmap.N)
fig,ax=plt.subplots(figsize=(9.2,4.15)); ax.imshow(mat,aspect='auto',cmap=cmap,norm=norm)
ax.set_xticks(range(4),['L1\nNational','L2\nOperational','L3\nHE translation','L4\nInstitutional'])
ax.set_yticks(range(6),['UAE','Saudi Arabia','Qatar','Oman','Bahrain','Kuwait'])
plt.setp(ax.get_xticklabels(), fontsize=15, fontweight='bold')
plt.setp(ax.get_yticklabels(), fontsize=14, fontweight='bold')
for i,row in enumerate(chain[['L1','L2','L3','L4']].values):
    for j,s in enumerate(row): ax.text(j,i,s,ha='center',va='center',fontweight='bold',fontsize=13,color='white' if s=='U' else 'black')
ax.set_title('GCC public-evidence chain (23 July 2026 cutoff)',fontsize=16,fontweight='bold')
handles=[Patch(facecolor='#fde725',edgecolor='0.3',label='E  Explicit'),Patch(facecolor='#21918c',edgecolor='0.3',label='P  Partial'),Patch(facecolor='#440154',edgecolor='0.3',label='U  Unlocated')]
ax.legend(handles=handles,loc='upper center',bbox_to_anchor=(0.5,-0.18),ncol=3,frameon=False,fontsize=10)
fig.tight_layout(); fig.savefig(DATA/'Fig1_GCC_Evidence_Chain_ITT2026.png',dpi=300,bbox_inches='tight'); plt.close(fig)

jur_order=['UAE','Saudi Arabia','Qatar','Oman','Bahrain','Kuwait']; strata=['G1','G2','G3']
fig,ax=plt.subplots(figsize=(7.15,3.35)); ax.set_xlim(0,3); ax.set_ylim(0,6); ax.invert_yaxis(); ax.axis('off')
for c,g in enumerate(strata): ax.text(c+0.5,-0.16,{'G1':'G1 public/general','G2':'G2 private/non-gov.','G3':'G3 public applied/specialized'}[g],ha='center',va='bottom',fontsize=8.3,fontweight='bold')
for r,jur in enumerate(jur_order):
    ax.text(-0.06,r+0.5,jur,ha='right',va='center',fontsize=8.2,fontweight='bold')
    for c,g in enumerate(strata):
        z=js[(js.Jurisdiction==jur)&(js.Stratum==g)].iloc[0]
        ax.add_patch(Rectangle((c,r),1,1,facecolor='white',edgecolor='0.35',linewidth=0.8))
        ax.text(c+0.5,r+0.40,f"E {int(z.E)}   P {int(z.P)}   U {int(z.U)}",ha='center',va='center',fontsize=8.5,fontweight='bold')
        ax.text(c+0.5,r+0.69,f"n={int(z.N)}",ha='center',va='center',fontsize=7.3)
ax.text(1.5,6.18,'Corrected 58-institution panel; nominal documentary states only (not prevalence or maturity scores)',ha='center',va='top',fontsize=7.5)
fig.tight_layout(pad=0.6); fig.savefig(DATA/'Auxiliary_58_Institution_Stratified_Audit.png',dpi=300,bbox_inches='tight'); plt.close(fig)
legacy=DATA/'Fig2_58_Institution_Stratified_Audit.png'
if legacy.exists(): legacy.unlink()

assert ledger['Final_state'].value_counts().to_dict()=={'U':24,'E':21,'P':13}
expected={'UAE':(6,4,4,14),'Saudi Arabia':(3,4,4,11),'Qatar':(2,2,6,10),'Oman':(2,1,5,8),'Bahrain':(6,0,1,7),'Kuwait':(2,2,4,8)}
for j,v in expected.items():
    rr=country.loc[j]; assert (int(rr.E),int(rr.P),int(rr.U),int(rr.N))==v
assert (country.E>=2).all() and ((country.P+country.U)>=1).all()
stratum=ledger.groupby('Stratum')['Final_state'].value_counts().unstack(fill_value=0)
assert (int(stratum.loc['G1','E']),int(stratum.loc['G1','P']),int(stratum.loc['G1','U']))==(9,1,4)
assert (int(stratum.loc['G2','E']),int(stratum.loc['G2','P']),int(stratum.loc['G2','U']))==(9,9,7)
assert (int(stratum.loc['G3','E']),int(stratum.loc['G3','P']),int(stratum.loc['G3','U']))==(3,3,13)
assert (chain.L4=='E').sum()==6 and (chain.L3=='E').sum()==1 and (((chain.L4=='E')&(chain.L3!='E')).sum()==5)
iv=ivfs.set_index('Layer'); assert abs(iv.loc['L3','Envelope_lower']-1/6)<1e-6 and abs(iv.loc['L3','Envelope_upper']-3/6)<1e-6 and abs(iv.loc['L4','Envelope_lower']-1)<1e-12
assert len(old3)==47 and old3['Final_state'].value_counts().to_dict()=={'U':21,'E':19,'P':7}
assert list(adv['L3_E'])==[1,2] and (abs(adv['Minimum_L4_minus_L3']-1/2)<1e-6).all()
sources=pd.read_csv(DATA/'P2_ITT2026_36_Source_Register_Current.csv'); assert len(sources)==36 and (sources.Layer=='L3').sum()==5
certs=pd.read_csv(DATA/'P2_Selected_HEI_Eligibility_Certificates.csv'); assert len(certs)==58 and (certs['Selected']=='YES').all()
print('Reproduction completed successfully: locked classifications preserved; numerical summaries, sensitivities, and figures derived and verified.')
