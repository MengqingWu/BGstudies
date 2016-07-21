#!/usr/bin/env python

import ROOT
import os,copy
from python.TreePlotter import TreePlotter
from python.MergedPlotter import MergedPlotter
from python.myStackPlotter import StackPlotter
from python.SimplePlot import *
from python.SetCuts import SetCuts

##--- Setup: inputs
indir="./METSkim_v4"; outdir="output/newcut/"
CheckDir(outdir) # if not, this will create it
onlyStats=False;scaleDphi=False;LogY=True;doRatio=False;
sigk=1000; lumi=2.318278305;
lepsf='llnunu_l1_l1_lepsf*llnunu_l1_l2_lepsf'
triggersf='triggersf'
setcuts = SetCuts()
cuts = setcuts.abcdCuts(channel="inclusive", whichRegion="SR", isPreSelect=True, zpt_cut='100', met_cut='50')
##--- Initialize: plotter
zjetsPlotters=[]
zjetsSamples = ['DYJetsToLL_M50_BIG'] # M50_BIG = M50 + M50_Ext
         
for sample in zjetsSamples:
    zjetsPlotters.append(TreePlotter(indir+'/'+sample+'.root','tree'))
    if not onlyStats:
        zjetsPlotters[-1].addCorrectionFactor('1./SumWeights','tree')
        zjetsPlotters[-1].addCorrectionFactor('xsec','tree')
        #zjetsPlotters[-1].addCorrectionFactor('(1921.8*3)','xsec')
        zjetsPlotters[-1].addCorrectionFactor('genWeight','tree')
        zjetsPlotters[-1].addCorrectionFactor('puWeight','tree')
        zjetsPlotters[-1].addCorrectionFactor(triggersf,'tree')
        zjetsPlotters[-1].addCorrectionFactor(lepsf,'tree')
        if scaleDphi:
            zjetsPlotters[-1].addCorrectionFactor('dphi_sf','tree')# to scale dphi shape in BCD regions as the one in regA
ZJets = MergedPlotter(zjetsPlotters)
ZJets.setFillProperties(1001,ROOT.kGreen+2)
                                                                                                                                            
sigPoints=[600, 800, 1000, 1200, 1400, 1600, 1800,
           2000, 2500, 3000, 3500, 4000, 4500]
sigPlotters=[]
sigSamples = [ 'BulkGravToZZToZlepZinv_narrow_'+str(point) for point in sigPoints ]
sigSampleNames = [ str(sigk) + ' x BulkG-' + str(mass) for mass in sigPoints]

# sigXsec = {
#     'BulkGravToZZToZlepZinv_narrow_800'  : 4.42472e-04*sigk,
#     'BulkGravToZZToZlepZinv_narrow_1000' : 1.33926e-04*sigk,
#     'BulkGravToZZToZlepZinv_narrow_1200' : 4.76544e-05*sigk,
# }
for sample in sigSamples:
    sigPlotters.append(TreePlotter(indir+'/'+sample+'.root','tree'))
    if not onlyStats:
        sigPlotters[-1].addCorrectionFactor('1./SumWeights','tree')
        #sigPlotters[-1].addCorrectionFactor(str(sigXsec[sample]),'tree')
        sigPlotters[-1].addCorrectionFactor('genWeight','tree')
        sigPlotters[-1].addCorrectionFactor('puWeight','tree')
        sigPlotters[-1].addCorrectionFactor(triggersf,'tree')
        sigPlotters[-1].addCorrectionFactor(lepsf,'tree')
        sigPlotters[-1].setFillProperties(0,ROOT.kWhite)

Stack = StackPlotter()
Stack.addPlotter(ZJets, "ZJets","Z+Jets", "background")
for i in range(len(sigSamples)):
    sigPlotters[i].setLineProperties(2,ROOT.kRed+i,2)
    Stack.addPlotter(sigPlotters[i],sigSamples[i],sigSampleNames[i],'signal')

Stack.setLog(LogY)
Stack.doRatio(doRatio)

##--- Execute: plotting
ROOT.gROOT.ProcessLine('.x ../src/tdrstyle.C')
Stack.drawComp('(llnunu_l1_pt+met_para)/llnunu_l1_pt', cuts, 
               10, -5.0, 5.0, titlex = "(p_{T}^{Z}+E_{T,para}^{miss})/p_{T}^{Z}", units = "GeV",
               output=outdir+"newcut.pdf")
