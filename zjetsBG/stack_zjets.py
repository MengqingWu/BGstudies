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
    def __init__(self, indir="./METSkim_v1", indir_dd="./METSkim_v3", outdir='./output/stacker/',
                 channel='inclusive',  whichregion='SR', zpt_cut='100', met_cut= '50',  lumi = 2.318278305,  
                 sepSig=True,   LogY=True,      doRatio=True,    addSig=True, addData=True):
        self.outdir=outdir
        self.channel=channel
        self.whichregion=whichregion
        self.zpt_cut, self.met_cut = zpt_cut, met_cut
        self.lumi=lumi
        CheckDir(self.outdir) # if not, this will create it
        #channel='inclusive'#raw_input("Please choose a channel (el or mu): \n")
        self.tag0='ZJstudy'
                
        self.plotter_dd=InitializePlotter(indir=indir_dd, addSig=addSig, addData=addData, doRatio=doRatio, scaleDphi=True)
        self.plotter=InitializePlotter(indir=indir, addSig=addSig, addData=addData, doRatio=doRatio)
        self.plotter.Stack.rmPlotter(self.plotter.ZJets, "ZJets","Z+Jets", "background")
        
        setcuts = SetCuts()
        self.cuts = setcuts.abcdCuts(channel=channel, whichRegion=whichregion, zpt_cut=zpt_cut, met_cut=met_cut)

        et1="TMath::Sqrt(llnunu_l1_pt*llnunu_l1_pt+llnunu_l1_mass*llnunu_l1_mass)"
        et2="TMath::Sqrt(llnunu_l2_pt*llnunu_l2_pt+llnunu_l1_mass*llnunu_l1_mass)"
        newMtB='TMath::Sqrt(2.0*(llnunu_l1_mass*llnunu_l1_mass+'+et1+'*'+et2+'-llnunu_l1_pt*llnunu_l2_pt*cos(llnunu_deltaPhi+TMath::Pi()*3/4)))'
        newMtD='TMath::Sqrt(2.0*(llnunu_l1_mass*llnunu_l1_mass+'+et1+'*'+et2+'-llnunu_l1_pt*llnunu_l2_pt*cos(llnunu_deltaPhi+TMath::Pi()/2)))'
        newMtC='TMath::Sqrt(2.0*(llnunu_l1_mass*llnunu_l1_mass+'+et1+'*'+et2+'-llnunu_l1_pt*llnunu_l2_pt*cos(llnunu_deltaPhi+TMath::Pi()/4)))'
        self.Mt={'A':'llnunu_mt',
                 'B':newMtB,
                 'C':newMtC,
                 'D':newMtD}
        self.fabsdPhi={'A': "fabs(llnunu_deltaPhi)",
                       'B': "fabs(llnunu_deltaPhi)+TMath::Pi()*3/4",
                       'D': "fabs(llnunu_deltaPhi)+TMath::Pi()/2",
                       'C': "fabs(llnunu_deltaPhi)+TMath::Pi()/4"}
        
        ROOT.gROOT.ProcessLine('.x ../src/tdrstyle.C')
        ROOT.gStyle.SetPadBottomMargin(0.2)
        ROOT.gStyle.SetPadLeftMargin(0.15)
        
    def drawDataDrivenStack(self):
        stackTag = self.tag0+'_'+'stacker'+'_'+self.whichregion+'_'+self.channel+'_'+'regA'+'_'+'absDphi'
        outTag=self.outdir+'/'+stackTag
                
        ### ----- Execute (plotting):
        self.plotter.Stack.drawStack(self.Mt['A'], self.cuts['regA'], str(self.lumi*1000), 70, 150.0, 500.0, titlex = "M_{T}^{ZZ}", units = "GeV",
                                     output=stackTag, outDir=self.outdir, separateSignal=True,
                                     drawtex=self.whichregion+' selection', channel=self.channel)
        
        #ha=self.plotter.ZJets.drawTH1('zjets', var, self.cuts['regA'], str(lumi*1000), 70, 150.0, 500.0, titlex = "M_{T}^{ZZ}", units = "GeV", drawStyle="HIST")
        hb=self.plotter_dd.Data.drawTH1('regB', self.Mt['B'], self.cuts['regB'], '1', 70, 150.0, 500.0, titlex = "M_{T}^{ZZ}", units = "GeV", drawStyle="HIST") 
        hc=self.plotter_dd.Data.drawTH1('regC', self.Mt['C'], self.cuts['regC'], '1', 70, 150.0, 500.0, titlex = "M_{T}^{ZZ}", units = "GeV", drawStyle="HIST") 
        hd=self.plotter_dd.Data.drawTH1('regD', self.Mt['D'], self.cuts['regD'], '1', 70, 150.0, 500.0, titlex = "M_{T}^{ZZ}", units = "GeV", drawStyle="HIST") 

        subb=self.plotter_dd.NonZBG.drawTH1('subregB',self.Mt['B'],self.cuts['regB'],str(self.lumi*1000),70, 150.0, 500.0, titlex = "M_{T}^{ZZ}", units="GeV") 
        subc=self.plotter_dd.NonZBG.drawTH1('subregC',self.Mt['C'],self.cuts['regC'],str(self.lumi*1000),70, 150.0, 500.0, titlex = "M_{T}^{ZZ}", units="GeV") 
        subd=self.plotter_dd.NonZBG.drawTH1('subregD',self.Mt['D'],self.cuts['regD'],str(self.lumi*1000),70, 150.0, 500.0, titlex = "M_{T}^{ZZ}", units="GeV") 
        hb.Add(subb,-1)
        hc.Add(subc,-1)
        hd.Add(subd,-1)
        hb.Scale(3.46)
        hc.Scale(2.45)
        hd.Scale(4.08)

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
            
        hsig1=fstack.Get(stackTag+'_BulkGravToZZToZlepZinv_narrow_800')
        hsig2=fstack.Get(stackTag+'_BulkGravToZZToZlepZinv_narrow_1000')
        hsig3=fstack.Get(stackTag+'_BulkGravToZZToZlepZinv_narrow_1200')
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
        #print hsnew
        hsnew.Add(h_zjets_dd)
            
        hratio=GetRatio_TH1(hdata,hsnew,True)
        
        # Let's remove the target bkg entries in the legend
        for ileg in legend.GetListOfPrimitives():
            if ileg.GetLabel() in ['Z+Jets']:
                legend.GetListOfPrimitives().Remove(ileg)

        myentry=ROOT.TLegendEntry(h_zjets_dd,"Z_Jets (data-driven)","f")
        legend.GetListOfPrimitives().AddFirst(myentry)
        
        # drawStack_simple(hframe, hsnew, hdata, hratio, legend,
        #                  hstack_opt="A, HIST",
        #                  outDir=self.outdir, output=stackTag+"_datadriven", channel=ROOT.TString(self.channel),
        #                  xmin=150, xmax=500, xtitle="M_{T}^{ZZ}" ,units="GeV",
        #                  lumi=self.lumi, notes=self.whichregion+" selection",
        #                  drawSig=True, hsig=[hsig1,hsig2,hsig3])
        return

    def ValidateDphiShapeCorr(self, whichvar='fabsDphi', isNormalized=True, whichbcd='allBG', scaleDphi=True, suffix=''):
        """ use shape correction that is derived from MC to apply to all the MC samples to validate the 'dphi_sf' algorithm 
        whichvar=(absDphi, mt, zpt, met)
        """
        lumi_str='1' if isNormalized else str(self.lumi*1000)

        validatorMC=InitializePlotter(indir="./METSkim_v4", addSig=False, addData=False, doRatio=False, scaleDphi=scaleDphi)
        compareTag = self.tag0+'_'+'closureTest'+'_'+self.whichregion+'_'+self.channel+'_'+'regA'+'_'+whichvar
        outTag=self.outdir+'/'+compareTag

        if whichvar=='fabsDphi':
            var=self.fabsdPhi
            nbins, xmin, xmax, titlex, units =4, 3*ROOT.TMath.Pi()/4, ROOT.TMath.Pi(), "|#Delta#phi_{Z,MET}|", ""
            
        elif whichvar=='mt':
            var=self.Mt
            if  int(self.zpt_cut)*int(self.met_cut) == 0: nbins, xmin, xmax, titlex, units =140, 100.0, 800.0, "M_{T}^{ZZ}", "GeV"
            else: nbins, xmin, xmax, titlex, units =13, 150.0, 800.0, "M_{T}^{ZZ}", "GeV"
        elif whichvar=='zpt':
            var=copy.deepcopy(self.Mt)
            for i in var: var[i]='llnunu_l1_pt'
            if int(self.zpt_cut)==0: nbins, xmin, xmax, titlex, units =60, 0.0, 1200.0, "p_{T}^{ll}", "GeV"
            else: xmin, xmax, titlex, units = int(self.zpt_cut)-10, 1200.0, "p_{T}^{ll}", "GeV"; nbins=int((xmax-xmin)/20) if (xmax-xmin)%10==0 else 50
            
        elif whichvar=='met':
            var=copy.deepcopy(self.Mt)
            for i in var: var[i]='llnunu_l2_pt'
            #if int(self.met_cut)==0: nbins, xmin, xmax, titlex, units =90, 0.0, 450.0, "E_{T}^{miss}", "GeV"
            #else: xmin, xmax, titlex, units = int(self.met_cut)-10, 450.0, "E_{T}^{miss}", "GeV"; nbins=int((xmax-xmin)/10) if (xmax-xmin)%10==0 else 40
            titlex, units = "E_{T}^{miss}", "GeV"
            xbins=[0,25,50,80,120,1000]
            xmin,xmax=0, 1000
            
        if whichbcd=='allBG':
            bcdPlotter = validatorMC.allBG
            notes='bcd from all bg'
        elif whichbcd=='ZJets':
            bcdPlotter = validatorMC.ZJets
            notes='bcd from zjets'
        else: print "[error] Please check the whichbcd = %s, is 'allBG' or 'ZJets'" % (whichbcd); exit(0)

        leg_suffix='corr.' if scaleDphi else ''
                    
        ### ----- Execute (plotting):
        if whichvar=='met':
            ha=self.plotter.ZJets.drawTH1Binned('regA', var['A'], self.cuts['regA'], lumi_str, xbins, titlex = titlex, unitsx = units)
            hb=bcdPlotter.drawTH1Binned('regB_shift', var['B'], self.cuts['regB'], lumi_str, xbins,titlex = titlex,unitsx = units)
            hc=bcdPlotter.drawTH1Binned('regC_shift', var['C'], self.cuts['regC'], lumi_str, xbins,titlex = titlex,unitsx = units)
            hd=bcdPlotter.drawTH1Binned('regD_shift', var['D'], self.cuts['regD'], lumi_str, xbins,titlex = titlex,unitsx = units)
        else:
            ha=self.plotter.ZJets.drawTH1('regA', var['A'], self.cuts['regA'], lumi_str, nbins, xmin, xmax, titlex = titlex, units = units)
            hb=bcdPlotter.drawTH1('regB_shift', var['B'], self.cuts['regB'], lumi_str, nbins, xmin, xmax,titlex = titlex,units = units)
            hc=bcdPlotter.drawTH1('regC_shift', var['C'], self.cuts['regC'], lumi_str, nbins, xmin, xmax,titlex = titlex,units = units)
            hd=bcdPlotter.drawTH1('regD_shift', var['D'], self.cuts['regD'], lumi_str, nbins, xmin, xmax,titlex = titlex,units = units)
        
        print 'regB: ', hb.GetSumOfWeights(),\
              '\nregC: ', hc.GetSumOfWeights(),\
              '\nregD(sum of weight): ', hd.GetSumOfWeights(), '; integral:', hd.Integral(0,1+hd.GetNbinsX())
        if isNormalized:
            ha.Scale(1./ha.Integral(0,1+ha.GetNbinsX()))
            hb.Scale(1./hb.Integral(0,1+hb.GetNbinsX()))
            hc.Scale(1./hc.Integral(0,1+hc.GetNbinsX()))
            hd.Scale(1./hd.Integral(0,1+hd.GetNbinsX()))
            ytitle='normalized'
        else: ytitle='events'
        
        drawCompareSimple(hb, ha, "reg.B"+' '+leg_suffix, "reg. A",
                          xmin=xmin, xmax=xmax, outdir=self.outdir, notes=notes,lumi=self.lumi,
                          tag=compareTag+'BA', units=units, ytitle=ytitle, setmax=2)

        drawCompareSimple(hc, ha, "reg.C"+' '+leg_suffix, "reg. A",
                          xmin=xmin, xmax=xmax, outdir=self.outdir, notes=notes,lumi=self.lumi,
                          tag=compareTag+'CA', units=units, ytitle=ytitle, setmax=2)

        drawCompareSimple(hd, ha, "reg.D"+' '+leg_suffix, "reg. A",
                          xmin=xmin, xmax=xmax, outdir=self.outdir, notes=notes,lumi=self.lumi,
                          tag=compareTag+'DA', units=units, ytitle=ytitle, setmax=2)

        ha.SetLineColor(ROOT.kRed)
        hb.SetLineColor(ROOT.kBlue)
        hc.SetLineColor(ROOT.kGreen)
        hd.SetLineColor(ROOT.kYellow)

        ha.SetMarkerColor(ROOT.kRed)
        hb.SetMarkerColor(ROOT.kBlue)
        hc.SetMarkerColor(ROOT.kGreen)
        hd.SetMarkerColor(ROOT.kYellow)
        
        c1=ROOT.TCanvas(1)
        legend=GetLegendv1(0.65,0.75,0.85,0.90,
                           [ha,hb,hc,hd],
                           ['reg. A','reg. B','reg. C','reg. D'],
                           opt=['lpe','lpe','lpe','lpe'])
        ha.Draw("e")
        hb.Draw("e same")
        hc.Draw("e same")
        hd.Draw("e same")
        legend.Draw("same")
        c1.SetLogy()
        nameseq=[whichvar, whichbcd, 'bcd', leg_suffix, 'ValidateDphiShapeCorr','met'+self.met_cut,'zpt'+self.zpt_cut, suffix]
        nameseq.remove('')
        c1.SaveAs(self.outdir+'/'+'_'.join(nameseq)+'.pdf')

        #fout=ROOT.TFile(self.outdir+'/'+'_'.join(nameseq)+'.root','recreate')
        
        return
