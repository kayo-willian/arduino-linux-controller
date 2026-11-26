#!/usr/bin/env bash
set -euo pipefail
root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
target="$HOME/painel-ubuntu.py"
if [[ -e "$target" ]] && ! cmp -s "$root/software/painel-ubuntu.py" "$target"; then
    echo "Existing different file: $target. Back it up or rename it before continuing." >&2
    exit 1
fi
install -m 0644 "$root/software/painel-ubuntu.py" "$target"
mkdir -p "$HOME/.config/autostart"
cat > "$HOME/.config/autostart/painel-ubuntu.desktop" <<EOF
[Desktop Entry]
Type=Application
Name=Arduino Linux Controller
Comment=Physical desktop controller
Exec=/usr/bin/python3 "$target"
Terminal=false
X-GNOME-Autostart-enabled=true
EOF
echo "Autostart configured for the next graphical login."
