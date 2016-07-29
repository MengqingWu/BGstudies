#!/usr/bin/env python
from stack_zjets import *

t=StackZjetsDD( indir_dd="./METSkim_v4", zpt_cut='100', met_cut= '50',scaleDphi=True)
t.drawDataDrivenStack()

#rab, rac, rad= t.getYieldCorr()
#t.getAllmcRegA()
#t.ValidateDphiShapeCorr("./METSkim_v5", whichvar='fabsDphi',isNormalized=True, yieldCorr=False, whichbcd='ZJets', scaleDphi=False, onlyStats=False)
#t.ValidateDphiShapeCorr("./METSkim_v5", whichvar='met',     isNormalized=True, yieldCorr=False, whichbcd='ZJets', scaleDphi=False, onlyStats=False)
#t.ValidateDphiShapeCorr("./METSkim_v5", whichvar='mt',      isNormalized=True, yieldCorr=False, whichbcd='ZJets', scaleDphi=False, onlyStats=False)
#t.ValidateDphiShapeCorr("./METSkim_v5", whichvar='zpt',     isNormalized=True, yieldCorr=False, whichbcd='ZJets', scaleDphi=False, onlyStats=False)
#t.ValidateDphiShapeCorr("./METSkim_v5", whichvar='metzpt',     isNormalized=True, yieldCorr=False, whichbcd='ZJets', scaleDphi=False, onlyStats=False)
