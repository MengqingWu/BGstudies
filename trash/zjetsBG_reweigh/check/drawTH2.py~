#!/usr/bin/env python
import ROOT, os, copy

outdir='../output/shape/'
whichbcd='ZJets'
tag0='ZJstudy'
TextFormat='.1e'

fin=ROOT.TFile(outdir+'/'+whichbcd+"_shape_correction_2d.root")
h2_AB_shape=fin.Get(tag0+'_regA_shiftB')
h2_AD_shape=fin.Get(tag0+'_regA_shiftD')
h2_AC_shape=fin.Get(tag0+'_regA_shiftC')

h2_A_shape=fin.Get(tag0+'_regA')
h2_B_shape=fin.Get(tag0+'_regB')
h2_D_shape=fin.Get(tag0+'_regD')
h2_C_shape=fin.Get(tag0+'_regC')

histo=[h2_AB_shape,h2_AD_shape,h2_AC_shape,h2_A_shape,h2_B_shape,h2_D_shape,h2_C_shape]

ROOT.gROOT.ProcessLine('.x ../tdrstyle.C')
ROOT.gStyle.SetPadBottomMargin(0.12)
ROOT.gStyle.SetPadLeftMargin(0.12)
ROOT.gStyle.SetPadRightMargin(0.12)
ROOT.gStyle.SetTitleXOffset(0.5)
ROOT.gStyle.SetTitleYOffset(0.5)
ROOT.gStyle.SetMarkerSize(2)
ROOT.gStyle.SetPaintTextFormat(TextFormat) # draw text format
ROOT.gStyle.SetPalette(ROOT.kBeach) # clair color for text printing
c1=ROOT.TCanvas("c1","c1",1)
    
for h2 in histo:
    c1.Clear()
    h2.Draw("colz1, text")
    #h2.GetXaxis().SetTickLength(0);
    c1.SaveAs(outdir+'/'+h2.GetName()+".pdf")
    c1.Clear()
