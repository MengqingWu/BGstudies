#!/usr/bin/env python
import ROOT, os, sys
#sys.path.append('/Users/mengqing/work/local_xzz2l2nu/python')
from python.TreePlotter import TreePlotter
from python.MergedPlotter import MergedPlotter
from python.SimplePlot import *

outdir='./plots/aux'
indir="../../AnalysisRegion"
#lumi=2.318278305
if not os.path.exists(outdir): os.system('mkdir '+outdir)

var_dic = {1:{'var':'abs(llnunu_deltaPhi-TMath::Pi()/2)', 'nick':'udPhi',
              'title':'#Delta#Phi_{Z,MET} - #pi/2',
              'par':(16, 0, 1.6)},
           2:{'var':'(llnunu_l2_pt*(llnunu_deltaPhi-TMath::Pi()/2)/abs(llnunu_deltaPhi-TMath::Pi()/2)/llnunu_l1_pt)', 'nick':'ptRatio_signed',
              'title':'(+/-)E_{T}^{miss}/p_{T}^{Z}',
              'par':(50, -5, 5)}}

fout=outdir+'/CorrFactor_'+var_dic[1]['nick']+'_'+var_dic[2]['nick']+'.txt'
outtxt = open(fout, 'a')

if os.stat(fout).st_size == 0:
    outtxt.write(" GetCorrelationFactor( "+var_dic[1]['var']+' : '+var_dic[2]['var']+" ) \n" )
    sout="{0:>6}, {1:>6}, {2:>20}, {3:>20}, {4:>20}\n"
    outtxt.write(sout.format("ZpT", "MET", "inclusive", "mu", "electron"))
else: pass

Channel=raw_input("Please choose a channel (inclusive, el or mu; print ALL if no input ): \n")
pdgID={'el':'11','mu':'13'}
if Channel=="": print "[info] all 3 channels will be plotted."

kincut=raw_input("Please choose ZpT (preselected at 100GeV) > a and met (preselected at 0) > b cuts (no cut applied if you skip): \n a,b = ")
ZpTCut='&&llnunu_l1_pt>'+kincut.split(',')[0]  if kincut.split(',')[0] else ''
MetCut='&&met_pt>'+kincut.split(',')[1]  if kincut.split(',')[1] else ''
#outtxt.write('[NEW] %s %s %s' % (ZpTCut,MetCut,'*'*20))# use for debug


#######----------- Prepare samples to plot:
zjetsPlotters=[]
zjetsSamples = ['DYJetsToLL_M50_BIG'] # M50_BIG = M50 + M50_Ext

for sample in zjetsSamples:
    zjetsPlotters.append(TreePlotter(indir+'/'+sample+'.root','tree'))
    #zjetsPlotters[-1].addCorrectionFactor('1./SumWeights','tree') # refers to sum of genWeight
    # zjetsPlotters[-1].addCorrectionFactor('xsec','tree')
    # zjetsPlotters[-1].addCorrectionFactor('(1921.8*3)','xsec')
    zjetsPlotters[-1].addCorrectionFactor('(genWeight/abs(genWeight))','tree') # to keep the sign but not the value 
    zjetsPlotters[-1].addCorrectionFactor('puWeight','tree')
    zjetsPlotters[-1].addCorrectionFactor('triggersf','tree')
    zjetsPlotters[-1].addCorrectionFactor('llnunu_l1_l1_lepsf*llnunu_l1_l2_lepsf','tree')
        
ZJets = MergedPlotter(zjetsPlotters)
ZJets.setFillProperties(1001,ROOT.kGreen+2)
    
#######----------- Start Plotting:

lsChannel=[]
if Channel=="": lsChannel=['inclusive','el','mu']
else: lsChannel.append(Channel)

res=dict()
for Channel in lsChannel:
    print "[info] ", Channel, '*'*20
    ROOT.gROOT.ProcessLine('.x ../src/tdrstyle.C')

    if Channel=='inclusive':
        factor_cuts='(nllnunu>0&&abs(llnunu_l1_mass-91.1876)<20.0'+ZpTCut+MetCut+')'
    else:
        factor_cuts='(nllnunu>0&&abs(llnunu_l1_mass-91.1876)<20.0&&abs(llnunu_l1_l1_pdgId)=='+pdgID[Channel]+ZpTCut+MetCut+')'
        
        
    print '[info] cuts used here: ', factor_cuts

    h2_var1_var2 = ZJets.drawTH2(var_dic[1]['var']+':'+var_dic[2]['var'],factor_cuts,str(1), #lumi*1000 
                                 var_dic[2]['par'][0], var_dic[2]['par'][1], var_dic[2]['par'][2],
                                 var_dic[1]['par'][0], var_dic[1]['par'][1], var_dic[1]['par'][2],
                                 titlex = var_dic[2]['title'], unitsx = "",
                                 titley = var_dic[1]['title'], unitsy = "",
                                 drawStyle = "COLZ")

    ROOT.gStyle.SetPadBottomMargin(0.15);
    ROOT.gStyle.SetPadLeftMargin(0.15);
    ROOT.gStyle.SetPadRightMargin(0.12);
    ROOT.gStyle.SetTitleXOffset(0.5);
    ROOT.gStyle.SetTitleYOffset(0.5);

    c1=ROOT.TCanvas("c1","c1",1)
    h2_var1_var2.Draw("COLZ")
    #print h2_var1_var2.GetEntries(), h2_var1_var2.GetSumOfWeights()
    
    print "%s:%s, correlation factor r = %.5f +- %.5f" %( var_dic[1]['var'], var_dic[2]['var'], h2_var1_var2.GetCorrelationFactor(), GetCorrelationFactorError(h2_var1_var2.GetCorrelationFactor(), h2_var1_var2.GetSumOfWeights()))
    
    res[Channel]=("%.5f +- %.5f" % ( h2_var1_var2.GetCorrelationFactor(), GetCorrelationFactorError(h2_var1_var2.GetCorrelationFactor(), h2_var1_var2.GetSumOfWeights())))
    
    c1.SaveAs(outdir+"/h2_"+var_dic[1]['nick']+'_'+var_dic[2]['nick']+Channel+'_'+kincut.split(',')[0]+'_'+kincut.split(',')[1]+".eps")
    c1.Clear()
    
print res
sout2="{inclusive:>20}, {mu:>20}, {el:>20}\n"
outtxt.write("{0:>6}, {1:>6}, ".format(*kincut.split(','))+sout2.format(**res))

