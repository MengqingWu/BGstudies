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
    def __init__(self, indir="./inds", outdir='./output/stacker/',
                 channel='inclusive',  whichregion='SR', zpt_cut='100', met_cut= '100',  lumi = 12.9,  
                 sepSig=True, LogY=True, doRatio=True, addSig=True, addData=True, onlyStats=False):
        self.outdir=outdir
        self.channel=channel
        self.whichregion=whichregion
        self.zpt_cut, self.met_cut = zpt_cut, met_cut
        self.lumi=lumi
        CheckDir(self.outdir) # if not, this will create it
        #channel='inclusive'#raw_input("Please choose a channel (el or mu): \n")
        self.tag0='ZJstudy'
                
        #self.plotter_dd = InitializePlotter(indir=indir, addSig=addSig, addData=addData, doRatio=doRatio, onlyStats=onlyStats)

        self.plotter = InitializePlotter(indir=indir, addSig=addSig, addData=addData, doRatio=doRatio, onlyStats=onlyStats)
        #self.Stack = self.plotter.GetStack(outdir=outdir, outtag=tag+'_'+whichregion+'_'+channel+'_absDphi')
        #self.plotter.Stack.rmPlotter(self.plotter.ZJets, "ZJets","Z+Jets", "background")
        
        setcuts = SetCuts()
        self.cuts_eld = setcuts.abcdCuts(channel=self.channel, whichRegion=whichregion, zpt_cut=zpt_cut, met_cut=met_cut)
        self.zjcuts = setcuts.GetZjetsCuts(whichRegion=whichregion, zpt_cut=zpt_cut, met_cut=met_cut)
        self.cuts = self.zjcuts[self.channel]
        
        # self.fabsDphi={'A': "fabs(llnunu_deltaPhi)",
        #                'B': "fabs(llnunu_deltaPhi)+TMath::Pi()/4",
        #                'C': "fabs(llnunu_deltaPhi)+TMath::Pi()/2",
        #                'D': "fabs(llnunu_deltaPhi)+TMath::Pi()*3/4"}
        self.fabsDphi="fabs(TVector2::Phi_mpi_pi(llnunu_l2_phi-llnunu_l1_phi))" 
        
        # et1="TMath::Sqrt(llnunu_l1_pt*llnunu_l1_pt+llnunu_l1_mass*llnunu_l1_mass)"
        # et2="TMath::Sqrt(llnunu_l2_pt*llnunu_l2_pt+llnunu_l1_mass*llnunu_l1_mass)"
        # newMtB='TMath::Sqrt(2.0*(llnunu_l1_mass*llnunu_l1_mass+'+et1+'*'+et2+'-llnunu_l1_pt*llnunu_l2_pt*cos('+self.fabsDphi['B']+')))'
        # newMtC='TMath::Sqrt(2.0*(llnunu_l1_mass*llnunu_l1_mass+'+et1+'*'+et2+'-llnunu_l1_pt*llnunu_l2_pt*cos('+self.fabsDphi['C']+')))'
        # newMtD='TMath::Sqrt(2.0*(llnunu_l1_mass*llnunu_l1_mass+'+et1+'*'+et2+'-llnunu_l1_pt*llnunu_l2_pt*cos('+self.fabsDphi['D']+')))'
        # self.Mt={'A':'llnunu_mt',
        #          'B':newMtB,
        #          'C':newMtC,
        #          'D':newMtD}
        self.Mt='llnunu_mt'
        
        self.mtxbins=[150,200,250,300,350,400,450,550,850]
        self.mtnbins, self.mtxmin, self.mtxmax= len(self.mtxbins), min(self.mtxbins), max(self.mtxbins)#14, 150.0, 850.0
                        
        
        ROOT.gROOT.ProcessLine('.x ../src/tdrstyle.C')
        ROOT.gStyle.SetPadBottomMargin(0.2)
        ROOT.gStyle.SetPadLeftMargin(0.15)

    def GetAllmcRegA(self):
        #stackTag = self.tag0+'_'+'stacker'+'_'+self.whichregion+'_'+self.channel+'_'+'regTrg'+'_'+'allMC'
        stackTag = '_'.join([self.tag0,'stacker',self.whichregion,'met'+self.met_cut,'3channels','regTrg','allMC'])
        
        Stack = self.plotter.GetStack(outdir=self.outdir, outtag=stackTag, lumi=self.lumi)
        for lepChan in ['mu','el','inclusive']:
            Stack.drawStack(self.Mt, self.zjcuts[lepChan]['regTrg'], str(self.lumi*1000), self.mtnbins, self.mtxmin, self.mtxmax, titlex = "M_{T}^{ZZ}", units = "GeV",
                            output=stackTag, outDir=self.outdir, separateSignal=True,
                            drawtex=self.whichregion+' selection', channel=lepChan, xbins=self.mtxbins)
        Stack.closePSFile()
        return
    
    def GetYieldCorr(self, plotter=None):
        if plotter==None: plotter=self.plotter
        var=self.fabsDphi
        nbins, xmin, xmax, titlex, units = 16, 0.0, 3.2, "|#Delta#phi_{Z,MET}|", ""
        lumi_str = str(self.lumi*1000)

        htr=plotter.ZJets.drawTH1('regTrg', var, self.cuts['regTrg'], lumi_str, nbins, xmin, xmax, titlex = titlex, units = units)
        hcr=plotter.ZJets.drawTH1('regCtrl',var, self.cuts['regCtrl'],lumi_str, nbins, xmin, xmax, titlex = titlex, units = units)
        # ha=plotter.ZJets.drawTH1('regTrg', var['A'], self.cuts['regTrg'], lumi_str, nbins, xmin, xmax, titlex = titlex, units = units)
        # hb=plotter.ZJets.drawTH1('regB_shift', var['B'], self.cuts['regB'], lumi_str, nbins, xmin, xmax,titlex = titlex,units = units)
        # hc=plotter.ZJets.drawTH1('regC_shift', var['C'], self.cuts['regC'], lumi_str, nbins, xmin, xmax,titlex = titlex,units = units)
        # hd=plotter.ZJets.drawTH1('regD_shift', var['D'], self.cuts['regD'], lumi_str, nbins, xmin, xmax,titlex = titlex,units = units)
            
        igtr=htr.Integral(0,1+htr.GetNbinsX())
        igcr=hcr.Integral(0,1+hcr.GetNbinsX())
        
        print 'regTrg: ', htr.GetSumOfWeights(), '; integral:', htr.Integral(0,1+htr.GetNbinsX()),\
            '\nregCtrl:', hcr.GetSumOfWeights(), '; integral:', hcr.Integral(0,1+hcr.GetNbinsX())
        
        ratio=igtr/igcr
        print "[info] yield ratio of Ntr/Ncr = %.2f" % (ratio)
        return  ratio                                                                                                 \
        
    def drawDataDrivenStack(self): # draw MT
        stackTag = '_'.join([self.tag0, 'stacker', self.whichregion, self.channel, 'regTrg', 'absDphi'])
        
        outTag=self.outdir+'/'+stackTag
        Stack = self.plotter.GetStack(outdir=self.outdir, outtag=stackTag, lumi=self.lumi)
        Stack.rmPlotter(self.plotter.ZJets, "ZJets","Z+Jets", "background")

        ### ----- Execute (plotting):
        Stack.drawStack(self.Mt, self.cuts['regTrg'], str(self.lumi*1000), self.mtnbins, self.mtxmin, self.mtxmax, titlex = "M_{T}^{ZZ}", units = "GeV",
                        output=stackTag, outDir=self.outdir, separateSignal=True,
                        drawtex=self.whichregion+' selection', channel=self.channel, xbins=self.mtxbins) # if xbins not empty, binned drawn
        Stack.closePSFile()
        #-> Use the CR data yield scaled by MC ratio 
        hcr=self.plotter.Data.drawTH1Binned('regCtrl', self.Mt, self.cuts['regCtrl'],'1', self.mtxbins, titlex = "M_{T}^{ZZ}", unitsx = "GeV") 
        subCtrl=self.plotter.NonZBG.drawTH1Binned('subregCtrl',self.Mt,self.cuts['regCtrl'],str(self.lumi*1000), self.mtxbins,titlex = "M_{T}^{ZZ}", unitsx="GeV") 
        hcr.Add(subCtrl,-1)
        ratio = self.GetYieldCorr()
        hcr.Scale(ratio)
        err_tr=ROOT.Double(0.0)
        Ntr = hcr.IntegralAndError(0, 1+hcr.GetNbinsX(), err_tr)
        
        print "[info] prediction = %.2f +- %.2f" % (Ntr, err_tr)
        
        #-> Use the shape of MC:
        htr=self.plotter.ZJets.drawTH1Binned('regTrg', self.Mt, self.cuts['regTrg'], str(self.lumi*1000), self.mtxbins, titlex = "M_{T}^{ZZ}", unitsx = "GeV")
        htr.Scale(Ntr/htr.Integral(0,1+htr.GetNbinsX()))
        htr.SetFillColor(ROOT.kGreen+2)

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
            
        hsig1=fstack.Get(stackTag+'_BulkGravToZZToZlepZinv_narrow_600')
        hsig2=fstack.Get(stackTag+'_BulkGravToZZToZlepZinv_narrow_1000')
        hsig3=fstack.Get(stackTag+'_BulkGravToZZToZlepZinv_narrow_1200')
        fstack.Close()
        
        print '[debug] SR regTrg, datadriven zjets: ', htr.Integral(0,htr.GetNbinsX()+1)
        print '[debug] SR regTrg, dt: ', hdata.Integral(0,hdata.GetNbinsX()+1)
            
        hsnew=ROOT.THStack(stackTag+"_stack_new","")
        
        # Let's remove the target bkg entries in the TStack
        nonresTag=[stackTag+'_'+sample for sample in ['ZJets'] ]
        for ihist in hs.GetHists():
            if ihist.GetName() in nonresTag: print '[Removing...] I am zjets bkg : ',ihist.GetName()
            else:  hsnew.Add(ihist)
            
        for ih in hsnew.GetHists():
            print '[debug] ', ih.GetName()
        #print hsnew
        hsnew.Add(htr)
            
        hratio=GetRatio_TH1(hdata,hsnew,True)
        
        # Let's remove the target bkg entries in the legend
        for ileg in legend.GetListOfPrimitives():
            if ileg.GetLabel() in ['Z+Jets']:
                legend.GetListOfPrimitives().Remove(ileg)

        myentry=ROOT.TLegendEntry(htr,"Z_Jets (data-driven)","f")
        legend.GetListOfPrimitives().AddFirst(myentry)
        
        drawStack_simple(hframe, hsnew, hdata, hratio, legend,
                         hstack_opt="A, HIST",
                         outDir=self.outdir, output=stackTag+"_datadriven", channel=ROOT.TString(self.channel),
                         xmin= self.mtxmin, xmax= self.mtxmax, xtitle="M_{T}^{ZZ}" ,units="GeV",
                         lumi=self.lumi, notes=self.whichregion+" selection",
                         drawSig=False, hsig=[hsig1,hsig2,hsig3])
        return

    def ValidateDphiShapeCorr(self, indir, whichvar='fabsDphi', isNormalized=True, yieldCorr=False, whichbcd='ZJets',
                              onlyStats=False, logy=True,suffix=''):
        """ use shape correction that is derived from MC to apply to all the MC samples to validate the 'dphi_sf' algorithm 
        whichvar=(absDphi, mt, zpt, met)
        """
        binnedPlots=['met', 'zpt', 'metzpt']
        if isNormalized: yieldCorr=False
        lumi_str='1' if isNormalized else str(self.lumi*1000)
        
        validatorMC=InitializePlotter(indir=indir, addSig=False, addData=False, doRatio=False, onlyStats=onlyStats)
        zjetsMC    =InitializePlotter(indir=indir, addSig=False, addData=False, doRatio=False, onlyStats=onlyStats)
        
        nom_suffix='normalized' if isNormalized else 'yield'
        #leg_suffix='corr.' if scaleDphi else ''
        leg_suffix=''
        
        compareTagseq=[self.tag0, 'closureTest',self.whichregion,self.channel, whichvar, nom_suffix]
        nameseq=[whichvar, self.tag0, 'closureTest', self.whichregion, self.channel, 'met'+self.met_cut,'zpt'+self.zpt_cut,
                 leg_suffix+'bcd'+whichbcd, nom_suffix, suffix]
        if '' in nameseq: nameseq.remove('')
        compareTag='_'.join(nameseq)
        #compareTag = self.tag0+'_'+'closureTest'+'_'+self.whichregion+'_'+self.channel+'_'+'regTrg'+'_'+whichvar
        outTag=self.outdir+'/'+compareTag

        if whichvar=='fabsDphi':
            var=self.fabsDphi
            nbins, xmin, xmax, titlex, units =4, 3*ROOT.TMath.Pi()/4, ROOT.TMath.Pi(), "|#Delta#phi_{Z,MET}|", ""
            
        elif whichvar=='mt':
            var=self.Mt
            if  int(self.zpt_cut)*int(self.met_cut) == 0: nbins, xmin, xmax, titlex, units =140, 100.0, 800.0, "M_{T}^{ZZ}", "GeV"
            else:
                binnedPlots.append(whichvar)
                xbins, nbins, xmin, xmax = self.mtxbins, self.mtnbins, self.mtxmin, self.mtxmax
                titlex, units = "M_{T}^{ZZ}", "GeV"
                
        elif whichvar=='zpt':
            var=copy.deepcopy(self.Mt)
            for i in var: var[i]='llnunu_l1_pt'
            titlex, units = "p_{T}^{Z}", "GeV"
            xbins=[0,100,150,200,300,400,1000]
            nbins=len(xbins)-1
            if int(self.zpt_cut)==0: xmin, xmax = 0.0, 1000.0
            else:                    xmin, xmax = int(self.zpt_cut), 1000.0
                
        elif whichvar=='met':
            var=copy.deepcopy(self.Mt)
            for i in var: var[i]='llnunu_l2_pt'
            #if int(self.met_cut)==0: nbins, xmin, xmax, titlex, units =90, 0.0, 450.0, "E_{T}^{miss}", "GeV"
            #else: xmin, xmax, titlex, units = int(self.met_cut)-10, 450.0, "E_{T}^{miss}", "GeV"; nbins=int((xmax-xmin)/10) if (xmax-xmin)%10==0 else 40
            xmin,xmax, titlex, units = 0, 1000, "E_{T}^{miss}", "GeV"
            xbins=[0,25,50,80,120,1000]
            nbins=len(xbins)-1

        elif whichvar=='zmass':
            var=copy.deepcopy(self.Mt)
            for i in var: var[i]='llnunu_l1_mass'
            nbins, xmin, xmax, titlex, units =40, 70., 110., "M_{Z}", "GeV"

        elif whichvar=='metzpt':
            var=copy.deepcopy(self.Mt)
            for i in var: var[i]='llnunu_l2_pt/llnunu_l1_pt'
            xmin, xmax, titlex, units = 0., 3., "E_{T}^{miss}/p_{T}^{Z}", ""
            xbins=[0,0.1,0.2,0.4,0.6,3]
            nbins=len(xbins)-1
        else: print "[error] not right whichvar = ", whichvar," please check!"; exit(0)
                            
        if whichbcd=='allBG':
            bcdPlotter = validatorMC.allBG
            notes='bcd from all bg'
        elif whichbcd=='ZJets':
            bcdPlotter = validatorMC.ZJets
            notes='bcd from zjets'
        else: print "[error] Please check the whichbcd = %s, is 'allBG' or 'ZJets'" % (whichbcd); exit(0)
                    
        ### ----- Execute (plotting):
        if whichvar in binnedPlots:
            ha=zjetsMC.ZJets.drawTH1Binned('regTrg', var['A'], self.cuts['regTrg'], lumi_str, xbins, titlex = titlex, unitsx = units)
            hb=bcdPlotter.drawTH1Binned('regB_shift', var['B'], self.cuts['regB'], lumi_str, xbins,titlex = titlex,unitsx = units)
            hc=bcdPlotter.drawTH1Binned('regC_shift', var['C'], self.cuts['regC'], lumi_str, xbins,titlex = titlex,unitsx = units)
            hd=bcdPlotter.drawTH1Binned('regD_shift', var['D'], self.cuts['regD'], lumi_str, xbins,titlex = titlex,unitsx = units)
        else:
            ha=self.plotter.ZJets.drawTH1('regTrg', var['A'], self.cuts['regTrg'], lumi_str, nbins, xmin, xmax, titlex = titlex, units = units)
            hb=bcdPlotter.drawTH1('regB_shift', var['B'], self.cuts['regB'], lumi_str, nbins, xmin, xmax,titlex = titlex,units = units)
            hc=bcdPlotter.drawTH1('regC_shift', var['C'], self.cuts['regC'], lumi_str, nbins, xmin, xmax,titlex = titlex,units = units)
            hd=bcdPlotter.drawTH1('regD_shift', var['D'], self.cuts['regD'], lumi_str, nbins, xmin, xmax,titlex = titlex,units = units)

        iga=ha.GetSumOfWeights() #ha.Integral(0,1+ha.GetNbinsX())
        igb=hb.GetSumOfWeights() #hb.Integral(0,1+hb.GetNbinsX())
        igc=hc.GetSumOfWeights() #hc.Integral(0,1+hc.GetNbinsX())
        igd=hd.GetSumOfWeights() #hd.Integral(0,1+hd.GetNbinsX())
        print 'regB: ', hb.GetSumOfWeights(),  '; integral:', hb.Integral(0,1+hb.GetNbinsX()),\
              '\nregC: ', hc.GetSumOfWeights(), '; integral:', hc.Integral(0,1+hc.GetNbinsX()),\
              '\nregD(sum of weight): ', hd.GetSumOfWeights(), '; integral:', hd.Integral(0,1+hd.GetNbinsX())
        if isNormalized:
            ha.Scale(1./iga)
            hb.Scale(1./igb)
            hc.Scale(1./igc)
            hd.Scale(1./igd)
            ytitle='normalized'
        else: # Scale yield of bcd regions
            if yieldCorr:
                hb.Scale(iga/igb)
                hc.Scale(iga/igc)
                hd.Scale(iga/igd)
                print "[info] yield ratios: A/B=%.2f, A/C=%.2f, A/D=%.2f" % (iga/igb,iga/igc,iga/igd)
            ytitle='events'
        
        drawCompareSimple(hb, ha, "reg.B"+' '+leg_suffix, "reg. A",
                          xmin=xmin, xmax=xmax, outdir=self.outdir, notes=notes,lumi=self.lumi,logy=logy,
                          tag=compareTag+'BA', units='', ytitle=ytitle, setmax=1)

        drawCompareSimple(hc, ha, "reg.C"+' '+leg_suffix, "reg. A",
                          xmin=xmin, xmax=xmax, outdir=self.outdir, notes=notes,lumi=self.lumi,logy=logy,
                          tag=compareTag+'CA', units='', ytitle=ytitle, setmax=1)

        drawCompareSimple(hd, ha, "reg.D"+' '+leg_suffix, "reg. A",
                          xmin=xmin, xmax=xmax, outdir=self.outdir, notes=notes,lumi=self.lumi,logy=logy,
                          tag=compareTag+'DA', units='', ytitle=ytitle, setmax=1)

        ha.SetLineColor(ROOT.kRed)
        hb.SetLineColor(ROOT.kBlue)
        hc.SetLineColor(ROOT.kGreen)
        hd.SetLineColor(ROOT.kYellow)

        ha.SetMarkerColor(ROOT.kRed)
        hb.SetMarkerColor(ROOT.kBlue)
        hc.SetMarkerColor(ROOT.kGreen)
        hd.SetMarkerColor(ROOT.kYellow)

        if suffix=='': nameseq.insert(-1, '3v1')
        else : nameseq.append('3v1')
        #if isNormalized:
        if not yieldCorr:
            c1=ROOT.TCanvas(1)
            legend=GetLegendv1(0.65,0.75,0.85,0.90, [ha,hb,hc,hd],['reg. A','reg. B','reg. C','reg. D'],opt=['lpe','lpe','lpe','lpe'])
            nostack=ROOT.THStack("hs","hs")
            nostack.Add(ha,"e")
            nostack.Add(hb,"e")
            nostack.Add(hc,"e")
            nostack.Add(hd,"e")
            nostack.Draw("nostack")
            
            if units: ytitle+=' /' + str((xmax-xmin)/nbins) + '['+ units +']'
            nostack.GetXaxis().SetTitle(titlex)
            nostack.GetYaxis().SetTitle(ytitle)
            c1.Update()
            legend.Draw("same")
            c1.SetLogy()
            c1.SaveAs(self.outdir+'/'+'_'.join(nameseq)+'.pdf')
            
        else:
            hb.Add(hc);hb.Add(hd);hb.Scale(1.0/3.0)
            drawCompareSimple(ha, hb, "reg.A(MC)", "reg.A(bcd)",
                              xmin=xmin, xmax=xmax, outdir=self.outdir, notes=notes,lumi=self.lumi,
                              tag='_'.join(nameseq), units=units, ytitle=ytitle, setmax=2)
            
        #fout=ROOT.TFile(self.outdir+'/'+'_'.join(nameseq)+'.root','recreate')
        
        return
