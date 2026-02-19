# CODE REFERENCE FOR REPORT DELIVERABLE

Canonical workflow code is maintained in exactly one location:
- `Project Deliverables/Code Files/Project1_Full_Workflow_Code.ipynb`

Backup automation script:
- `Project Deliverables/Code Files/full_workflow.py`

This report folder does not duplicate the full workflow script to avoid drift.

## Run the Canonical Workflow
From repository root:

```bash
python3 -m pip install -r "Project Deliverables/Code Files/requirements.txt"
jupyter nbconvert --to notebook --execute "Project Deliverables/Code Files/Project1_Full_Workflow_Code.ipynb" --output /tmp/Project1_Full_Workflow_Code.executed.ipynb
python3 "Project Deliverables/Code Files/full_workflow.py"
```

## Build the Final Report PDF (Strict Notebook->PDF)
```bash
"Project Deliverables/Report/build_report_pdf.sh"
```

## Related Documentation
- Code run instructions: `Project Deliverables/Code Files/README.md`
- Strict PDF build requirements: `Project Deliverables/Report/REPORT_BUILD_REQUIREMENTS.md`
