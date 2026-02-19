# REPORT BUILD REQUIREMENTS (STRICT NOTEBOOK->PDF)

This folder supports a strict notebook-to-PDF path that is reproducible on this machine.

## Required Commands
- `jupyter` (nbconvert available)
- `pandoc`
- `xelatex`
- `python3`

## Version Checks
Run this from repo root:

```bash
jupyter --version
python3 --version
pandoc --version | head -n 1
xelatex --version | head -n 1
```

## Strict Build Command
From repo root:

```bash
"Project Deliverables/Report/build_report_pdf.sh"
```

## Why This Works with Pandoc 3.x
- Some nbconvert + pandoc 3.x combinations emit `\pandocbounded{...}` in generated LaTeX.
- The strict script injects a compatibility macro:
  - `\providecommand{\pandocbounded}[1]{#1}`
- Then it compiles LaTeX with `xelatex` twice and writes:
  - `Project Deliverables/Report/STAT5243_Project1_Team2_Final.pdf`

## Success Criteria
- Script exits with code `0`.
- Final PDF exists at:
  - `Project Deliverables/Report/STAT5243_Project1_Team2_Final.pdf`
