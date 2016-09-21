#!/usr/bin/env python
from ROOT import *
import math, os, sys, copy
import myStackPlotter as mystack

def CheckDir(outdir):
    dirlist=outdir.split('/')
    dirTest=''
    for idir in range(0,len(dirlist)):
        if dirlist[idir]=='': continue
        dirTest+=dirlist[idir]+'/'
        if not os.path.exists(dirTest):os.system('mkdir '+dirTest)

def GetHistRelativeErr(hstat):
    hrel=hstat.Clone(hstat.GetName()+'_relative')
    hrel.Reset()
    for ii in range(hstat.GetNbinsX()+1):
        hrel.SetBinContent(ii, 1.0)
        if hstat.GetBinContent(ii)>0:
            irelerr=hstat.GetBinError(ii)
            irelerr/=hstat.GetBinContent(ii)
        else:
            irelerr=0.0
 
        hrel.SetBinError(ii, irelerr)

    return hrel

def GetHistAbsErr(h1, hrel):
    """ hrel has bin content==1, with relative error drawn which corresponds to the h1 bin content. """
    if h1.GetNbinsX()!=hrel.GetNbinsX():
        print "[Error!] h1(%s) and hrel(%s) have different binning, CHECK!\n EXIT!" % (h1.GetName(), hrel.GetName())
        exit(0)
    for ii in range(h1.GetNbinsX()+1):
        if h1.GetBinContent(ii)>0: 
            h1.SetBinError(ii, hrel.GetBinError()*h1.GetBinContent())
        else: continue
    return
    
def GetCorrelationFactorError(corr, num):
    se=math.sqrt((1-corr**2)/(num-2))
    return se

def GetError(A, B, a=0., b=0.):
    # q=A/B, sigma(A)=a, sigma(B)=b, sigma(q)=error:
    if a*b==0:
        a=math.sqrt(A)
        b=math.sqrt(B)
    error=math.sqrt((a/B)**2+(b*A/B**2)**2)
    return error

def myIntegralAndError(h1, x1, x2, error):
    '''h1 is TH1, x1 x2 refers to the bin content, error is ROOT.Double(0.0),
    NB: bin is filled as [x1,x2), please choose correctly the x2'''
    binx1 = h1.GetXaxis().FindBin(x1)
    binx2 = h1.GetXaxis().FindBin(x2)
    return h1.IntegralAndError(binx1, binx2, error)

def ShiftXaxisTH1(inputHist, Shift, suffix):
    nbinsx=inputHist.GetNbinsX()
    hshift = copy.deepcopy(inputHist)
    hshift.SetName(inputHist.GetName() + suffix)
    hshift.Reset()
    
    for binx in range(0, nbinsx+1):
        Bin = hshift.GetBin(binx)
        if inputHist.GetBinContent(Bin):
            ix = inputHist.GetBinContent(Bin)
            errx = inputHist.GetBinError(Bin)
            
            shiftx = Shift + inputHist.GetBinCenter(Bin)
            shiftBin = hshift.FindBin(shiftx)
            
            hshift.SetBinContent(shiftBin, ix)
            hshift.SetBinError(shiftBin, errx)
        else: continue
    #hshift.Print("all")
    return hshift

def addOverflowTH2(h2):
    """ add overflow bins to the last bin of th2"""
    nbinsx, nbinsy = h2.GetNbinsX(), h2.GetNbinsY()
    for binx in range(0,nbinsx):
        lastBin=h2.GetBin(binx, nbinsy)
        offBin=h2.GetBin(binx, nbinsy+1)
        Content = h2.GetBinContent(lastBin)
        Content += h2.GetBinContent(offBin)
        err2 = h2.GetBinError(lastBin)*h2.GetBinError(lastBin)
        err2 += h2.GetBinError(offBin)*h2.GetBinError(offBin)
        h2.SetBinContent(lastBin, Content)
        h2.SetBinContent(lastBin, TMath.Sqrt(err2))
        
