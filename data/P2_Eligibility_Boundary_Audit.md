# Eligibility and selection-boundary audit

The pre-outcome selection rule is preserved, but the complete eligible universe beyond the original oldest-four boundary was not archived before AI-policy outcomes were known. This release therefore **does not retroactively label a newly assembled web list as the original pre-outcome universe**.

To strengthen auditability without changing the design, the archive now provides:

1. `P2_Selected_HEI_Eligibility_Certificates.csv`: an official-source eligibility certificate for each of the 58 selected institutions;
2. `P2_Official_Eligibility_Registry_Sources.csv`: jurisdiction-level official registry/authority sources used to corroborate HEI status;
3. `P2_Retrospective_Eligibility_Boundary_Audit.csv`: preserved selection-review and boundary cases, including known eligible/ineligible/unresolved candidates; and
4. the original `P2_58_Institution_Selection.csv` and `P2_Verified_Selection_Review.csv`.

These objects support independent checking that the **selected institutions satisfy the stated HEI eligibility boundary** and make non-traditional cases (for example BIBF, Qatar Aeronautical Academy, Qatar Leadership Centre, Qatar Finance and Business Academy, PAAET, and Oman College of Health Sciences) explicit. They do not prove that every possible excluded institution has been reconstructed after the fact.

For that reason, the paper does not report an oldest-five sensitivity. Rebuilding a fifth institution now from live web sources after outcomes are known would weaken, rather than strengthen, the pre-outcome design.
