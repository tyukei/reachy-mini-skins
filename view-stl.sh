#!/usr/bin/env bash
set -euo pipefail

project_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
viewer_root="$project_dir/../.local/fstl"

if [[ $# -eq 0 ]]; then
    set -- "$project_dir/ninja/stl/reachy_mini_ninja_hood.stl"
fi

if command -v fstl >/dev/null 2>&1; then
    exec fstl "$@"
elif [[ -x "$viewer_root/usr/bin/fstl" ]]; then
    export LD_LIBRARY_PATH="$viewer_root/usr/lib/x86_64-linux-gnu${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
    export QT_PLUGIN_PATH="$viewer_root/usr/lib/x86_64-linux-gnu/qt5/plugins"
    exec "$viewer_root/usr/bin/fstl" "$@"
else
    echo "fstl is not installed. On Ubuntu, run: sudo apt install fstl" >&2
    echo "You can also open the STL files in Cura, PrusaSlicer, or Bambu Studio." >&2
    exit 1
fi
