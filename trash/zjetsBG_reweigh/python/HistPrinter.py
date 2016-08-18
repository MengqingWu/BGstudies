#!/usr/bin/env python
import ROOT, os, sys
from math import *
from collections import OrderedDict

### ----- Finalizing:
def mergePrinter(histo, outTag, drawStyle="HIST"):
    ''' make sure histo is a dictionary in format of:
    histo={'<cutTag1>': (cut1, histo1, histo2 ...),
           '<cutTag2>': (cut2, histo1, histo2 ...)}
    '''
    ROOT.gROOT.ProcessLine('.x ../src/tdrstyle.C')
    ROOT.gStyle.SetPadBottomMargin(0.2)
    ROOT.gStyle.SetPadLeftMargin(0.15)
    
    ROOT.TGaxis.SetMaxDigits(3)
    fout = ROOT.TFile(outTag+'.root','recreate')
    canvas = ROOT.TCanvas('c1', 'c1', 600,630)
    canvas.Print(outTag+'.ps[')
        
    for key in histo:
        canvas.Clear()
        pt=ROOT.TPaveText(.05,.1,.95,.8,"brNDC")
        pt.SetTextSize(0.03)
        pt.SetTextAlign(12)
        pt.SetTextFont(42)
        cutTex=['- '+item for item in histo[key][0].split('&&')]
        cutTex.insert(0, key+':')
        y=0.95
        for tex in cutTex:
            if ROOT.TString(tex).Contains("(nunu_l2_pt*(abs(llnunu_deltaPhi)-TMath::Pi()/2)"):
                tex='(+/-) E_{T}^{miss}/p_{T}^{Z}'
            pt.AddText(0.02, y , tex)
            y-=0.065
        pt.Draw()
        canvas.Print(outTag+'.ps')
        canvas.Clear()
        for ih in range(1, len(histo[key])):
            canvas.Clear()
            if ROOT.TString(histo[key][ih].GetName()).Contains("h2"):
                histo[key][ih].Draw("COLZ")
                canvas.SetLogz()
            else:  histo[key][ih].Draw(drawStyle)
            canvas.Print(outTag+'.ps')
            histo[key][ih].Write()
            canvas.Clear()
    
    canvas.Print(outTag+'.ps]')
    os.system('ps2pdf '+outTag+'.ps '+outTag+'.pdf')    
    fout.Close()
    


def printCut(cuttag, cuttex, canvas, outtag):
    canvas.Clear()
    pt=ROOT.TPaveText(.05,.1,.95,.8,"brNDC")
    pt.SetTextSize(0.03)
    pt.SetTextAlign(12)
    pt.SetTextFont(42)
    
    cutTex=['- '+item for item in cuttex.split('&&')]
    cutTex.insert(0, cuttag+':')
    
    y=0.95
    for tex in cutTex:
        if ROOT.TString(tex).Contains("(llnunu_l2_pt*(abs(llnunu_deltaPhi)-TMath::Pi()/2)"):
            tex='#splitline{(llnunu_l2_pt*(abs(llnunu_deltaPhi)-TMath::Pi()/2)}{/abs(abs(llnunu_deltaPhi)-TMath::Pi()/2)/llnunu_l1_pt)>0.4}'
        pt.AddText(0.02, y , tex)
        y-=0.065
            
    canas.cd()
    pt.Draw()
    canvas.Print(outtag+'.ps')
    canvas.Clear()
        
