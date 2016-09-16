#!/usr/bin/env python
from stack_nonResDD import *

dotest=False
met=200
var='mt'
blind=False
blindCut=0

#--> mtc in these samples == the latter default 'llnunu_mt'
mtxbins = [150,200,250,300,350,400,450,550,850]
if var=='mt':
   if met>100:      blind=True;blindCut=400.0;
   toplot={('llnunu_mtc', 'elmununu_mtc'):(len(mtxbins), min(mtxbins), max(mtxbins), "M_{T}^{ZZ}", "GeV", 0, 0, mtxbins)} 
   #toplot={('llnunu_mtc', 'elmununu_mtc'):(50, 200, 1200, "M_{T}^{ZZ}", "GeV", 0 , 0, [])}
elif var=='mZ': toplot={('llnunu_l1_mass', 'elmununu_l1_mass'): (8, 70.0, 110.0, "M_{Z}^{ll}", "GeV", 70.0, 110.0, [])}
elif var=='met': toplot={('llnunu_l2_pt', 'elmununu_l2_pt'): (50, 0.0, 500.0, "E_{T}^{miss}", "GeV", 0.0, 500.0, [])}
else: print "Error var!!"; exit(0);
        
if dotest: # met cut at 100
   test=StackDataDriven(indir="./nonResSkim_v3.2_light", scaleElMu=True, met=100)
   for var in toplot:
      test.doClosureTest(var[0], var[1], toplot[var][0], toplot[var][1], toplot[var][2], toplot[var][3], toplot[var][4],
                         xcutmin=toplot[var][5], xcutmax=toplot[var][6], xbins=toplot[var][7])

else:
   
   if met==0: t=StackDataDriven(indir="./nonResSkim_v3.1", side='both')
   elif met==100: t=StackDataDriven(indir="./nonResSkim_v3.2", met=100, side='both')
   elif met==200: t=StackDataDriven(indir="./nonResSkim_v3.3", met=200, side='right')
   else:
      print "Error met!"
      exit(0)

   for var in toplot:
      #t.compareDataDrivenMC(var[0], var[1], toplot[var][0], toplot[var][1], toplot[var][2], toplot[var][3], toplot[var][4],
      #                      xcutmin=toplot[var][5], xcutmax=toplot[var][6])
      t.drawMCStack(var[0], var[1], toplot[var][0], toplot[var][1], toplot[var][2], toplot[var][3], toplot[var][4],
                    xbins = toplot[var][7], blind=blind, blindCut=blindCut)  

      #t.drawDataDrivenStack(var[0], var[1], toplot[var][0], toplot[var][1], toplot[var][2], toplot[var][3], toplot[var][4],
      #                      xcutmin=toplot[var][5], xcutmax=toplot[var][6], xbins = mtxbins, blind=blind, blindCut=blindCut)
