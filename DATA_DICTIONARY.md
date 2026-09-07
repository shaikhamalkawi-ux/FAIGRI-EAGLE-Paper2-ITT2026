# Data dictionary

## Locked analytical inputs
- `data/P2_ITT2026_Primary_Chain.csv`: final six-jurisdiction L1-L4 E/P/U classifications used as locked analytical inputs.
- `data/P2_58_Institution_Selection.csv`: finalized 58-case deterministic institutional membership.
- `data/P2_58_Institution_Evidence_Ledger.csv`: institution-level E/P/U evidence coding and locators.
- `data/P2_ITT2026_36_Source_Register_Current.csv`: national/regional official-source register supporting the jurisdiction-level chain.
- `data/P2_ITT2026_Source_Recovery_Ledger.csv`: pre-cutoff source-recovery record, including the SQU and UAE OBEF sensitivities.
- `data/P2_Documented_Bilingual_Search_Log_29.csv`: documented bilingual searches for U/P boundary cases.
- `data/P2_Source_Provenance_Extended.csv`: source identity, version/date, language, locator, preservation/retrieval status, and source role.
- `data/P2_Verified_Selection_Review.csv`: preserved source-backed selection review used to check founding-year and eligibility decisions.

## Eligibility and search-transparency files
- `data/P2_Selected_HEI_Eligibility_Certificates.csv`: official-source eligibility certificates for all 58 selected institutions. These verify selected cases; they do not recreate the complete pre-outcome eligible universe.
- `data/P2_Official_Eligibility_Registry_Sources.csv`: jurisdiction-level official higher-education registry/authority sources used for retrospective eligibility corroboration.
- `data/P2_Retrospective_Eligibility_Boundary_Audit.csv`: official-source checks for non-traditional and boundary institutions, with explicit eligibility/exclusion status.
- `data/P2_Eligibility_Boundary_Audit.md`: narrative statement of the eligibility-audit boundary and the non-reconstruction of the full pre-outcome universe.
- `data/P2_U_Search_Stopping_Rule.md`: documented stopping rule actually used for U (unlocated public evidence).
- `data/P2_Sensitivity_Scenario_Definitions.csv`: scenario definitions used to derive the reported SQU and broader-UAE robustness rows.

## Generated numerical outputs
`reproduce.py` preserves the locked documentary classifications above and derives the following outputs from them:
- `data/P2_Country_State_Summary.csv`
- `data/P2_Jurisdiction_Stratum_Summary.csv`
- `data/P2_Equal_Cell_Sensitivity.csv`
- `data/P2_Oldest3_Tie_Sensitivity_Membership.csv`
- `data/P2_Oldest3_Tie_Sensitivity_Summary.csv`
- `data/P2_ITT2026_IVFS_Representation_Robustness.csv`
- `data/P2_ITT2026_Robustness_Summary.csv`
- `data/P2_UAE_OBEF_L3_Broader_Sensitivity.csv`
- `data/Fig1_GCC_Evidence_Chain_ITT2026.png`
- `data/Auxiliary_58_Institution_Stratified_Audit.png` (repository-only; not a manuscript figure).

E = explicit qualifying public instrument; P = partial/indirect AI-specific evidence that does not pass the relevant layer gate; U = qualifying public evidence not located under the documented protocol.
