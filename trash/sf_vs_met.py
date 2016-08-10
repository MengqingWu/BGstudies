#!/usr/bin/env python
import ROOT,os
from math import *
import numpy as np
from python.SetCuts import SetCuts
from python.InitializePlotter import InitializePlotter
from python.SimplePlot import *

tag0='sf_vs_met'
tag = tag0+'_'+'test'
outdir='sfvsMet1/'
indir="../AnalysisRegion"
lumi=2.318278305

if not os.path.exists(outdir): os.system('mkdir '+outdir)

met_pt=np.arange(30,150,5).tolist()

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
    h_met_dt=plotter_ll.Data.drawTH1('h_met_dt','llnunu_l2_pt',cuts_met0[key],"1",100,0,500,titlex='E_T^{miss}',units='GeV',drawStyle="HIST")
    #h_met_dt.Write()
    # MET (non-zjets):
    h_met_nonZ=plotter_ll.NonZBG.drawTH1('h_met_nonZ','llnunu_l2_pt',cuts_met0[key],str(lumi*1000),100,0,500,titlex='E_T^{miss}',units='GeV',drawStyle="HIST")
    #h_met_nonZ.Write()
    # MET (zjets):
    h_met=plotter_ll.ZJets.drawTH1('h_met','llnunu_l2_pt',cuts_met0[key],str(lumi*1000),100,0,500,titlex='E_T^{miss}',units='GeV',drawStyle="HIST")
    #h_met.Write()
    histo[key]={'h_met_dt':h_met_dt,
                'h_met_nonZ':h_met_nonZ,
                'h_met':h_met}
                
### ----- Execute (plotting):
h_sfVSmet_ac=ROOT.TH1F("h_sfVSmet_ac","MC sf vs met; E_{T}^{miss} [GeV]; N_{A}^{mc}/N_{C}^{mc}",24, 30, 150)
h_sfVSmet_bd_mc=ROOT.TH1F("h_sfVSmet_bd_mc","MC sf vs met; E_{T}^{miss} [GeV]; N_{B}^{mc}/N_{D}^{mc}",24, 30, 150)
h_sfVSmet_bd_dt=ROOT.TH1F("h_sfVSmet_bd_mc","data sf vs met; E_{T}^{miss} [GeV]; N_{B}^{data}/N_{D}^{data}",24, 30, 150)

ROOT.TH1.AddDirectory(ROOT.kFALSE)
ROOT.gROOT.ProcessLine('.x tdrstyle.C')
for metcut in met_pt:
    cuts_abcd = setcuts.abcdCuts('mu', 'SR', met_cut=str(metcut))

    yields={}
    err={}
    err['data']={}; 
    yields['data']={}
    err['Zjets']={}
    yields['Zjets']={}
    err['non-Zjets']={}
    yields['non-Zjets']={}

    whichBin=0
    for ib in range(0,histo['SR']['h_met_dt'].GetNbinsX()):
        if h_met_dt.GetBinCenter(ib)==metcut+2.5 :
            whichBin=ib
            break

    for key in cuts_abcd:
        err['data'][key]=ROOT.Double(0.0)
        yields['data'][key]=histo[key]['h_met_dt'].IntegralAndError(whichBin, 1+h_met_dt.GetNbinsX(),err['data'][key])
        err['non-Zjets'][key]=ROOT.Double(0.0)
        yields['non-Zjets'][key]=histo[key]['h_met_nonZ'].IntegralAndError(whichBin, 1+h_met_nonZ.GetNbinsX(),err['non-Zjets'][key])
        err['Zjets'][key]=ROOT.Double(0.0)
        yields['Zjets'][key]=histo[key]['h_met'].IntegralAndError(whichBin, 1+h_met.GetNbinsX(),err['Zjets'][key])

    err_ac=GetError(yields['Zjets']['SR'], yields['Zjets']['CRc'], err['Zjets']['SR'], err['Zjets']['CRc'])
    err_bd=GetError(yields['Zjets']['CRb'], yields['Zjets']['CRd'], err['Zjets']['CRb'], err['Zjets']['CRd'])
    
    B_data=yields['data']['CRb']-yields['non-Zjets']['CRb']
    D_data=yields['data']['CRd']-yields['non-Zjets']['CRd']
    err_B_data=math.sqrt(err['data']['CRb']**2+err['non-Zjets']['CRb']**2)
    err_D_data=math.sqrt(err['data']['CRd']**2+err['non-Zjets']['CRd']**2)
    err_bd_dt=GetError(B_data, D_data, err_B_data, err_D_data)
    
    sf={}
    sf['sf_ac_mc']=yields['Zjets']['SR']/yields['Zjets']['CRc']
    sf['sf_bd_mc']=yields['Zjets']['CRb']/yields['Zjets']['CRd']
    sf['sf_bd_dt']=B_data/D_data
    sys_sf={}
    sys_sf['sys_var_corr']=abs(sf['sf_ac_mc']-sf['sf_bd_mc'])/(sf['sf_ac_mc']+sf['sf_bd_mc'])
    sys_sf['sys_nonZ_sub']=abs(sf['sf_bd_mc']-sf['sf_bd_dt'])/(sf['sf_bd_mc']+sf['sf_bd_dt'])
    sys_bd_dt=math.sqrt(sys_sf['sys_var_corr']**2+sys_sf['sys_nonZ_sub']**2)

    outBin=0
    for iob in range(0,h_sfVSmet_ac.GetNbinsX()):
        if h_met_dt.GetBinCenter(iob)==metcut+2.5 :
            outBin=iob
            break
            
    h_sfVSmet_ac.Fill(metcut, sf['sf_ac_mc'])
    h_sfVSmet_ac.SetBinError(outBin,err_ac)
    
    h_sfVSmet_bd_mc.Fill(metcut, sf['sf_bd_mc'])
    h_sfVSmet_bd_mc.SetBinError(outBin,err_bd)
    
    h_sfVSmet_bd_dt.Fill(metcut, sf['sf_bd_dt'])
    h_sfVSmet_bd_dt.SetBinError(outBin,err_bd_dt)

    
### ----- Finalizing:
#fout = ROOT.TFile(outdir+tag+"_"+channel+'.root','recreate')
fout.cd()
h_sfVSmet_ac.Write()
#h_sfVSmet_ac.Print("all")
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



