#!/usr/bin/env python
import ROOT
import os, copy
from collections import OrderedDict
from python.SetCuts import SetCuts
from python.InitializePlotter import InitializePlotter
from python.SimplePlot import * # for CheckDir()

### ----- Parameter setting:
indir="./METSkim_v1"
outdir='./output/comparison2D'; CheckDir(outdir)
lumi=2.318278305
tag0='ZJstudy'

whichregion='SR'
channel='inclusive'
zpt_cut, met_cut= '100', '50'
yvar, xvar='llnunu_l2_pt','llnunu_l1_pt'
ymin, ymax, ytitle, xunits =   50, 300, "E_{T}^{miss}", "GeV"
xmin, xmax, xtitle, yunits =  100, 600, "p_{T}^{Z}", "GeV"
nbinsy, nbinsx = int((ymax-ymin)/5.),  int((xmax-xmin)/5.)

### ----- Initialize (samples):
plotter=InitializePlotter(indir=indir)
setcuts = SetCuts()
cuts=setcuts.abcdCuts(channel=channel, whichRegion=whichregion, zpt_cut=zpt_cut, met_cut=met_cut)
histo=OrderedDict()

### ----- Execute (plotting):
for reg in cuts:
    nameseq=[tag0, '2D', yvar, xvar, reg]
    h2 = plotter.ZJets.drawTH2('_'.join(nameseq), yvar+':'+xvar, cuts[reg], str(lumi*1000),
                               nbinsx, xmin, xmax, nbinsy, ymin, ymax, titlex = xtitle, unitsx = xunits, titley = ytitle, unitsy = yunits)
    histo[reg]=h2

### ----- Finalize (Save to file):
ROOT.TH1.AddDirectory(ROOT.kFALSE)
outseq=[tag0, '2D', yvar, xvar]
fout2d=ROOT.TFile(outdir+'/'+'_'.join(outseq)+".root","recreate")
fout2d.cd()
for ih in histo:
    histo[ih].Write()

fout2d.Print("all")
fout2d.Close()
