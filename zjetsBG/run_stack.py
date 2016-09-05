#!/usr/bin/env python
from stack_zjets import *

t=StackZjetsDD(indir="./inds", channel='inclusive', whichregion='VR',zpt_cut='100', met_cut= '100')
#t.GetYieldCorr()
t.drawDataDrivenStack()
#t.GetAllmcRegA()
#rab, rac, rad= t.getYieldCorr()

# for i in ['fabsDphi', 'met', 'mt', 'zpt', 'metzpt']:
#     t.ValidateDphiShapeCorr("./METSkim_v4.0", whichvar=i, isNormalized=True, yieldCorr=True, whichbcd='ZJets',
#                             scaleDphi=True, onlyStats=True, logy=False, suffix='nonLogy')

#t.ValidateDphiShapeCorr("./METSkim_v5", whichvar='metzpt',  isNormalized=True, yieldCorr=False, whichbcd='ZJets', scaleDphi=False, onlyStats=False)
