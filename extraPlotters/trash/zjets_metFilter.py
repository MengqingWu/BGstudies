#!/usr/bin/env python

import ROOT
import os
from math import *
from python.TreePlotter import TreePlotter
from python.MergedPlotter import MergedPlotter
from python.StackPlotter import StackPlotter
from python.SimplePlot import *

outdir='metFilter'
indir="/afs/cern.ch/work/m/mewu/public/76X_new"
#indir="../AnalysisRegion/"
lumi=2.169126704526

if not os.path.exists(outdir): os.system('mkdir '+outdir)

tag = 'metFilter_log'
outTag=outdir+'/'+tag

metFilter='(Flag_eeBadScFilter==1&&Flag_goodVertices==1&&Flag_EcalDeadCellTriggerPrimitiveFilter==1&&Flag_CSCTightHalo2015Filter==1&&Flag_HBHENoiseIsoFilter==1&&Flag_HBHENoiseFilter==1)'
#metFilter='1'
ptCut='(llnunu_l1_pt>100.0)'

cuts = {0: ['no metFilter', '1'],
        1: ['metFilter only', metFilter],
        2: ['only p_{T}^{Z}>100GeV', ptCut],
        3: ['metFilter+p_{T}^{Z}>100GeV', '('+metFilter+'&&'+ptCut+')']}

### ----- Initialize (samples):

zjetsPlotters=[]
zjetsSamples = ['DYJetsToLL_M50'] # M50_BIG = M50 + M50_Ext, 150M evts

for sample in zjetsSamples:
    zjetsPlotters.append(TreePlotter(indir+'/'+sample+'/vvTreeProducer/tree.root','tree'))
    zjetsPlotters[-1].setupFromFile(indir+'/'+sample+'/skimAnalyzerCount/SkimReport.txt')
    #zjetsPlotters.append(TreePlotter(indir+'/'+sample+'.root','tree'))
    #zjetsPlotters[-1].addCorrectionFactor('1./SumWeights','tree')
    zjetsPlotters[-1].addCorrectionFactor('xsec','tree')
    zjetsPlotters[-1].addCorrectionFactor('genWeight','tree')
    zjetsPlotters[-1].addCorrectionFactor('puWeight','tree')

ZJets = MergedPlotter(zjetsPlotters)
ZJets.setFillProperties(1001,ROOT.kGreen+2)

### ----- Execute (plotting):

ROOT.gROOT.ProcessLine('.x tdrstyle.C')
ROOT.gStyle.SetPadBottomMargin(0.2)
ROOT.gStyle.SetPadLeftMargin(0.15)

fout = ROOT.TFile(outTag+'.root','recreate')

# MET:

histo_arr=[ ZJets.drawTH1('met_pt',cuts[i][1],str(lumi*1000),50,0,1000,titlex='E_{T}^{miss}',units='GeV',drawStyle="HIST") for i in range(4)]
for x, y in zip(histo_arr, cuts):
    x.SetName(cuts[y][0])
    x.Write()


def mycompare(num1, num2, outdir, tag):
    histo_arr[num1].SetLineColor(ROOT.kRed)
    histo_arr[num1].SetFillColor(ROOT.kRed)
    histo_arr[num2].SetMarkerStyle(20)
    histo_arr[num2].SetMarkerSize(1.0)

    hstack=ROOT.THStack("h_stack","stack histograms")
    hstack.Add(histo_arr[num1],"hist,0")
    hstack.Add(histo_arr[num2],"p,0")

    drawCompare( hstack=hstack,
                 hratio=GetRatio_TH1(histo_arr[num2],histo_arr[num1]),
                 legend=GetLegend(histo_arr[num1],cuts[num1][0], "f", histo_arr[num2], cuts[num2][0], 'lpe'),
                 outdir=outdir,tag=tag,
                 xmin=0., xmax=800,
                 xtitle="E_{T}^{miss}", units="GeV",
                 notes="")
    
mycompare(0,1, outdir, tag)
mycompare(2,3, outdir, tag+'_ZpT100')

### ----- Finalizing:

fout.Close()