def GetCumulativeAndError(inputHist,forward=True, suffix=''):
    """ Derived from the root TH1::GetCumulative() function
    taking into consider of underflow and overflow bins;
    adding errorbar tranfer.
    """
    #nbinsx, nbinsy, nbinsz = inputHist.GetNbinsX(), inputHist.GetNbinsY(), inputHist.GetNbinsZ()
    nbinsx=inputHist.GetNbinsX()
    
    hintegrated = copy.deepcopy(inputHist)
    hintegrated.SetName(inputHist.GetName() + suffix)
    hintegrated.Reset()
    
    if forward: # Forward computation
        Sum = 0.
        igerr2 = 0.
        #for binz in range(0, nbinsz+1):
        #for biny in range(0, nbinsy+1):
        for binx in range(0, nbinsx+1):
            #bin = hintegrated.GetBin(binx, biny, binz)
            Bin = hintegrated.GetBin(binx)
            Sum += inputHist.GetBinContent(Bin)
            igerr2 += inputHist.GetBinError(Bin)*inputHist.GetBinError(Bin)
            hintegrated.SetBinContent(Bin, Sum)
            hintegrated.SetBinError(Bin, TMath.Sqrt(igerr2))
            
    else: # Backward computation
        Sum = 0.
        igerr2 = 0.
        #for binz in reversed(range(0, nbinsz+1)):
        #for biny in reversed(range(0, nbinsy+1)):
        for binx in reversed(range(0, nbinsx+2)):
            #bin = hintegrated.GetBin(binx, biny, binz)
            Bin = hintegrated.GetBin(binx)
            Sum += inputHist.GetBinContent(Bin)
            igerr2 += inputHist.GetBinError(Bin)*inputHist.GetBinError(Bin)
            hintegrated.SetBinContent(Bin, Sum)
            hintegrated.SetBinError(Bin, TMath.Sqrt(igerr2))
            #print binx, Bin, Sum, TMath.Sqrt(igerr2)
            
    return hintegrated
    

def GetRatio_TH1(h1, h2, h2_isStack=False, blinding=False, blindingCut=100):
    ''' h1/h2 '''
    hratio = h1.Clone("hRatio")
    h2.Draw()
    if h2_isStack:
        # h2_new = h2.GetHistogram()
        # h2_new.SetName('hstackmerge')
        # for hist in h2.GetHists():
        #     h2_new.Add(hist)
        h2_new = mystack.GetStackMerge(h2)
    else:
        h2_new=h2.Clone("single h2 as denominator")
            
    for i in xrange(h1.GetXaxis().GetNbins()+1):
        N1 = h1.GetBinContent(i)
        N2 = h2_new.GetBinContent(i)
        E1 = h1.GetBinError(i)
        E2 = h2_new.GetBinError(i)
        RR = N1/N2 if N2>0 else 0
        EE = 0 if N2<=0 else GetError(N1,N2,E1,E2) #math.sqrt(N2*N2*E1*E1+N1*N1*E2*E2)/N2/N2

        hratio.SetBinContent(i, RR)
        hratio.SetBinError(i, EE)
        if blinding and h1.GetBinCenter(i)>blindingCut: 
            hratio.SetBinContent(i, 0)
            hratio.SetBinError(i, 0)

    hratio.SetMarkerStyle(20)
    hratio.SetLineWidth(1)
    hratio.SetMarkerSize(1.)
    hratio.SetMarkerColor(kBlack)
    hratio.GetXaxis().SetTitle('')
    hratio.GetYaxis().SetTitle('Data/MC')
    hratio.GetYaxis().SetRangeUser(0.0,2.0)
    hratio.GetXaxis().SetLabelFont(42)
    hratio.GetXaxis().SetLabelOffset(0.007)
    hratio.GetXaxis().SetLabelSize(0.1)
    hratio.GetXaxis().SetTitleSize(0.05)
    hratio.GetXaxis().SetTitleOffset(1.15)
    hratio.GetXaxis().SetTitleFont(42)
    hratio.GetYaxis().SetLabelFont(42)
    hratio.GetYaxis().SetLabelOffset(0.01)
    hratio.GetYaxis().SetLabelSize(0.06)
    hratio.GetYaxis().SetTitleSize(0.12)
    hratio.GetYaxis().SetTitleOffset(0.5)
    hratio.GetYaxis().SetTitleFont(42)
    hratio.GetZaxis().SetLabelFont(42)
    hratio.GetZaxis().SetLabelOffset(0.007)
    hratio.GetZaxis().SetLabelSize(0.045)
    hratio.GetZaxis().SetTitleSize(0.05)
    hratio.GetZaxis().SetTitleFont(42)

    return hratio

