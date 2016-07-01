#!/usr/bin/env python

import ROOT
import os,copy
from math import *
from collections import OrderedDict
from python.SetCuts import SetCuts
from python.InitializePlotter import InitializePlotter
from python.HistPrinter import mergePrinter
from python.SimplePlot import *


#  ll in Z | ll out Z
# --------------------  M_out [35,65] U [115,120]
#  eu in Z | eu out Z
#  M_in (70,110)
class StackDataDriven:
    def __init__(self, indir="./nonResSkim_v3", outdir='stack_test',
                 lumi = 2.318278305,  sepSig=True,
                 LogY=True,   doRatio=True,
                 addSig=True, addData=True):
        if not os.path.exists(outdir): os.system('mkdir '+outdir)
        self.logy=LogY
        self.outdir = outdir
        self.lumi = lumi
        self.plotter_eu=InitializePlotter(indir, addSig=False, addData=True, doRatio=doRatio, doElMu=True, LogY=LogY)
        self.plotter_ll=InitializePlotter(indir, addSig=addSig, addData=True, doRatio=doRatio, LogY=LogY)
        self.plotter_ll.Stack.rmPlotter(self.plotter_ll.TT, "TT","TT", "background")
        self.plotter_ll.Stack.rmPlotter(self.plotter_ll.WW, "WW","WW, WZ non-reson.", "background")
        self.plotter_ll.Stack.rmPlotter(self.plotter_ll.WJets, "WJets","W+Jets", "background")
        
        self.setcuts=SetCuts()
        ROOT.gROOT.ProcessLine('.x ../src/tdrstyle.C')
        self.zpt_cut, self.met_cut= '0', '0'
        self.cuts=self.setcuts.GetAlphaCuts(zpt_cut=self.zpt_cut, met_cut=self.met_cut)
        
    def drawDataDrivenMC(self, var_ll, var_emu, nbinsx, xmin, xmax, titlex, units, xcutmin, xcutmax):
        
        h_nonRes_dd = self.plotter_eu.Data.drawTH1(var_emu, var_emu, self.cuts['emu']['in'], '1',
                                                   nbinsx, xmin, xmax, titlex = titlex, units = units, drawStyle="HIST")
        h_nonRes_mc = self.plotter_ll.NonResBG.drawTH1(var_ll, var_ll, self.cuts['ll']['in'], str(self.lumi*1000),
                                                       nbinsx, xmin, xmax, titlex = titlex, units = units, drawStyle="HIST")
        
        drawCompareSimple(h_nonRes_dd, h_nonRes_mc, "non-reson. data-driven", "non-reson. MC",
                          xmin=xcutmin, xmax=xcutmax, outdir=self.outdir, notes="",
                          tag='compare_dataDriven_MC'+'_'+var_ll, units=units, lumi=self.lumi, ytitle='events')
        
    def drawDataDrivenStack(self, var_ll, var_emu, nbinsx, xmin, xmax, titlex, units, xcutmin, xcutmax):
        tag = 'stack_nonResDD'+'_'+'test'
        outTag = self.outdir+'/'+tag
        stackTag=tag+'_'+var_ll
                
        self.plotter_ll.Stack.drawStack(var_ll, self.cuts['ll']['in'], str(self.lumi*1000), nbinsx, xmin, xmax, titlex = titlex, units = units,
                                        output=stackTag, outDir=self.outdir, separateSignal=True, drawtex="", channel="")
        h_nonRes_dd = self.plotter_eu.Data.drawTH1(var_emu, var_emu, self.cuts['emu']['in'], '1',
                                                   nbinsx, xmin, xmax, titlex = titlex, units = units, drawStyle="HIST")
        h_nonRes_dd.SetFillColor(ROOT.kAzure-9)
        
        # Draw the m_ll in z window with data-driven non-res bkg
        ROOT.TH1.AddDirectory(ROOT.kFALSE)
        fstack=ROOT.TFile(self.outdir+'/'+stackTag+'.root')
        hs=fstack.Get(stackTag+"_stack")

        hframe=fstack.Get(stackTag+'_frame')
        hframe.GetXaxis().SetRangeUser(xcutmin, xcutmax)
        if ROOT.TString(var_ll).Contains("mass"):
            if self.logy: hframe.SetMaximum(hframe.GetMaximum()*100)
            else: hframe.SetMaximum(hframe.GetMaximum()*1.2)
        
        hdata=fstack.Get(stackTag+'_data')
        legend=fstack.Get(stackTag+'_legend')
        
        hsig1=fstack.Get(stackTag+'_BulkGravToZZToZlepZinv_narrow_800')
        hsig2=fstack.Get(stackTag+'_BulkGravToZZToZlepZinv_narrow_1000')
        hsig3=fstack.Get(stackTag+'_BulkGravToZZToZlepZinv_narrow_1200')
        fstack.Close()

        print '[debug] llin, datadriven nonres: ', h_nonRes_dd.Integral()
        print '[debug] llin, dt: ', hdata.Integral()

        
        hsnew=ROOT.THStack(stackTag+"_stack_new","")
        hsnew.Add(h_nonRes_dd)
        
        nonresTag=[stackTag+'_'+sample for sample in ['WJets','TT','WW'] ]
        for ihist in hs.GetHists():
            if ihist.GetName() in nonresTag: print '[Removing...] I am a nonres bkg : ',ihist.GetName()
            else:  hsnew.Add(ihist)
        
        for ih in hsnew.GetHists():
            print '[debug] ', ih.GetName()
        print hsnew
        
        hratio=GetRatio_TH1(hdata,hsnew,True)
        
        myentry=ROOT.TLegendEntry(h_nonRes_dd,"non-reson. (data-driven)","f")
        
        # Let's remove the signal entries in the legend
        for ileg in legend.GetListOfPrimitives():
            if ileg.GetLabel() in ['W+Jets', 'TT', 'WW, WZ non-reson.']:
                legend.GetListOfPrimitives().Remove(ileg)
            if ileg.GetLabel()=='Data': beforeObject=ileg
        
        legend.GetListOfPrimitives().AddBefore(beforeObject,myentry)
        
        drawStack_simple(hframe, hsnew, hdata, hratio, legend,
                         hstack_opt="A, HIST",
                         outDir=self.outdir, output=stackTag+"_datadriven", channel=ROOT.TString("inclusive"),
                         xmin=xcutmin, xmax=xcutmax, xtitle=titlex ,units=units,
                         lumi=self.lumi, notes="no E_{T}^{miss}/P_{T}^{Z} cuts",
                         drawSig=True, hsig=[hsig1, hsig2, hsig3])
    
