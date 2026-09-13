#!/usr/bin/env bash
set -euo pipefail

# TeX Live and its tools are preinstalled in the pinned Debian container.
lualatex --version
biber --version
latexmk --version

# Keep the image's Debian mirror and signing-key settings.
sed -i 's/^Components: main$/Components: main contrib/' \
  /etc/apt/sources.list.d/debian.sources
apt-get update
DEBIAN_FRONTEND=noninteractive apt-get install --yes --no-install-recommends \
  ttf-mscorefonts-installer

# Pin the mathematical font independently of TeX Live's bundled version.
stix_dir="$HOME/.local/share/fonts/stix-two"
mkdir -p "$stix_dir"
curl --fail --location --retry 3 \
  https://raw.githubusercontent.com/stipub/stixfonts/02b4b9b6093e2c5d6379b935ea340ea40f7e863b/fonts/static_otf/STIXTwoMath-Regular.otf \
  --output "$stix_dir/STIXTwoMath-Regular.otf"
printf '%s  %s\n' \
  95bc2729e41faf93b0bcae9e96c4dc4da45855067fd0581e621e30734fe8d90b \
  "$stix_dir/STIXTwoMath-Regular.otf" | sha256sum --check
fc-cache --force
luaotfload-tool --update --force
for font in 'Times New Roman' Arial 'Courier New' 'STIX Two Math'; do
  fc-match --format='%{family}\n' "$font" | grep --fixed-strings --line-regexp "$font"
done

# Use the same formatter version locally and in CI.
formatter_dir="$RUNNER_TEMP/latexindent-bin"
mkdir -p "$formatter_dir"
curl --fail --location --retry 3 \
  https://github.com/cmhughes/latexindent.pl/releases/download/V4.0.2/latexindent-linux \
  --output "$formatter_dir/latexindent"
printf '%s  %s\n' \
  df8a86dd347516ae55c3e45e92a7e4459670ad26f807fc17360224a998f1d17a \
  "$formatter_dir/latexindent" | sha256sum --check
chmod +x "$formatter_dir/latexindent"
printf '%s\n' "$formatter_dir" >> "$GITHUB_PATH"
"$formatter_dir/latexindent" --version
