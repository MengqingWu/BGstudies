#!/usr/bin/env python
from stack_zjets import *

t=StackZjetsDD(zpt_cut='100', met_cut= '50')
# t.drawDataDrivenStack()
t.ValidateDphiShapeCorr(whichvar='fabsDphi', isNormalized=False, whichbcd='ZJets',scaleDphi=True)
t.ValidateDphiShapeCorr(whichvar='met', isNormalized=False, whichbcd='ZJets',scaleDphi=True)
t.ValidateDphiShapeCorr(whichvar='mt', isNormalized=False, whichbcd='ZJets',scaleDphi=True)
t.ValidateDphiShapeCorr(whichvar='zpt', isNormalized=False, whichbcd='ZJets',scaleDphi=True)
