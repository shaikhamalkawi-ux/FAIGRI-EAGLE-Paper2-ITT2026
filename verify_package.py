#!/usr/bin/env python3
from pathlib import Path
import hashlib, subprocess, tempfile, shutil, sys, pandas as pd
ROOT=Path(__file__).resolve().parent

def sha(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return h.hexdigest()

# Static release-package integrity is checked when a release manifest is present.
manifest=ROOT/'SHA256SUMS.txt'
if manifest.exists():
    for line in manifest.read_text().splitlines():
        if not line.strip(): continue
        digest,rel=line.split('  ',1); p=ROOT/rel
        if not p.exists() or sha(p)!=digest: raise SystemExit(f'Integrity mismatch: {rel}')

# Scientific checks on locked inputs.
d=ROOT/'data'
ledger=pd.read_csv(d/'P2_58_Institution_Evidence_Ledger.csv')
assert len(ledger)==58 and ledger.Final_state.value_counts().to_dict()=={'U':24,'E':21,'P':13}
chain=pd.read_csv(d/'P2_ITT2026_Primary_Chain.csv')
assert len(chain)==6 and (chain.L4=='E').sum()==6 and (chain.L3=='E').sum()==1
certs=pd.read_csv(d/'P2_Selected_HEI_Eligibility_Certificates.csv')
assert len(certs)==58 and certs.Institution.nunique()==58

# Fresh-copy derivation. Locked classification inputs are not overwritten.
generated=[
 'data/P2_Country_State_Summary.csv',
 'data/P2_Jurisdiction_Stratum_Summary.csv',
 'data/P2_Equal_Cell_Sensitivity.csv',
 'data/P2_ITT2026_Robustness_Summary.csv',
 'data/P2_Oldest3_Tie_Sensitivity_Membership.csv',
 'data/P2_Oldest3_Tie_Sensitivity_Summary.csv',
 'data/P2_UAE_OBEF_L3_Broader_Sensitivity.csv',
 'data/P2_ITT2026_IVFS_Representation_Robustness.csv',
 'data/Fig1_GCC_Evidence_Chain_ITT2026.png',
 'data/Auxiliary_58_Institution_Stratified_Audit.png',
]
with tempfile.TemporaryDirectory() as td:
    dst=Path(td)/'pkg'; shutil.copytree(ROOT,dst)
    cp=subprocess.run([sys.executable,'reproduce.py'],cwd=dst,text=True,capture_output=True)
    if cp.returncode!=0:
        print(cp.stdout); print(cp.stderr,file=sys.stderr); raise SystemExit('Fresh-copy reproduction failed')
    for rel in generated:
        if sha(dst/rel)!=sha(ROOT/rel): raise SystemExit(f'Fresh-copy output mismatch: {rel}')
print('Scientific inputs and fresh-copy derivation verified successfully.')
