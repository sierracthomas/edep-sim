#!/bin/bash

# To go in build/ directory

#source /home/sthoma31/software/geant/geant4-v11.1.1-build/geant4make.sh

#export BUILD_DIR=/home/sthoma31/geant-scripts/geant4-11.1.1/clear_build
export SOURCE_DIR=/home/sthoma31/edep/build_22

#cd $BUILD_DIR
mkdir -p energies
cd energies

energy_arr=(7.708)
#(4.473)
#  5.393  5.656  5.850  5.8803 6.0536 6.0835 6.100  6.2838 6.3387
# 6.476  6.5662 6.9216 7.190  7.246  7.271  7.281  7.519  7.626  7.708) 


for val in ${energy_arr[*]}
do
    echo "Starting now..."
    echo $val
    mkdir -p $val
    cd $val
    cp $SOURCE_DIR/run1.mac .
    new_energy='s/ENERGY/$val/g'
    eval sed -i $new_energy run1.mac
    cp ../../test_copied.gdml .
    bash ../../run_edep.sh 100


    # only keep data
    #sed -n '/EveTraParXYZdEProc/w EveTraParXYZdEProc.csv' run.txt
    # remove stuff until first comma
    #eval sed -i 's/[^,]*,//' EveTraParXYZdEProc.csv #EveTraParXYZdEProc.csv
    #rm run.txt steps.txt
    python ../../hitsegments.py
    echo "Done. "
    cd ../
done

