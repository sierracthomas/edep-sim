#!/bin/bash

# Check if an argument is provided
if [ "$#" -eq 0 ]; then
    echo "Usage: $0 <argument>"
    exit 1
fi

# Access the first argument passed to the script
argument="$1"

# Print the argument
echo "The provided argument is: $argument events"
edep-sim -o my-output.root -g test_copied.gdml -u -e $argument run1.mac > run1.txt

#python hitsegments.py
#python round5.py
#python merge.py
