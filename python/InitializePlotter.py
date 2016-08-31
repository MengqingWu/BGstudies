#!/usr/bin/env python

import ROOT
import os,copy,string
from TreePlotter import TreePlotter
from MergedPlotter import MergedPlotter
from myStackPlotter import StackPlotter

class InitializePlotter:
    def __init__(self, indir="./80X_20160825_light_Skim",
                 LogY=True,   doRatio=True,
                 addSig=True, addData=True,
                 doElMu=False, scaleElMu=False,
                 onlyStats=False,
                 sigK=1000):

        #--> Coefficiency:
        elmuWt=1.51 # number from 76X
        puWeight='puWeight68075'
        DataHLT=True
        doRhoScale=True
        ZJetsZPtWeight=True
        SignalAll1pb=True
        sigk=sigK if sigK else 1000

        if doElMu: # FIXME
            lepsf='elmununu_l1_l1_lepsf*elmununu_l1_l2_lepsf'
            triggersf='triggersf_elmu'
        else:
            lepsf='isosf*idsf*trksf'
            triggersf='trgsf'
        if doRhoScale: 
            lepsf=lepsf+"*(0.602*exp(-0.5*pow((rho-8.890)/6.187,2))+0.829*exp(-0.5*pow((rho-21.404)/10.866,2)))"
    
        if onlyStats: print "[info] plotters: only statistics involved"
        #######----------- Prepare samples to plot:
        zjetsPlotters=[]
        #self.zjetsSamples = ['DYJetsToLL_M50_BIG'] # 76X: M50_BIG = M50 + M50_Ext
        self.zjetsSamples = ['DYJetsToLL_M50', 'DYJetsToLL_M50_MGMLM_Ext1']

        print '[Info] zjets sample: %s' %(indir+'/'+self.zjetsSamples[0]+'.root')
        for sample in self.zjetsSamples:
            zjetsPlotters.append(TreePlotter(indir+'/'+sample+'.root','tree'))
            if not onlyStats:
                #zjetsPlotters[-1].addCorrectionFactor('1./SumWeights','norm')
                zjetsPlotters[-1].addCorrectionFactor('(1)','norm')    
                if ZJetsZPtWeight: zjetsPlotters[-1].addCorrectionFactor('ZPtWeight','ZPtWeight')    
                #zjetsPlotters[-1].addCorrectionFactor('xsec','tree')
                zjetsPlotters[-1].addCorrectionFactor('(1921.8*3)','xsec') # FEWZ NNLO.results_z_m50_nnlo_inclusive_NNPDF30_nlo_as_0118
                #zjetsPlotters[-1].addCorrectionFactor('genWeight','tree')
                zjetsPlotters[-1].addCorrectionFactor('ZJetsGenWeight','genWeight')
                zjetsPlotters[-1].addCorrectionFactor(puWeight,'tree')
                zjetsPlotters[-1].addCorrectionFactor(triggersf,'tree')
                zjetsPlotters[-1].addCorrectionFactor(lepsf,'tree')

        self.ZJets = MergedPlotter(zjetsPlotters)
        self.ZJets.setFillProperties(1001,ROOT.kGreen+2)


        wwPlotters=[]
        #self.wwSamples = ['WWTo2L2Nu','WWToLNuQQ','WZTo1L1Nu2Q'] # 76X
        self.wwSamples = ['WWTo2L2Nu','WWToLNuQQ_BIG','WZTo1L1Nu2Q']


        for sample in self.wwSamples:
            wwPlotters.append(TreePlotter(indir+'/'+sample+'.root','tree'))
            if not onlyStats:
                wwPlotters[-1].addCorrectionFactor('1./SumWeights','tree')
                wwPlotters[-1].addCorrectionFactor('xsec','tree')
                wwPlotters[-1].addCorrectionFactor('genWeight','tree')
                wwPlotters[-1].addCorrectionFactor(puWeight,'tree')
                wwPlotters[-1].addCorrectionFactor(triggersf,'tree')
                wwPlotters[-1].addCorrectionFactor(lepsf,'tree')
            
        self.WW = MergedPlotter(wwPlotters)
        self.WW.setFillProperties(1001,ROOT.kOrange)
            
            
        vvPlotters=[]
        #self.vvSamples = ['WZTo2L2Q','WZTo3LNu','ZZTo2L2Nu','ZZTo2L2Q','ZZTo4L']#76X
        self.vvSamples = ['WZTo2L2Q','WZTo3LNu_AMCNLO',
                          'ZZTo2L2Nu',
                          'ZZTo2L2Q','ZZTo4L']
            
        for sample in self.vvSamples:
            vvPlotters.append(TreePlotter(indir+'/'+sample+'.root','tree'))
            if not onlyStats:
                vvPlotters[-1].addCorrectionFactor('1./SumWeights','tree')
                vvPlotters[-1].addCorrectionFactor('xsec','tree')
                vvPlotters[-1].addCorrectionFactor('genWeight','tree')
                vvPlotters[-1].addCorrectionFactor(puWeight,'tree')
                vvPlotters[-1].addCorrectionFactor(triggersf,'tree')
                vvPlotters[-1].addCorrectionFactor(lepsf,'tree')
  
        
        self.VV = MergedPlotter(vvPlotters)
        self.VV.setFillProperties(1001,ROOT.kMagenta)

        #ggZZPlotters=[]
        #ggZZSamples = ['ggZZTo2e2nu','ggZZTo2mu2nu']

        #for sample in ggZZSamples:
        #    ggZZPlotters.append(TreePlotter(indir+'/'+sample+'.root','tree'))
        #    ggZZPlotters[-1].addCorrectionFactor('1./SumWeights','tree')
        #    ggZZPlotters[-1].addCorrectionFactor('xsec','tree')
        #    ggZZPlotters[-1].addCorrectionFactor('genWeight','genWeight')
        #    ggZZPlotters[-1].addCorrectionFactor(puWeight,'tree')
        #    ggZZPlotters[-1].addCorrectionFactor('(llnunu_l1_l1_lepsf*llnunu_l1_l2_lepsf)','tree')
        #    ggZZPlotters[-1].addCorrectionFactor('triggersf','tree')
        #    allPlotters[sample] = ggZZPlotters[-1]

        #self.ggZZ = MergedPlotter(ggZZPlotters)
        #self.ggZZ.setFillProperties(1001,ROOT.kRed)

        wjetsPlotters=[]
        self.wjetsSamples = ['WJetsToLNu']
            
        for sample in self.wjetsSamples:
            wjetsPlotters.append(TreePlotter(indir+'/'+sample+'.root','tree'))
            if not onlyStats:
                wjetsPlotters[-1].addCorrectionFactor('1./SumWeights','tree')
                wjetsPlotters[-1].addCorrectionFactor('xsec','tree')
                wjetsPlotters[-1].addCorrectionFactor('genWeight','tree')
                wjetsPlotters[-1].addCorrectionFactor(puWeight,'tree')
                wjetsPlotters[-1].addCorrectionFactor(triggersf,'tree')
                wjetsPlotters[-1].addCorrectionFactor(lepsf,'tree')
    
        self.WJets = MergedPlotter(wjetsPlotters)
        self.WJets.setFillProperties(1001,ROOT.kBlue-6)

        ttPlotters=[]
        #self.ttSamples = ['TTTo2L2Nu']#,'TTZToLLNuNu','TTWJetsToLNu'] #76X
        self.ttSamples = ['TTTo2L2Nu','TTZToLLNuNu','TTWJetsToLNu']

        for sample in self.ttSamples:
            ttPlotters.append(TreePlotter(indir+'/'+sample+'.root','tree'))
            if not onlyStats:
                ttPlotters[-1].addCorrectionFactor('1./SumWeights','tree')
                ttPlotters[-1].addCorrectionFactor('xsec','tree')
                ttPlotters[-1].addCorrectionFactor('genWeight','tree')
                ttPlotters[-1].addCorrectionFactor(puWeight,'tree')
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

        allBGPlotters = zjetsPlotters + wwPlotters + vvPlotters + wjetsPlotters + ttPlotters
        self.allBGSamples = self.zjetsSamples + self.wwSamples + self.vvSamples + self.wjetsSamples + self.ttSamples
        self.allBG = MergedPlotter(allBGPlotters)
        self.allBG.setFillProperties(1001, ROOT.kRed)
        
        # --> Prepare the signal plotters:
        self.sigPlotters=[]
        self.sigSamples = [
            'BulkGravToZZToZlepZinv_narrow_600',
            #'BulkGravToZZToZlepZinv_narrow_800',
            'BulkGravToZZToZlepZinv_narrow_1000',
            #'BulkGravToZZToZlepZinv_narrow_1200',
            #'BulkGravToZZToZlepZinv_narrow_1400',
            #'BulkGravToZZToZlepZinv_narrow_1600', 
            #'BulkGravToZZToZlepZinv_narrow_1800', 
            'BulkGravToZZToZlepZinv_narrow_2000',
            #'BulkGravToZZToZlepZinv_narrow_2500',
            #'BulkGravToZZToZlepZinv_narrow_3000',
            #'BulkGravToZZToZlepZinv_narrow_3500', 
            #'BulkGravToZZToZlepZinv_narrow_4000', 
            #'BulkGravToZZToZlepZinv_narrow_4500', 
        ]

        sigSampleNames = {
            'BulkGravToZZToZlepZinv_narrow_600': str(sigk)+' x BulkG-600',
            'BulkGravToZZToZlepZinv_narrow_800': str(sigk)+' x BulkG-800',
            'BulkGravToZZToZlepZinv_narrow_1000':str(sigk)+' x BulkG-1000',
            'BulkGravToZZToZlepZinv_narrow_1200':str(sigk)+' x BulkG-1200',
            'BulkGravToZZToZlepZinv_narrow_1400':str(sigk)+' x BulkG-1400',
            'BulkGravToZZToZlepZinv_narrow_1600':str(sigk)+' x BulkG-1600',
            'BulkGravToZZToZlepZinv_narrow_1800':str(sigk)+' x BulkG-1800',
            'BulkGravToZZToZlepZinv_narrow_2000':str(sigk)+' x BulkG-2000',
            'BulkGravToZZToZlepZinv_narrow_2500':str(sigk)+' x BulkG-2500',
            'BulkGravToZZToZlepZinv_narrow_3000':str(sigk)+' x BulkG-3000',
            'BulkGravToZZToZlepZinv_narrow_3500':str(sigk)+' x BulkG-3500',
            'BulkGravToZZToZlepZinv_narrow_4000':str(sigk)+' x BulkG-4000',
            'BulkGravToZZToZlepZinv_narrow_4500':str(sigk)+' x BulkG-4500',
        }
        BulkGZZ2l2nuXsec = {
            600:8.61578e-03,
            800:1.57965e-03,
            1000:4.21651e-04,
            1200:1.39919e-04,
            1400:5.32921e-05,
            1600:2.24428e-05,
            1800:1.01523e-05,
            2000:4.86037e-06,
            2500:9.08739e-07,
            3000:1.98856e-07,
            3500:4.87505e-08,
            4000:1.25937e-08,
            4500:1.0,
        }
        sigXsec = {
            'BulkGravToZZToZlepZinv_narrow_600'  : BulkGZZ2l2nuXsec[600]*sigk,
            'BulkGravToZZToZlepZinv_narrow_800'  : BulkGZZ2l2nuXsec[800]*sigk,
            'BulkGravToZZToZlepZinv_narrow_1000' : BulkGZZ2l2nuXsec[1000]*sigk,
            'BulkGravToZZToZlepZinv_narrow_1200' : BulkGZZ2l2nuXsec[1200]*sigk,
            'BulkGravToZZToZlepZinv_narrow_1400' : BulkGZZ2l2nuXsec[1400]*sigk,
            'BulkGravToZZToZlepZinv_narrow_1600' : BulkGZZ2l2nuXsec[1600]*sigk,
            'BulkGravToZZToZlepZinv_narrow_1800' : BulkGZZ2l2nuXsec[1800]*sigk,
            'BulkGravToZZToZlepZinv_narrow_2000' : BulkGZZ2l2nuXsec[2000]*sigk,
            'BulkGravToZZToZlepZinv_narrow_2500' : BulkGZZ2l2nuXsec[2500]*sigk,
            'BulkGravToZZToZlepZinv_narrow_3000' : BulkGZZ2l2nuXsec[3000]*sigk,
            'BulkGravToZZToZlepZinv_narrow_3500' : BulkGZZ2l2nuXsec[3500]*sigk,
            'BulkGravToZZToZlepZinv_narrow_4000' : BulkGZZ2l2nuXsec[4000]*sigk,
            'BulkGravToZZToZlepZinv_narrow_4500' : BulkGZZ2l2nuXsec[4500]*sigk,
        }

        if SignalAll1pb:
            for sig in self.sigSamples:
                sigXsec[sig] = 1.0
                sigSampleNames[sig] = string.replace(sigSampleNames[sig], str(sigk)+' x', '1 pb')
        
        if addSig:
            for sample in self.sigSamples:
                self.sigPlotters.append(TreePlotter(indir+'/'+sample+'.root','tree'))
                if not onlyStats:
                    self.sigPlotters[-1].addCorrectionFactor('1./SumWeights','tree')
                    self.sigPlotters[-1].addCorrectionFactor(str(sigXsec[sample]),'xsec')
                    self.sigPlotters[-1].addCorrectionFactor('genWeight','tree')
                    self.sigPlotters[-1].addCorrectionFactor(puWeight,'tree')
                    self.sigPlotters[-1].addCorrectionFactor(triggersf,'tree')
                    self.sigPlotters[-1].addCorrectionFactor(lepsf,'tree')
                    self.sigPlotters[-1].setFillProperties(0,ROOT.kWhite)
        else:
            print "[Info] NO Signal samples added to plot "
                
        # --> Prepare data plotters:    
        dataPlotters=[]
        if doElMu:
            self.dataSamples = ['MuonEG_Run2015C_25ns_16Dec',
                                'MuonEG_Run2015D_16Dec'] #FIXME
        else:
            self.dataSamples = [
                #'SingleMuon_Run2016B_PromptReco_v2',
                #'SingleElectron_Run2016B_PromptReco_v2',
                #'SingleMuon_Run2016C_PromptReco_v2',
                #'SingleElectron_Run2016C_PromptReco_v2',
                #'SingleMuon_Run2016D_PromptReco_v2',
                #'SingleElectron_Run2016D_PromptReco_v2',
                'SingleEMU_Run2016BCD_PromptReco',
            ]
            
        if addData:
            for sample in self.dataSamples:
                if doElMu and scaleElMu:
                    dataPlotters.append(TreePlotter(indir+'/'+sample+'.root','tree', elmuWt))
                    dataPlotters[-1].addCorrectionFactor('Melmu_sf','tree')
                else:
                    dataPlotters.append(TreePlotter(indir+'/'+sample+'.root','tree'))
            if DataHLT:
                dataPlotters[0].addCorrectionFactor('(HLT_MUv2||HLT_ELEv2)','HLT') 
            self.Data = MergedPlotter(dataPlotters)
            self.Data.setFillProperties(1001,ROOT.kGreen+2) # for zjets data-driven plot
            
        else:
            self.Data = None
            print "[Info] NO Data samples added to plot "

        #--> stack plotter prepared:
        self.Stack = StackPlotter()
        if addData: self.Stack.addPlotter(self.Data, "data_obs", "Data", "data")
        #self.Stack.addPlotter(self.WJets, "WJets","W+Jets", "background")
        self.Stack.addPlotter(self.WW, "VVNonReso","WW/WZ non-reson.", "background")
        self.Stack.addPlotter(self.TT, "TT","TT", "background")
        self.Stack.addPlotter(self.VV, "VVZReso","ZZ/WZ reson.", "background")
        #Stack.addPlotter(self.ggZZ, "ggZZ","ggZZ", "background")
        self.Stack.addPlotter(self.ZJets, "ZJets","Z+Jets", "background")
        
        if addSig:
            for i in range(len(self.sigSamples)):
                self.sigPlotters[i].setLineProperties(2,ROOT.kRed+i,2)
                self.Stack.addPlotter(self.sigPlotters[i],self.sigSamples[i],sigSampleNames[self.sigSamples[i]],'signal')  

        self.Stack.setLog(LogY)
        self.Stack.doRatio(doRatio)
        
    def GetStack(self):
        return self.Stack

