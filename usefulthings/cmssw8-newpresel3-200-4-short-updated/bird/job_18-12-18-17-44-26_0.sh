#!/bin/zsh
echo "$QUEUE $JOB $HOST"
source /cvmfs/cms.cern.ch/cmsset_default.sh
export SCRAM_ARCH=slc6_amd64_gcc530
cd /afs/desy.de/user/k/kutznerv/cmssw/CMSSW_8_0_28/src
#cmsenv
eval `scramv1 runtime -sh`
echo $CMSSW_BASE
cd /nfs/dust/cms/user/kutznerv/shorttrack/cutoptimization/tmva/newpresel3-200-4-short-updated
./runTMVA.sh
if [ $? -eq 0 ]
then
    echo "Success"
else
    echo "Failed"
fi
