#!/usr/bin/env python

import ROOT
import os
from math import *
from collections import OrderedDict
from python.SetCuts import SetCuts
from python.InitializePlotter import InitializePlotter
from python.HistPrinter import mergePrinter

#Channel=raw_input("Please choose a channel (el or mu): \n")
tag0='nonResBkg'
outdir='test'
indir="../../AnalysisRegion_nonRes"
lumi=2.318278305
zpt_cut, met_cut= '100', '100'
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
setcuts=SetCuts()
cuts_ll={'inclusive':  setcuts.alphaCuts(Zmass='inclusive', zpt_cut=zpt_cut, met_cut=met_cut),
         'in':  setcuts.alphaCuts(isll=True, Zmass='in', zpt_cut=zpt_cut, met_cut=met_cut),
         'out': setcuts.alphaCuts(isll=True, Zmass='out', zpt_cut=zpt_cut, met_cut=met_cut)}
cuts_eu={'inclusive': setcuts.alphaCuts(isll=False, Zmass='inclusive', zpt_cut=zpt_cut, met_cut=met_cut),
         'in' : setcuts.alphaCuts(isll=False, Zmass='in', zpt_cut=zpt_cut, met_cut=met_cut),
         'out': setcuts.alphaCuts(isll=False, Zmass='out', zpt_cut=zpt_cut, met_cut=met_cut)}

ROOT.gROOT.ProcessLine('.x ../src/tdrstyle.C')

### ----- Execute (plotting):

plotter_ll.Stack.drawStack('llnunu_l1_mass', cuts_ll['inclusive'], str(lumi*1000), 10, 0.0, 200.0, titlex = "M_{Z}^{ll}", units = "GeV",
                       output=tag+'_mll',outDir=outdir, separateSignal=True,
                       drawtex="", channel="")
plotter_eu.Stack.drawStack('elmununu_l1_mass', cuts_eu['inclusive'], str(lumi*1000), 10, 0.0, 200.0, titlex = "M_{Z}^{e#mu}", units = "GeV",
                        output=tag+'_melmu',outDir=outdir, separateSignal=True,
                        drawtex="", channel="")

histo=OrderedDict()
yields=OrderedDict()
err=OrderedDict()
var_dic=OrderedDict({'elmununu_l1_mass':(10, 0.0, 200.0),
                  'llnunu_l1_mass':(10, 0.0, 200.0)})
keys=['nonres', 'res', 'dt']

