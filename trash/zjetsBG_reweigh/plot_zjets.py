#!/usr/bin/env python
import ROOT, os, sys
from math import *
from collections import OrderedDict
#sys.path.append('/Users/mengqing/work/local_xzz2l2nu/bkgStudies/python')
from python.SetCuts import SetCuts
from python.InitializePlotter import InitializePlotter

channel=raw_input("Please choose a channel (el or mu, default mu): \n")
Channel=channel if channel else 'mu'
region=raw_input("Please choose a benchmarck Region (SR or VR, default SR): \n")
Region=region if region else 'SR'
indir="../zjetsSkim/"
outdir='./plots/Kin/'
if not os.path.exists(outdir): os.system('mkdir '+outdir)

lumi=2.318278305
zpt_cut, met_cut ='100', '100'

tag0='ZJstudy'+'_'+Channel+'_'+Region
tags=[]
for itag in [tag0, tag0+'_Bulk1000']:
    itag = outdir+ '/'+ itag + '_'+'zpt'+zpt_cut+'met'+met_cut
    tags.append(itag)

#  A | C
# ------- sin(Dphi(Z,MET)) = 1.5
#  B | D
# +/- 1(met/pt) = 0.4
var_dic = {1:{'var':'abs(abs(llnunu_deltaPhi)-TMath::Pi()/2)',
              'nick':'udPhi',
              'title':'||#Delta#Phi_{Z,MET}| - #pi/2|',
              'par':(16, 0, 1.6)},
           2:{'var':'(llnunu_l2_pt*(abs(llnunu_deltaPhi)-TMath::Pi()/2)/abs(abs(llnunu_deltaPhi)-TMath::Pi()/2)/llnunu_l1_pt)',
              'nick':'ptRatio_signed',
              'title':'(+/-)E_{T}^{miss}/p_{T}^{Z}',
              'par':(50, -5, 5)}}

### ----- Initialize (cuts and samples):
Plotters = InitializePlotter(indir,addSig=True, addData=True)
plotters = [(Plotters.ZJets, tags[0]), 
            (Plotters.sigPlotters[1], tags[1])]
#ZJets = plotter.ZJets
#ZJets=plotter.sigPlotters[1]

mycuts = SetCuts()
#tex_dic = mycuts.Tex_dic
cuts = mycuts.abcdCuts(Channel, Region)
preSelect = mycuts.abcdCuts(Channel, Region, isPreSelect=True, zpt_cut=zpt_cut, met_cut=met_cut)
preCuts = OrderedDict({'preSelect':  preSelect,
                       'preSelect_dphiJMet2': preSelect+'&&(dPhi_jetMet_min>0.2)',
                       'preSelect_dphiJMet2a': preSelect+'&&(dPhi_jetMet_min_a>0.2)',
                       'preSelect_dphiJMet2b': preSelect+'&&(dPhi_jetMet_min_b>0.2)',
                       'preSelect_dphiJMet4': preSelect+'&&(dPhi_jetMet_min>0.4)',
                       'preSelect_dphiJMet4a': preSelect+'&&(dPhi_jetMet_min_a>0.4)',
                       'preSelect_dphiJMet4b': preSelect+'&&(dPhi_jetMet_min_b>0.4)',
                       'preSelect_dphiJMet2a_plus7': preSelect+'&&(dPhi_jetMet_min_a>0.2)&&(llnunu_l1_pt/llnunu_mtc<0.7)',
                       'preSelect_dphiJMet2a_plus8': preSelect+'&&(dPhi_jetMet_min_a>0.2)&&(llnunu_l1_pt/llnunu_mtc<0.8)',
                       'preSelect_dphiJMet4a_plus7': preSelect+'&&(dPhi_jetMet_min_a>0.4)&&(llnunu_l1_pt/llnunu_mtc<0.7)',
                       'preSelect_dphiJMet4a_plus8': preSelect+'&&(dPhi_jetMet_min_a>0.4)&&(llnunu_l1_pt/llnunu_mtc<0.8)',
                       'preSelect_dphiJMet4b_plus7': preSelect+'&&(dPhi_jetMet_min_b>0.4)&&(llnunu_l1_pt/llnunu_mtc<0.7)',
                       'preSelect_dphiJMet4b_plus8': preSelect+'&&(dPhi_jetMet_min_b>0.4)&&(llnunu_l1_pt/llnunu_mtc<0.8)',
                       })
for key in cuts:
    print key, cuts[key]
        
### ----- Execute (plotting):
ROOT.gROOT.ProcessLine('.x ../src/tdrstyle.C')
ROOT.gStyle.SetPadBottomMargin(0.2)
ROOT.gStyle.SetPadLeftMargin(0.15)

