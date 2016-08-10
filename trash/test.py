#!/usr/bin/env python

from python.SimplePlot import *
from ROOT import *
file=TFile("sfvsMet/sf_vs_met_test_mu.root","read")
h1=file.Get("h_metCRb")
h1.Print("all")
hsum=h1.GetCumulative(kFALSE)
hsum.SetMarkerColor(kRed)

hsum2=GetCumulativeAndError(h1,forward=False)

c1 = TCanvas(1)
hsum.Draw("p")
hsum2.Draw("same")
c1.SaveAs("test.eps")
