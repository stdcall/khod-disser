#!/usr/bin/env bash
set -euo pipefail

repo_root=$(git rev-parse --show-toplevel)
cd "$repo_root"
format_temp=$(mktemp -d)
trap 'rm -rf "$format_temp"' EXIT
git ls-files -z -- dissertation.tex synopsis.tex \
  'common/*.tex' 'Dissertation/*.tex' 'Synopsis/*.tex' 'biblio/*.tex' \
  > "$format_temp/sources"
status=0
while IFS= read -r -d '' file; do
  output="$format_temp/$(basename "$file")"
  latexindent -m -c "$format_temp" -l ./latexindent.yaml "$file" > "$output"
  if ! diff -u "$file" "$output"; then
    printf '::error file=%s::Formatting differs from latexindent 4.0.2\n' "$file"
    status=1
  fi
done < "$format_temp/sources"
exit "$status"
