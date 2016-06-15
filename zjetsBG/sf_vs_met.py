#!/usr/bin/env python
import ROOT,os,sys
from math import *
import numpy as np
#sys.path.append('/Users/mengqing/work/local_xzz2l2nu/python')
from python.SetCuts import SetCuts
from python.InitializePlotter import InitializePlotter
from python.SimplePlot import *

tag0='sf_vs_met'
tag = tag0+'_'+'test'
outdir='sfvsMet/'
indir="../../AnalysisRegion"
lumi=2.3182783052

if not os.path.exists(outdir): os.system('mkdir '+outdir)

#met_pt=np.arange(30,150,5).tolist()

### ----- Initialize (samples):
plotter_ll=InitializePlotter(addSig=False, addData=True,doRatio=False, indir=indir)
#plotter_eu=InitializePlotter(addSig=False, addData=True,doRatio=False, doElMu=True)
setcuts=SetCuts()
# print "I am cuts_ll:"
# cuts_ll=setcuts.alphaCuts(Zmass='inclusive')
# print "I am cuts_eu:"
# cuts_eu=setcuts.alphaCuts(isll=False, Zmass='inclusive')
# ROOT.gROOT.ProcessLine('.x tdrstyle.C')

channel = raw_input("[info] 'sf_vs_met.py' -> Please choose el/mu channel (el or mu, default mu): \n")
if channel=='':
    channel='mu'
cuts_met0=setcuts.abcdCuts(channel, 'SR', met_cut='0')

fout = ROOT.TFile(outdir+tag+"_"+channel+'.root','recreate')
histo={}
for key in cuts_met0:
    # MET (data):
    h_met_dt=plotter_ll.Data.drawTH1('h_met_dt'+key,'llnunu_l2_pt',cuts_met0[key],"1",24,30,150,titlex='E_T^{miss}',units='GeV',drawStyle="HIST")
    # MET (non-zjets):
    h_met_nonZ=plotter_ll.NonZBG.drawTH1('h_met_nonZ'+key,'llnunu_l2_pt',cuts_met0[key],str(lumi*1000),24,30,150,titlex='E_T^{miss}',units='GeV',drawStyle="HIST")
    # MET (zjets):
    h_met=plotter_ll.ZJets.drawTH1('h_met'+key,'llnunu_l2_pt',cuts_met0[key],str(lumi*1000),24,30,150,titlex='E_T^{miss}',units='GeV',drawStyle="HIST")
    
    h_met_dt.Add(h_met_nonZ,-1)
    
    fout.cd()
    h_met_dt.Write()
    h_met_nonZ.Write()
    h_met.Write()

    histo[key]={'h_met_dt':GetCumulative_dev(h_met_dt,forward=False,suffix='cumulative'),
                #'h_met_dt':h_met_dt.GetCumulative(ROOT.kFALSE),
                #'h_met_nonZ':h_met_nonZ.GetCumulative(),
                'h_met':GetCumulative_dev(h_met,forward=False,suffix='cumulative')}
    for ihist in histo[key]: 
        histo[key][ihist].Write()
    

### ----- Execute (plotting):
#h_sfVSmet_ac=ROOT.TH1F("h_sfVSmet_ac","MC sf vs met; E_{T}^{miss} [GeV]; N_{A}^{mc}/N_{C}^{mc}",24, 30, 150)
#h_sfVSmet_bd_mc=ROOT.TH1F("h_sfVSmet_bd_mc","MC sf vs met; E_{T}^{miss} [GeV]; N_{B}^{mc}/N_{D}^{mc}",24, 30, 150)
#h_sfVSmet_bd_dt=ROOT.TH1F("h_sfVSmet_bd_mc","data sf vs met; E_{T}^{miss} [GeV]; N_{B}^{data}/N_{D}^{data}",24, 30, 150)

h_sfVSmet_ac=histo['SR']['h_met'].Clone("h_sfVSmet_ac")
h_sfVSmet_ac.Divide(histo['CRc']['h_met'])
h_sfVSmet_bd_mc=histo['CRb']['h_met'].Clone("h_sfVSmet_bd_mc")
h_sfVSmet_bd_mc.Divide(histo['CRd']['h_met'])
h_sfVSmet_bd_dt=histo['CRb']['h_met_dt'].Clone("h_sfVSmet_bd_dt")
h_sfVSmet_bd_dt.Divide(histo['CRd']['h_met_dt'])

ROOT.TH1.AddDirectory(ROOT.kFALSE)
ROOT.gROOT.ProcessLine('.x tdrstyle.C')

    
### ----- Finalizing:
#fout = ROOT.TFile(outdir+tag+"_"+channel+'.root','recreate')
fout.cd()
h_sfVSmet_ac.Write()
h_sfVSmet_ac.Print("all")
h_sfVSmet_bd_mc.Write()
h_sfVSmet_bd_dt.Write()

c1=ROOT.TCanvas(1)
h_sfVSmet_ac.SetMarkerStyle(20)
h_sfVSmet_ac.SetMarkerSize(1.0)
h_sfVSmet_ac.Draw("p")
c1.SaveAs(outdir+"h_sfVSmet_ac_"+channel+".eps")
c1.Clear()

h_sfVSmet_bd_mc.SetMarkerStyle(20)
h_sfVSmet_bd_mc.SetMarkerSize(1.0)
h_sfVSmet_bd_mc.Draw("p")
c1.SaveAs(outdir+"h_sfVSmet_bd_mc_"+channel+".eps")
c1.Clear()

h_sfVSmet_bd_dt.SetMarkerStyle(20)
h_sfVSmet_bd_dt.SetMarkerSize(1.0)
h_sfVSmet_bd_dt.Draw("p")
c1.SaveAs(outdir+"h_sfVSmet_bd_dt_"+channel+".eps")

fout.Print()
fout.Close()

exit(0)



