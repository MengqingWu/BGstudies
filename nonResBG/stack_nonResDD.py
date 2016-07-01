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
        
        self.outdir = outdir
        self.lumi = lumi
        self.plotter_eu=InitializePlotter(indir, addSig=False, addData=True, doRatio=doRatio, doElMu=True, LogY=LogY)
        self.plotter_ll=InitializePlotter(indir, addSig=addSig, addData=True, doRatio=doRatio, LogY=LogY)
        self.plotter_ll.Stack.rmPlotter(self.plotter_ll.TT, "TT","TT", "background")
        self.plotter_ll.Stack.rmPlotter(self.plotter_ll.WW, "WW","WW, WZ non-reson.", "background")
        self.plotter_ll.Stack.rmPlotter(self.plotter_ll.WJets, "WJets","W+Jets", "background")
        
        self.setcuts=SetCuts()

        var={('llnunu_l1_mass', 'elmununu_l1_mass'): (40, 0.0, 200.0, "M_{Z}^{ll}", "GeV")}
        ROOT.gROOT.ProcessLine('.x ../src/tdrstyle.C')

    def drawDataDrivenStack(self):
        tag = 'stack_nonResDD'+'_'+'test'
        outTag = self.outdir+'/'+tag
        stackTag=tag+'_mll'
        zpt_cut, met_cut= '0', '0'
        cuts=self.setcuts.GetAlphaCuts(zpt_cut=zpt_cut, met_cut=met_cut)
                
        self.plotter_ll.Stack.drawStack('llnunu_l1_mass', cuts['ll']['inclusive'], str(self.lumi*1000), 40, 0.0, 200.0, titlex = "M_{Z}^{ll}", units = "GeV",
                                        output=stackTag, outDir=self.outdir, separateSignal=True, drawtex="", channel="")
        h_nonRes_dd = self.plotter_eu.Data.drawTH1('elmununu_l1_mass','elmununu_l1_mass', cuts['emu']['inclusive'], '1',
                                                   40, 0.0, 200.0, titlex = "M_{Z}^{e#mu}", units = "GeV", drawStyle="HIST")
        h_nonRes_dd.SetFillColor(ROOT.kAzure-9)
        
        # Draw the m_ll in z window with data-driven non-res bkg
        ROOT.TH1.AddDirectory(ROOT.kFALSE)
        fstack=ROOT.TFile(self.outdir+'/'+stackTag+'.root')
        hs=fstack.Get(stackTag+"_stack")
        hframe=fstack.Get(stackTag+'_frame')
        hframe.GetXaxis().SetRangeUser(70, 100)
        hdata=fstack.Get(stackTag+'_data')
        legend=fstack.Get(stackTag+'_legend')
        fstack.Close()
        
        hsnew=ROOT.THStack(stackTag+"_stack_new","")
        hsnew.Add(h_nonRes_dd)
        
        nonresTag=[stackTag+'_'+sample for sample in ['WJets','TT','WW'] ]
        for ihist in hs.GetHists():
            if ihist.GetName() in nonresTag: print '[Removing...] I am a nonres bkg : ',ihist.GetName()
            else:  hsnew.Add(ihist)
        
        for ih in hsnew.GetHists():
            print '[debug] ', ih.GetName()
        print hsnew
        #hsnew.Draw()
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
                         xmin=70, xmax=110, xtitle="M_{Z}^{ll}" ,units="GeV",
                         lumi=self.lumi, notes="")
        
    
