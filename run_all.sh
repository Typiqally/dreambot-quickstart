#!/bin/bash

python quickstart.py

read -p "Enter the minimum delay time (in seconds): " min_delay
read -p "Enter the maximum delay time (in seconds): " max_delay

delay_range=$((max_delay - min_delay + 1))

echo "Running all quick starts..."

if [ ! -d "output" ]; then
    echo "Directory 'output' does not exist."
    exit 1
fi
cd output

# Find .cmd files, sort naturally
mapfile -t files < <(find . -maxdepth 1 -type f -name "*.cmd" | sort -V)
total=${#files[@]}

if [ "$total" -eq 0 ]; then
    echo "No .cmd files found in output/"
    exit 0
fi

index=0
for f in "${files[@]}"; do
    ((index++))
    delay=$((RANDOM % delay_range + min_delay))
    echo "[$index/$total] Waiting for $delay seconds before calling \"$f\"..."
    sleep "$delay"
    cmd.exe //C "$f"   # This runs the .cmd file[1][2]
done

# Delete all contents inside output/ but keep the directory
shopt -s dotglob
rm -rf ./*

echo "All done."
