#!/usr/bin/env python

import ROOT
import os
from math import *
from python.SetCuts import SetCuts
from python.InitializePlotter import InitializePlotter

#Channel=raw_input("Please choose a channel (el or mu): \n")
tag0='nonResBkg'
outdir='test'
indir="./AnalysisRegion_nonRes"
lumi=2.169126704526

if not os.path.exists(outdir): os.system('mkdir '+outdir)

tag = tag0+'_'+'test'

#  ll in Z | ll out Z
# --------------------  M_out [35,65] U [115,120]
#  eu in Z | eu out Z
#  M_in (70,110)

### ----- Initialize (samples):
plotter_ll=InitializePlotter(addSig=False, addData=True,doRatio=False)
plotter_eu=InitializePlotter(addSig=False, addData=True,doRatio=False, doElMu=True)
setcuts=SetCuts()
print "I am cuts_ll:"
cuts_ll=setcuts.alphaCuts(Zmass='inclusive')
print "I am cuts_eu:"
cuts_eu=setcuts.alphaCuts(isll=False, Zmass='inclusive')
ROOT.gROOT.ProcessLine('.x tdrstyle.C')

### ----- Execute (plotting):

plotter_ll.Stack.drawStack('llnunu_l1_mass', cuts_ll, str(lumi*1000), 10, 0.0, 200.0, titlex = "M_{Z}^{ll}", units = "GeV",
                       output=tag+'_mll',outDir=outdir, separateSignal=True,
                       drawtex="", channel="")

plotter_eu.Stack.drawStack('elmununu_l1_mass', cuts_eu, str(lumi*1000), 10, 0.0, 200.0, titlex = "M_{Z}^{e#mu}", units = "GeV",
                        output=tag+'_melmu',outDir=outdir, separateSignal=True,
                        drawtex="", channel="")

h_Memu_nonRes=plotter_eu.NonResBG.drawTH1('elmununu_l1_mass',cuts_eu,str(lumi*1000),10,0.0, 200.0,titlex='M_{Z}^{e#mu}',units='GeV',drawStyle="HIST")
h_Memu_res=plotter_eu.ResBG.drawTH1('elmununu_l1_mass',cuts_eu,str(lumi*1000),10,0.0, 200.0,titlex='M_{Z}^{e#mu}',units='GeV',drawStyle="HIST")

h_Mll_nonRes=plotter_ll.NonResBG.drawTH1('llnunu_l1_mass',cuts_ll,str(lumi*1000),10,0.0, 200.0,titlex='M_{Z}^{ll}',units='GeV',drawStyle="HIST")
h_Mll_res=plotter_ll.ResBG.drawTH1('llnunu_l1_mass',cuts_ll,str(lumi*1000),10,0.0, 200.0,titlex='M_{Z}^{ll}',units='GeV',drawStyle="HIST")

met_pt=[50, 80, 100, 125, 200]

#h_alphaVSmet=TH1("h_alphaVSmet","alpha vs met; E_{T}^{miss};#alpha",15, 50, 200)



### ----- Finalizing:



