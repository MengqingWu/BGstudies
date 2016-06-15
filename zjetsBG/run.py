#!/usr/bin/env python
import sys
sys.path.append('/Users/mengqing/work/local_xzz2l2nu/python')
from abcd import *

#t=abcdAnalyzer(indir="../../AnalysisRegion_zjets")

#t.draw_A() # for VR
#t.draw_A(True) 
#t.draw_BCD()

b=abcdAnalyzer(indir="../../AnalysisRegion_zjets", addSig=True, addData=False,doRatio=False)
b.draw_A(True) 
