#!/usr/bin/env bash
set -euo pipefail

# Strict notebook->PDF build that stays compatible with pandoc 3.x output.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
NOTEBOOK_PATH="${SCRIPT_DIR}/Project1_Final_Submission.ipynb"
OUTPUT_PDF_PATH="${SCRIPT_DIR}/STAT5243_Project1_Team2_Final.pdf"
TMP_BASENAME="_nb_strict_build"
TMP_TEX_PATH="${SCRIPT_DIR}/${TMP_BASENAME}.tex"
TMP_PDF_PATH="${SCRIPT_DIR}/${TMP_BASENAME}.pdf"

for cmd in jupyter pandoc xelatex python3; do
  if ! command -v "$cmd" >/dev/null 2>&1; then
    echo "ERROR: required command not found: $cmd" >&2
    exit 1
  fi
done

cd "${SCRIPT_DIR}"

echo "[strict-build] converting notebook to latex"
jupyter nbconvert --to latex "${NOTEBOOK_PATH}" --output "${TMP_BASENAME}" \
  --TagRemovePreprocessor.enabled=True \
  --TagRemovePreprocessor.remove_cell_tags='["hide"]'

echo "[strict-build] injecting pandoc compatibility macro + image sizing"
python3 - <<'PY'
from pathlib import Path
import re

tex_path = Path("_nb_strict_build.tex")
text = tex_path.read_text()

# 1) Pandoc 3.x compatibility
macro = "\\providecommand{\\pandocbounded}[1]{#1}\n"
if "\\providecommand{\\pandocbounded}" not in text:
    idx = text.find("\\begin{document}")
    if idx == -1:
        raise SystemExit("ERROR: \\begin{document} not found in generated LaTeX")
    text = text[:idx] + macro + text[idx:]

# 2) Shrink all images to 60% textwidth for compact PDF
text = re.sub(
    r'\\includegraphics(\[.*?\])?\{',
    r'\\includegraphics[width=0.60\\textwidth]{',
    text
)

tex_path.write_text(text)
PY

echo "[strict-build] compiling xelatex pass 1"
xelatex -interaction=nonstopmode -halt-on-error "${TMP_BASENAME}.tex" >/dev/null
echo "[strict-build] compiling xelatex pass 2"
xelatex -interaction=nonstopmode -halt-on-error "${TMP_BASENAME}.tex" >/dev/null

if [[ ! -f "${TMP_PDF_PATH}" ]]; then
  echo "ERROR: strict build failed to produce ${TMP_PDF_PATH}" >&2
  exit 1
fi

cp "${TMP_PDF_PATH}" "${OUTPUT_PDF_PATH}"
echo "[strict-build] wrote ${OUTPUT_PDF_PATH}"

# Keep workspace clean for git status.
rm -f "${SCRIPT_DIR}/${TMP_BASENAME}.aux" \
      "${SCRIPT_DIR}/${TMP_BASENAME}.log" \
      "${SCRIPT_DIR}/${TMP_BASENAME}.out" \
      "${SCRIPT_DIR}/${TMP_BASENAME}.tex" \
      "${SCRIPT_DIR}/${TMP_BASENAME}.pdf"

echo "[strict-build] complete"
