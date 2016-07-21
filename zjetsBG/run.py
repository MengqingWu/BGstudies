#!/usr/bin/env python
from stack_zjets import *

t=StackZjetsDD( indir_dd="./METSkim_v5", zpt_cut='100', met_cut= '50',scaleDphi=True)
#rab, rac, rad= t.getYieldCorr()
#t.getAllmcRegA()
#t.drawDataDrivenStack()
#t.ValidateDphiShapeCorr("./METSkim_v5", whichvar='fabsDphi',isNormalized=False, yieldCorr=True, whichbcd='ZJets', scaleDphi=True, onlyStats=False)
#t.ValidateDphiShapeCorr("./METSkim_v5", whichvar='met',     isNormalized=False, yieldCorr=True, whichbcd='ZJets', scaleDphi=True, onlyStats=False)
#t.ValidateDphiShapeCorr("./METSkim_v5", whichvar='mt',      isNormalized=False, yieldCorr=True, whichbcd='ZJets', scaleDphi=True, onlyStats=False)
#t.ValidateDphiShapeCorr("./METSkim_v5", whichvar='zpt',     isNormalized=False, yieldCorr=True, whichbcd='ZJets', scaleDphi=True, onlyStats=False)
t.ValidateDphiShapeCorr("./METSkim_v5", whichvar='metzpt',     isNormalized=True, yieldCorr=False, whichbcd='ZJets', scaleDphi=False, onlyStats=False)
