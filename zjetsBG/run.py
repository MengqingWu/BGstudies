#!/usr/bin/env python
from python.abcd import *

#t=abcdAnalyzer(indir="../../AnalysisRegion_zjets")

#t.draw_A() # for VR
#t.draw_A(True) 
#t.draw_BCD()

b=abcdAnalyzer(indir="./METSkim", addSig=True, addData=True, doRatio=True, doMetCorr=True)
b.draw_A(True) 
b.draw_BCD()
