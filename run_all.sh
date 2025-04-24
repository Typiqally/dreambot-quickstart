#!/bin/bash

# Set terminal color (not directly portable; Git Bash may not support 'color' command)
# You can use tput for colors, or skip this step

python quickstart.py

read -p "Enter the minimum delay time (in seconds): " min_delay
read -p "Enter the maximum delay time (in seconds): " max_delay

delay_range=$((max_delay - min_delay + 1))

echo "Running all quick starts..."

cd output || exit 1

# Gather list of .sh files (or .bat if you still use them)
mapfile -t files < <(find . -maxdepth 1 -type f -name "*.sh" | sort -V)
total=${#files[@]}
index=0

for f in "${files[@]}"; do
    ((index++))
    delay=$((RANDOM % delay_range + min_delay))
    echo "[$index/$total] Waiting for $delay seconds before calling \"$f\"..."
    sleep "$delay"
    bash "$f"
done

# Delete all contents inside output/ but keep the directory
rm -rf ./*

# If you want to also remove hidden files (except . and ..)
shopt -s dotglob
rm -rf ./*

# Done