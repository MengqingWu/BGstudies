#!/usr/bin/env python

import ROOT
import os, copy
from math import *
from collections import OrderedDict
from python.SetCuts import SetCuts
from python.InitializePlotter import InitializePlotter
from python.HistPrinter import mergePrinter
from python.SimplePlot import *

outtxt = open('closure_test.txt', 'a')

#Channel=raw_input("Please choose a channel (el or mu): \n")
tag0='nonResBkg'
outdir='closureTest'
indir="./nonResSkim_v2"
lumi=2.318278305
zpt_cut, met_cut= '0', '0'
if not os.path.exists(outdir): os.system('mkdir '+outdir)

tag = tag0+'_'+'test'
outTag=outdir+'/'+tag

bkg='nonRes' #'ttbar'

#  ll in Z | ll out Z
# --------------------  M_out (35,65) U (115,180)
#  eu in Z | eu out Z
#  M_in (70,110)

### ----- Initialize (samples):
plotter_ll=InitializePlotter(indir, addSig=False, addData=True,doRatio=False)
plotter_eu=InitializePlotter(indir, addSig=False, addData=True,doRatio=False, doElMu=True)
#bkg_ll, bkg_eu = plotter_ll.TT, plotter_eu.TT
bkg_ll, bkg_eu = plotter_ll.NonResBG, plotter_eu.NonResBG

setcuts = SetCuts()
cuts=setcuts.GetAlphaCuts(zpt_cut=zpt_cut, met_cut=met_cut)

outtxt.write( '\n'+ '*'*20+'\n')
for reg in cuts:
    outtxt.write(reg+" inclusive : "+cuts[reg]['inclusive']+'\n'+'-'*20+'\n')

ROOT.gROOT.ProcessLine('.x ../src/tdrstyle.C')

#histo=OrderedDict() # will have histo[<reg><zmass>]=[cuts, h1, h2...]
yields=OrderedDict() # will have yields[<reg><zmass>][<memeber>]=yield
err=OrderedDict() # will have yields[<reg><zmass>][<memeber>]=err
nbins, xmin, xmax=40, 0.0, 200.0

# def myIntegralAndError(h1, x1, x2, error):
#     '''h1 is TH1, x1 x2 refers to the bin content, error is ROOT.Double(0.0),
#     NB: bin is filled as [x1,x2), please choose correctly the x2'''
#     binx1 = h1.GetXaxis().FindBin(x1)
#     binx2 = h1.GetXaxis().FindBin(x2)
#     return h1.IntegralAndError(binx1, binx2, error)

### ----- Execute (plotting):

# Inclusive stack plot:
# plotter_ll.Stack.drawStack('llnunu_l1_mass', cuts['ll']['inclusive'], str(lumi*1000), 20, 0.0, 200.0, titlex = "M_{Z}^{ll}", units = "GeV",
#                            output=tag+'_mll',outDir=outdir, separateSignal=True, drawtex="", channel="")
# plotter_eu.Stack.drawStack('elmununu_l1_mass', cuts['emu']['inclusive'], str(lumi*1000), 20, 0.0, 200.0, titlex = "M_{Z}^{e#mu}", units = "GeV",
#                            output=tag+'_melmu',outDir=outdir, separateSignal=True, drawtex="", channel="")

h_Mll_yield_mc=bkg_ll.drawTH1('llnunu_l1_mass','llnunu_l1_mass', cuts['ll']['inclusive'],str(lumi*1000),nbins, xmin, xmax,titlex='M_{Z}^{ll}',units='GeV',drawStyle="HIST")
h_Mll_shape_mc=copy.deepcopy(h_Mll_yield_mc)
h_Mll_shape_mc.Scale(1./h_Mll_shape_mc.Integral(0, 1+h_Mll_shape_mc.GetNbinsX()))

h_Meu_yield_mc=bkg_eu.drawTH1('elmununu_l1_mass','elmununu_l1_mass',cuts['emu']['inclusive'],str(lumi*1000),nbins, xmin, xmax,titlex='M_{Z}^{e#mu}',units='GeV',drawStyle="HIST")
Integral_Meu_yield_mc = h_Meu_yield_mc.Integral(0, 1+h_Meu_yield_mc.GetNbinsX())
h_Meu_shape_mc=copy.deepcopy(h_Meu_yield_mc)
h_Meu_shape_mc.Scale(1./Integral_Meu_yield_mc)

h_Meu_yield_mc_corr=copy.deepcopy(h_Mll_shape_mc)
h_Meu_yield_mc_corr.Scale(Integral_Meu_yield_mc)

