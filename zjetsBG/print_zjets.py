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
outdir='./output/printer/'
indir="./METSkim_v1.1"
lumi=2.318278305
whichregion='SR'
zpt_cut, met_cut= '100', '50'
var="fabs(llnunu_deltaPhi)"

doSub=True
whichdt='dt_sub' if doSub else 'dt'
whichbcd='zjets' if doSub else 'allmc'

tag = tag0+'_'+'printer'
outTag=outdir+'/'+tag

CheckDir(outdir)
outtxt = open(outdir+'/num_out.txt', 'a')

### ----- Initialize (samples):
plotter=InitializePlotter(indir=indir, addData=True)

setcuts = SetCuts()
cuts=setcuts.abcdCuts(channel=channel, whichRegion=whichregion, zpt_cut=zpt_cut, met_cut=met_cut,extra_cut='dPhi_jetMet_min_b>0.5')

outtxt.write( '\n'+ '*'*20+'\n')
outtxt.write( '\n'+ whichregion+'\n')
for reg in cuts:
    outtxt.write(reg+" "+channel+" : "+cuts[reg]+'\n'+'-'*20+'\n')

histo=OrderedDict() # will have histo[<reg>]=[h1, h2...]
yields=OrderedDict() # will have yields[<reg>][<memeber>]=yield
err=OrderedDict() # will have yields[<reg>][<memeber>]=err
nbins, xmin, xmax=32, 0.0, 3.2
members={'non-zjets': plotter.NonZBG,
         'zjets': plotter.ZJets,
         'dt': plotter.Data } # in format: members[<reg>][<mem>]=plotter

ROOT.gROOT.ProcessLine('.x ../src/tdrstyle.C')
ROOT.gStyle.SetPadBottomMargin(0.2)
ROOT.gStyle.SetPadLeftMargin(0.15)

textodraw=setcuts.Tex_dic
### ----- Execute (plotting):
for reg in cuts:
    plotter.Stack.drawStack(var, cuts[reg], str(lumi*1000), 30, 0.0, 3.0, titlex = "|#Delta#phi_{Z, MET}|", units = "",
                            output=tag+'_'+whichregion+'_'+channel+'_'+reg+'_absDphi',outDir=outdir,
                            separateSignal=True, drawtex = textodraw[reg], channel="inclusive")
    histo[reg]=OrderedDict()
    yields[reg]=OrderedDict()
    err[reg]=OrderedDict()

    hname='dphi_'+channel+'_'+whichregion+'_'+reg

    for mem in members:
        lumi_str='1' if mem=='dt' else str(lumi*1000)
        hvar=members[mem].drawTH1(hname+'_'+mem, var, cuts[reg], lumi_str, nbins, xmin, xmax, titlex = "|#Delta#phi_{Z, MET}|", units = "", drawStyle="HIST") 
        err_reg=ROOT.Double(0.0)
        num_reg = hvar.IntegralAndError(0, 1+hvar.GetNbinsX(), err_reg)
        hreg_shape = copy.deepcopy(hvar)
        hreg_shape.SetName(hname+'_'+mem+'_shape')
        if num_reg==0: print "[warning]: num_reg==0 for ",mem ,' in ', reg
        else:    hreg_shape.Scale(1./num_reg)

        err[reg][mem] = err_reg
        yields[reg][mem] = num_reg
        histo[reg][mem] = [hvar, hreg_shape]

    # get the nonzjets contamination subtracted in data:
    h_dt_sub=copy.deepcopy(histo[reg]['dt'][0])
    h_dt_sub.SetName(hname+"_dt_sub")
    h_dt_sub.Add(histo[reg]['non-zjets'][0], -1)
    err_dtsub=ROOT.Double(0.0)
    num_dtsub=h_dt_sub.IntegralAndError(0, 1+h_dt_sub.GetNbinsX(), err_dtsub)
    h_dt_sub_shape=copy.deepcopy(h_dt_sub)
    h_dt_sub_shape.SetName(hname+"_dt_sub_shape")
    h_dt_sub_shape.Scale(1./num_dtsub)
    err[reg]['dt_sub'] = err_dtsub
    yields[reg]['dt_sub'] = num_dtsub
    histo[reg]['dt_sub'] = [h_dt_sub, h_dt_sub_shape]

    h_allmc=copy.deepcopy(histo[reg]['zjets'][0])
    h_allmc.SetName(hname+"_allMC")
    h_allmc.Add(histo[reg]['non-zjets'][0], 1)
    err_allmc=ROOT.Double(0.0)
    num_allmc=h_allmc.IntegralAndError(0, 1+h_allmc.GetNbinsX(), err_allmc)
    err[reg]['allmc'] = err_allmc
    yields[reg]['allmc'] = num_allmc
    histo[reg]['allmc'] = [h_allmc]
    
