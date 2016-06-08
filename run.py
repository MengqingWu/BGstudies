#!/usr/bin/env python

from python.abcd import *

#t=abcdAnalyzer(indir="../AnalysisRegion",addSig=False)

#t.draw_A() # for VR
#t.draw_A(True) 
#t.draw_BCD()

b=abcdAnalyzer(indir="../AnalysisRegion",addSig=False, addData=False,doRatio=False)
b.draw_A(True) 
