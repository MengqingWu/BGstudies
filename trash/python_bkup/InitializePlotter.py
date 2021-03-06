#!/usr/bin/env python

import ROOT
import os,copy
from TreePlotter import TreePlotter
from MergedPlotter import MergedPlotter
from myStackPlotter import StackPlotter

class InitializePlotter:
    def __init__(self, indir="../AnalysisRegion",
                 LogY=True,   doRatio=True,
                 addSig=True, addData=True,
                 doElMu=False):
        
        if doElMu: lepsf='elmununu_l1_l1_lepsf*elmununu_l1_l2_lepsf'
        else: lepsf='llnunu_l1_l1_lepsf*llnunu_l1_l2_lepsf'
        
        #######----------- Prepare samples to plot:
        zjetsPlotters=[]
        #zjetsSamples = ['DYJetsToLL_M50_HT100to200','DYJetsToLL_M50_HT200to400','DYJetsToLL_M50_HT400to600','DYJetsToLL_M50_HT600toInf']
        #zjetsSamples = ['DYJetsToLL_M50','DYJetsToLL_M50_Ext']
        zjetsSamples = ['DYJetsToLL_M50_BIG'] # M50_BIG = M50 + M50_Ext

        for sample in zjetsSamples:
            zjetsPlotters.append(TreePlotter(indir+'/'+sample+'.root','tree'))
            zjetsPlotters[-1].addCorrectionFactor('1./SumWeights','tree')
            #zjetsPlotters[-1].addCorrectionFactor('xsec','tree')
            zjetsPlotters[-1].addCorrectionFactor('(1921.8*3)','xsec')
            zjetsPlotters[-1].addCorrectionFactor('genWeight','tree')
            zjetsPlotters[-1].addCorrectionFactor('puWeight','tree')
            zjetsPlotters[-1].addCorrectionFactor('triggersf','tree')
            zjetsPlotters[-1].addCorrectionFactor(lepsf,'tree')

        self.ZJets = MergedPlotter(zjetsPlotters)
        self.ZJets.setFillProperties(1001,ROOT.kGreen+2)


        wwPlotters=[]
        wwSamples = ['WWTo2L2Nu','WWToLNuQQ','WZTo1L1Nu2Q']
        
        for sample in wwSamples:
            wwPlotters.append(TreePlotter(indir+'/'+sample+'.root','tree'))
            wwPlotters[-1].addCorrectionFactor('1./SumWeights','tree')
            wwPlotters[-1].addCorrectionFactor('xsec','tree')
            wwPlotters[-1].addCorrectionFactor('genWeight','tree')
            wwPlotters[-1].addCorrectionFactor('puWeight','tree')
            wwPlotters[-1].addCorrectionFactor('triggersf','tree')
            wwPlotters[-1].addCorrectionFactor(lepsf,'tree')
            
        self.WW = MergedPlotter(wwPlotters)
        self.WW.setFillProperties(1001,ROOT.kOrange)
            
            
        vvPlotters=[]
        vvSamples = ['WZTo2L2Q','WZTo3LNu',
                     'ZZTo2L2Nu',
                     'ZZTo2L2Q','ZZTo4L']
            
        for sample in vvSamples:
            vvPlotters.append(TreePlotter(indir+'/'+sample+'.root','tree'))
            vvPlotters[-1].addCorrectionFactor('1./SumWeights','tree')
            vvPlotters[-1].addCorrectionFactor('xsec','tree')
            vvPlotters[-1].addCorrectionFactor('genWeight','tree')
            vvPlotters[-1].addCorrectionFactor('puWeight','tree')
            vvPlotters[-1].addCorrectionFactor('triggersf','tree')
            vvPlotters[-1].addCorrectionFactor(lepsf,'tree')
        
        self.VV = MergedPlotter(vvPlotters)
        self.VV.setFillProperties(1001,ROOT.kMagenta)
            
        wjetsPlotters=[]
        wjetsSamples = ['WJetsToLNu']
            
        for sample in wjetsSamples:
            wjetsPlotters.append(TreePlotter(indir+'/'+sample+'.root','tree'))
            wjetsPlotters[-1].addCorrectionFactor('1./SumWeights','tree')
            wjetsPlotters[-1].addCorrectionFactor('xsec','tree')
            wjetsPlotters[-1].addCorrectionFactor('genWeight','tree')
            wjetsPlotters[-1].addCorrectionFactor('puWeight','tree')
            wjetsPlotters[-1].addCorrectionFactor('triggersf','tree')
            wjetsPlotters[-1].addCorrectionFactor(lepsf,'tree')

        self.WJets = MergedPlotter(wjetsPlotters)
        self.WJets.setFillProperties(1001,ROOT.kBlue-6)

        ttPlotters=[]
        ttSamples = ['TTTo2L2Nu']#,'TTZToLLNuNu','TTWJetsToLNu']

        for sample in ttSamples:
            ttPlotters.append(TreePlotter(indir+'/'+sample+'.root','tree'))
            ttPlotters[-1].addCorrectionFactor('1./SumWeights','tree')
            ttPlotters[-1].addCorrectionFactor('xsec','tree')
            ttPlotters[-1].addCorrectionFactor('genWeight','tree')
            ttPlotters[-1].addCorrectionFactor('puWeight','tree')
            ttPlotters[-1].addCorrectionFactor('triggersf','tree')
            ttPlotters[-1].addCorrectionFactor(lepsf,'tree')
            
        self.TT = MergedPlotter(ttPlotters)
        self.TT.setFillProperties(1001,ROOT.kAzure-9)

        # --> define different background sets:
        nonZBGPlotters = []
        nonZBGSamples = wwSamples + vvSamples + wjetsSamples + ttSamples
        
        for sample in nonZBGSamples:
            nonZBGPlotters.append(TreePlotter(indir+'/'+sample+'.root','tree'))
            nonZBGPlotters[-1].addCorrectionFactor('1./SumWeights','tree')
            nonZBGPlotters[-1].addCorrectionFactor('xsec','tree')
            nonZBGPlotters[-1].addCorrectionFactor('genWeight','tree')
            nonZBGPlotters[-1].addCorrectionFactor('puWeight','tree')
            nonZBGPlotters[-1].addCorrectionFactor('triggersf','tree')
            nonZBGPlotters[-1].addCorrectionFactor(lepsf,'tree')

        self.NonZBG = MergedPlotter(nonZBGPlotters)
        self.NonZBG.setFillProperties(1001,ROOT.kPink+6)

        nonResBGPlotters = []
        nonResBGSamples = wwSamples + wjetsSamples + ttSamples
        
        for sample in nonResBGSamples:
            nonResBGPlotters.append(TreePlotter(indir+'/'+sample+'.root','tree'))
            nonResBGPlotters[-1].addCorrectionFactor('1./SumWeights','tree')
            nonResBGPlotters[-1].addCorrectionFactor('xsec','tree')
            nonResBGPlotters[-1].addCorrectionFactor('genWeight','tree')
            nonResBGPlotters[-1].addCorrectionFactor('puWeight','tree')
            nonResBGPlotters[-1].addCorrectionFactor('triggersf','tree')
            nonResBGPlotters[-1].addCorrectionFactor(lepsf,'tree')

        self.NonResBG = MergedPlotter(nonResBGPlotters)
        self.NonResBG.setFillProperties(1001,ROOT.kYellow)

        
        resBGPlotters = []
        resBGSamples = zjetsSamples + vvSamples

        for sample in resBGSamples:
            resBGPlotters.append(TreePlotter(indir+'/'+sample+'.root','tree'))
            resBGPlotters[-1].addCorrectionFactor('1./SumWeights','tree')
            resBGPlotters[-1].addCorrectionFactor('xsec','tree')
            resBGPlotters[-1].addCorrectionFactor('genWeight','tree')
            resBGPlotters[-1].addCorrectionFactor('puWeight','tree')
            resBGPlotters[-1].addCorrectionFactor('triggersf','tree')
            resBGPlotters[-1].addCorrectionFactor(lepsf,'tree')

        self.ResBG = MergedPlotter(resBGPlotters)
        self.ResBG.setFillProperties(1001,ROOT.kRed)

        
        # --> Prepare the signal plotters:
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
        if addSig:
            for sample in sigSamples:
                sigPlotters.append(TreePlotter(indir+'/'+sample+'.root','tree'))
                sigPlotters[-1].addCorrectionFactor('1./SumWeights','tree')
                sigPlotters[-1].addCorrectionFactor(str(sigXsec[sample]),'tree')
                sigPlotters[-1].addCorrectionFactor('genWeight','tree')
                sigPlotters[-1].addCorrectionFactor('puWeight','tree')
                sigPlotters[-1].addCorrectionFactor('triggersf','tree')
                sigPlotters[-1].addCorrectionFactor(lepsf,'tree')
                sigPlotters[-1].setFillProperties(0,ROOT.kWhite)
        else:
            print "[Info] I do not add Signal samples to plot "
                
        # --> Prepare data plotters:    
        dataPlotters=[]
        if doElMu:
            dataSamples = ['MuonEG_Run2015C_25ns_16Dec',
                           'MuonEG_Run2015D_16Dec']
        else: 
            dataSamples = ['SingleElectron_Run2015C_25ns_16Dec',
                           'SingleElectron_Run2015D_16Dec',
                           'SingleMuon_Run2015C_25ns_16Dec',
                           'SingleMuon_Run2015D_16Dec']
        if addData:
            for sample in dataSamples:
                dataPlotters.append(TreePlotter(indir+'/'+sample+'.root','tree'))
            
            self.Data = MergedPlotter(dataPlotters)
            self.Data.setFillProperties(1001,ROOT.kGreen+2)
            
        else:
            self.Data = None
            print "[Info] I do not add Data samples to plot "
            
        self.Stack = StackPlotter()
        if addData: self.Stack.addPlotter(self.Data, "data_obs", "Data", "data")
        self.Stack.addPlotter(self.WJets, "WJets","W+Jets", "background")
        self.Stack.addPlotter(self.WW, "WW","WW, WZ non-reson.", "background")
        self.Stack.addPlotter(self.TT, "TT","TT", "background")
        self.Stack.addPlotter(self.VV, "ZZ","ZZ, WZ reson.", "background")
        self.Stack.addPlotter(self.ZJets, "ZJets","Z+Jets", "background")
        
        if addSig:
            for i in range(len(sigSamples)):
                sigPlotters[i].setLineProperties(2,ROOT.kRed+i,2)
                self.Stack.addPlotter(sigPlotters[i],sigSamples[i],sigSampleNames[i],'signal')  

        self.Stack.setLog(LogY)
        self.Stack.doRatio(doRatio)
        
    def GetStack(self):
        return self.Stack