for key in cuts_ll:
    if key=='inclusive': continue

    err['emu'+'_'+key] = OrderedDict({'nonres':ROOT.Double(0.0), 'res':ROOT.Double(0.0), 'dt':ROOT.Double(0.0)})
    err['ll'+'_'+key] = OrderedDict({'nonres':ROOT.Double(0.0), 'res':ROOT.Double(0.0), 'dt':ROOT.Double(0.0)})
    
    h_Memu_nonRes=plotter_eu.NonResBG.drawTH1('elmununu_l1_mass_nonRes'+'_'+'emu'+'_'+key, 'elmununu_l1_mass',cuts_eu[key],str(lumi*1000),10,0.0, 200.0,titlex='M_{Z}^{e#mu}',units='GeV',drawStyle="HIST")
    h_Memu_res=plotter_eu.ResBG.drawTH1('elmununu_l1_mass_res'+'_'+'emu'+'_'+key, 'elmununu_l1_mass',cuts_eu[key],str(lumi*1000),10,0.0, 200.0,titlex='M_{Z}^{e#mu}',units='GeV',drawStyle="HIST")
    h_Memu_dt=plotter_eu.Data.drawTH1('elmununu_l1_mass_dt'+'_'+'emu'+'_'+key,'elmununu_l1_mass',cuts_eu[key],'1',10,0.0, 200.0,titlex='M_{Z}^{e#mu}',units='GeV',drawStyle="HIST") 
    yields['emu'+'_'+key]=OrderedDict({'nonres': h_Memu_nonRes.IntegralAndError(0,1+h_Memu_nonRes.GetNbinsX(),err['emu'+'_'+key]['nonres']),
                                   'res':    h_Memu_res.IntegralAndError(0,1+h_Memu_res.GetNbinsX(),err['emu'+'_'+key]['res']),
                                   'dt':     h_Memu_dt.IntegralAndError(0,1+h_Memu_dt.GetNbinsX(),err['emu'+'_'+key]['dt']) })

    h_Mll_nonRes=plotter_ll.NonResBG.drawTH1('llnunu_l1_mass_nonRes'+'_'+'ll'+'_'+key,'llnunu_l1_mass',cuts_ll[key],str(lumi*1000),10,0.0, 200.0,titlex='M_{Z}^{ll}',units='GeV',drawStyle="HIST")
    h_Mll_res=plotter_ll.ResBG.drawTH1('llnunu_l1_mass_res'+'_'+'ll'+'_'+key,'llnunu_l1_mass',cuts_ll[key],str(lumi*1000),10,0.0, 200.0,titlex='M_{Z}^{ll}',units='GeV',drawStyle="HIST")
    h_Mll_dt=plotter_ll.Data.drawTH1('llnunu_l1_mass_dt'+'_'+'ll'+'_'+key,'llnunu_l1_mass',cuts_ll[key],'1',10,0.0, 200.0,titlex='M_{Z}^{ll}',units='GeV',drawStyle="HIST")
    yields['ll'+'_'+key]=OrderedDict({'nonres': h_Mll_nonRes.IntegralAndError(0,1+h_Mll_nonRes.GetNbinsX(),err['ll'+'_'+key]['nonres']),
                                   'res':    h_Mll_res.IntegralAndError(0,1+h_Mll_res.GetNbinsX(),err['ll'+'_'+key]['res']),
                                   'dt':     h_Mll_dt.IntegralAndError(0,1+h_Mll_dt.GetNbinsX(),err['ll'+'_'+key]['dt']) })


    histo['emu'+'_'+key]  = (cuts_eu[key],h_Mll_nonRes,h_Mll_res,h_Mll_dt)
    histo['ll'+'_'+key] = (cuts_ll[key],h_Memu_nonRes,h_Memu_res,h_Memu_dt)

### ----- Finalizing:
mergePrinter(histo=histo, outTag=outTag+'_all')
print '*'*20
for key in yields:
    for x in yields[key]:
        print key, ' ', x, ': ', yields[key][x], '+-', err[key][x]

        
ll_out_dt=yields['ll_out']['dt']-yields['ll_out']['res']
emu_in_dt=yields['emu_in']['dt']-yields['emu_in']['res']
emu_out_dt=yields['emu_out']['dt']-yields['emu_out']['res']

err_diff=lambda x, y: sqrt(x**2+y**2) # x-y or y-x
err_ll_out_dt=err_diff(err['ll_out']['dt'],err['ll_out']['res'])
err_emu_in_dt=err_diff(err['emu_in']['dt'],err['emu_in']['res'])
err_emu_out_dt=err_diff(err['emu_out']['dt'],err['emu_out']['res'])

sf='ll_out_dt/emu_out_dt'
ll_pred='ll_out_dt*emu_in_dt/emu_out_dt'

err_product=lambda A, B, a, b: sqrt((a*B)**2+(b*A)**2) # A*B
err_division=lambda A, B, a, b: sqrt((a/B)**2+(b*A/B**2)**2) # A/B
err_sf = err_division(ll_out_dt,emu_out_dt, err_ll_out_dt, err_emu_out_dt)
err_ll_pred = err_product(eval(sf), emu_in_dt, err_sf, err_emu_in_dt)

ll_exp=yields['ll_in']['nonres']
err_ll_exp=err['ll_in']['nonres']

print '*'*20
print "result: predict = %.2f +- %.2f, expectation = %.2f +- %.2f" % (eval(ll_pred), err_ll_pred, ll_exp, err_ll_exp)
print "N_llout/N_euout: ratio = %.2f +- %.2f" % (eval(sf), err_sf)
