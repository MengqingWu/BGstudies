#!/usr/bin/env python
import ROOT, os, sys
from math import *
from collections import OrderedDict

sys.path.append('/Users/mengqing/work/local_xzz2l2nu/python')
from SetCuts import SetCuts
from InitializePlotter import InitializePlotter

Channel=raw_input("Please choose a channel (el, mu or both, default both): \n")
if Channel=='el': channelCut='(abs(llnunu_l1_l1_pdgId)==11)'
elif Channel=='mu': channelCut='(abs(llnunu_l1_l1_pdgId)==13)'
elif Channel=='both': channelCut=''
else: channelCut=''; print "[Info] invalid Channel input, default 'both' used."

tag0='SRstudy'+'_'+Channel
#outdir='SRstudy/'
outdir='test'
indir="../AnalysisRegion_zjets"
lumi=2.318278305

if not os.path.exists(outdir): os.system('mkdir '+outdir)

tag = tag0+'_'+'test'
outTag=outdir+'/'+tag

var_dic = {1:{'var':'abs(llnunu_deltaPhi-TMath::Pi()/2)', 'nick':'udPhi',
              'title':'#Delta#Phi_{Z,MET} - #pi/2',
              'par':(16, 0, 1.6)},
           2:{'var':'(llnunu_l2_pt*(llnunu_deltaPhi-TMath::Pi()/2)/abs(llnunu_deltaPhi-TMath::Pi()/2)/llnunu_l1_pt)', 'nick':'ptRatio_signed',
              'title':'(+/-)E_{T}^{miss}/p_{T}^{Z}',
              'par':(50, -5, 5)}}

### ----- Initialize (cuts and samples):
mycuts = SetCuts()
#tex_dic = mycuts.Tex_dic
srcuts = mycuts.GetSRCut()
srcuts_dev = OrderedDict({'SR':srcuts,
                          'SR_LepVeto': srcuts+'&&(nlep<3)'})
for key in srcuts_dev:
    print key, srcuts_dev[key]

plotter = InitializePlotter(indir)
Stack = plotter.Stack
        
### ----- Execute (plotting):
ROOT.gROOT.ProcessLine('.x tdrstyle.C')
ROOT.gStyle.SetPadBottomMargin(0.2)
ROOT.gStyle.SetPadLeftMargin(0.15)
#ROOT.TH1.AddDirectory(ROOT.kFALSE) #in this way you could close the TFile after you registe the histograms
yields = OrderedDict()
err = OrderedDict()
histo = OrderedDict()
nan = 0

for cut in srcuts_dev:
    # deltaPhi(Zmumu,MET)
    Stack.drawStack('llnunu_deltaPhi',srcuts_dev[cut],str(lumi*1000),18,0,3.6,titlex='#Delta#Phi^{Z_{#mu,#mu},MET}',units='',output=tag+'llnunu_deltaPhi'+'_'+cut,outDir=outdir)
    
    # MET:
    Stack.drawStack('llnunu_l2_pt',srcuts_dev[cut],str(lumi*1000),25,0,500,titlex='E_{T}^{miss}',units='[GeV]',output=tag+'met_pt'+'_'+cut,outDir=outdir)
    #err[cut]=ROOT.Double(0.0)
    #yields[cut]=h_met.IntegralAndError(0,1+h_met.GetNbinsX(),err[cut])
    # deltaPhi(jet,MET)
    Stack.drawStack('dPhi_jetMet_min',srcuts_dev[cut],str(lumi*1000),18,0,3.6,titlex='#Delta#Phi^{jet,MET}_{min}',units='',output=tag+'dPhi_jetMet_min'+'_'+cut,outDir=outdir)
    #hdPhiJetMet.GetYaxis().SetTitle("Events")

    #histo[cut]=(srcuts_dev[cut],h_met,hdPhiJetMet)
    
print ' -- Yields:    ', yields
print ' -- Stat. Err.:', err

exit(0)
### ----- Finalizing:

# ROOT.TGaxis.SetMaxDigits(3)
# fout = ROOT.TFile(outTag+'.root','recreate')
# canvas = ROOT.TCanvas('c1', 'c1', 600,630)
# canvas.Print(outTag+'.ps[')

# for key in histo:
#     canvas.Clear()
#     pt=ROOT.TPaveText(.05,.1,.95,.8,"brNDC")
#     pt.SetTextSize(0.03)
#     pt.SetTextAlign(12)
#     pt.SetTextFont(42)
#     cutTex=['- '+item for item in histo[key][0].split('&&')]
#     cutTex.insert(0, key+':')
#     y=0.95
#     for tex in cutTex:
#         if ROOT.TString(tex).Contains("(llnunu_l2_pt*(llnunu_deltaPhi-TMath::Pi()/2)"):
#             tex='#splitline{(llnunu_l2_pt*(llnunu_deltaPhi-TMath::Pi()/2)}{/abs(llnunu_deltaPhi-TMath::Pi()/2)/llnunu_l1_pt)>0.4}'
#         pt.AddText(0.02, y , tex)
#         y-=0.065
#     pt.Draw()
#     canvas.Print(outTag+'.ps')
#     canvas.Clear()
#     for ih in range(1, len(histo[key])):
#         canvas.Clear()
#         if ROOT.TString(histo[key][ih].GetName()).Contains("h2"):
#             histo[key][ih].Draw("COLZ")
#             canvas.SetLogz()
#         else:  histo[key][ih].Draw()
#         canvas.Print(outTag+'.ps')
#         histo[key][ih].Write()
#         canvas.Clear()

# canvas.Print(outTag+'.ps]')
# os.system('ps2pdf '+outTag+'.ps '+outTag+'.pdf')    
# fout.Close()


