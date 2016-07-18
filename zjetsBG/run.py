#!/usr/bin/env python
from stack_zjets import *

t=StackZjetsDD(zpt_cut='100', met_cut= '50')
# t.drawDataDrivenStack()
t.ValidateDphiShapeCorr("./METSkim_v5", whichvar='fabsDphi', isNormalized=True, whichbcd='ZJets',scaleDphi=True,onlyStats=False)
t.ValidateDphiShapeCorr("./METSkim_v5", whichvar='met', isNormalized=True, whichbcd='ZJets',scaleDphi=True,onlyStats=False)
t.ValidateDphiShapeCorr("./METSkim_v5", whichvar='mt', isNormalized=True, whichbcd='ZJets',scaleDphi=True,onlyStats=False)
t.ValidateDphiShapeCorr("./METSkim_v5", whichvar='zpt', isNormalized=True, whichbcd='ZJets',scaleDphi=True,onlyStats=False)