def GetLegendv1(xmin, ymin, xmax,  ymax, hist, label, opt=[]):
    """ hist, label and opt are in type of list """
    legend=TLegend(xmin, ymin, xmax, ymax,"","brNDC");
    legend.SetFillStyle(0); #set legend box transparent
    legend.SetBorderSize(0);
    legend.SetTextSize(0.05);
    legend.SetTextFont(42);
#    legend.SetNColumns(2);
    legend.SetLineColor(0);
    if len(hist)!=len(label): print "[Error] GetLegendv1(): %d hists and %d labels, please check accordingly! " % (len(hist), len(label)); exit(0)
    if len(opt)!=0 and len(opt)!=len(hist):  print "[Error] GetLegendv1(): %d hists and %d labels, please check accordingly! "; exit(0)

    for ih, ilabel,iopt in zip(hist, label, opt):
        legend.AddEntry(ih,ilabel,iopt);

    return legend

def GetLegend(h1,label1,opt1,h2,label2,opt2):
    """ a fixed legend box with 2 entries only """
    legend=TLegend(0.65,0.75,0.85,0.90,"","brNDC");
    legend.SetFillStyle(0); #set legend box transparent
    legend.SetBorderSize(0);
    legend.SetTextSize(0.05);
    legend.SetTextFont(42);
#    legend.SetNColumns(2);
    legend.SetLineColor(0);
    legend.AddEntry(h1,label1,opt1);
    legend.AddEntry(h2,label2,opt2);

    return legend

