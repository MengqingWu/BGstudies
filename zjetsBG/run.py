#!/usr/bin/env python
from python.abcd import *

#t=abcdAnalyzer(indir="../../AnalysisRegion_zjets")

#t.draw_A() # for VR
#t.draw_A(True) 
#t.draw_BCD()

b=abcdAnalyzer(indir="../../AnalysisRegion_zjets", addSig=True, addData=False,doRatio=False)
b.draw_A(True) 
