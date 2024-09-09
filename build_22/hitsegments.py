#! /usr/bin/env python
#
# Read almost every field in the event tree.
#

from __future__ import print_function
import glob, os, re, sys, getopt
from ROOT import *
gSystem.Load("libedepsim_io.so")
from ROOT import TG4Event


def is_eioni(pt):
    if pt.GetProcess() == 2 and pt.GetSubprocess() == 2:
        val = 2
    else:
        val =  0
    return val



def printTrajectoryPoint(depth, trajectoryPoint, trajectory):
    print(depth,"Class: ", trajectoryPoint.ClassName())
    event_num = event.EventId
    print(depth,"Position:", trajectoryPoint.GetPosition().X(),
          trajectoryPoint.GetPosition().Y(),
          trajectoryPoint.GetPosition().Z(),
          trajectoryPoint.GetPosition().T())
    temp_string = "{}, {}, {}, {}, {}, {}, {}, {} \n".format(event_num, trajectory.GetTrackId(), trajectory.GetPDGCode(), trajectoryPoint.GetPosition().X(), trajectoryPoint.GetPosition().Y(), trajectoryPoint.GetPosition().Z(), trajectoryPoint.GetProcess(), trajectoryPoint.GetSubprocess())
    tracks.write(temp_string)
    print(depth,"Momentum:", trajectoryPoint.GetMomentum().X(),
          trajectoryPoint.GetMomentum().Y(),
          trajectoryPoint.GetMomentum().Z(),
          trajectoryPoint.GetMomentum().Mag())
    print(depth,"Process",trajectoryPoint.GetProcess())
    print(depth,"Subprocess",trajectoryPoint.GetSubprocess())

# Print the fields in a TG4Trajectory object
def printTrajectory(depth, trajectory):
    print(depth,"Class: ", trajectory.ClassName())
    depth = depth + ".."
    print(depth,"Track Id/Parent Id:",
          trajectory.GetTrackId(),
          trajectory.GetParentId())
    print(depth,"Name:",trajectory.GetName())
    print(depth,"PDG Code",trajectory.GetPDGCode())
    print(depth,"Initial Momentum:",trajectory.GetInitialMomentum().X(),
          trajectory.GetInitialMomentum().Y(),
          trajectory.GetInitialMomentum().Z(),
          trajectory.GetInitialMomentum().E(),
          trajectory.GetInitialMomentum().P(),
          trajectory.GetInitialMomentum().M())
    for trajectoryPoint in trajectory.Points:
        printTrajectoryPoint(depth,trajectoryPoint, trajectory)


# Print the fields in a TG4HitSegment object
def printHitSegment(depth, hitSegment):
    event_num = event.EventId
    print(depth,"Class: ", hitSegment.ClassName())
    print(depth,"Primary Id:", hitSegment.GetPrimaryId());
    print(depth,"Energy Deposit:",hitSegment.GetEnergyDeposit())
    print(depth,"Secondary Deposit:", hitSegment.GetSecondaryDeposit())
    print(depth,"Track Length:",hitSegment.GetTrackLength())
    print(depth,"Start:", hitSegment.GetStart().X(),
          hitSegment.GetStart().Y(),
          hitSegment.GetStart().Z(),
          hitSegment.GetStart().T())
    print(depth,"Stop:", hitSegment.GetStop().X(),
          hitSegment.GetStop().Y(),
          hitSegment.GetStop().Z(),
          hitSegment.GetStop().T())
    contrib = [contributor for contributor in hitSegment.Contrib]
    if event.Trajectories[contrib[-1]].GetPDGCode() == 11:
        hits.write("{}, {}, {}, {}, {}, {}, {}, {}, {}, {} \n".format(event_num, contrib[-1], hitSegment.GetStart().X(), hitSegment.GetStart().Y(), hitSegment.GetStart().Z(), hitSegment.GetStop().X(), hitSegment.GetStop().Y(), hitSegment.GetStop().Z(), hitSegment.GetEnergyDeposit(),  hitSegment.GetTrackLength()))
    
    print(depth,"Contributor:", [contributor for contributor in hitSegment.Contrib])
    if len(contrib) > 1:
        print("Multiple contributors")
    

    
    for i in [contrib[-1]]:
        
        
        num_traj = len(event.Trajectories[i].Points)
        print("event number: ", event.EventId)
        event_num = event.EventId
        particle = event.Trajectories[i].GetPDGCode()
        if num_traj:# <= 2:
            point_list = event.Trajectories[i].Points
            for step, pt in enumerate(point_list):
                if step == 0:
                    continue
                else:
                    x, y, z = pt.GetPosition().X(), pt.GetPosition().Y(), pt.GetPosition().Z()
                    xi, yi, zi = point_list[step - 1].GetPosition().X(), point_list[step - 1].GetPosition().Y(), point_list[step - 1].GetPosition().Z()
                    sxi, syi, szi = hitSegment.GetStart().X(), hitSegment.GetStart().Y(), hitSegment.GetStart().Z()
                    sxf, syf, szf = hitSegment.GetStop().X(), hitSegment.GetStop().Y(), hitSegment.GetStop().Z()

                    my_file.write("{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {} \n".format(event_num, i, particle, pt.GetPosition().X(), pt.GetPosition().Y(), pt.GetPosition().Z(), hitSegment.GetEnergyDeposit(), is_eioni(pt), xi, yi, zi, event.Trajectories[i].GetParentId()))
                
                    # if xyz != segxyz:
                #   edep = 0.0
                #elif xyz == segxyz:
                #   realedep 
                #print(depth, "Track ID: ", event.Trajectories[contributor[0]].GetTrackId())
# Print the fields in a single element of the SegmentDetectors map.
# The container name is the key, and the hitSegments is the value (a
# vector of TG4HitSegment objects).
def printSegmentContainer(depth, containerName, hitSegments):
    print(depth,"Detector: ", containerName, hitSegments.size())
    depth = depth + ".."
    for hitSegment in hitSegments: printHitSegment(depth, hitSegment)



# Read a file and dump it.
def main(argv=None):
    if argv is None:
        argv = sys.argv

    # The input file is generated in a previous test (100TestTree.sh).
    inputFile=TFile("my-output.root")

    outputFile="output.txt"# Open a file for writing
    global my_file
    my_file = open(outputFile, "w")

    outputhits = "hits.txt"

    global hits
    hits = open(outputhits, "w")
    # Get the input tree out of the file.
    inputTree=inputFile.Get("EDepSimEvents")
    print("Class:",inputTree.ClassName())

    global tracks
    tracks = open("tracks.txt", "w")

    global ms
    global ss

    ms = open("ms.txt", "w")
    ss = open("ss.txt", "w")
    
    # Attach a brach to the events.
    global event;
    event = TG4Event()
    inputTree.SetBranchAddress("Event",event)

    
    # Read all of the events.
    entries=inputTree.GetEntriesFast()
    for jentry in xrange(entries):
        nb = inputTree.GetEntry(jentry)
        if nb<=0: continue
        for containerName, hitSegments in event.SegmentDetectors:
            printSegmentContainer("HH", containerName, hitSegments)
        my_file.write("\n")
        for trajectory in event.Trajectories:
            printTrajectory("TT",trajectory)
    my_file.close()
    hits.close()
    tracks.close()
    ms.close()
    ss.close()
if __name__ == "__main__":
    
    sys.exit(main())
    
