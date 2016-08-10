#!/bin/sh
dir=$LOC/workarea/BGstudies
rsync -vrac  mewu@lxplus.cern.ch:$dir/zjetsBG/plots .
rsync -vrac  mewu@lxplus.cern.ch:$dir/zjetsBG/num_out.txt .
