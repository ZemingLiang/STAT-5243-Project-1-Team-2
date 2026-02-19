# FINAL_POLISH_PLAN

## Session 0: Plan Freeze + Working Branch
- Scope: lock a single execution plan so work does not drift.
- Actions:
  - Create this `FINAL_POLISH_PLAN.md`.
  - Create working branch from `Main-Final-Deliverable` (`codex/temporary-execution-branch-report-polish`).
  - Capture baseline commit SHA + repository file manifest.
- Deliverables:
  - `FINAL_POLISH_PLAN.md`
  - `Project Workspace/qa/baseline_manifest_session0.json`
- Gate: baseline manifest committed before any content edits.

## Session 1: Evidence Harvest (Numbers + Artifacts)
- Scope: collect quantitative evidence for report claims.
- Actions:
  - Parse report artifact JSON files.
  - Extract missingness, correlation, p-values, anomaly rates, model metrics.
  - Build registry: `claim_id -> figure_png -> json_source -> metric_values`.
- Deliverable:
  - `Project Workspace/qa/evidence_registry_report_depth.json`
- Gate: every major claim has at least one exact figure + JSON source.

## Session 2: Expand Cleaning Narrative (03 Section)
- Scope: deepen cleaning/preprocessing methodology.
- Actions:
  - Rewrite `03_cleaning_preprocessing.tex` with explicit decisions for:
    - missingness strategy
    - duplicates policy
    - outlier policy
    - type corrections
    - transformations
    - scaling/encoding rationale
  - Embed concrete evidence anchors.
- Deliverable:
  - Expanded section with claim-evidence anchors.
- Gate: all six decision categories explicitly covered with concrete evidence references.

## Session 3: Expand EDA Interpretation (04 Section)
- Scope: move EDA from descriptive to analytical.
- Actions:
  - Rewrite `04_eda.tex` using exact rho/p-values/anomaly metrics.
  - Add interpretation and caveats.
- Deliverable:
  - Expanded 04 section with numeric interpretation.
- Gate: advanced-statistics claims include explicit values + artifact citations.

## Session 4: Build Feature Ablation Artifacts
- Scope: justify feature utility via measured lift.
- Actions:
  - Implement ablation (baseline vs +sentiment vs +topics) in integrated workflow code.
  - Output comparison table JSON + figure.
- Deliverables:
  - `Project Workspace/Supporting Materials/Report Sources/artifacts/json/05_feature_ablation_table.json`
  - `Project Workspace/Supporting Materials/Report Sources/artifacts/figures/05_feature_ablation_comparison.png`
- Gate: deterministic/reproducible outputs with fixed seed.

## Session 5: Strengthen Feature Engineering Writeup (05 Section)
- Scope: explain why feature additions improve utility.
- Actions:
  - Update `05_feature_engineering.tex` with ablation results, interpretation, tradeoffs, limitations.
- Deliverable:
  - Revised 05 section.
- Gate: includes measurable before/after evidence.

## Session 6: Add Figure-to-Finding Trace Table
- Scope: tighten claim-to-evidence traceability.
- Actions:
  - Insert traceability table into report source mapping key findings to exact PNG + JSON paths.
- Deliverable:
  - Trace table in report source.
- Gate: each key finding linked to at least one figure + JSON.

## Session 7: Reproducibility Verification Block in README
- Scope: make validation quick and explicit.
- Actions:
  - Add reproducibility verification block to root README.
  - Include expected outputs + validation command + pass criteria.
- Deliverable:
  - Updated root README.
- Gate: validation command passes.

## Session 8: Notebook and PDF Consistency Pass
- Scope: align notebook and final PDF content/order.
- Actions:
  - Synchronize headings/summary/evidence references between notebook and report sources.
  - Rebuild final PDF.
  - Generate consistency report.
- Deliverables:
  - Rebuilt PDF.
  - `Project Workspace/qa/notebook_pdf_consistency_report.md`.
- Gate: assignment section order exactly matches.

## Session 9: Final QA + Rubric Re-Scoring
- Scope: confirm advanced-level coverage.
- Actions:
  - Refresh checklist and rubric evidence files.
  - Run final checks: path integrity, artifact parity, trace completeness, reproducibility.
- Deliverables:
  - Updated QA JSON files + readiness summary.
- Gate: no unresolved high/medium issues.

## Session 10: Branch Finalization
- Scope: transparent final delivery with provenance.
- Actions:
  - Commit session-by-session (no squash).
  - Push working branch and merge into `Main-Final-Deliverable`.
  - Refresh provenance SHAs.
- Deliverable:
  - Final pushed branch state.
- Gate: clean working tree + remote branch synced.
