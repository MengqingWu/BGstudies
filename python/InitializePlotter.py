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
                 doElMu=False, scaleElMu=False,
                 doMetCorr=False, scaleDphi=False,
                 zjetsscale=False,
                 sigK=1000):
        
        if doElMu:
            lepsf='elmununu_l1_l1_lepsf*elmununu_l1_l2_lepsf'
            triggersf='triggersf_elmu'
        else:
            lepsf='llnunu_l1_l1_lepsf*llnunu_l1_l2_lepsf'
            triggersf='triggersf'

        suffix="_V4_doJetsCorrUseLepResPtErrSel8JetLepSigProtectV2MetShift" if doMetCorr else ""
 
        #######----------- Prepare samples to plot:
        zjetsPlotters=[]
        #zjetsSamples = ['DYJetsToLL_M50_HT100to200','DYJetsToLL_M50_HT200to400','DYJetsToLL_M50_HT400to600','DYJetsToLL_M50_HT600toInf']
        #zjetsSamples = ['DYJetsToLL_M50','DYJetsToLL_M50_Ext']
        if doMetCorr:
            self.zjetsSamples = ['DYJetsToLL_M50_BIG_ZPt_V4_doJetsCorrUseLepResPtErrSel8JetLepSigProtectV2MetShiftZJetsReso'] # M50_BIG = M50 + M50_Ext
        else:
            self.zjetsSamples = ['DYJetsToLL_M50_BIG'] # M50_BIG = M50 + M50_Ext
        
        print '[Info] zjets sample: ', self.zjetsSamples[0]
        for sample in self.zjetsSamples:
            zjetsPlotters.append(TreePlotter(indir+'/'+sample+'.root','tree'))
            zjetsPlotters[-1].addCorrectionFactor('1./SumWeights','tree')
            #zjetsPlotters[-1].addCorrectionFactor('xsec','tree')
            zjetsPlotters[-1].addCorrectionFactor('(1921.8*3)','xsec')
            zjetsPlotters[-1].addCorrectionFactor('genWeight','tree')
            zjetsPlotters[-1].addCorrectionFactor('puWeight','tree')
            zjetsPlotters[-1].addCorrectionFactor(triggersf,'tree')
            zjetsPlotters[-1].addCorrectionFactor(lepsf,'tree')
            if doMetCorr and zjetsscale:
                zjetsPlotters[-1].addCorrectionFactor('dphi_sf','tree')# to scale dphi shape in BCD regions as the one in regA
                        
        self.ZJets = MergedPlotter(zjetsPlotters)
        self.ZJets.setFillProperties(1001,ROOT.kGreen+2)


        wwPlotters=[]
        self.wwSamples = ['WWTo2L2Nu','WWToLNuQQ','WZTo1L1Nu2Q']
        
        for sample in self.wwSamples:
            wwPlotters.append(TreePlotter(indir+'/'+sample+suffix+'.root','tree'))
            wwPlotters[-1].addCorrectionFactor('1./SumWeights','tree')
            wwPlotters[-1].addCorrectionFactor('xsec','tree')
            wwPlotters[-1].addCorrectionFactor('genWeight','tree')
            wwPlotters[-1].addCorrectionFactor('puWeight','tree')
            wwPlotters[-1].addCorrectionFactor(triggersf,'tree')
            wwPlotters[-1].addCorrectionFactor(lepsf,'tree')
            
        self.WW = MergedPlotter(wwPlotters)
        self.WW.setFillProperties(1001,ROOT.kOrange)
            
            
        vvPlotters=[]
        self.vvSamples = ['WZTo2L2Q','WZTo3LNu',
                          'ZZTo2L2Nu',
                          'ZZTo2L2Q','ZZTo4L']
            
        for sample in self.vvSamples:
            vvPlotters.append(TreePlotter(indir+'/'+sample+suffix+'.root','tree'))
            vvPlotters[-1].addCorrectionFactor('1./SumWeights','tree')
            vvPlotters[-1].addCorrectionFactor('xsec','tree')
            vvPlotters[-1].addCorrectionFactor('genWeight','tree')
            vvPlotters[-1].addCorrectionFactor('puWeight','tree')
            vvPlotters[-1].addCorrectionFactor(triggersf,'tree')
            vvPlotters[-1].addCorrectionFactor(lepsf,'tree')
        
        self.VV = MergedPlotter(vvPlotters)
        self.VV.setFillProperties(1001,ROOT.kMagenta)
            
        wjetsPlotters=[]
        self.wjetsSamples = ['WJetsToLNu']
            
        for sample in self.wjetsSamples:
            wjetsPlotters.append(TreePlotter(indir+'/'+sample+suffix+'.root','tree'))
            wjetsPlotters[-1].addCorrectionFactor('1./SumWeights','tree')
            wjetsPlotters[-1].addCorrectionFactor('xsec','tree')
            wjetsPlotters[-1].addCorrectionFactor('genWeight','tree')
            wjetsPlotters[-1].addCorrectionFactor('puWeight','tree')
            wjetsPlotters[-1].addCorrectionFactor(triggersf,'tree')
            wjetsPlotters[-1].addCorrectionFactor(lepsf,'tree')

        self.WJets = MergedPlotter(wjetsPlotters)
        self.WJets.setFillProperties(1001,ROOT.kBlue-6)

        ttPlotters=[]
        self.ttSamples = ['TTTo2L2Nu']#,'TTZToLLNuNu','TTWJetsToLNu']

        for sample in self.ttSamples:
            ttPlotters.append(TreePlotter(indir+'/'+sample+suffix+'.root','tree'))
            ttPlotters[-1].addCorrectionFactor('1./SumWeights','tree')
            ttPlotters[-1].addCorrectionFactor('xsec','tree')
            ttPlotters[-1].addCorrectionFactor('genWeight','tree')
            ttPlotters[-1].addCorrectionFactor('puWeight','tree')
            ttPlotters[-1].addCorrectionFactor(triggersf,'tree')
            ttPlotters[-1].addCorrectionFactor(lepsf,'tree')
            
        self.TT = MergedPlotter(ttPlotters)
        self.TT.setFillProperties(1001,ROOT.kAzure-9)

        # --> define different background sets:
        nonZBGPlotters = wwPlotters + vvPlotters + wjetsPlotters + ttPlotters
        self.nonZBGSamples = self.wwSamples + self.vvSamples + self.wjetsSamples + self.ttSamples
        self.NonZBG = MergedPlotter(nonZBGPlotters)
        self.NonZBG.setFillProperties(1001,ROOT.kPink+6)

        nonResBGPlotters =  wwPlotters + wjetsPlotters + ttPlotters
        self.nonResBGSamples = self.wwSamples + self.wjetsSamples + self.ttSamples
        self.NonResBG = MergedPlotter(nonResBGPlotters)
        self.NonResBG.setFillProperties(1001,ROOT.kYellow)

        
        resBGPlotters = zjetsPlotters + vvPlotters
        self.resBGSamples = self.zjetsSamples + self.vvSamples
        self.ResBG = MergedPlotter(resBGPlotters)
        self.ResBG.setFillProperties(1001,ROOT.kRed)

        
        # --> Prepare the signal plotters:
        self.sigPlotters=[]
        self.sigSamples = [
            'BulkGravToZZToZlepZinv_narrow_800', 
            'BulkGravToZZToZlepZinv_narrow_1000', 
            'BulkGravToZZToZlepZinv_narrow_1200', 
        ]
        sigk=sigK if sigK else 1000
        self.sigSampleNames = [
            str(sigk)+' x BulkG-800',
            str(sigk)+' x BulkG-1000',
            str(sigk)+' x BulkG-1200',
        ]
        sigXsec = {
            'BulkGravToZZToZlepZinv_narrow_800'  : 4.42472e-04*sigk,
            'BulkGravToZZToZlepZinv_narrow_1000' : 1.33926e-04*sigk,
            'BulkGravToZZToZlepZinv_narrow_1200' : 4.76544e-05*sigk,
        }
        
        if addSig:
            for sample in self.sigSamples:
                self.sigPlotters.append(TreePlotter(indir+'/'+sample+suffix+'.root','tree'))
                self.sigPlotters[-1].addCorrectionFactor('1./SumWeights','tree')
                self.sigPlotters[-1].addCorrectionFactor(str(sigXsec[sample]),'tree')
                self.sigPlotters[-1].addCorrectionFactor('genWeight','tree')
                self.sigPlotters[-1].addCorrectionFactor('puWeight','tree')
                self.sigPlotters[-1].addCorrectionFactor(triggersf,'tree')
                self.sigPlotters[-1].addCorrectionFactor(lepsf,'tree')
                self.sigPlotters[-1].setFillProperties(0,ROOT.kWhite)
        else:
            print "[Info] I do not add Signal samples to plot "
                
        # --> Prepare data plotters:    
        dataPlotters=[]
        if doElMu:
            self.dataSamples = ['MuonEG_Run2015C_25ns_16Dec',
                           'MuonEG_Run2015D_16Dec']
        else:
            self.dataSamples = ['SingleElectron_Run2015C_25ns_16Dec',
                                'SingleElectron_Run2015D_16Dec',
                                'SingleMuon_Run2015C_25ns_16Dec',
                                'SingleMuon_Run2015D_16Dec']
        if addData:
            for sample in self.dataSamples:
                if doElMu and scaleElMu:
                    dataPlotters.append(TreePlotter(indir+'/'+sample+suffix+'.root','tree', weight='1.51'))
                    dataPlotters[-1].addCorrectionFactor('Melmu_sf','tree')
                else:
                    dataPlotters.append(TreePlotter(indir+'/'+sample+suffix+'.root','tree'))
                    if doMetCorr and scaleDphi:
                        dataPlotters[-1].addCorrectionFactor('dphi_sf','tree')# to scale dphi shape in BCD regions as the one in regA
                    
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
            for i in range(len(self.sigSamples)):
                self.sigPlotters[i].setLineProperties(2,ROOT.kRed+i,2)
                self.Stack.addPlotter(self.sigPlotters[i],self.sigSamples[i],self.sigSampleNames[i],'signal')  

        self.Stack.setLog(LogY)
        self.Stack.doRatio(doRatio)
        
    def GetStack(self):
        return self.Stack

