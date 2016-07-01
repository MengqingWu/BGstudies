#!/usr/bin/env python

import ROOT
import os,copy
from math import *
from collections import OrderedDict
from python.SetCuts import SetCuts
from python.InitializePlotter import InitializePlotter
from python.HistPrinter import mergePrinter
from python.SimplePlot import *

outtxt = open('num_out.txt', 'a')
doshapeCorr=True
doResSubInElmu=False
whichdt='dt_sub' if doResSubInElmu else 'dt'
whichdt+='_corr' if doshapeCorr else ''

#Channel=raw_input("Please choose a channel (el or mu): \n")
tag0='nonResBkg'
outdir='test'
indir="./nonResSkim_v3"
lumi=2.318278305
logy=True
zpt_cut, met_cut= '0', '0'
if not os.path.exists(outdir): os.system('mkdir '+outdir)

tag = tag0+'_'+'test'
outTag=outdir+'/'+tag

#  ll in Z | ll out Z
# --------------------  M_out [35,65] U [115,120]
#  eu in Z | eu out Z
#  M_in (70,110)

### ----- Initialize (samples):
plotter_ll=InitializePlotter(indir, addSig=False, addData=True,doRatio=True, LogY=logy)
plotter_eu=InitializePlotter(indir, addSig=False, addData=True,doRatio=True, doElMu=True, scaleElMu=False, LogY=logy)
setcuts=SetCuts()
cuts=setcuts.GetAlphaCuts(zpt_cut=zpt_cut, met_cut=met_cut)

outtxt.write( '\n'+ '*'*20+'\n')
for reg in cuts:
    outtxt.write(reg+" inclusive : "+cuts[reg]['inclusive']+'\n'+'-'*20+'\n')

ROOT.gROOT.ProcessLine('.x ../src/tdrstyle.C')

### ----- Execute (plotting):

#Inclusive stack plot:
plotter_ll.Stack.drawStack('llnunu_l1_mass', cuts['ll']['inclusive'], str(lumi*1000), 20, 0.0, 200.0, titlex = "M_{Z}^{ll}", units = "GeV",
                           output=tag+'_mll',outDir=outdir, separateSignal=True,
                           drawtex="", channel="")
plotter_eu.Stack.drawStack('elmununu_l1_mass', cuts['emu']['inclusive'], str(lumi*1000), 20, 0.0, 200.0, titlex = "M_{Z}^{e#mu}", units = "GeV",
                           output=tag+'_melmu',outDir=outdir, separateSignal=True,
                           drawtex="", channel="")

exit(0)
# Make numbers:
histo=OrderedDict() # will have histo[<reg>][<member>]=h1
yields=OrderedDict() # will have yields[<reg><zmass>][<member>]=yield
err=OrderedDict() # will have yields[<reg><zmass>][<member>]=err
var_dic=OrderedDict({'emu': ['elmununu_l1_mass', (40, 0.0, 200.0)],
                     'll': ['llnunu_l1_mass', (40, 0.0, 200.0)]}) # in format: var_dic[<reg>]=[<var>, (nbins, xmin, xmax)]
members={'ll': {'nonres': plotter_ll.NonResBG,
                'res': plotter_ll.ResBG,
                'dt': plotter_ll.Data},
         'emu': {'nonres': plotter_eu.NonResBG,
               'res': plotter_eu.ResBG,
               'dt': plotter_eu.Data}
         } # in format: members[<reg>][<mem>]=plotter

for reg in cuts: #  'll' or 'emu'
    histo[reg] = OrderedDict()
    for mem in members[reg]: # loop 'nonres', 'res' and 'dt'
        lumi_str='1' if mem=='dt' else str(lumi*1000)
        h_tmp= members[reg][mem].drawTH1(var_dic[reg][0]+'_'+mem+'_'+reg+'_inclusive',
                                         var_dic[reg][0], cuts[reg]['inclusive'],
                                         lumi_str, var_dic[reg][1][0], var_dic[reg][1][1], var_dic[reg][1][2],
                                         titlex='M_{Z}^{e#mu}',units='GeV', drawStyle="HIST")
        histo[reg][mem]=h_tmp

    h_dt_sub=copy.deepcopy(histo[reg]['dt'])
    h_dt_sub.Add(histo[reg]['res'],-1)
    histo[reg]['dt_sub']=h_dt_sub

# Scale the Meu shape using MC to account for selection efficiency diffed per event:
h_ll_shape=copy.deepcopy(histo['ll']['nonres'])
h_ll_shape.Scale(1./h_ll_shape.Integral(0, 1+h_ll_shape.GetNbinsX())) # normalized to 1
h_emu_shape=copy.deepcopy(histo['emu']['nonres'])
if not doResSubInElmu: h_emu_shape.Add(histo['emu']['res'])
h_emu_shape.Scale(1./h_emu_shape.Integral(0, 1+h_emu_shape.GetNbinsX()))  # normalized to 1

h_ll_shape.Divide(h_emu_shape)
h_ll_shape.SetName("sf_vs_Memu")
iamdt='dt_sub' if doResSubInElmu else 'dt'
h_dt_corr=copy.deepcopy(histo['emu'][iamdt])
h_dt_corr.Multiply(h_ll_shape)
histo['emu'][iamdt+'_corr']=h_dt_corr

