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
plotter_ll.Stack.drawStack('llnunu_l1_mass', cuts_inclusive['ll'], str(lumi*1000), 20, 0.0, 200.0, titlex = "M_{Z}^{ll}", units = "GeV",
                           output=tag+'_mll',outDir=outdir, separateSignal=True,
                           drawtex="", channel="")
plotter_eu.Stack.drawStack('elmununu_l1_mass', cuts_inclusive['emu'], str(lumi*1000), 20, 0.0, 200.0, titlex = "M_{Z}^{e#mu}", units = "GeV",
                           output=tag+'_melmu',outDir=outdir, separateSignal=True,
                           drawtex="", channel="")

h_Mll_shape_mc=plotter_ll.TT.drawTH1('llnunu_l1_mass','llnunu_l1_mass', cuts_inclusive['ll'],str(lumi*1000),20,0.0,200.0,titlex='M_{Z}^{ll}',units='GeV',drawStyle="HIST")
h_Mll_shape_mc.Scale(1./h_Mll_shape_mc.Integral(0, 1+h_Mll_shape_mc.GetNbinsX()))

h_Meu_mc_corr=copy.deepcopy(h_Mll_shape_mc)

h_Meu_shape_mc=plotter_eu.TT.drawTH1('elmununu_l1_mass','elmununu_l1_mass',cuts_inclusive['emu'],str(lumi*1000),20,0.0,200.0,titlex='M_{Z}^{e#mu}',units='GeV',drawStyle="HIST")
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
c1.SaveAs(outdir+"/h_Meu_mc_corr.pdf")



# get the scale factor
histo=OrderedDict() # will have histo[<reg><zmass>]=[cuts, h1, h2...]
yields=OrderedDict() # will have yields[<reg><zmass>][<memeber>]=yield
err=OrderedDict() # will have yields[<reg><zmass>][<memeber>]=err
var_dic=OrderedDict({'emu': ['elmununu_l1_mass', (20, 0.0, 200.0)],
                     'll': ['llnunu_l1_mass', (20, 0.0, 200.0)]}) # in format: var_dic[<reg>]=[<var>, (nbins, xmin, xmax)]
members={'ll': {'tt': plotter_ll.TT},
         'emu': {'tt': plotter_eu.TT}} # in format: memebers[<reg>][<mem>]=plotter

for reg in cuts: #  'll' or 'emu'
    for zmass in cuts[reg]: # 'in' or 'out'
        histo[reg+zmass] = [cuts[reg][zmass],] # save the cut tex
        err[reg+zmass] = OrderedDict()
        yields[reg+zmass] = OrderedDict()
        for mem in members[reg]: # loop 'nonres', 'res' and 'dt'
            lumi_str='1' if mem=='dt' else str(lumi*1000)
            
            h_tmp= members[reg][mem].drawTH1(var_dic[reg][0]+'_'+mem+'_'+reg+'_'+zmass,
                                             var_dic[reg][0], cuts[reg][zmass],
                                             lumi_str, var_dic[reg][1][0], var_dic[reg][1][1], var_dic[reg][1][2],
                                             titlex='M_{Z}^{e#mu}',units='GeV', drawStyle="HIST")
            histo[reg+zmass].append(h_tmp)
            err[reg+zmass][mem] = ROOT.Double(0.0)
            yields[reg+zmass][mem] = h_tmp.IntegralAndError(0, 1+h_tmp.GetNbinsX(), err[reg+zmass][mem])

### ----- Finalizing:
mergePrinter(histo=histo, outTag=outTag+'_all')

outtxt.write('\n'+'*'*20+'\n')
for key in yields:
    for x in yields[key]:
        #print "%s, %s: yield = %.2f +- %.2f" % (key, x, yields[key][x], err[key][x])
        outtxt.write("%s, %s: yield = %.2f +- %.2f \n" % (key, x, yields[key][x], err[key][x]))
        
                        
ll_out_dt=yields['llout']['tt']
emu_in_dt=yields['emuin']['tt']
emu_out_dt=yields['emuout']['tt']

err_ll_out_dt=err['llout']['tt']
err_emu_in_dt=err['emuin']['tt']
err_emu_out_dt=err['emuout']['tt']

sf='ll_out_dt/emu_out_dt'
ll_pred='ll_out_dt*emu_in_dt/emu_out_dt'

err_product=lambda A, B, a, b: sqrt((a*B)**2+(b*A)**2) # A*B
err_division=lambda A, B, a, b: sqrt((a/B)**2+(b*A/B**2)**2) # A/B
err_sf = err_division(ll_out_dt,emu_out_dt, err_ll_out_dt, err_emu_out_dt)
err_ll_pred = err_product(eval(sf), emu_in_dt, err_sf, err_emu_in_dt)

ll_exp=yields['llin']['tt']
err_ll_exp=err['llin']['tt']

outtxt.write('\n'+'*'*20+'\n')
outtxt.write("result: predict = %.2f +- %.2f, expectation = %.2f +- %.2f\n" % (eval(ll_pred), err_ll_pred, ll_exp, err_ll_exp))
outtxt.write("N_llout/N_euout: ratio = %.2f +- %.2f\n" % (eval(sf), err_sf))

outtxt.close()

os.system('cat '+outtxt.name)
