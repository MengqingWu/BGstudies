#!/usr/bin/env python
from ROOT import *
import math, os, sys, copy
from  itertools import product
#sys.path.append('/Users/mengqing/work/local_xzz2l2nu/python')
from python.SimplePlot import *
from python.abcd import *

abcd=abcdAnalyzer(indir='../zjetsSkim',addSig=False)
outDir='plots/shape'
if not os.path.exists(outDir): os.system('mkdir '+outDir)
pair=[('SR','CRb'), ('CRc','CRd'), ('SR','CRc'), ('CRb','CRd')]

Tag=abcd.Channel+abcd.whichregion
Var=('llnunu_l2_pt','llnunu_mta')
isData=True
lumi=2.318278305
parameter={'llnunu_l2_pt': ('E_{T}^{miss}',25,0,500), 'llnunu_mta': ('M_{T}',17, 100.0,780)}

print abcd.cuts

for p, var in product(pair, Var):
    x, y=p[0], p[1]
    Lumi="1" if isData else str(lumi*1000)

    xMax=abcd.xMax if abcd.whichregion=="VR" and var=='llnunu_l2_pt' else parameter[var][3]
    xMin=parameter[var][2]

    h_var_dt1=abcd.plotter.Data.drawTH1('h_var_dt1',var,abcd.cuts[x],"1",parameter[var][1],parameter[var][2],parameter[var][3],titlex=parameter[var][0] ,drawStyle="HIST")
    h_var_dt1_tosub=abcd.plotter.NonZBG.drawTH1('h_var_dt1_tosub',var,abcd.cuts[x],str(lumi*1000),parameter[var][1],parameter[var][2],parameter[var][3],titlex=parameter[var][0] ,drawStyle="HIST")
    
    h_var_dt2=abcd.plotter.Data.drawTH1('h_var_dt2',var,abcd.cuts[y],"1",parameter[var][1],parameter[var][2],parameter[var][3],titlex=parameter[var][0],drawStyle="HIST")
    h_var_dt2_tosub=abcd.plotter.NonZBG.drawTH1('h_var_dt2_tosub',var,abcd.cuts[y],str(lumi*1000),parameter[var][1],parameter[var][2],parameter[var][3],titlex=parameter[var][0],drawStyle="HIST")

    print "%r, data: %r = %r; %r = %r\n" % (var, x, h_var_dt1.Integral(), y, h_var_dt2.Integral() )  
    print "%r, nonZ MC: %r = %r; %r = %r\n" % (var, x, h_var_dt1_tosub.Integral(), y, h_var_dt2_tosub.Integral() )  
    h_var_dt1.Add(h_var_dt1_tosub,-1)
    h_var_dt1.Scale(1./h_var_dt1.Integral())

    h_var_dt2.Add(h_var_dt1_tosub,-1)    
    h_var_dt2.Scale(1./h_var_dt2.Integral())

    drawCompareSimple(h_var_dt1, h_var_dt2, abcd.tex_dic[x], abcd.tex_dic[y],
                      xmin=xMin, xmax=xMax, outdir=outDir, notes=abcd.Channel+abcd.whichregion+'from Data',
                      tag=var+'_'+Tag+'_'+x+'_'+y+'_dt', units='GeV', ytitle='normalized')

    
    h_var_mc1=abcd.plotter.ZJets.drawTH1('h_var_mc1',var,abcd.cuts[x],str(lumi*1000),parameter[var][1],parameter[var][2],parameter[var][3],titlex=parameter[var][0],drawStyle="HIST")
    h_var_mc2=abcd.plotter.ZJets.drawTH1('h_var_mc2',var,abcd.cuts[y],str(lumi*1000),parameter[var][1],parameter[var][2],parameter[var][3],titlex=parameter[var][0],drawStyle="HIST")
    
    print "%r, MC: %r = %r; %r = %r\n" % (var, x, h_var_mc1.Integral(), y, h_var_mc2.Integral() )
    h_var_mc1.Scale(1./h_var_mc1.Integral())
    h_var_mc2.Scale(1./h_var_mc2.Integral())
        
    drawCompareSimple(h_var_mc1, h_var_mc2, abcd.tex_dic[x], abcd.tex_dic[y],
                      xmin=xMin, xmax=xMax, outdir=outDir, notes=abcd.Channel+abcd.whichregion+'from Zjets MC',
                      tag=var+'_'+Tag+'_'+x+'_'+y+'_mc', units='GeV', ytitle='normalized')  

for v in Var:
    os.system('gs -dBATCH -dNOPAUSE -q -sDEVICE=pdfwrite -sOutputFile='+outDir+'/compare_'+v+'_'+Tag+'_'+'all.pdf '+outDir+'/*'+v+'_'+Tag+'*.eps')
