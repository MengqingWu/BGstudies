#!/usr/bin/env python
from stack_nonResDD import *
import sys

test=StackDataDriven(indir="./nonResSkim_Lite_20160915_met100", outdir="./closure_step2", scaleElMu=True, met=100, side="both")
#test.GetAlpha(isTest=True)
mtxbins = [150,200,250,325,425,850]
test.drawDataDrivenStack('llnunu_mtc', 'elmununu_mtc', len(mtxbins), min(mtxbins), max(mtxbins), "M_{T}^{ZZ}", "GeV", 0, 0, mtxbins, doSysErr=True)
exit(0)

print 'Number of arguments:', len(sys.argv), 'arguments.'
print 'Argument List:', str(sys.argv)

if len(sys.argv)<3:
   print "Usage: ./run.py met_cut var_to_draw (sideband='both') (doMzWt=True) (dotest=False)\n EXIT!"
   exit(0)
met = float(sys.argv[1]) #1
var = sys.argv[2] #2
sideband = 'both' #3
if len(sys.argv)>3 and sys.argv[3] in ['both', 'right']:
   sideband = sys.argv[3]
doMzWt = True #4
if len(sys.argv)>4 and sys.argv[4] in ['0','false','False','no']:
   doMzWt = False
dotest = False #5
if len(sys.argv)>5 and sys.argv[5] in ['1','true','True','yes']:
   dotest = True

#print met, var, doMzWt, dotest

#--> pre-set value not changed:
blind=False; blindCut=0;
#mtxbins = [150,200,250,300,350,400,450,550,850]
mtxbins = [150,200,250,325,425,850]

#--> mtc in these samples == the latter default 'llnunu_mt'
if var=='mt':
   if met>100:      blind=True; blindCut=400.0;
   toplot={('llnunu_mtc', 'elmununu_mtc'):(len(mtxbins), min(mtxbins), max(mtxbins), "M_{T}^{ZZ}", "GeV", 0, 0, mtxbins)} 
   #toplot={('llnunu_mtc', 'elmununu_mtc'):(50, 200, 1200, "M_{T}^{ZZ}", "GeV", 0 , 0, [])}
elif var in ['mZ','mz']: toplot={('llnunu_l1_mass', 'elmununu_l1_mass'): (8, 70.0, 110.0, "M_{Z}^{ll}", "GeV", 70.0, 110.0, [])}
elif var=='met': toplot={('llnunu_l2_pt', 'elmununu_l2_pt'): (50, 0.0, 500.0, "E_{T}^{miss}", "GeV", 0.0, 500.0, [])}
else: print "Error var!!"; exit(0);
        
if dotest: # met cut at 100
   #if met==0: test=StackDataDriven(indir="./nonResSkim_v3.2_light", scaleElMu=True, met=100)
   if met==0: test=StackDataDriven(indir="./nonResSkim_Lite_20160915_met0", outdir="./closure_step2", scaleElMu=doMzWt, side=sideband)
   elif met==100: test=StackDataDriven(indir="./nonResSkim_Lite_20160915_met100", outdir="./closure_step2", scaleElMu=doMzWt, met=100, side=sideband)
   elif met==200: test=StackDataDriven(indir="./nonResSkim_Lite_20160915_met200", outdir="./closure_step2", scaleElMu=doMzWt, met=200, side=sideband)
   else:
      print "Error met!"
      exit(0)
      
   for var in toplot:
      test.doClosureTest(var[0], var[1], toplot[var][0], toplot[var][1], toplot[var][2], toplot[var][3], toplot[var][4],
                         xcutmin=toplot[var][5], xcutmax=toplot[var][6], xbins=toplot[var][7])

else:
   
   if met==0: t=StackDataDriven(indir="./nonResSkim_Lite_20160915_met0", outdir="./out_step2", scaleElMu=True, side=sideband)
   elif met==100: t=StackDataDriven(indir="./nonResSkim_Lite_20160915_met100", outdir="./out_step2", scaleElMu=True, met=100, side=sideband)
   elif met==200: t=StackDataDriven(indir="./nonResSkim_Lite_20160915_met200", outdir="./out_step2", scaleElMu=True, met=200, side=sideband)
   else:
      print "Error met!"
      exit(0)

   for var in toplot:
      t.compareDataDrivenMC(var[0], var[1], toplot[var][0], toplot[var][1], toplot[var][2], toplot[var][3], toplot[var][4],
                            xcutmin=toplot[var][5], xcutmax=toplot[var][6], xbins=toplot[var][7])
      t.drawMCStack(var[0], var[1], toplot[var][0], toplot[var][1], toplot[var][2], toplot[var][3], toplot[var][4],
                    xbins = toplot[var][7], blind=blind, blindCut=blindCut)  

      t.drawDataDrivenStack(var[0], var[1], toplot[var][0], toplot[var][1], toplot[var][2], toplot[var][3], toplot[var][4],
                            xcutmin=toplot[var][5], xcutmax=toplot[var][6], xbins = toplot[var][7], blind=blind, blindCut=blindCut)
