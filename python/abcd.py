#!/usr/bin/env python

import ROOT
import os,copy

from python.InitializePlotter import InitializePlotter
from python.SimplePlot import *
from python.SetCuts import SetCuts


class abcdAnalyzer:
    def __init__(self, indir="../AnalysisRegion", outdir='plots',
                 lumi = 2.318278305,  sepSig=True,
                 LogY=True,   doRatio=True,
                 addSig=True, addData=True):

        if not os.path.exists(outdir): os.system('mkdir '+outdir)

        self.plotter=InitializePlotter(indir,addSig=addSig,addData=addData)
        self.mycuts= SetCuts()
        self.Channel=raw_input("Please choose a channel (el or mu): \n")
        self.outdir = outdir
        self.lumi = lumi
        self.sepSig = sepSig
        self.tex_dic = self.mycuts.Tex_dic
        self.whichregion=raw_input("Please choose a benchmarck Region (SR or VR): \n")
        
        self.cuts = self.mycuts.abcdCuts(self.Channel, self.whichregion)
        self.preCuts = self.mycuts.abcdCuts(self.Channel, self.whichregion, True)

        if self.whichregion=="VR":
            self.nbins, self.xMin, self.xMax = 10, 0, float(self.mycuts.met_pt)
        else:
            self.nbins, self.xMin, self.xMax = 10, 0, 500
                        
        self.plotter.Stack.setLog(LogY)
        self.plotter.Stack.doRatio(doRatio)
        ROOT.gROOT.ProcessLine('.x tdrstyle.C')

