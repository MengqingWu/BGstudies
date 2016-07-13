#!/usr/bin/env python
import ROOT
import os, copy
from math import *
from collections import OrderedDict
from python.SetCuts import SetCuts
from python.InitializePlotter import InitializePlotter
from python.HistPrinter import mergePrinter
from python.SimplePlot import *


channel='inclusive'#raw_input("Please choose a channel (el or mu): \n")
tag0='ZJstudy'
outdir='./output/shape/'
indir="./METSkim_v1"
lumi=2.318278305
whichregion='SR'
zpt_cut, met_cut= '100', '50'
whichbcd='ZJets'
#whichbcd='allBG'
var={'A': "fabs(llnunu_deltaPhi)",
     'AtoB': "fabs(llnunu_deltaPhi)-TMath::Pi()*3/4",
     'AtoD': "fabs(llnunu_deltaPhi)-TMath::Pi()/2",
     'AtoC': "fabs(llnunu_deltaPhi)-TMath::Pi()/4"}
nbins=8
xmin=[0, ROOT.TMath.Pi()/4, ROOT.TMath.Pi()/2, 3*ROOT.TMath.Pi()/4]
xmax=[ROOT.TMath.Pi()/4, ROOT.TMath.Pi()/2, 3*ROOT.TMath.Pi()/4, ROOT.TMath.Pi()]

tag = tag0+'_'+'shapeCorrector'
outTag=outdir+'/'+tag

CheckDir(outdir)
outtxt = open(outdir+'num_out.txt', 'a')

### ----- Initialize (samples):
plotter=InitializePlotter(indir=indir, addData=True)

setcuts = SetCuts()
cuts=setcuts.abcdCuts(channel=channel, whichRegion=whichregion, zpt_cut=zpt_cut, met_cut=met_cut)
# print cuts
outtxt.write( '\n'+ '*'*20+'\n')
outtxt.write( '\n'+ whichregion+'\n')
for reg in cuts:
    outtxt.write(reg+" "+channel+" : "+cuts[reg]+'\n'+'-'*20+'\n')

ROOT.gROOT.ProcessLine('.x ../src/tdrstyle.C')
ROOT.gStyle.SetPadBottomMargin(0.2)
ROOT.gStyle.SetPadLeftMargin(0.15)
#ROOT.TH1.AddDirectory(ROOT.kFALSE)

### ----- Execute (plotting):
#ha=plotter.ZJets.drawTH1('regA', var['A'], cuts['regA'], str(lumi*1000), nbins, xmin, xmax, titlex = "#Delta#phi_{Z,MET}", units = "GeV", drawStyle="HIST")
#print plotter.ZJets, plotter.allBG
if whichbcd=='allBG':
    bcdPlotter=plotter.allBG
elif whichbcd=='ZJets':
    bcdPlotter=plotter.ZJets
else: print "[error] whichbcd = ", whichbcd, ", which is not 'allBG' nor 'ZJets', please check!"; exit(0)
print "[info] I am using ",whichbcd," bcd for shape correction weighting factor."

print "[info] I am drawing the fabs(dphi) in region BCD shifted from A... (be patient)"
h_AB_shape=plotter.ZJets.drawTH1(tag0+'_regA_shiftB',var['AtoB'],cuts['regA'],str(lumi*1000),nbins, xmin[0], xmax[0], titlex = "#Delta#phi_{Z,MET}", units='', drawStyle="HIST")
h_AD_shape=plotter.ZJets.drawTH1(tag0+'_regA_shiftD',var['AtoD'],cuts['regA'],str(lumi*1000),nbins, xmin[1], xmax[1], titlex = "#Delta#phi_{Z,MET}", units='', drawStyle="HIST")
h_AC_shape=plotter.ZJets.drawTH1(tag0+'_regA_shiftC',var['AtoC'],cuts['regA'],str(lumi*1000),nbins, xmin[2], xmax[2], titlex = "#Delta#phi_{Z,MET}", units='', drawStyle="HIST")
print "[info] I am drawing the fabs(dphi) in region BCD... (be patient)"
h_A_shape=plotter.ZJets.drawTH1(tag0+'_regA',var['A'],cuts['regA'],str(lumi*1000),nbins, xmin[3], xmax[3], titlex = "#Delta#phi_{Z,MET}", units='', drawStyle="HIST")
h_B_shape=bcdPlotter.drawTH1(tag0+'_regB',var['A'],cuts['regB'],str(lumi*1000),nbins, xmin[0], xmax[0], titlex = "#Delta#phi_{Z,MET}", units='', drawStyle="HIST")
h_D_shape=bcdPlotter.drawTH1(tag0+'_regD',var['A'],cuts['regD'],str(lumi*1000),nbins, xmin[1], xmax[1], titlex = "#Delta#phi_{Z,MET}", units='', drawStyle="HIST")
h_C_shape=bcdPlotter.drawTH1(tag0+'_regC',var['A'],cuts['regC'],str(lumi*1000),nbins, xmin[2], xmax[2], titlex = "#Delta#phi_{Z,MET}", units='', drawStyle="HIST")


outtxt.write('*result*\nregA: '+ str(h_AB_shape.GetSumOfWeights())+\
             '\nregB: '+ str(h_B_shape.GetSumOfWeights())+\
             '\nregC: '+ str(h_C_shape.GetSumOfWeights())+\
             '\nregD: '+ str(h_D_shape.GetSumOfWeights()) + '\n')
outtxt.close()
os.system('cat '+outtxt.name)

h_AB_shape.Scale(1./h_AB_shape.GetSumOfWeights())
h_AC_shape.Scale(1./h_AC_shape.GetSumOfWeights())
h_AD_shape.Scale(1./h_AD_shape.GetSumOfWeights())

h_A_shape.Scale(1./h_A_shape.GetSumOfWeights())
h_B_shape.Scale(1./h_B_shape.GetSumOfWeights())
h_C_shape.Scale(1./h_C_shape.GetSumOfWeights())
h_D_shape.Scale(1./h_D_shape.GetSumOfWeights())

h_AB_shape.Divide(h_B_shape)
h_AC_shape.Divide(h_C_shape)
h_AD_shape.Divide(h_D_shape)

### ----- Finalize (Saving):
fdtshape=ROOT.TFile(outdir+'/'+whichbcd+"_shape_correction.root","recreate")
fdtshape.cd()
h_A_shape.Write()
h_B_shape.Write()
h_C_shape.Write()
h_D_shape.Write()
h_AB_shape.Write()
h_AC_shape.Write()
h_AD_shape.Write()
fdtshape.Print("all")
fdtshape.Close()
