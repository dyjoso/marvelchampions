#!/bin/sh
# Re-sync data/modular-sets.js with VillainTheory's master Google Doc.
# Run from the repository root: sh tools/update-modulars.sh
set -e
DOC=1AOED4MPkrEGIOAVzV4VJaFAc4bWHfhstOSVTqhSpvHU
TMP=$(mktemp -d)
curl -sL -o "$TMP/doc.html" "https://docs.google.com/document/d/$DOC/export?format=html"
python tools/doc_tables.py "$TMP/doc.html" "$TMP/tables.json"
python tools/build_modulars.py "$TMP/tables.json" data/modular-sets.js
rm -rf "$TMP"
echo "Done. Check the result with: git diff data/modular-sets.js"