#######----------- Start Plotting:
    def draw_preselection(self):

        tag='PreSelection_'+self.Channel+'_'
        #print self.Stack.log
        
        if self.plotter.Stack.log: tag=tag+'log_'
        
        self.plotter.Stack.drawStack('llnunu_l2_pt', self.preCuts, str(self.lumi*1000), self.nbins, self.xMin, self.xMax, titlex = "E_{T}^{miss}", units = "GeV",
                        output=tag+'met_low',outDir=self.outdir,separateSignal=self.sepSig,
                        drawtex=self.whichregion+" pre-selection", channel=self.Channel)
        self.plotter.Stack.drawStack('llnunu_l1_deltaR', self.preCuts, str(self.lumi*1000), 30,0,3, titlex = "#Delta R(l,l)", units = "",
                        output=tag+'dR_ll',outDir=self.outdir,separateSignal=self.sepSig,
                        drawtex=self.whichregion+" pre-selection", channel=self.Channel)
        self.plotter.Stack.drawStack('llnunu_deltaPhi', self.preCuts, str(self.lumi*1000), 35,0,3.5, titlex = "#Delta#Phi(Z,E_{T}^{miss})", units = "",
                        output=tag+'dPhi_llvv',outDir=self.outdir,separateSignal=self.sepSig,
                        drawtex=self.whichregion+" pre-selection", channel=self.Channel)
        self.plotter.Stack.drawStack('llnunu_l1_deltaPhi',self.preCuts, str(self.lumi*1000), 30,0,3, titlex = "#Delta#Phi(l,l)", units = "",
                        output=tag+'dPhi_ll',outDir=self.outdir,separateSignal=self.sepSig,
                        drawtex=self.whichregion+" pre-selection", channel=self.Channel)
        self.plotter.Stack.drawStack('llnunu_l1_mass',  self.preCuts, str(self.lumi*1000), 50, 50, 150, titlex = "M_{ll}", units = "GeV",
                        output=tag+'zmass',outDir=self.outdir,separateSignal=self.sepSig,
                        drawtex=self.whichregion+" pre-selection", channel=self.Channel)
        self.plotter.Stack.drawStack('llnunu_mt',self.preCuts, str(self.lumi*1000), 30, 0.0, 600.0, titlex = "M_{T}^{ll#nu#nu}", units = "GeV",
                        output=tag+'mt_low',outDir=self.outdir,separateSignal=self.sepSig,
                        drawtex=self.whichregion+" pre-selection", channel=self.Channel)
        #self.plotter.Stack.drawStack('llnunu_mt', self.preCuts, str(self.lumi*1000), 60, 0.0, 1200.0, titlex = "M_{T}^{ll#nu#nu}", units = "GeV", output=tag+'mt',outDir=self.outdir,separateSignal=self.sepSig,drawtex=self.whichregion+" pre-selection", channel=self.Channel)
        #self.plotter.Stack.drawStack('llnunu_mt', self.preCuts, str(self.lumi*1000), 150, 0.0, 3000.0, titlex = "M_{T}^{ll#nu#nu}", units = "GeV", output=tag+'mt_high',outDir=self.outdir,separateSignal=self.sepSig,drawtex=self.whichregion+" pre-selection", channel=self.Channel)
    
        # merge all output plots into one pdf file
        os.system('gs -dBATCH -dNOPAUSE -q -sDEVICE=pdfwrite -sOutputFile='+self.outdir+'/'+tag+'all.pdf '+self.outdir+'/'+tag+'*.eps')
        print 'All plots merged in single pdf file '+tag+'.pdf .'
        # merge root file
        os.system('hadd -f '+self.outdir+'/'+tag+'all.root '+self.outdir+'/'+tag+'*.root')
        return

    def draw_BCD(self):
        #cuts=python.SetCuts.Cuts(self.Channel)

        for key in self.tex_dic:
            if ROOT.TString(key).Contains("SR"):
                continue
            else:
                tag = key+'_'+self.whichregion+'_'+self.Channel+'_'
                if self.plotter.Stack.log: tag=tag+'log_'
                else: pass
                self.plotter.Stack.drawStack('llnunu_mt', self.cuts[key], str(self.lumi*1000), 60, 0.0, 1200.0, titlex = "M_{T}", units = "GeV",
                                     output=tag+'mt',outDir=self.outdir,separateSignal=self.sepSig,
                                     drawtex=self.tex_dic[key],channel=self.Channel)
                self.plotter.Stack.drawStack('llnunu_mt', self.cuts[key], str(self.lumi*1000), 150, 0.0, 3000.0, titlex = "M_{T}", units = "GeV",
                                     output=tag+'mt_high',outDir=self.outdir,separateSignal=self.sepSig,
                                     drawtex=self.tex_dic[key],channel=self.Channel)
                self.plotter.Stack.drawStack('llnunu_l1_pt', self.cuts[key], str(self.lumi*1000), 100, 0, 1000, titlex = "p_{T}^{ll}", units = "GeV",
                                     output=tag+'pt',outDir=self.outdir,separateSignal=self.sepSig,
                                     drawtex=self.tex_dic[key],channel=self.Channel)
                self.plotter.Stack.drawStack('llnunu_l2_pt', self.cuts[key], str(self.lumi*1000), self.nbins, self.xMin, self.xMax, titlex = "E_{T}^{miss}", units = "GeV",
                                     output=tag+'met_low',outDir=self.outdir,separateSignal=self.sepSig,
                                     drawtex=self.tex_dic[key],channel=self.Channel)
                # merge all output plots into one pdf file
                os.system('gs -dBATCH -dNOPAUSE -q -sDEVICE=pdfwrite -sOutputFile='+self.outdir+'/'+tag+'all.pdf '+self.outdir+'/'+tag+'*.eps')
                print 'All plots merged in single pdf file '+tag+'.pdf .'
                # merge root file
                os.system('hadd -f '+self.outdir+'/'+tag+'all.root '+self.outdir+'/'+tag+'*.root')
        return

    def draw_A(self, useMC = False, sf_bd = 0.0):
        tag ='regionA_'+self.whichregion+'_'+self.Channel+'_'

        if not useMC:
            if sf_bd == 0.0: sf_bd=ROOT.Double(raw_input("Please give the scale factor derived from B,D regions: \n"))
            else: pass
    
            self.plotter.Stack.rmPlotter(self.plotter.ZJets, "ZJets","Z+Jets", "background")
            self.plotter.Stack.drawStack('llnunu_l2_pt', self.cuts['SR'], str(self.lumi*1000), self.nbins, self.xMin, self.xMax,
                                  titlex = "E_{T}^{miss}", units = "GeV",output=tag+'met_low',outDir=self.outdir,separateSignal=self.sepSig,
                                  drawtex=self.tex_dic['SR'],channel=self.Channel)
            
            file=ROOT.TFile(self.outdir+'/'+tag+'met_low.root')
    
            h_met_zjets_a=self.plotter.ZJets.drawTH1('llnunu_l2_pt','llnunu_l2_pt',self.cuts['SR'],str(self.lumi*1000),self.nbins,self.xMin,self.xMax,titlex='E_{T}^{miss}',units='GeV',drawStyle="HIST")
            h_met_zjets_a.Scale(1./h_met_zjets_a.Integral())
            h_met_zjets_c=self.plotter.ZJets.drawTH1('llnunu_l2_pt','llnunu_l2_pt',self.cuts['CRc'],str(self.lumi*1000),self.nbins,self.xMin,self.xMax,titlex='E_{T}^{miss}',units='GeV',drawStyle="HIST")
            h_met_zjets_c.Scale(1./h_met_zjets_c.Integral())
            h_met_zjets_a.Divide(h_met_zjets_c)
    
            h_met_zjets=self.plotter.Data.drawTH1('llnunu_l2_pt','llnunu_l2_pt',self.cuts['CRc'],str('1'),self.nbins,self.xMin,self.xMax,titlex='E_{T}^{miss}',units='GeV',drawStyle="HIST")
            h_met_nonzjets=self.plotter.NonZBG.drawTH1('llnunu_l2_pt','llnunu_l2_pt',self.cuts['CRc'],str(self.lumi*1000),self.nbins,self.xMin,self.xMax,titlex='E_{T}^{miss}',units='GeV',drawStyle="HIST")
            h_met_zjets.Add(h_met_nonzjets,-1) # subtract the non-z bkg MC from data-C
            h_met_zjets.Multiply(h_met_zjets_a)
            h_met_zjets.Scale(sf_bd)
            
            hframe=file.Get(tag+'met_low_frame')
            hs=file.Get(tag+'met_low_stack')
            hs.Add(h_met_zjets)
            hdata=file.Get(tag+'met_low_data')
            hratio=GetRatio_TH1(hdata,hs,True)
        
            legend=file.Get(tag+'met_low_legend')
            myentry=ROOT.TLegendEntry(h_met_zjets,"Z+jets(data-driven)","f")
            legend.GetListOfPrimitives().AddFirst(myentry)
    
            # Let's remove the signal entries in the legend 
            for i in legend.GetListOfPrimitives():
                if ROOT.TString(i.GetLabel()).Contains("Bulk"):
                    legend.GetListOfPrimitives().Remove(i)
                    
                    
            drawStack_simple(hframe, hs, hdata, hratio, legend,
                             hstack_opt="A, HIST",
                             outDir=self.outdir, output=self.whichregion+'_regionA_'+self.Channel+'_met_low',channel=ROOT.TString(self.Channel),
                             xmin=self.xMin, xmax=self.xMax, xtitle="E_{T}^{miss}" ,units="GeV",
                             lumi=self.lumi, notes="Region A ("+self.whichregion+")")
    
    
            self.plotter.Stack.addPlotter(self.plotter.ZJets, "ZJets","Z+Jets", "background")

        else:
            self.plotter.Stack.drawStack('llnunu_l2_pt', self.cuts['SR'], str(self.lumi*1000), self.nbins, self.xMin, self.xMax,
                                         titlex = "E_{T}^{miss}", units = "GeV",output=tag+'met_low',outDir=self.outdir,separateSignal=self.sepSig,
                                         drawtex=self.tex_dic['SR'],channel=self.Channel)
            
        return
        