def drawStack_simple(frame, hstack, hdata, hratio, legend,
                     hserr=[], hmask=[], hstack_opt="nostack",
                     outDir="./", output="output", channel="",
                     xmin=50., xmax=500., xtitle="" ,units="",
                     lumi=2.169, notes="", drawSig=False, hsig=[]):
    TH1.SetDefaultSumw2()
    gROOT.ProcessLine('.x ../src/tdrstyle.C')
            
    fout = TFile(outDir+'/'+output+'_'+channel.Data()+'.root', 'recreate')
        
    c1 = TCanvas(output+'_'+"c1", "c1", 600, 750); c1.Draw()
    c1.SetWindowSize(600 + (600 - c1.GetWw()), (750 + (750 - c1.GetWh())))
    p1 = TPad(output+'_'+"pad1","pad1",0,0.25,1,0.99)
    p1.SetBottomMargin(0.15)
    p1.SetLeftMargin(0.15)
    p1.Draw()
    p2 = TPad(output+'_'+"pad2","pad2",0,0,1,0.25)
    p2.SetTopMargin(0.03)
    p2.SetBottomMargin(0.3)
    p2.SetLeftMargin(0.15)
    p2.SetFillStyle(0)
    p2.Draw()
    
    gStyle.SetOptStat(0)
    gStyle.SetOptTitle(0)
    
    p1.cd()
    frame.Draw()
    hstack.Draw(hstack_opt+", same")

    hstack.SetMinimum(0.01)
    hstack.GetHistogram().GetXaxis().SetRangeUser(xmin,xmax)

    maxi=hstack.GetHistogram().GetXaxis().GetXmax()
    mini=hstack.GetHistogram().GetXaxis().GetXmin()
    bins=hstack.GetHistogram().GetNbinsX()
    if len(units)>0:
        hstack.GetHistogram().GetXaxis().SetTitle(xtitle + " (" +units+")")
        hstack.GetHistogram().GetYaxis().SetTitle("Events / "+str((maxi-mini)/bins)+ " "+units)
    else:
        hstack.GetHistogram().GetXaxis().SetTitle(xtitle)
        hstack.GetHistogram().GetYaxis().SetTitle("Events")

    if len(hserr):
        hserr[0].SetName(output+'_'+'ErrorCombo')
        p1.cd()
        hserr[0].Draw("nostack, same")

    hdata.Draw("P,E1,same")
    if drawSig and len(hsig)!=0:
        for ihsig in hsig: ihsig.Draw("HIST, same")
    legend.Draw("same")

    ##--> lower pad:
    hratio.SetName(output+'_'+'hratio')        
    hline = copy.deepcopy(hratio)
    for ii in range(hline.GetNbinsX()+1):
        hline.SetBinContent(ii,1.0)
        hline.SetBinError(ii,0.0)
    hline.SetLineColor(kRed)
    hline.SetFillStyle(0)
    
    p2.cd()
    hratio.Draw('AXIS')
    hline.Draw('HIST,SAME')
    if len(hserr)>1:
        hserr[1].SetName(output+'_'+'RelErrorCombo')
        hserr[1].Draw("nostack, same")
        
    hratio.Draw('P,E1,SAME')
    if len(hmask):
        if hmask[0]:
            p1.cd()
            hmask[0].Draw("HIST,SAME")
        if len(hmask)>1 and hmask[1]:
            p2.cd()
            hmask[1].Draw("HIST,SAME")
    hratio.GetXaxis().SetRangeUser(xmin,xmax)
    hline.GetXaxis().SetRangeUser(xmin,xmax)

    p1.Update()
    p2.Update()
    c1.Update()

    #-------- draw pave tex
    pt =TLatex() #(0.1577181,0.9562937,0.9580537,0.9947552,"brNDC")
    pt.SetNDC()
    pt.SetTextAlign(12)
    pt.SetTextFont(42)
    pt.SetTextSize(0.03)

    p1.cd()
    pt.DrawLatex(0.20,0.97,"CMS Preliminary")
    pt.DrawLatex(0.55,0.97,"#sqrt{s} = 13 TeV, #intLdt = "+"{:.3}".format(float(lumi))+" fb^{-1}")
    pt.SetTextSize(0.04)
    pt.DrawLatex(0.25,0.86, notes)
    p1.SetLogy()
    p1.RedrawAxis()
    p1.Update()

    if channel!="":
        if channel.Contains("el"): channel_tex="ee"
        elif channel.Contains("mu"): channel_tex="#mu#mu"
        else: channel_tex=channel.Data()
        pt.DrawLatex(0.25,0.82, channel_tex+" channel")
            
    fout.cd()
    c1.Write()
    hratio.Write()
    hstack.Write()
    if len(hserr):
        for ihserr in hserr:
            ihserr.Write()
    hdata.Write()
    fout.Close()

    c1.SaveAs(outDir+'/'+output+'_'+channel.Data()+'.eps')
    return

