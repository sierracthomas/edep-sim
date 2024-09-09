#!/bin/bash

# To go in build/ directory

#source /home/sthoma31/software/geant/geant4-v11.1.1-build/geant4make.sh

#export BUILD_DIR=/home/sthoma31/geant-scripts/geant4-11.1.1/clear_build
export SOURCE_DIR=/home/sthoma31/edep/build_22

#cd $BUILD_DIR
mkdir -p energies_ar39
cd energies_ar39

energy_arr=(5.751284044776426 18.664196751895858 31.842686762190922 44.55096270479088 57.62222622755884 70.70440338773419 83.79258304848354 96.88621952793657 109.9880412354451 123.09531976165731 136.20750942470278 149.32679295206304 162.4520789799974 175.58336750850572 188.7233869469399 201.8688632040778 215.0236160530119 228.18600844813113 241.35767743504664 254.53534892253617 267.72502541117376 280.1222505614008 298.1364217285897 313.86395163189997 330.6566859476013 343.25123668437726 354.4861821174716 368.78858189434015 381.4589329469496 392.93191246080875 404.4058923914302 416.4907267971359 427.97517775653654 438.8537096302136 449.7355762264319 460.6151085168713 472.0960913648292 484.1785247703054 496.24835292457607 508.91004582484237 522.1551999703007 535.3781630530306 547.3729175082027)



for val in ${energy_arr[*]}
do
    echo "Starting now..."
    echo $val
    mkdir -p $val
    cd $val
    cp $SOURCE_DIR/run_ar39.mac .
    new_energy='s/ENERGY/$val/g'
    eval sed -i $new_energy run_ar39.mac
    cp ../../test_copied.gdml .
    bash ../../run_edep_ar39.sh 10


    # only keep data
    #sed -n '/EveTraParXYZdEProc/w EveTraParXYZdEProc.csv' run.txt
    # remove stuff until first comma
    #eval sed -i 's/[^,]*,//' EveTraParXYZdEProc.csv #EveTraParXYZdEProc.csv
    #rm run.txt steps.txt
    python ../../hitsegments.py
    echo "Done. "
    cd ../
done

