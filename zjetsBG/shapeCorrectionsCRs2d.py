#!/usr/bin/env python
import ROOT, os, copy
#from array import *
from math import *
from collections import OrderedDict
from python.SetCuts import SetCuts
from python.InitializePlotter import InitializePlotter
from python.HistPrinter import mergePrinter
from python.SimplePlot import *

channel='inclusive'#raw_input("Please choose a channel (el or mu): \n")
lumi=2.318278305
indir="./METSkim_v1"
outdir='./output/shape/'; CheckDir(outdir)
tag0='ZJstudy'
tag = tag0+'_'+'shapeCorrector'
outTag=outdir+'/'+tag
outtxt = open(outdir+'num_out_2d.txt', 'a')

whichregion='SR'
zpt_cut, met_cut= '100', '50'
whichbcd='ZJets' #whichbcd='allBG'
onlyStats=False

xvar={'A': "fabs(llnunu_deltaPhi)",
     'AtoB': "fabs(llnunu_deltaPhi)-TMath::Pi()*3/4",
     'AtoD': "fabs(llnunu_deltaPhi)-TMath::Pi()/2",
     'AtoC': "fabs(llnunu_deltaPhi)-TMath::Pi()/4"}
nbinsx=4
xmin=[0, ROOT.TMath.Pi()/4, ROOT.TMath.Pi()/2, 3*ROOT.TMath.Pi()/4]
xmax=[ROOT.TMath.Pi()/4, ROOT.TMath.Pi()/2, 3*ROOT.TMath.Pi()/4, ROOT.TMath.Pi()]
#yvar, ytitle="llnunu_l2_pt/llnunu_l1_pt","E_{T}^{miss}/p_{T}^{Z}"
yvar, ytitle="llnunu_l2_pt","E_{T}^{miss}"
#ybins=[0,0.1,0.2,0.4,0.6,3]
ybins=[0,25,50,80,120,1000]

### ----- Initialize (samples):
plotter=InitializePlotter(indir=indir, addData=True, onlyStats=onlyStats)

setcuts = SetCuts()
cuts=setcuts.abcdCuts(channel=channel, whichRegion=whichregion, zpt_cut=zpt_cut, met_cut=met_cut)
# print cuts

outtxt.write( '\n'+ '*'*20+'\n')
outtxt.write( '\n'+ whichregion+'\n')
for reg in cuts:
    outtxt.write(reg+" "+channel+" : "+cuts[reg]+'\n'+'-'*20+'\n')

### ----- Execute (plotting):
#ha=plotter.ZJets.drawTH1('regA', xvar['A'], cuts['regA'], str(lumi*1000), nbins, xmin, xmax, titlex = "#Delta#phi_{Z,MET}", units = "GeV", drawStyle="HIST")
#print plotter.ZJets, plotter.allBG
if whichbcd=='allBG':
    bcdPlotter=plotter.allBG
elif whichbcd=='ZJets':
    bcdPlotter=plotter.ZJets
else: print "[error] whichbcd = ", whichbcd, ", which is not 'allBG' nor 'ZJets', please check!"; exit(0)
print "[info] I am using ",whichbcd," bcd for shape correction weighting factor."

print "[info] I am drawing 'met vs fabs(dphi)' in region BCD shifted from A... (be patient)"

h2_AB_shape=plotter.ZJets.drawTH2Binnedv1(tag0+'_regA_shiftB', yvar+':'+xvar['AtoB'], cuts['regA'], str(lumi*1000), 
                                          nbinsx, xmin[0], xmax[0], ybins, titlex = "|#Delta#phi_{Z,MET}|", unitsx='', titley = ytitle, unitsy='')
h2_AD_shape=plotter.ZJets.drawTH2Binnedv1(tag0+'_regA_shiftD', yvar+':'+xvar['AtoD'], cuts['regA'], str(lumi*1000), 
                                          nbinsx, xmin[1], xmax[1], ybins, titlex = "|#Delta#phi_{Z,MET}|", unitsx='', titley = ytitle, unitsy='')
h2_AC_shape=plotter.ZJets.drawTH2Binnedv1(tag0+'_regA_shiftC', yvar+':'+xvar['AtoC'], cuts['regA'], str(lumi*1000), 
                                          nbinsx, xmin[2], xmax[2], ybins, titlex = "|#Delta#phi_{Z,MET}|", unitsx='', titley = ytitle, unitsy='')

print "[info] I am drawing 'met vs fabs(dphi)' in region BCD... (be patient)"

h2_A_shape=plotter.ZJets.drawTH2Binnedv1(tag0+'_regA', yvar+':'+xvar['A'], cuts['regA'], str(lumi*1000), 
                                          nbinsx, xmin[3], xmax[3], ybins, titlex = "|#Delta#phi_{Z,MET}|", unitsx='', titley = ytitle, unitsy='')
h2_B_shape=bcdPlotter.drawTH2Binnedv1(tag0+'_regB', yvar+':'+xvar['A'], cuts['regB'], str(lumi*1000), 
                                      nbinsx, xmin[0], xmax[0], ybins, titlex = "|#Delta#phi_{Z,MET}|", unitsx='', titley = ytitle, unitsy='')
h2_D_shape=bcdPlotter.drawTH2Binnedv1(tag0+'_regD', yvar+':'+xvar['A'], cuts['regD'], str(lumi*1000), 
                                      nbinsx, xmin[1], xmax[1], ybins, titlex = "|#Delta#phi_{Z,MET}|", unitsx='', titley = ytitle, unitsy='')
h2_C_shape=bcdPlotter.drawTH2Binnedv1(tag0+'_regC', yvar+':'+xvar['A'], cuts['regC'], str(lumi*1000), 
                                      nbinsx, xmin[2], xmax[2], ybins, titlex = "|#Delta#phi_{Z,MET}|", unitsx='', titley = ytitle, unitsy='')

outtxt.write('*result*\nregA: '+ str(h2_AB_shape.Integral(0,5,0,6))+\
             '\nregB: '+ str(h2_B_shape.Integral(0,5,0,6))+\
             '\nregC: '+ str(h2_C_shape.Integral(0,5,0,6))+\
             '\nregD: '+ str(h2_D_shape.Integral(0,5,0,6)) + '\n')
outtxt.close()
os.system('cat '+outtxt.name)

h2_AB_shape.Scale(1./h2_AB_shape.GetSumOfWeights())
h2_AC_shape.Scale(1./h2_AC_shape.GetSumOfWeights())
h2_AD_shape.Scale(1./h2_AD_shape.GetSumOfWeights())

h2_A_shape.Scale(1./h2_A_shape.GetSumOfWeights())
h2_B_shape.Scale(1./h2_B_shape.GetSumOfWeights())
h2_C_shape.Scale(1./h2_C_shape.GetSumOfWeights())
h2_D_shape.Scale(1./h2_D_shape.GetSumOfWeights())

h2_AB_shape.Divide(h2_B_shape)
h2_AC_shape.Divide(h2_C_shape)
h2_AD_shape.Divide(h2_D_shape)

### ----- Finalize (Saving):
ROOT.TH1.AddDirectory(ROOT.kFALSE)
fdtshape=ROOT.TFile(outdir+'/'+whichbcd+"_shape_correction_2d.root","recreate")
fdtshape.cd()
h2_A_shape.Write()
h2_B_shape.Write()
h2_C_shape.Write()
h2_D_shape.Write()
h2_AB_shape.Write()
h2_AC_shape.Write()
h2_AD_shape.Write()
fdtshape.Print("all")
fdtshape.Close()
