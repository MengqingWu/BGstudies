#!/usr/bin/env python
from stack_zjets import *

t=StackZjetsDD(zpt_cut='100', met_cut= '50')
# t.drawDataDrivenStack()
t.ValidateDphiShapeCorr(whichvar='fabsDphi', isNormalized=True, whichbcd='ZJets',scaleDphi=True,onlyStats=False)
t.ValidateDphiShapeCorr(whichvar='met', isNormalized=True, whichbcd='ZJets',scaleDphi=True,onlyStats=False)
t.ValidateDphiShapeCorr(whichvar='mt', isNormalized=True, whichbcd='ZJets',scaleDphi=True,onlyStats=False)
t.ValidateDphiShapeCorr(whichvar='zpt', isNormalized=True, whichbcd='ZJets',scaleDphi=True,onlyStats=False)