def drawCompare(hstack, hratio, legend,
                hstack_opt="nostack",outdir="./",tag="test",
                xmin=50., xmax=500., xtitle="" , ytitle="Events", units="",
                lumi=2.169, logy=True, notes="", setmax=0):
    TH1.SetDefaultSumw2()
    fout = TFile(outdir+'/'+tag+'.root', 'recreate')
    
    c1 = TCanvas(tag+"_c1", "c1", 600, 750); c1.Draw()
    c1.SetWindowSize(600 + (600 - c1.GetWw()), (750 + (750 - c1.GetWh())))
    p1 = TPad(tag+"_pad1","pad1",0,0.25,1,0.99)
    p1.SetBottomMargin(0.15)
    p1.SetLeftMargin(0.15)
    p1.Draw()
    p2 = TPad(tag+"_pad2","pad2",0,0,1,0.25)
    p2.SetTopMargin(0.03)
    p2.SetBottomMargin(0.3)
    p2.SetLeftMargin(0.15)
    p2.SetFillStyle(0)
    p2.Draw()
    
    gStyle.SetOptStat(0)
    gStyle.SetOptTitle(0)
    
    p1.cd()
    hstack.Draw(hstack_opt)
    if setmax!=0:
        print 'I am setting maximum*', setmax
        hstack.SetMaximum(hstack.GetMaximum()*setmax)
    legend.Draw("same")
        
    hstack.SetMinimum(0.01)
    hstack.GetHistogram().GetXaxis().SetRangeUser(xmin,xmax)
    
    maxi=hstack.GetHistogram().GetXaxis().GetXmax()
    mini=hstack.GetHistogram().GetXaxis().GetXmin()
    bins=hstack.GetHistogram().GetNbinsX()
    
    if len(units)>0:
        hstack.GetHistogram().GetXaxis().SetTitle(xtitle + " (" +units+")")
        hstack.GetHistogram().GetYaxis().SetTitle(ytitle +" / "+"{:.1f}".format((maxi-mini)/bins)+ " "+units)
    else:
        hstack.GetHistogram().GetXaxis().SetTitle(xtitle)
        hstack.GetHistogram().GetYaxis().SetTitle(ytitle)

    hratio.SetName(tag+'_'+'hratio')
    hline = copy.deepcopy(hratio)
    for ii in range(hline.GetNbinsX()+1):
        hline.SetBinContent(ii,1.0)
        hline.SetBinError(ii,0.0)
    hline.SetLineColor(kRed)
    hline.SetFillStyle(0)
    p2.cd()
    hratio.Draw('AXIS')
    hline.Draw('HIST,SAME')
    hratio.Draw('P,E1,SAME')
    hratio.GetXaxis().SetRangeUser(xmin,xmax)

    if logy:    p1.SetLogy()
    p1.RedrawAxis()
    p1.Update()
    p2.Update()
    c1.Update()
        
    #-------- draw pave tex
    pt =TLatex() #(0.1577181,0.9562937,0.9580537,0.9947552,"brNDC")
    pt.SetNDC()
    pt.SetTextAlign(12)
    pt.SetTextFont(42)
    pt.SetTextSize(0.03)
    
    p1.cd()
    pt.DrawLatex(0.19,0.97,"CMS Preliminary")
    pt.DrawLatex(0.55,0.97,"#sqrt{s} = 13 TeV, #intLdt = "+"{:.3}".format(float(lumi))+" fb^{-1}")
    pt.SetTextSize(0.04)
    pt.DrawLatex(0.65,0.7, notes)
       
    fout.cd()
    c1.Write()
    hratio.Write()
    hstack.Write()
    fout.Close()
    
    c1.Print(outdir+'/'+tag+'.eps')
    c1.Clear()
    
    return

def drawCompareSimple(h1, h2, leg1, leg2,
                      xmin=50., xmax=500., xtitle="" , ytitle="", units="",
                      lumi=2.169, notes="",
                      outdir="./", tag="test", setmax=0, logy=True):

    h1.SetLineColor(kRed)
    h1.SetFillColor(kRed)
    h2.SetMarkerStyle(20)
    h2.SetMarkerSize(1.0)
    herror=copy.deepcopy(h1)
    herror.SetFillColor(kBlue)
    herror.SetFillStyle(3345)
    herror.SetMarkerSize(0)
    
    hstack=THStack("h_stack","stack histograms")
    hstack.Add(h1,"hist,0")
    hstack.Add(herror,"e2,0")
    hstack.Add(h2,"p,0")

    if xtitle=="": xtitle=h1.GetXaxis().GetTitle()
    if ytitle=="": ytitle=h1.GetYaxis().GetTitle()
    
    drawCompare( hstack=hstack,
                 hratio=GetRatio_TH1(h2,h1),
                 legend=GetLegend(h1,leg1, "f", h2, leg2, 'lpe'),
                 outdir=outdir, tag=tag,
                 xmin=xmin, xmax=xmax,
                 xtitle=xtitle, ytitle=ytitle, units=units,
                 lumi=lumi, logy=logy,
                 notes=notes, setmax=setmax)
    return
