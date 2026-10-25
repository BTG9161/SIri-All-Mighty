#!/bin/sh 
chmod +x restore_ses
sudo ln -sf "$(pwd)/restore_ses" /usr/local/bin/restore
mkdir -p .config
touch .config/SOUL.md .config/USER.md