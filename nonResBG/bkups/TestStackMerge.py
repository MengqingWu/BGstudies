#!/usr/bin/env python

import ROOT
import copy

ROOT.gROOT.ProcessLine('.x ../src/tdrstyle.C')

filein = ROOT.TFile("./stack_test/stack_nonResDD_met200_MC_llnunu_mtc.root")
hstack = filein.Get("stack_nonResDD_met200_MC_llnunu_mtc_stack")
herror=copy.deepcopy(hstack.GetHists().At(0))
herror.Clear()

for ibin in range(0, herror.GetNbinsX()+2):
    """ deal with the under/overflow bins"""
    igcont=0.0
    igerr2=0.0
    for ihist in hstack.GetHists():
        if ibin==0: print "[debug] ihist=",ihist.GetName()
        if ihist.GetBinContent(ibin)<0:
            cont=0.0
            err2=0.0
        else:
            cont=ihist.GetBinContent(ibin)
            err2=ihist.GetBinError(ibin)*ihist.GetBinError(ibin)
         
        print "  ibin=",ibin,", content=", cont,", err=", ROOT.TMath.Sqrt(err2)
        igcont+=cont
        igerr2+=err2
    herror.SetBinContent(ibin,igcont)
    herror.SetBinError(ibin,ROOT.TMath.Sqrt(igerr2))
    
herror.SetMarkerColor(ROOT.kRed)

herror.Print("all")

herror1=copy.deepcopy(hstack.GetHists().At(0))
herror1.Clear()
for ihist in hstack.GetHists():
    print "[debug] ihist=",ihist.GetName()
    herror1.Add(ihist)
#herror1.SetFillColor(ROOT.kBlue)
#herror1.SetFillStyle(3345)
#herror1.SetMarkerSize(0)
herror1.SetLineColor(ROOT.kBlack)

c1=ROOT.TCanvas(1)
herror.Draw("p")
herror1.Draw("same")
c1.SaveAs("test.pdf")
