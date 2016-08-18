#!/bin/sh
dir=/afs/cern.ch/work/m/mewu/CMSSW_7_6_3_patch2/src/CMGTools/XZZ2l2nu/workarea/BGstudies/extraPlotters
#rsync -vrac  mewu@lxplus.cern.ch:$dir/output .
rsync -vrac  mewu@lxplus.cern.ch:$dir/dphi_zmet_100zpt50met_red_dphijetMetB_blue_dphijetMetA.pdf .
