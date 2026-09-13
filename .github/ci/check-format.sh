#!/usr/bin/env bash
set -euo pipefail

cd "$(git rev-parse --show-toplevel)"
format_temp=$(mktemp -d)
trap 'rm -rf "$format_temp"' EXIT
status=0
while IFS= read -r -d '' file; do
  output="$format_temp/$(basename "$file")"
  latexindent -c "$format_temp" -l ./latexindent.yaml "$file" > "$output"
  if ! diff -u "$file" "$output"; then
    printf '::error file=%s::Formatting differs from latexindent 4.0.2\n' "$file"
    status=1
  fi
done < <(git ls-files -z -- dissertation.tex synopsis.tex \
  'common/*.tex' 'Dissertation/*.tex' 'Synopsis/*.tex' 'biblio/*.tex')
exit "$status"
