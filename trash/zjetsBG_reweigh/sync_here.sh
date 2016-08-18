#!/bin/sh
dir=$LOC/workarea/BGstudies
#scp $dir/zjetsBG/output/stacker/*eps ./output/stacker/
#scp $dir/zjetsBG/output/stacker/*pdf ./output/stacker/

rsync -vrac  mewu@lxplus.cern.ch:$dir/zjetsBG/output/stacker/ ./output/stacker/
#rsync -vrac  mewu@lxplus.cern.ch:$dir/zjetsBG/num_out.txt .
