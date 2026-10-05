#!/bin/bash
# Mac 로그인 시 자동 실행 설정 (LaunchAgent)
# 사용법: bash setup_launchagent.sh

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PYTHON="$(which python3)"
PLIST="$HOME/Library/LaunchAgents/com.pastor.md-watcher.plist"

cat > "$PLIST" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>com.pastor.md-watcher</string>

  <key>ProgramArguments</key>
  <array>
    <string>$PYTHON</string>
    <string>$SCRIPT_DIR/watch_and_convert.py</string>
  </array>

  <key>RunAtLoad</key>
  <true/>

  <key>KeepAlive</key>
  <true/>

  <key>StandardOutPath</key>
  <string>$HOME/Library/Logs/md-watcher.log</string>

  <key>StandardErrorPath</key>
  <string>$HOME/Library/Logs/md-watcher.log</string>
</dict>
</plist>
EOF

launchctl unload "$PLIST" 2>/dev/null
launchctl load "$PLIST"

echo "설정 완료."
echo "감시 폴더: ~/Desktop/변환대기"
echo "출력 폴더: ~/Documents/jeonpumsayeok-homepage/obsidian/20-원자료/인박스"
echo "로그:      ~/Library/Logs/md-watcher.log"
