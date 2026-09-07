# GitHub repository status

Status: **PRIVATE review-stage reproducibility repository**

Repository purpose: support the ITT 2026 Paper 2 analysis while preserving double-blind anonymity. The repository must remain private until the review-stage anonymity requirement is lifted or the venue explicitly permits an author-identifying public artifact.

## Scientific state reproduced
- cutoff: 23 July 2026
- institutional panel: N=58 = 21 E / 13 P / 24 U
- primary chain: L3 explicit 1/6; L4 explicit 6/6; L4=E with L3!=E in 5/6 jurisdictions
- primary L3 interval envelope: [0.167, 0.500]
- L4 interval envelope: [1.000, 1.000]
- minimum L4-L3 gap: 0.500
- broader UAE OBEF sensitivity: L3 explicit 2/6; minimum gap remains 0.500
- oldest-three-with-ties sensitivity: N=47 = 19 E / 7 P / 21 U

## Included reproducibility components
- locked six-jurisdiction primary chain
- 36-record national/regional source register
- 58-row institutional selection and evidence ledgers
- official eligibility registry sources and selected-HEI eligibility certificates
- retrospective eligibility-boundary audit for non-traditional/boundary institutions
- documented bilingual U-search stopping rule and search log
- source-recovery ledger and sensitivity scenario definitions
- derived country, jurisdiction-stratum, equal-cell, IVFS, OBEF, robustness, and oldest-three outputs
- deterministic `reproduce.py`, `run.sh`, `verify_package.py`, requirements, and GitHub Actions workflow
- source-provenance documentation and claim-to-artifact map

Generated figures are recreated deterministically by `bash run.sh`; the auxiliary institutional-panel visualization is repository-only and is not a numbered manuscript figure.

## Binary manuscript files
The manuscript PDFs remain controlled submission artifacts outside the GitHub tree during the review stage. Their absence does not affect numerical reproduction. They can be added to a public camera-ready release after double-blind review if desired.

## Zenodo
No Zenodo deposition is used at the current stage. Zenodo metadata and upload-guide files were removed from this repository.
