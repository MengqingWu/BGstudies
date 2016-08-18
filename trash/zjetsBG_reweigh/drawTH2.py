#!/usr/bin/env python
import ROOT, os, copy
from python.SimplePlot import *

##--- parse arguments:
# default parameters:
lumi=2.318278305
TextFormat=".1e"
filename="./output/comparison2D/ZJstudy_2D_llnunu_l2_pt_llnunu_l1_pt.root"
listtmp=filename.split('/')
for ii in listtmp:
    if '.root' in ii:
        listtmp.remove(ii)
outdir='/'.join(listtmp)

# style setup:
ROOT.gROOT.ProcessLine('.x ../src/tdrstyle.C')
ROOT.gStyle.SetPadBottomMargin(0.12)
ROOT.gStyle.SetPadLeftMargin(0.12)
ROOT.gStyle.SetPadRightMargin(0.12)
ROOT.gStyle.SetTitleXOffset(0.65)
ROOT.gStyle.SetTitleYOffset(1)
ROOT.gStyle.SetMarkerSize(2)
ROOT.gStyle.SetPaintTextFormat(TextFormat) # draw text format
#ROOT.gStyle.SetPalette(ROOT.kBeach) # clair color for text printing

# prepare a note latex:
pt = ROOT.TLatex() #(0.1577181,0.9562937,0.9580537,0.9947552,"brNDC")
pt.SetNDC()
pt.SetTextAlign(12)
pt.SetTextFont(42)

# to draw:
fin=ROOT.TFile(filename)
c1=ROOT.TCanvas("c1","c1",1)
                    
for key in fin.GetListOfKeys():
    
    name=key.GetName()
    for iname in name.split('_'):
        if 'reg' in iname: reg=iname

    h2=fin.Get(name)
    print "%s: corr = %f +- %f"% ( name, h2.GetCorrelationFactor(), GetCorrelationFactorError(h2.GetCorrelationFactor(), h2.GetSumOfWeights()))
    c1.Clear()
    h2.Draw("colz")
    #h2.GetXaxis().SetTickLength(0);
    pt.SetTextSize(0.03)
    pt.DrawLatex(0.20,0.97,"CMS Preliminary")
    pt.DrawLatex(0.55,0.97,"#sqrt{s} = 13 TeV, #intLdt = "+"{:.3}".format(float(lumi))+" fb^{-1}")
    pt.SetTextSize(0.04)
    pt.DrawLatex(0.25,0.86, reg)
        
    c1.SetLogz(1)
    c1.SaveAs(outdir+'/'+name+".pdf")
    c1.Clear()
    
