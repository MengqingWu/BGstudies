#!/usr/bin/env python

import ROOT
import os,copy
from CMGTools.XZZ2l2nu.plotting.TreePlotter import TreePlotter
from CMGTools.XZZ2l2nu.plotting.MergedPlotter import MergedPlotter
from CMGTools.XZZ2l2nu.plotting.StackPlotter import StackPlotter
from CMGTools.XZZ2l2nu.plotting.SimplePlot import *



class NtupleStacker:
    def __init__(self, indir="/afs/cern.ch/work/m/mewu/public/76X_new", outdir='./NtuplePlots',
                 lumi = 2.169126704526,  sepSig=True,
                 LogY=True,   doRatio=True):
        if not os.path.exists(outdir): os.system('mkdir '+outdir)

        #self.Channel=raw_input("Please choose a channel (el or mu): \n")
        self.outdir = outdir
        self.lumi = lumi
        self.sepSig = sepSig
        #self.whichregion=raw_input("Please choose a benchmarck Region (SR or VR): \n")
        #self.cuts = python.SetCuts.Cuts(self.Channel, self.whichregion)
        #self.preCuts = python.SetCuts.Cuts(self.Channel, self.whichregion, True)
        
        #######----------- Prepare samples to plot:
        wwPlotters=[]
        wwSamples = ['WWTo2L2Nu','WWToLNuQQ','WZTo1L1Nu2Q']
        
        for sample in wwSamples:
            wwPlotters.append(TreePlotter(indir+'/'+sample+'/vvTreeProducer/tree.root','tree'))
            wwPlotters[-1].setupFromFile(indir+'/'+sample+'/skimAnalyzerCount/SkimReport.pck')
            wwPlotters[-1].addCorrectionFactor('xsec','tree')
            wwPlotters[-1].addCorrectionFactor('genWeight','tree')
            wwPlotters[-1].addCorrectionFactor('puWeight','tree')
            
        WW = MergedPlotter(wwPlotters)
        WW.setFillProperties(1001,ROOT.kOrange)
            
            
        vvPlotters=[]
        vvSamples = ['WZTo2L2Q','WZTo3LNu',
                     'ZZTo2L2Nu',
                     'ZZTo2L2Q','ZZTo4L']
            
        for sample in vvSamples:
            vvPlotters.append(TreePlotter(indir+'/'+sample+'/vvTreeProducer/tree.root','tree'))
            vvPlotters[-1].setupFromFile(indir+'/'+sample+'/skimAnalyzerCount/SkimReport.pck')
            vvPlotters[-1].addCorrectionFactor('xsec','tree')
            vvPlotters[-1].addCorrectionFactor('genWeight','tree')
            vvPlotters[-1].addCorrectionFactor('puWeight','tree')
            
        VV = MergedPlotter(vvPlotters)
        VV.setFillProperties(1001,ROOT.kMagenta)
            
        wjetsPlotters=[]
        wjetsSamples = ['WJetsToLNu']
            
        for sample in wjetsSamples:
            wjetsPlotters.append(TreePlotter(indir+'/'+sample+'/vvTreeProducer/tree.root','tree'))
            wjetsPlotters[-1].setupFromFile(indir+'/'+sample+'/skimAnalyzerCount/SkimReport.pck')
            wjetsPlotters[-1].addCorrectionFactor('xsec','tree')
            wjetsPlotters[-1].addCorrectionFactor('genWeight','tree')
            wjetsPlotters[-1].addCorrectionFactor('puWeight','tree')

        WJets = MergedPlotter(wjetsPlotters)
        WJets.setFillProperties(1001,ROOT.kBlue-6)

        zjetsPlotters=[]
        #zjetsSamples = ['DYJetsToLL_M50_HT100to200','DYJetsToLL_M50_HT200to400','DYJetsToLL_M50_HT400to600','DYJetsToLL_M50_HT600toInf']
        #zjetsSamples = ['DYJetsToLL_M50','DYJetsToLL_M50_Ext']
        zjetsSamples = ['DYJetsToLL_M50_BIG'] # M50_BIG = M50 + M50_Ext

        for sample in zjetsSamples:
            zjetsPlotters.append(TreePlotter(indir+'/'+sample+'/vvTreeProducer/tree.root','tree'))
            zjetsPlotters[-1].setupFromFile(indir+'/'+sample+'/skimAnalyzerCount/SkimReport.pck')
            zjetsPlotters[-1].addCorrectionFactor('xsec','tree')
            zjetsPlotters[-1].addCorrectionFactor('genWeight','tree')
            zjetsPlotters[-1].addCorrectionFactor('puWeight','tree')

        self.ZJets = MergedPlotter(zjetsPlotters)
        self.ZJets.setFillProperties(1001,ROOT.kGreen+2)

        ttPlotters=[]
        ttSamples = ['TTTo2L2Nu']#,'TTZToLLNuNu','TTWJetsToLNu']

        for sample in ttSamples:
            ttPlotters.append(TreePlotter(indir+'/'+sample+'/vvTreeProducer/tree.root','tree'))
            ttPlotters[-1].setupFromFile(indir+'/'+sample+'/skimAnalyzerCount/SkimReport.pck')
            ttPlotters[-1].addCorrectionFactor('xsec','tree')
            ttPlotters[-1].addCorrectionFactor('genWeight','tree')
            ttPlotters[-1].addCorrectionFactor('puWeight','tree')
            
        TT = MergedPlotter(ttPlotters)
        TT.setFillProperties(1001,ROOT.kAzure-9)

        sigPlotters=[]
        sigSamples = [
            'BulkGravToZZToZlepZinv_narrow_800', 
            'BulkGravToZZToZlepZinv_narrow_1000', 
            'BulkGravToZZToZlepZinv_narrow_1200', 
        ]
        k=1000
        sigSampleNames = [
            str(k)+' x BulkG-800',
            str(k)+' x BulkG-1000',
            str(k)+' x BulkG-1200',
        ]
        sigXsec = {
            'BulkGravToZZToZlepZinv_narrow_800'  : 4.42472e-04*k,
            'BulkGravToZZToZlepZinv_narrow_1000' : 1.33926e-04*k,
            'BulkGravToZZToZlepZinv_narrow_1200' : 4.76544e-05*k,
        }

        for sample in sigSamples:
            sigPlotters.append(TreePlotter(indir+'/'+sample+'/vvTreeProducer/tree.root','tree'))
            sigPlotters[-1].setupFromFile(indir+'/'+sample+'/skimAnalyzerCount/SkimReport.pck')
            sigPlotters[-1].addCorrectionFactor(str(sigXsec[sample]),'tree')
            sigPlotters[-1].addCorrectionFactor('genWeight','tree')
            sigPlotters[-1].addCorrectionFactor('puWeight','tree')
            sigPlotters[-1].setFillProperties(0,ROOT.kWhite)


        dataPlotters=[]
        dataSamples = ['SingleElectron_Run2015C_25ns_16Dec',
                       'SingleElectron_Run2015D_16Dec',
                       'SingleMuon_Run2015C_25ns_16Dec',
                       'SingleMuon_Run2015D_16Dec']
        for sample in dataSamples:
            dataPlotters.append(TreePlotter(indir+'/'+sample+'/vvTreeProducer/tree.root','tree'))
            
        self.Data = MergedPlotter(dataPlotters)

        self.Stack = StackPlotter()
        self.Stack.addPlotter(self.Data, "data_obs", "Data", "data")
        #Stack.addPlotter(WJets, "WJets","W+Jets", "background")
        self.Stack.addPlotter(WW, "WW","WW, WZ non-reson.", "background")
        self.Stack.addPlotter(TT, "TT","TT", "background")
        self.Stack.addPlotter(VV, "ZZ","ZZ, WZ reson.", "background")
        self.Stack.addPlotter(self.ZJets, "ZJets","Z+Jets", "background")
        
        for i in range(len(sigSamples)):
            sigPlotters[i].setLineProperties(2,ROOT.kRed+i,2)
            self.Stack.addPlotter(sigPlotters[i],sigSamples[i],sigSampleNames[i],'signal')  
 
        self.Stack.setLog(LogY)
        self.Stack.doRatio(doRatio)
        ROOT.gROOT.ProcessLine('.x tdrstyle.C')

    def GetStack(self):
        return self.Stack

    def DrawRegion(self, cuts):

        tag ='looseCuts_'

        self.Stack.rmPlotter(self.Data, "data_obs","Data", "data")
        self.Stack.drawStack('met_pt', cuts, str(lumi*1000), 50, 0, 500, titlex = "E_{T}^{miss}", units = "GeV",output=tag+'met_low',outDir=outdir,separateSignal=sepSig,blinding=Blind,blindingCut=200)
        
        file=ROOT.TFile(self.outdir+'/'+tag+'met_low.root')
        hdata=self.Data.drawTH1('met_JECJER_pt', cuts,str(self.lumi*1000), 50, 0, 500,titlex='E_{T}^{miss}',units='GeV',drawStyle="HIST")
        
        hframe=file.Get(tag+'met_low_frame')
        hs=file.Get(tag+'met_low_stack')
        hs.Add(h_met_zjets)
        #hdata=file.Get(tag+'met_low_data')
        hratio=GetRatio_TH1(hdata,hs,True)
    
        legend=file.Get(tag+'met_low_legend')
        myentry=ROOT.TLegendEntry(hdata,"data","p")
        legend.GetListOfPrimitives().AddFirst(myentry)

        # Let's remove the signal entries in the legend 
        #for i in legend.GetListOfPrimitives():
            #if ROOT.TString(i.GetLabel()).Contains("Bulk"):
             #   legend.GetListOfPrimitives().Remove(i)
                
        drawStack_simple(hframe, hs, hdata,hratio,legend,
                         hstack_opt="A, HIST",
                         outDir=self.outdir, output=tag+'JER_met_low',channel=ROOT.TString(self.Channel),
                         xmin=xMin, xmax=xMax, xtitle="E_{T}^{miss}" ,units="GeV",
                         lumi=self.lumi, notes="MET with JEC and JER corrected jets")

        return
        