####**** begin: save all histos
fdtshape=ROOT.TFile(outdir+'/'+"all_histos.root","recreate")
fdtshape.cd()
for ih in histo:
    for imem in histo[ih]:
        for iih in histo[ih][imem]:
            iih.Write()
####**** end: save all histos

# drawCompareSimple(h_Mll_shape_mc, h_Meu_shape_mc, "ll inclusive", "e#mu inclusive",
#                   xmin=0.0, xmax=200.0, outdir=outdir, notes='from '+bkg+' MC',
#                   tag=tag+'_zmass_mc_norm', units='GeV', lumi=lumi, ytitle='normalized')

# c1=ROOT.TCanvas("1")
# h_Meu_yield_mc_corr.Rebin(2)
# h_Meu_yield_mc_corr.Draw()
# h_Meu_yield_mc_corr.GetXaxis().SetTitle("M_{Z}^{e#mu}")
# c1.SaveAs(outdir+"/h_Meu_yield_mc_corr.pdf")

        
### ----- Finalizing:
#mergePrinter(histo=histo, outTag=outTag+'_all')

outtxt.write('\n'+'*'*20+'\n')
for key in yields:
    for x in yields[key]:
        #print "%s, %s: yield = %.2f +- %.2f" % (key, x, yields[key][x], err[key][x])
        outtxt.write("%s, %s: yield = %.2f +- %.2f \n" % (key, x, yields[key][x], err[key][x]))
        
err_product=lambda A, B, a, b: sqrt((a*B)**2+(b*A)**2) # A*B
err_division=lambda A, B, a, b: sqrt((a/B)**2+(b*A/B**2)**2) # A/B
    
ratioAB=yields['regA']['zjets']/yields['regB'][whichbcd]
ratioAC=yields['regA']['zjets']/yields['regC'][whichbcd]
ratioAD=yields['regA']['zjets']/yields['regD'][whichbcd]

err_ratioAB=err_division(yields['regA']['zjets'], yields['regB'][whichbcd], err['regA']['zjets'],err['regB'][whichbcd])
err_ratioAC=err_division(yields['regA']['zjets'], yields['regC'][whichbcd], err['regA']['zjets'],err['regC'][whichbcd])
err_ratioAD=err_division(yields['regA']['zjets'], yields['regD'][whichbcd], err['regA']['zjets'],err['regD'][whichbcd])

regA_pred=(ratioAB*yields['regB'][whichdt]\
          +ratioAC*yields['regC'][whichdt]\
          +ratioAD*yields['regD'][whichdt])/3
err_regA_pred = sqrt(err_product(ratioAB,yields['regB'][whichdt],err_ratioAB,err['regB'][whichdt])**2\
                   + err_product(ratioAC,yields['regC'][whichdt],err_ratioAB,err['regC'][whichdt])**2\
                   + err_product(ratioAD,yields['regD'][whichdt],err_ratioAB,err['regD'][whichdt])**2)

zjets_exp=yields['regA']['zjets']
err_zjets_exp=err['regA']['zjets']

outtxt.write('\n'+'*'*20+'\n')
outtxt.write("result: predict = %.2f +- %.2f, expectation = %.2f +- %.2f\n" \
             % (regA_pred, err_regA_pred, zjets_exp, err_zjets_exp))
outtxt.write(" A/B = %.2f +- %.2f\n A/C = %.2f +- %.2f\n A/D = %.2f +- %.2f\n" \
             % ( ratioAB,err_ratioAB, ratioAC, err_ratioAC, ratioAD, err_ratioAD ))

outtxt.close()
os.system('cat '+outtxt.name)
fdtshape.Close()
# h_Meu_yield_mc_corr.Scale(eval(sf))
# h_Mll_yield_mc.Rebin(2)
# drawCompareSimple(h_Mll_yield_mc, h_Meu_yield_mc_corr, "ll expect", "ll predict",
#                   xmin=70.0, xmax=110.0, outdir=outdir, notes='from '+bkg+' MC',
#                   tag=tag+'_zmass_mc_final', units='GeV', lumi=lumi, ytitle='')