for pair in plotters: 
    yields = {}
    err = {}
    histo = OrderedDict()
    nan = 0
    plotter, outTag = pair[0], pair[1]

    for pcut in preCuts:
        # deltaPhi(Zmumu,MET)
        hdPhiZmmMet=plotter.drawTH1('llnunu_deltaPhi'+'_'+pcut,'abs(llnunu_deltaPhi)',preCuts[pcut],str(lumi*1000),18,0,3.6,titlex='|#Delta#Phi^{Z_{#mu,#mu},MET}|',units='',drawStyle="HIST")
        hdPhiZmmMet.GetYaxis().SetTitle("Events")
        h2_var1_var2 = plotter.drawTH2('h2'+var_dic[1]['nick']+'_'+var_dic[2]['nick']+'_'+pcut,
                                     var_dic[1]['var']+':'+var_dic[2]['var'],
                                     preCuts[pcut],
                                     str(1), #lumi*1000 for data
                                     var_dic[2]['par'][0], var_dic[2]['par'][1], var_dic[2]['par'][2],
                                     var_dic[1]['par'][0], var_dic[1]['par'][1], var_dic[1]['par'][2],
                                     titlex = var_dic[2]['title'], unitsx = "",
                                     titley = var_dic[1]['title'], unitsy = "",
                                     drawStyle = "COLZ")
        if pcut=='preSelect':
            hmet_preselect=plotter.drawTH1('llnunu_l2_pt'+'_'+pcut,'llnunu_l2_pt',preCuts[pcut],str(lumi*1000),25,0,500,titlex='E_{T}^{miss}',units='[GeV]',drawStyle="HIST")
            hzpt_preselect=plotter.drawTH1('llnunu_l1_pt'+'_'+pcut,'llnunu_l1_pt',preCuts[pcut],str(lumi*1000),25,0,500,titlex='p_{T}^{Z}',units='[GeV]',drawStyle="HIST")
            histo[pcut]=(preCuts[pcut],hmet_preselect, hzpt_preselect, hdPhiZmmMet, h2_var1_var2)
        else:
            histo[pcut]=(preCuts[pcut],hdPhiZmmMet, h2_var1_var2)
        
    for cut in cuts:
        # MET:
        h_met=plotter.drawTH1('llnunu_l2_pt'+'_'+cut,'llnunu_l2_pt',cuts[cut],str(lumi*1000),25,0,500,titlex='E_{T}^{miss}',units='[GeV]',drawStyle="HIST")
        err[cut]=ROOT.Double(0.0)
        yields[cut]=h_met.IntegralAndError(0,1+h_met.GetNbinsX(),err[cut])
        # MT:
        h_mt=plotter.drawTH1('llnunu_mtc'+'_'+cut,'llnunu_mtc',cuts[cut],str(lumi*1000),60,0,1200,titlex='M_{T}^{ZZ}',units='[GeV]',drawStyle="HIST")
        h_mt.GetYaxis().SetTitle("/"+'{:.2f}'.format(lumi)+"fb^{-1}")
        # deltaPhi(jet,MET)
        hdPhiJetMet=plotter.drawTH1('dPhi_jetMet_min_a'+'_'+cut,'dPhi_jetMet_min_a',cuts[cut],str(lumi*1000),18,0,3.6,titlex='#Delta#Phi^{looseJet,MET}_{min}',units='',drawStyle="HIST")
        hdPhiJetMet.GetYaxis().SetTitle("/"+'{:.2f}'.format(lumi)+"fb^{-1}")
    
        histo[cut]=(cuts[cut], h_met, h_mt, hdPhiJetMet)
        
    print ' -- Yields:    ', yields
    print ' -- Stat. Err.:', err
    
    ### ----- Finalizing:
    
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
            if ROOT.TString(tex).Contains("(llnunu_l2_pt*(abs(llnunu_deltaPhi)-TMath::Pi()/2)"):
                tex='#splitline{(llnunu_l2_pt*(abs(llnunu_deltaPhi)-TMath::Pi()/2)}{/abs(abs(llnunu_deltaPhi)-TMath::Pi()/2)/llnunu_l1_pt)>0.4}'
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
            else:  histo[key][ih].Draw()
            canvas.Print(outTag+'.ps')
            histo[key][ih].Write()
            canvas.Clear()
    
    canvas.Print(outTag+'.ps]')
    os.system('ps2pdf '+outTag+'.ps '+outTag+'.pdf')    
    fout.Close()
    

