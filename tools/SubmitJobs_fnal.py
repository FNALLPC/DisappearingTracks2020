import os, sys


defaultInfile = "/eos/uscms/store/user/cmsdas/2020/long_exercises/DisappearingTracks/BackgroundEstimate/Run2016C-17Jul2018-v1.SingleMuonAOD_50000-C0DD97F4-E47F-E711-B9E4-001E67E71C04_RA2AnalysisTree.root"

defaultkey = defaultInfile.split('/')[-1].split('.root')[0]
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbosity", type=bool, default=False,help="analyzer script to batch")
parser.add_argument("-analyzer", "--analyzer", type=str,default='tools/ResponseMaker.py',help="analyzer")
parser.add_argument("-fin", "--fnamekeyword", type=str,default=defaultInfile,help="file")
parser.add_argument("-dtmode", "--dtmode", type=str, default='PixAndStrips',help="PixAndStrips, PixOnly, PixOrStrips")
parser.add_argument("-pu", "--pileup", type=str, default='Nom',help="Nom, Low, Med, High")
args = parser.parse_args()
fnamekeyword = args.fnamekeyword
dtmode = args.dtmode
analyzer = args.analyzer
pileup = args.pileup
    
istest = False

try: 
	moreargs = ' '.join(sys.argv)
	moreargs = moreargs.split('--fnamekeyword')[-1]	
	moreargs = ' '.join((moreargs.split()[1:]))
except: moreargs = ''

moreargs = moreargs.strip()
print 'moreargs', moreargs



cwd = os.getcwd()

fnamefilename = 'usefulthings/filelist.txt'
print 'fnamefilename', fnamefilename
fnamefile = open(fnamefilename)
fnamelines = fnamefile.readlines()
fnamefile.close()
import random
random.shuffle(fnamelines)

def main():
    for fname_ in fnamelines:
        if not (fnamekeyword in fname_): continue
        fname = fname_.strip()
        job = analyzer.split('/')[-1].replace('.py','').replace('.jdl','')+'-'+fname.strip()+dtmode
        job = job.replace('.root','')
        #print 'creating jobs:',job
        newjdl = open('jobs/'+job+'.jdl','w')
        newjdl.write(jdltemplate.replace('CWD',cwd).replace('JOBKEY',job))
        newjdl.close()
        newsh = open('jobs/'+job+'.sh','w')
        newshstr = shtemplate.replace('ANALYZER',analyzer).replace('FNAMEKEYWORD',fname).replace('MOREARGS',moreargs)
        newsh.write(newshstr)
        newsh.close()
        os.chmod('jobs/'+job+'.sh',0755)
        if not os.path.exists('output/'+fnamekeyword.replace(' ','')): 
            os.system('mkdir output/'+fnamekeyword.replace(' ',''))
        os.chdir('output/'+fnamekeyword.replace(' ',''))
        cmd =  'condor_submit '+'../../jobs/'+job+'.jdl'        
        print cmd
        os.system(cmd)
        os.chdir('../../')
        if istest: break


jdltemplate = '''
universe = vanilla
Executable = CWD/jobs/JOBKEY.sh
Output = CWD/jobs/JOBKEY.out
Error = CWD/jobs/JOBKEY.err
Log = CWD/jobs/JOBKEY.log
+REQUIRED_OS = "rhel7"
+DesiredOS = REQUIRED_OS
Should_Transfer_Files = YES
WhenToTransferOutput = ON_EXIT_OR_EVICT
transfer_input_files=CWD/tools, CWD/usefulthings 
x509userproxy = $ENV(X509_USER_PROXY)
want_graceful_removal = true
on_exit_remove = (ExitBySignal == False) && (ExitCode == 0)
on_exit_hold = ( (ExitBySignal == True) || (ExitCode != 0) )
on_exit_hold_reason = strcat("Job held by ON_EXIT_HOLD due to ",\
                    ifThenElse((ExitBySignal == True), "exit by signal", \
strcat("exit code ",ExitCode)), ".")
Queue 1
'''



shtemplate = '''#!/bin/bash
source /cvmfs/cms.cern.ch/cmsset_default.sh
export SCRAM_ARCH=slc7_amd64_gcc700
echo $PWD
ls
scram project CMSSW_10_6_4
cd CMSSW_10_6_4/src
eval `scramv1 runtime -sh`
cd ${_CONDOR_SCRATCH_DIR}
echo $PWD
ls
python ANALYZER --fnamekeyword FNAMEKEYWORD MOREARGS
'''

main()
print 'done'