ftest=ROOT.TFile(outdir+"test.root","recreate")
ROOT.TH1.AddDirectory(ROOT.kFALSE)
h_Mll_shape_mc.Write()
h_Meu_yield_mc.Write()
ftest.Close()

histo={'ll':h_Mll_yield_mc, 'emu':h_Meu_yield_mc_corr}
xRange={'out':(35,65,115,180), 'in':(70,110)}
for reg in histo:
    for zmass in xRange:
        if len(xRange[zmass])>2:
            err1,err2=ROOT.Double(0.0),ROOT.Double(0.0)
            yield1 = myIntegralAndError(histo[reg],xRange[zmass][0],xRange[zmass][1]-1,err1)
            yield2 = myIntegralAndError(histo[reg],xRange[zmass][2],xRange[zmass][3]-1,err2)
            print reg, zmass,  yield1, yield2
            yields[reg+zmass]={bkg:yield1+yield2}
            err[reg+zmass]={bkg:math.sqrt(err1**2+err2**2)}

        else:
            err0=ROOT.Double(0.0)
            yields[reg+zmass]={bkg: myIntegralAndError(histo[reg],xRange[zmass][0],xRange[zmass][1]-1,err0)}
            err[reg+zmass]={bkg: err0}
##
h_Mll_shape_mc.Rebin(2)
h_Meu_shape_mc.Rebin(2)
drawCompareSimple(h_Mll_shape_mc, h_Meu_shape_mc, "ll inclusive", "e#mu inclusive",
                  xmin=0.0, xmax=200.0, outdir=outdir, notes='from '+bkg+' MC',
                  tag=tag+'_zmass_mc_norm', units='GeV', lumi=lumi, ytitle='normalized')

print Integral_Meu_yield_mc
ROOT.gStyle.SetPadBottomMargin(0.2)
ROOT.gStyle.SetPadLeftMargin(0.15)

c1=ROOT.TCanvas("1")
h_Meu_yield_mc_corr.Rebin(2)
h_Meu_yield_mc_corr.Draw()
h_Meu_yield_mc_corr.GetXaxis().SetTitle("M_{Z}^{e#mu}")
c1.SaveAs(outdir+"/h_Meu_yield_mc_corr.pdf")

        
### ----- Finalizing:
#mergePrinter(histo=histo, outTag=outTag+'_all')

outtxt.write('\n'+'*'*20+'\n')
for key in yields:
    for x in yields[key]:
        #print "%s, %s: yield = %.2f +- %.2f" % (key, x, yields[key][x], err[key][x])
        outtxt.write("%s, %s: yield = %.2f +- %.2f \n" % (key, x, yields[key][x], err[key][x]))
        
                        
ll_out_dt=yields['llout'][bkg]
emu_in_dt=yields['emuin'][bkg]
emu_out_dt=yields['emuout'][bkg]

err_ll_out_dt=err['llout'][bkg]
err_emu_in_dt=err['emuin'][bkg]
err_emu_out_dt=err['emuout'][bkg]

sf='ll_out_dt/emu_out_dt'
ll_pred='ll_out_dt*emu_in_dt/emu_out_dt'

err_product=lambda A, B, a, b: sqrt((a*B)**2+(b*A)**2) # A*B
err_division=lambda A, B, a, b: sqrt((a/B)**2+(b*A/B**2)**2) # A/B
err_sf = err_division(ll_out_dt,emu_out_dt, err_ll_out_dt, err_emu_out_dt)
err_ll_pred = err_product(eval(sf), emu_in_dt, err_sf, err_emu_in_dt)

ll_exp=yields['llin'][bkg]
err_ll_exp=err['llin'][bkg]

outtxt.write('\n'+'*'*20+'\n')
outtxt.write("result: predict = %.2f +- %.2f, expectation = %.2f +- %.2f\n" % (eval(ll_pred), err_ll_pred, ll_exp, err_ll_exp))
outtxt.write("N_llout/N_euout: ratio = %.2f +- %.2f\n" % (eval(sf), err_sf))

outtxt.close()
h_Meu_yield_mc_corr.Scale(eval(sf))
h_Mll_yield_mc.Rebin(2)
drawCompareSimple(h_Mll_yield_mc, h_Meu_yield_mc_corr, "ll expect", "ll predict",
                  xmin=70.0, xmax=110.0, outdir=outdir, notes='from '+bkg+' MC',
                  tag=tag+'_zmass_mc_final', units='GeV', lumi=lumi, ytitle='')


os.system('cat '+outtxt.name)
