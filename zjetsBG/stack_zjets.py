#!/usr/bin/env python
import ROOT
import os, copy
from math import *
from collections import OrderedDict
from python.SetCuts import SetCuts
from python.InitializePlotter import InitializePlotter
from python.HistPrinter import mergePrinter
from python.SimplePlot import *


class StackZjetsDD:
    def __init__(self, indir="./METSkim_v2",   outdir='./output/stacker/',
                 channel='inclusive',  whichregion='SR',
                 zpt_cut='100', met_cut= '50',
                 lumi = 2.318278305,  sepSig=True,
                 LogY=True,   doRatio=True,
                 addSig=True, addData=True):
        self.outdir=outdir
        self.channel=channel
        self.whichregion=whichregion
        self.zpt_cut, self.met_cut = zpt_cut, met_cut
        self.lumi=lumi
        CheckDir(self.outdir) # if not, this will create it
        #channel='inclusive'#raw_input("Please choose a channel (el or mu): \n")
        self.tag0='ZJstudy'
                
        self.plotter_dd=InitializePlotter(indir="./METSkim_v3", addSig=addSig, addData=addData, doRatio=doRatio, doMetCorr=True, scaleDphi=True)
        self.plotter=InitializePlotter(indir=indir, addSig=addSig, addData=addData, doRatio=doRatio, doMetCorr=True)
        self.plotter.Stack.rmPlotter(self.plotter.ZJets, "ZJets","Z+Jets", "background")
        
        setcuts = SetCuts()
        self.cuts = setcuts.abcdCuts(channel=channel, whichRegion=whichregion, zpt_cut=zpt_cut, met_cut=met_cut)
        
        ROOT.gROOT.ProcessLine('.x ../src/tdrstyle.C')
        ROOT.gStyle.SetPadBottomMargin(0.2)
        ROOT.gStyle.SetPadLeftMargin(0.15)
        
    def drawDataDrivenStack(self):
        stackTag = self.tag0+'_'+'stacker'+'_'+self.whichregion+'_'+self.channel+'_'+'regA'+'_'+'absDphi'
        outTag=self.outdir+'/'+stackTag
        var="llnunu_mtc"
        
        et1="TMath::Sqrt(llnunu_l1_pt*llnunu_l1_pt+llnunu_l1_mass*llnunu_l1_mass)"
        et2="TMath::Sqrt(llnunu_l2_pt*llnunu_l2_pt+llnunu_l1_mass*llnunu_l1_mass)"
        newMtB='TMath::Sqrt(2.0*(llnunu_l1_mass*llnunu_l1_mass+'+et1+'*'+et2+'-llnunu_l1_pt*llnunu_l2_pt*cos(llnunu_deltaPhi+TMath::Pi()*3/4)))'
        newMtD='TMath::Sqrt(2.0*(llnunu_l1_mass*llnunu_l1_mass+'+et1+'*'+et2+'-llnunu_l1_pt*llnunu_l2_pt*cos(llnunu_deltaPhi+TMath::Pi()/2)))'
        newMtC='TMath::Sqrt(2.0*(llnunu_l1_mass*llnunu_l1_mass+'+et1+'*'+et2+'-llnunu_l1_pt*llnunu_l2_pt*cos(llnunu_deltaPhi+TMath::Pi()/4)))'
        
        ### ----- Execute (plotting):
        self.plotter.Stack.drawStack(var, self.cuts['regA'], str(self.lumi*1000), 70, 150.0, 500.0, titlex = "M_{T}^{ZZ}", units = "GeV",
                                     output=stackTag, outDir=self.outdir, separateSignal=True,
                                     drawtex=self.whichregion+' selection', channel=self.channel)
        
        #ha=self.plotter.ZJets.drawTH1('zjets', var, self.cuts['regA'], str(lumi*1000), 70, 150.0, 500.0, titlex = "M_{T}^{ZZ}", units = "GeV", drawStyle="HIST")
        hb=self.plotter_dd.Data.drawTH1('regB', newMtB, self.cuts['regB'], '1', 70, 150.0, 500.0, titlex = "M_{T}^{ZZ}", units = "GeV", drawStyle="HIST") #'3.65'
        hc=self.plotter_dd.Data.drawTH1('regC', newMtC, self.cuts['regC'], '1', 70, 150.0, 500.0, titlex = "M_{T}^{ZZ}", units = "GeV", drawStyle="HIST") #'2.73'
        hd=self.plotter_dd.Data.drawTH1('regD', newMtD, self.cuts['regD'], '1', 70, 150.0, 500.0, titlex = "M_{T}^{ZZ}", units = "GeV", drawStyle="HIST") #'3.69'

        #-> Use 3 CRs to get the zjets distribution in regA:
        h_zjets_dd=copy.deepcopy(hb)
        h_zjets_dd.Add(hc)
        h_zjets_dd.Add(hd)
        h_zjets_dd.Scale(1.0/3.0)
        h_zjets_dd.SetFillColor(ROOT.kGreen+2)

        ROOT.TH1.AddDirectory(ROOT.kFALSE)
        fstack=ROOT.TFile(self.outdir+'/'+stackTag+'.root')
        hs=fstack.Get(stackTag+"_stack")
        
        hframe=fstack.Get(stackTag+'_frame')
        #hframe.GetXaxis().SetRangeUser(xcutmin, xcutmax)
        # if ROOT.TString(var_ll).Contains("mass"):
        #     if self.logy: hframe.SetMaximum(hframe.GetMaximum()*100)
        #     else: hframe.SetMaximum(hframe.GetMaximum()*1.2)
            
        hdata=fstack.Get(stackTag+'_data0')
        legend=fstack.Get(stackTag+'_legend')
            
        hsig=fstack.Get(stackTag+'_BulkGravToZZToZlepZinv_narrow_1000_V3MetShiftBeforeJetNewSelV6NoMetLepAnyWayAllJetsBigSig1p4LepResSigProtect')
        fstack.Close()
        
        print '[debug] SR regA, datadriven zjets: ', h_zjets_dd.Integral(0,h_zjets_dd.GetNbinsX()+1)
        print '[debug] SR regA, dt: ', hdata.Integral(0,hdata.GetNbinsX()+1)
            
        hsnew=ROOT.THStack(stackTag+"_stack_new","")
        
        # Let's remove the target bkg entries in the TStack
        nonresTag=[stackTag+'_'+sample for sample in ['ZJets'] ]
        for ihist in hs.GetHists():
            if ihist.GetName() in nonresTag: print '[Removing...] I am zjets bkg : ',ihist.GetName()
            else:  hsnew.Add(ihist)
            
        for ih in hsnew.GetHists():
            print '[debug] ', ih.GetName()
        print hsnew
        hsnew.Add(h_zjets_dd)
            
        hratio=GetRatio_TH1(hdata,hsnew,True)
        
        # Let's remove the target bkg entries in the legend
        for ileg in legend.GetListOfPrimitives():
            if ileg.GetLabel() in ['Z+Jets']:
                legend.GetListOfPrimitives().Remove(ileg)

        myentry=ROOT.TLegendEntry(h_zjets_dd,"Z_Jets (data-driven)","f")
        legend.GetListOfPrimitives().AddFirst(myentry)
        
        drawStack_simple(hframe, hsnew, hdata, hratio, legend,
                         hstack_opt="A, HIST",
                         outDir=self.outdir, output=stackTag+"_datadriven", channel=ROOT.TString(self.channel),
                         xmin=150, xmax=500, xtitle="M_{T}^{ZZ}" ,units="GeV",
                         lumi=self.lumi, notes=self.whichregion+" selection",
                         drawSig=True, hsig=[hsig])
        return
                                            
    def ValidateDphiShapeCorr(self):
        plotter_zjets=InitializePlotter(indir="./METSkim_v4", addSig=True, addData=True, doRatio=True, doMetCorr=True, scaleDphi=True, zjetsscale=True)
        var_check="abs(llnunu_deltaPhi)"
        ha=plotter_zjets.ZJets.drawTH1('regA',var_check, self.cuts['regA'],str(self.lumi*1000),32, 0., 3.2, titlex = "#Delta#phi_{Z,MET}", units = "", drawStyle="HIST")
        hb=plotter_zjets.ZJets.drawTH1('regB',var_check, self.cuts['regB'],str(self.lumi*1000),32, 0., 3.2, titlex = "#Delta#phi_{Z,MET}", units = "", drawStyle="HIST")
        hc=plotter_zjets.ZJets.drawTH1('regC',var_check, self.cuts['regC'],str(self.lumi*1000),32, 0., 3.2, titlex = "#Delta#phi_{Z,MET}", units = "", drawStyle="HIST")
        hd=plotter_zjets.ZJets.drawTH1('regD',var_check, self.cuts['regD'],str(self.lumi*1000),32, 0., 3.2, titlex = "#Delta#phi_{Z,MET}", units = "", drawStyle="HIST")

        newhb=ShiftXaxisTH1(hb, 3*ROOT.TMath.Pi()/4, '_shiftB')
        newhc=ShiftXaxisTH1(hc, ROOT.TMath.Pi()/4, '_shiftC')
        newhd=ShiftXaxisTH1(hd, ROOT.TMath.Pi()/2, '_shiftD')
            
        ha.SetLineColor(ROOT.kRed)
        newhb.SetLineColor(ROOT.kBlue)
        newhc.SetLineColor(ROOT.kBlack)
        newhd.SetLineColor(ROOT.kYellow)

        ha.Scale(1./ha.Integral(0,1+ha.GetNbinsX()))
        newhb.Scale(1./newhb.Integral(0,1+newhb.GetNbinsX()))
        newhc.Scale(1./newhc.Integral(0,1+newhc.GetNbinsX()))
        newhd.Scale(1./newhd.Integral(0,1+newhd.GetNbinsX()))
        #TLegend leg()
        c1=ROOT.TCanvas(1)
        ha.Draw("L")
        ha.GetXaxis().SetRangeUser(2.2, 3.2)
        newhb.Draw("same")
        newhc.Draw("same")
        newhd.Draw("same")
        c1.SaveAs(self.outdir+"ValidateDphiShapeCorr_out.pdf")