#------ begin: save
ROOT.TH1.AddDirectory(ROOT.kFALSE)
sfFile=ROOT.TFile("shape_correction.root","recreate")
sfFile.cd()
h_ll_shape.Write()
histo['ll']['nonres'].Write()
histo['emu']['nonres'].Write()
histo['emu']['res'].Write()
sfFile.Close()
#------ end: save


# compute yields/err for the in/out regions:
xRange={'out':(35,65,115,180), 'in':(70,110)}
for Reg in histo:
    for zmass in xRange:
        yields[Reg+zmass]=OrderedDict()
        err[Reg+zmass]=OrderedDict()
        for Mem in histo[Reg]:
            if len(xRange[zmass])>2:
                err1,err2=ROOT.Double(0.0),ROOT.Double(0.0)
                yield1 = myIntegralAndError(histo[Reg][Mem],xRange[zmass][0],xRange[zmass][1]-1,err1)
                yield2 = myIntegralAndError(histo[Reg][Mem],xRange[zmass][2],xRange[zmass][3]-1,err2)
                yields[Reg+zmass][Mem]=yield1+yield2
                err[Reg+zmass][Mem]=math.sqrt(err1**2+err2**2)
                
            else:
                err0=ROOT.Double(0.0)
                yields[Reg+zmass][Mem]=myIntegralAndError(histo[Reg][Mem],xRange[zmass][0],xRange[zmass][1]-1,err0)
                err[Reg+zmass][Mem]= err0
               
### ----- Finalizing:
#mergePrinter(histo=histo, outTag=outTag+'_all')

outtxt.write('\n'+'*'*20+'\n')
for key in yields:
    for x in yields[key]:
        #print "%s, %s: yield = %.2f +- %.2f" % (key, x, yields[key][x], err[key][x])
        outtxt.write("%s, %s: yield = %.2f +- %.2f \n" % (key, x, yields[key][x], err[key][x]))

        
ll_out_dt=yields['llout']['dt_sub']
emu_in_dt=yields['emuin'][whichdt]
emu_out_dt=yields['emuout'][whichdt]

err_ll_out_dt=err['llout']['dt_sub']
err_emu_in_dt=err['emuin'][whichdt]
err_emu_out_dt=err['emuout'][whichdt]

sf='ll_out_dt/emu_out_dt'
ll_pred='ll_out_dt*emu_in_dt/emu_out_dt'

err_product=lambda A, B, a, b: sqrt((a*B)**2+(b*A)**2) # A*B
err_division=lambda A, B, a, b: sqrt((a/B)**2+(b*A/B**2)**2) # A/B
err_sf = err_division(ll_out_dt,emu_out_dt, err_ll_out_dt, err_emu_out_dt)
err_ll_pred = err_product(eval(sf), emu_in_dt, err_sf, err_emu_in_dt)

ll_exp=yields['llin']['nonres']
err_ll_exp=err['llin']['nonres']

outtxt.write('\n'+'*'*20+'\n')
outtxt.write("result: predict = %.2f +- %.2f, expectation = %.2f +- %.2f\n" % (eval(ll_pred), err_ll_pred, ll_exp, err_ll_exp))
outtxt.write("N_llout/N_euout: ratio = %.2f +- %.2f\n" % (eval(sf), err_sf))

outtxt.close()

os.system('cat '+outtxt.name)

# Draw the m_ll in z window with data-driven non-res bkg
h_mll_nonres_dd=copy.deepcopy(histo['emu'][whichdt])
h_mll_nonres_dd.Scale(eval(sf))
#h_mll_nonres_dd.Rebin(2)
h_mll_nonres_dd.SetFillColor(ROOT.kAzure-9)

stackTag=tag+'_mll'
fstack=ROOT.TFile(outdir+'/'+stackTag+'.root')
hs=fstack.Get(stackTag+"_stack")
hframe=fstack.Get(stackTag+'_frame')
hframe.GetXaxis().SetRangeUser(70, 100)
hdata=fstack.Get(stackTag+'_data')
legend=fstack.Get(stackTag+'_legend')

hsnew=ROOT.THStack(stackTag+"_stack_new","")
hsnew.Add(h_mll_nonres_dd)

nonresTag=[stackTag+'_'+sample for sample in ['WJets','TT','WW'] ]

for ihist in hs.GetHists():
    if ihist.GetName() in nonresTag: print 'I am a nonres bkg: ',ihist.GetName()
    else:  hsnew.Add(ihist)

for ih in hsnew.GetHists():
    print '[debug] ', ih.GetName()
print hsnew
#hsnew.Draw()
hratio=GetRatio_TH1(hdata,hsnew,True)

myentry=ROOT.TLegendEntry(h_mll_nonres_dd,"non-Res. bkg(data-driven)","f")

# Let's remove the signal entries in the legend
for ileg in legend.GetListOfPrimitives():
    if ileg.GetLabel() in ['W+Jets', 'TT', 'WW, WZ non-reson.']:
        legend.GetListOfPrimitives().Remove(ileg)
    if ileg.GetLabel()=='Data': beforeObject=ileg

legend.GetListOfPrimitives().AddBefore(beforeObject,myentry)

drawStack_simple(hframe, hsnew, hdata, hratio, legend,
                 hstack_opt="A, HIST",
                 outDir=outdir, output=stackTag+"_datadriven", channel=ROOT.TString("inclusive"),
                 xmin=70, xmax=110, xtitle="M_{Z}^{ll}" ,units="GeV",
                 lumi=lumi, notes="")
