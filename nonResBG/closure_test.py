#!/usr/bin/env python

import ROOT
import os, copy
from math import *
from collections import OrderedDict
from python.SetCuts import SetCuts
from python.InitializePlotter import InitializePlotter
from python.HistPrinter import mergePrinter
from python.SimplePlot import *

outtxt = open('num_out.txt', 'a')

#Channel=raw_input("Please choose a channel (el or mu): \n")
tag0='nonResBkg'
outdir='test'
indir="../../AnalysisRegion_nonRes"
lumi=2.318278305
zpt_cut, met_cut= '0', '0'
if not os.path.exists(outdir): os.system('mkdir '+outdir)

tag = tag0+'_'+'test'
outTag=outdir+'/'+tag

#  ll in Z | ll out Z
# --------------------  M_out [35,65] U [115,120]
#  eu in Z | eu out Z
#  M_in (70,110)

### ----- Initialize (samples):
plotter_ll=InitializePlotter(indir, addSig=False, addData=True,doRatio=False)
plotter_eu=InitializePlotter(indir, addSig=False, addData=True,doRatio=False, doElMu=True)
setcuts = SetCuts()
cuts_inclusive={'ll':  setcuts.alphaCuts(Zmass='inclusive', zpt_cut=zpt_cut, met_cut=met_cut),
                'emu': setcuts.alphaCuts(isll=False, Zmass='inclusive', zpt_cut=zpt_cut, met_cut=met_cut)}

outtxt.write( '\n'+ '*'*20+'\n')
for cut_inclu in cuts_inclusive:
    outtxt.write(cut_inclu+" : "+cuts_inclusive[cut_inclu]+'\n'+'-'*20+'\n')
cuts=setcuts.GetAlphaCuts(zpt_cut=zpt_cut, met_cut=met_cut)

ROOT.gROOT.ProcessLine('.x ../src/tdrstyle.C')

### ----- Execute (plotting):

# Inclusive stack plot:
plotter_ll.Stack.drawStack('llnunu_l1_mass', cuts_inclusive['ll'], str(lumi*1000), 10, 0.0, 200.0, titlex = "M_{Z}^{ll}", units = "GeV",
                       output=tag+'_mll',outDir=outdir, separateSignal=True,
                       drawtex="", channel="")
plotter_eu.Stack.drawStack('elmununu_l1_mass', cuts_inclusive['emu'], str(lumi*1000), 10, 0.0, 200.0, titlex = "M_{Z}^{e#mu}", units = "GeV",
                        output=tag+'_melmu',outDir=outdir, separateSignal=True,
                        drawtex="", channel="")

h_Mll_shape_mc=plotter_ll.TT.drawTH1('llnunu_l1_mass','llnunu_l1_mass', cuts_inclusive['ll'],str(lumi*1000),10,0.0,200.0,titlex='M_{Z}^{ll}',units='GeV',drawStyle="HIST")
h_Mll_shape_mc.Scale(1./h_Mll_shape_mc.Integral(0, 1+h_Mll_shape_mc.GetNbinsX()))

h_Meu_mc_corr=copy.deepcopy(h_Mll_shape_mc)

h_Meu_shape_mc=plotter_eu.TT.drawTH1('elmununu_l1_mass','elmununu_l1_mass',cuts_inclusive['emu'],str(lumi*1000),10,0.0,200.0,titlex='M_{Z}^{e#mu}',units='GeV',drawStyle="HIST")
eu_mc_yield=h_Meu_shape_mc.Integral(0, 1+h_Meu_shape_mc.GetNbinsX())
h_Meu_shape_mc.Scale(1./h_Meu_shape_mc.Integral(0, 1+h_Meu_shape_mc.GetNbinsX()))

drawCompareSimple(h_Mll_shape_mc, h_Meu_shape_mc, "ll inclusive", "e#mu inclusive",
                  xmin=0.0, xmax=200.0, outdir=outdir, notes='from ttbar MC',
                  tag=tag+'_zmass_mc', units='GeV', lumi=lumi, ytitle='normalized')

print eu_mc_yield
ROOT.gStyle.SetPadBottomMargin(0.2)
ROOT.gStyle.SetPadLeftMargin(0.15)
h_Meu_mc_corr.Scale(eu_mc_yield)
c1=ROOT.TCanvas("1")
h_Meu_mc_corr.Draw()
h_Meu_mc_corr.GetXaxis().SetTitle("M_{Z}^{e#mu}")
c1.SaveAs("test.pdf")

exit(0)


