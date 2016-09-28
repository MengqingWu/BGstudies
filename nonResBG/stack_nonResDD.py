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
# --------------------  M_out [50,65] U [115,180]
#  eu in Z | eu out Z
#  M_in (70,110)

""" 
the M_ll shape reweight is done as:
   f(non_res, data_ll) =  f(res+non_res, data_eu) * f(non_res, mc_ll)/f(res+non_res, mc_eu)
to account for selection efficiency differed bin by bin in M_ll distribution.

   alpha = N(non_res, data, ll_out) / N(non_res, data, eu_out)
where:
N(non_res, data, ll_out) substracts the res-bkg using MC
N(non_res, data, eu_out) refers to the data(non_res+res) reweighted to f(non_res, data_ll).
"""

class StackDataDriven:
    def __init__(self, indir="./nonResSkim_v3.0", outdir='stack_test',
                 lumi = 2.318278305,  sepSig=True,
                 LogY=True,   doRatio=True,
                 addSig=True, addData=True,
                 scaleElMu=True,
                 zpt=100, met=0, side='both'):
        if not os.path.exists(outdir): os.system('mkdir '+outdir)
        self.logy=LogY
        self.outdir = outdir
        self.lumi = lumi
        self.MzWtTag='MzWtOn' if scaleElMu else 'MzWtOff' # a tag for output file
        self.SideTag=side+'Side'
        
        # plotter_eu: the MuonEG data has the weight (scaleElMu) which reweights Meu as Mll distribution using MC
        self.plotter_eu=InitializePlotter(indir, addSig=False, addData=True, doRatio=doRatio, doElMu=True, scaleElMu=scaleElMu, LogY=LogY)

        self.plotter_ll=InitializePlotter(indir, addSig=addSig, addData=True, doRatio=doRatio, LogY=LogY)
        self.Stack_ll = self.plotter_ll.GetStack() 
        self.Stack_ll.rmPlotter(self.plotter_ll.TT, "TT","TT", "background")
        self.Stack_ll.rmPlotter(self.plotter_ll.WW, "WW","WW, WZ non-reson.", "background")
        self.Stack_ll.rmPlotter(self.plotter_ll.WJets, "WJets","W+Jets", "background")
        
        self.setcuts=SetCuts()
        ROOT.gROOT.ProcessLine('.x ../src/tdrstyle.C')
        self.zpt_cut, self.met_cut= str(zpt), str(met)
        self.cuts=self.setcuts.GetAlphaCuts(zpt_cut=self.zpt_cut, met_cut=self.met_cut, side=side)

        if self.zpt_cut==0 and self.met_cut==0: self.note = "no E_{T}^{miss}/P_{T}^{Z} cuts"
        else: self.note = "E_{T}^{miss}>" + self.met_cut + ", P_{T}^{Z}>" + self.zpt_cut

        self.chan = "inclusive"

        ##-> tools
        self.err_product=lambda A, B, a, b: sqrt((a*B)**2+(b*A)**2) # A*B
        self.err_division=lambda A, B, a, b: sqrt((a/B)**2+(b*A/B**2)**2) # A/B
        
    def GetAlpha(self, var_ll="llnunu_l1_mass", var_emu="elmununu_l1_mass", nbinsx=40, xmin=0.0, xmax=200.0, isTest=False):
        ROOT.TH1.SetDefaultSumw2()
        data_ll = self.plotter_ll.allBG if isTest else self.plotter_ll.Data
        data_eu = self.plotter_eu.allBG if isTest else self.plotter_eu.Data
        lumi_str = str(self.lumi*1000)  if isTest else '1'
        
        h_ll_out_dt = data_ll.drawTH1(var_ll+'_dt', var_ll, self.cuts['ll']['out'], lumi_str,
                                      nbinsx, xmin, xmax, titlex = var_ll)
        h_res_out_mc = self.plotter_ll.ResBG.drawTH1(var_ll+'_mc', var_ll, self.cuts['ll']['out'], str(self.lumi*1000),
                                                    nbinsx, xmin, xmax, titlex = var_ll)
        h_ll_out_dt.Add(h_res_out_mc, -1)
        
        h_eu_out_dt = data_eu.drawTH1(var_emu+'_dt', var_emu, self.cuts['emu']['out'], lumi_str,
                                      nbinsx, xmin, xmax, titlex = var_emu)

        err_llout, err_euout = ROOT.Double(0.0), ROOT.Double(0.0)
        ig_ll_out_dt = h_ll_out_dt.IntegralAndError(1, h_ll_out_dt.GetNbinsX(), err_llout)
        ig_eu_out_dt = h_eu_out_dt.IntegralAndError(1, h_eu_out_dt.GetNbinsX(), err_euout)
        
        alpha = ig_ll_out_dt/ig_eu_out_dt
        err_alpha = self.err_division(ig_ll_out_dt, ig_eu_out_dt, err_llout, err_euout)

        #print "\n[debug] cuts: ", self.cuts['emu']['out']
        if isTest: print "\n[info]--> alpha computed for closure test:"
        print "\n[info] N_llout_dt = %.2f,  N_euout_dt = %.2f" %(ig_ll_out_dt, ig_eu_out_dt)
        print "[info] alpha (N_llout/N_euout) =  %.2f +- %.2f" %(alpha,err_alpha)

        return alpha, err_alpha

    
    def compareDataDrivenMC(self, var_ll, var_emu, nbinsx, xmin, xmax, titlex, units, xcutmin, xcutmax, xbins=[], isTest=False):
        """
        compare data-driven estimate wrt MC expectation of var_ll for non-reso. bkg
        """
        ROOT.TH1.SetDefaultSumw2()
        data_eu =  self.plotter_eu.Data
        lumi_str = '1'
        compTagger = ['compare_dataDriven_MC', var_ll, self.MzWtTag, 'met'+self.met_cut, self.SideTag]
        if isTest:
            data_eu = self.plotter_eu.allBG 
            lumi_str = str(self.lumi*1000) 
            compTagger += ['closureTest']
            
        compTag = '_'.join(compTagger) 
        
        dobinned = True if len(xbins) else False
        
        if dobinned:
            h_nonRes_dd = data_eu.drawTH1Binned(var_emu+'nonres_dt_emuin', var_emu, self.cuts['emu']['in'], lumi_str,
                                                xbins, titlex = titlex, unitsx = units)
            h_nonRes_mc = self.plotter_ll.NonResBG.drawTH1Binned(var_ll+'nonres_mc_llin', var_ll, self.cuts['ll']['in'], str(self.lumi*1000),
                                                                 xbins, titlex = titlex, unitsx = units)
        else:
            h_nonRes_dd = data_eu.drawTH1(var_emu+'nonres_dt_emuin', var_emu, self.cuts['emu']['in'], lumi_str,
                                          nbinsx, xmin, xmax, titlex = titlex, units = units)
            h_nonRes_mc = self.plotter_ll.NonResBG.drawTH1(var_ll+'nonres_mc_llin', var_ll, self.cuts['ll']['in'], str(self.lumi*1000),
                                                           nbinsx, xmin, xmax, titlex = titlex, units = units)

        alpha, err_alpha = self.GetAlpha(isTest=isTest)
            
        h_nonRes_dd.Scale(alpha)

        err1, err2=ROOT.Double(0.0), ROOT.Double(0.0)
        igr1, igr2 = h_nonRes_dd.IntegralAndError(0, h_nonRes_dd.GetNbinsX()+1, err1), h_nonRes_mc.IntegralAndError(0, h_nonRes_mc.GetNbinsX()+1, err2)
        print '[info] llin, data-driven pred.:  %.2f +- %.2f' %(igr1, err1)
        print '[info] llin, MC exp.:  %.2f +- %.2f' %(igr2, err2)
                
        drawCompareSimple(h_nonRes_mc, h_nonRes_dd, "non-reson. MC", "non-reson. data-driven",
                          xmin=xcutmin, xmax=xcutmax, outdir=self.outdir, notes="",
                          tag = compTag, units='', lumi=self.lumi, ytitle='events', setmax=10)

        PredDivideExp=h_nonRes_dd.Clone("nonres. MC pred. divde MC exp.")
        PredDivideExp.Divide(h_nonRes_mc)
        
        return PredDivideExp


    def CombineError(self, h1, hsys, sysGlobal):
        # h1 is the data-driven non-res histogram.
        # hsys is the MC pred/exp difference as a estimate sys. err (each content need to minus 1 to get the relative sys. err)
        # sysGlobal is the sum of all other global relative err^2 (such as the alpha stat. error)
        # return hcombo: bincontent as h1, but with sqrt(sys**2+stat**2) error bar

        hcombo=h1.Clone("h_allsys") 
        hcombo.Reset()
        for ii in range(h1.GetNbinsX()+1):
            iMeanVal=h1.GetBinContent(ii)                
            if iMeanVal>0:
                ibias=hsys.GetBinContent(ii)-1
                istat=h1.GetBinError(ii)
                igrerr2=(ibias*iMeanVal)**2+(sysGlobal*iMeanVal)**2+istat**2
                print "[debug] @%.f = %f, sys = %.2f, stat = %.2f, combo = %.2f"%(h1.GetBinCenter(ii), iMeanVal, ROOT.TMath.Sqrt((ibias*iMeanVal)**2+(sysGlobal*iMeanVal)**2), istat, ROOT.TMath.Sqrt(igrerr2))

                hcombo.SetBinContent(ii, iMeanVal)
                hcombo.SetBinError(ii, ROOT.TMath.Sqrt(igrerr2))
            else: continue # nothing to do with empty/negative bins
                
        # ctemp = ROOT.TCanvas(1)
        # hcombo.SetFillColor(ROOT.kBlue)
        # hcombo.SetFillStyle(3354)
        # hcombo.SetMarkerSize(0)
        # hcombo.SetLineColor(0)
        # hcombo.Draw("e2")
        # #hstat.SetFillColor(ROOT.kRed)
        # h1.Draw("e2, same")
        # ctemp.SaveAs("GetSysErrorTest.pdf")

        return hcombo
    

    #def drawDataDrivenStack(self, var_ll, var_emu, nbinsx, xmin, xmax, titlex, units, xcutmin=0, xcutmax=0, xbins=[], blind=False, blindCut=100.0, doCombineErr=False):
    def drawDataDrivenStack(self, stackFileName, hres_stat, hres_stat_sys=None, blind=False, blindCut=100.0):
        #tag = '_'.join(['stack_nonResDD','met'+self.met_cut, self.SideTag])
        #stackTag=tag+'_'+var_ll
        #dobinned = True if len(xbins) else False
        #if xcutmin==0: xcutmin = xmin
        #if xcutmax==0: xcutmax = xmax
        
        #--> to have all histogram with stat. err. computed correctly
        ROOT.TH1.SetDefaultSumw2()

        #alpha, err_alpha = self.GetAlpha()
        
        #h_res_llin_mc = self.plotter_ll.ResBG.drawTH1(var_ll, var_ll, self.cuts['ll']['in'], str(self.lumi*1000), nbinsx, xmin, xmax, titlex=titlex, units=units)
        #ctemp = ROOT.TCanvas(1)
        #h_res_llin_mc.Draw()
        #ctemp.SaveAs("test.pdf")

        #self.Stack_ll.drawStack(var_ll, self.cuts['ll']['in'], str(self.lumi*1000), nbinsx, xmin, xmax, titlex = titlex, units = units,
        #                        output=stackTag, outDir=self.outdir, separateSignal=True, drawtex="", channel=self.chan, xbins = xbins,
        #                        blinding = blind, blindingCut = blindCut)
        # if dobinned:
        #     h_nonRes_dd = self.plotter_eu.Data.drawTH1Binned(var_emu, var_emu, self.cuts['emu']['in'], '1', xbins, titlex = titlex, unitsx = units)
        # else:
        #     h_nonRes_dd = self.plotter_eu.Data.drawTH1(var_emu, var_emu, self.cuts['emu']['in'], '1', nbinsx, xmin, xmax, titlex = titlex, units = units)
        hres_stat.SetFillColor(ROOT.kAzure-9)        
        #h_nonRes_dd.Scale(alpha)
        #if doCombineErr and 'l1_mass' not in var_ll: # think about how to deal with mZ distribution [FIXME]
        #    hbias=self.compareDataDrivenMC(var_ll, var_emu, nbinsx, xmin, xmax, titlex, units, xcutmin, xcutmax, xbins=xbins, isTest=True)
        #    igrerr2=(err_alpha/alpha)**2
            
        # Draw the m_ll in z window with data-driven non-res bkg
        ROOT.TH1.AddDirectory(ROOT.kFALSE)
        fstack=ROOT.TFile(stackFileName)
        stackTag=stackFileName.split('/')[-1].replace(".root","")
        outdir='/'.join(stackFileName.split('/')[:-1])
        #if '.root' not in stackTag: print "[Error!] Check the stackTag: %s, it is not a root file!"%(stackTag); exit(0);
        if not os.path.isdir(outdir):  print "[Error!] Directory: %s, does NOT exit!! "%(outdir); exit(0);
        
        hs=fstack.Get(stackTag+"_stack")

        hframe=fstack.Get(stackTag+'_frame')
        #hframe.GetXaxis().SetRangeUser(xcutmin, xcutmax)
        #if ROOT.TString(var_ll).Contains("mass"):
        #    if self.logy: hframe.SetMaximum(hframe.GetMaximum()*100)
        #    else: hframe.SetMaximum(hframe.GetMaximum()*1.2)

        hmask_data=fstack.Get(stackTag+'_hmask_data')
        hmask_ratio=fstack.Get(stackTag+'_hmask_ratio')

        hserr=fstack.Get(stackTag+'_StackError')
        hserr.SetLineColor(0)
        hserr_sys = hserr.Clone(hserr.GetName()+'_withsys')
        hserr_sys.SetFillStyle(3354)
        hserr.Add(hres_stat)
        #hserr.SetFillColor(ROOT.kBlue)
        #hserr.SetFillStyle(3345)
        
        hdata=fstack.Get(stackTag+'_data0')
        hdataG=fstack.Get(stackTag+'_dataG')
        legend=fstack.Get(stackTag+'_legend')
        
        hsig1=fstack.Get(stackTag+'_BulkGravToZZToZlepZinv_narrow_800')
        hsig2=fstack.Get(stackTag+'_BulkGravToZZToZlepZinv_narrow_1000')
        hsig3=fstack.Get(stackTag+'_BulkGravToZZToZlepZinv_narrow_1200')
        fstack.Close()

        #err1, err2, err3=ROOT.Double(0.0), ROOT.Double(0.0), ROOT.Double(0.0)
        #igr1, igr2, igr3=hres_stat.IntegralAndError(0, hres_stat.GetNbinsX()+1, err1), h_res_llin_mc.IntegralAndError(0, h_res_llin_mc.GetNbinsX()+1, err2),hdata.IntegralAndError(0, hdata.GetNbinsX()+1, err3)
        #print '[info] llin, data-driven nonres:  %.2f +- %.2f' %(igr1, err1)
        #print '[info] llin, MC res. bkg:  %.2f +- %.2f' %(igr2, err2)
        #print '[info] llin, data obs.: %.2f +- %.2f' %(igr3, err3)

        
        hsnew=ROOT.THStack(stackTag+"_stack_new","")
        hsnew.Add(hres_stat)
        
        nonresTag=[stackTag+'_'+sample for sample in ['WJets0','TT0','WW0'] ]
        for ihist in hs.GetHists():
            if ihist.GetName() in nonresTag: print '[Removing...] I am a nonres bkg : ',ihist.GetName()
            else:  hsnew.Add(ihist)
        
        #for ih in hsnew.GetHists():
        #    print '[debug] ', ih.GetName()
        #print hsnew
     
        hratio=GetRatio_TH1(hdata,hsnew,True, blinding=blind, blindingCut=blindCut)

        # Let's find out the data entry in legend:
        for ileg in legend.GetListOfPrimitives():
            if ileg.GetLabel() in ['W+Jets', 'TT', 'WW, WZ non-reson.']:
                legend.GetListOfPrimitives().Remove(ileg)
            if ileg.GetLabel()=='Data': beforeObject=ileg
            
        datadrivenEntry=ROOT.TLegendEntry(hres_stat,"non-reson. (data-driven)","f")
        statErrorEntry=ROOT.TLegendEntry(hserr,"stat-only error","f")
        legend.GetListOfPrimitives().AddBefore(beforeObject,datadrivenEntry)
        legend.GetListOfPrimitives().AddAfter(beforeObject,statErrorEntry)

        
        errstack=ROOT.THStack("hs_combine_sys_stat_error","sys and stat combined histograms")
        errstack.Add(hserr, "e2, 0")
        hserr_rel = GetHistRelativeErr(hserr)
        errstack2 = ROOT.THStack("hratio_combine_sys_stat_error","relative sys and stat combined histograms")
        errstack2.Add(hserr_rel, "e2,0")
        
        #if hres_stat_sys and 'l1_mass' not in var_ll: # think about how to deal with mZ distribution [FIXME]
        if hres_stat_sys:
            hserr_sys.Add(hres_stat_sys)
            sysErrorEntry=ROOT.TLegendEntry(hserr_sys,"sys+stat error","f")
            legend.GetListOfPrimitives().AddAfter(beforeObject,sysErrorEntry)
            
            errstack.Add(hserr_sys, "e2, 0")

            hserr_sys_rel = GetHistRelativeErr(hserr_sys)
            errstack2.Add(hserr_sys_rel, "e2,0")
            
        
        drawStack_simple(hframe, hsnew, hdataG, hratio, legend,
                         hserr=[errstack, errstack2], hmask=[hmask_data, hmask_ratio], hstack_opt = "A, HIST",
                         outDir = outdir, output = stackTag+"_datadriven", channel = ROOT.TString(self.chan),
                         #xmin = xcutmin, xmax = xcutmax, xtitle = titlex ,units = units,
                         lumi = self.lumi, notes = self.note,
                         drawSig=True, hsig=[hsig1, hsig2, hsig3])
        return

    def doClosureTest(self, var_ll, var_emu, nbinsx, xmin, xmax, titlex, units, xcutmin, xcutmax, xbins=[],):
        """ taking all MC samples as if they are the data to inject to:
        f(non_res, data_ll) =  f(res+non_res, data_eu) * f(non_res, mc_ll)/f(res+non_res, mc_eu)
        target: compare the data-driven technique predicted non-res in data_ll, with the MC_ll expectation.
        """
        print "\n[info] A closure TEST will be performed: take ALL MC as the data to inject to the estimate technique :D"
        print "[Processing] I am comparing data-driven result w.r.t. MC expectation"
        self.compareDataDrivenMC(var_ll, var_emu, nbinsx, xmin, xmax, titlex, units, xcutmin, xcutmax, xbins=xbins, isTest=True)
        
        return

    def drawMCStack(self, var_ll, var_emu, nbinsx, xmin, xmax, titlex, units, xbins=[], blind=False, blindCut=100.0):
        """
        simply draw all background MC stacked compared with data, with signals on top of them.
        """
        tag = '_'.join(['stack_nonResDD','met'+self.met_cut,'MC'])
        stackTag=tag+'_'+var_ll

        allStack_ll = self.plotter_ll.GetStack() 

        allStack_ll.drawStack(var_ll, self.cuts['ll']['in'], str(self.lumi*1000), nbinsx, xmin, xmax, titlex = titlex, units = units,
                              output=stackTag, outDir=self.outdir, separateSignal=True, drawtex=self.note, channel=self.chan, xbins = xbins,
                              blinding = blind, blindingCut = blindCut)

        return

    
    def drawDataDriven(self, var_ll, var_emu, nbinsx, xmin, xmax, titlex, units, xbins=[], blind=False, blindCut=100.0,
                       addSys=True, doStack=False, doClosure=False, doCompare=False ):
        """ Draw a data driven non-res distribution, 
        -> sys+stat uncertainty can be switched off by addSys=False 
        -> stack with other bkg can be switched on by doStack=True
        -> closure Test can be switched on by doClosure=True
        -> data-driven vs MC can be plotted by doCompare=True
        """
        ROOT.TH1.SetDefaultSumw2()
        tagger = ['nonResDD', var_ll, self.MzWtTag, 'met'+self.met_cut, self.SideTag]
        #tag = '_'.join(tagger)
        dobinned = True if len(xbins) else False
        
        alpha, err_alpha = self.GetAlpha()
        if addSys: alpha_mc, err_alpha_mc = self.GetAlpha(isTest=True)
        igrerr2=(err_alpha/alpha)**2
        
        if dobinned:
            hres_stat = self.plotter_eu.Data.drawTH1Binned(var_emu,var_emu, self.cuts['emu']['in'],'1',xbins, titlex = titlex, unitsx = units)
            if addSys:
                h_eu_fakedt = self.plotter_eu.allBG.drawTH1Binned(var_emu+'_in_fakedt',var_emu, self.cuts['emu']['in'],str(self.lumi*1000),xbins,titlex = titlex,unitsx = units)
                h_ll_mc = self.plotter_ll.NonResBG.drawTH1Binned(var_ll+'_in_mc',var_ll, self.cuts['ll']['in'], str(self.lumi*1000),xbins,titlex = titlex,unitsx = units)  
        else:
            hres_stat = self.plotter_eu.Data.drawTH1(var_emu, var_emu, self.cuts['emu']['in'], '1', nbinsx, xmin, xmax, titlex = titlex, units = units)
            if addSys:
                h_eu_fakedt = self.plotter_eu.allBG.drawTH1(var_emu+'_in_fakedt',var_emu,self.cuts['emu']['in'],str(self.lumi*1000),nbinsx,xmin,xmax,titlex = titlex,units = units)
                h_ll_mc = self.plotter_ll.NonResBG.drawTH1(var_ll+'_in_mc',var_ll,self.cuts['ll']['in'],str(self.lumi*1000),nbinsx,xmin,xmax,titlex = titlex,units = units)
            
        hres_stat.Scale(alpha)
        hres_stat.SetMarkerSize(0)

        
        if doClosure:
            closureTag = '_'.join(['compare_DatadrivenMC']+tagger+['closureTest']) 
            drawCompareSimple(h_ll_mc, h_eu_fakedt, "non-reson. MC", "non-reson. data-driven",
                              xmin=xmin, xmax=xmax, outdir=self.outdir, notes="",
                              tag = closureTag, units=units, lumi=self.lumi, ytitle='Events', setmax=10)
        if addSys:
            h_eu_fakedt.Scale(alpha_mc)
            h_eu_fakedt.Divide(h_ll_mc)
            hres_stat_sys=self.CombineError( hres_stat, h_eu_fakedt, igrerr2)
            hres_stat_sys.SetFillStyle(3354)

        if doCompare:
            print "[debug] line color: ", h_ll_mc.GetLineColor()
            h_ll_mc.SetLineColor(ROOT.kBlack)
            compTag = '_'.join(['compare_DatadrivenMC']+tagger) 
            drawCompareSimple(hres_stat, h_ll_mc, "data-driven pred.", "MC exp.",
                              xmin=xmin, xmax=xmax, outdir=self.outdir, notes="", ratiotitle="Exp/Pred",
                              tag = compTag, units=units, lumi=self.lumi, ytitle='Events', setmax=10)

        if doStack:
            stackTag='_'.join(['stack']+tagger+['_sys']) if addSys else '_'.join(['stack']+tagger)
            
            self.Stack_ll.drawStack(var_ll, self.cuts['ll']['in'], str(self.lumi*1000), nbinsx, xmin, xmax, titlex = titlex, units = units,
                                    output=stackTag, outDir=self.outdir, separateSignal=True, drawtex="", channel=self.chan, xbins = xbins,
                                    blinding = blind, blindingCut = blindCut)
            
            self.drawDataDrivenStack(self.outdir+'/'+stackTag+'.root', hres_stat, hres_stat_sys, blind=blind, blindCut=blindCut)

 
            
        ##--> testing <--##
        ctemp = ROOT.TCanvas(1)
        hres_stat.SetFillStyle(3345)
        hres_stat.SetFillColor(ROOT.kRed)
        hres_stat.Draw("e2")
        if addSys:   hres_stat_sys.Draw("e2, same")
        ctemp.SaveAs("test.pdf")
        ###----------------------###
        
        return #hres_stat, hres_stat_sys
    
