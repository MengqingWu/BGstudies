#!/usr/bin/env python

import ROOT, os, sys
from math import *
from itertools import combinations, product

from python.SimplePlot import *
from python.SetCuts import SetCuts
from python.InitializePlotter import InitializePlotter

printfile = open('num_out.txt', 'a')

Channel=raw_input("Please choose a channel (el or mu): \n")
lsChannel=[]
if Channel=="": lsChannel=['el', 'mu']
else: lsChannel.append(Channel)

mycuts=SetCuts()

tag0='ZJstudy'
outdir='test'
indir="../zjetsSkim/"
lumi=2.318278305
doprint=True

if not os.path.exists(outdir): os.system('mkdir '+outdir)

tag = tag0+'_'+'test'
outTag=outdir+'/'+tag

#  B | A
# ------- |dphi-pi/2|
#  D | C
#  +- met/pt
tex_dic=mycuts.Tex_dic
whichregion=raw_input("Please choose a benchmarck Region (SR or VR): \n")
lswhichregion=[]
if whichregion=="": lswhichregion=['SR', 'VR']
else: lswhichregion.append(whichregion)

### ----- Initialize (samples):
plotter = InitializePlotter(indir=indir, addData=True)
ZJets = plotter.ZJets
Data = plotter.Data
otherBG = plotter.NonZBG

### ----- Execute (plotting):
comb=[lsChannel, lswhichregion]
print list(product(*comb))

for Channel, whichregion in list(product(*comb)):
    
    cuts=mycuts.abcdCuts(Channel, whichregion)
    cuts_loose=mycuts.abcdCuts(Channel, whichregion, met_cut='40')
    print cuts
    
    ROOT.gROOT.ProcessLine('.x ../src/tdrstyle.C')
    ROOT.gStyle.SetPadBottomMargin(0.2)
    ROOT.gStyle.SetPadLeftMargin(0.15)
    
    #ROOT.TH1.AddDirectory(ROOT.kFALSE) #in this way you could close the TFile after you registe the histograms
    yields={}
    err={}
    err['data']={}
    yields['data']={}
    err['Zjets']={}
    yields['Zjets']={}
    err['non-Zjets']={}
    yields['non-Zjets']={}
    
    nan=0
    #fout = ROOT.TFile(outTag+'.root','recreate')
    
    #canvas = ROOT.TCanvas('c1', 'c1', 600,630)
    #canvas.Print(outTag+'.ps[')
    
    for key in tex_dic:
        # MET (data):
        h_met_dt=Data.drawTH1('met_dt','llnunu_l2_pt',cuts[key],"1",50,0,500,titlex='E_T^{miss}',units='GeV',drawStyle="HIST")
        err['data'][key]=ROOT.Double(0.0)
        yields['data'][key]=h_met_dt.IntegralAndError(0,1+h_met_dt.GetNbinsX(),err['data'][key])
        
        # MET (non-zjets):
        h_met_nonZ=otherBG.drawTH1('met_nonZ','llnunu_l2_pt',cuts[key],str(lumi*1000),50,0,500,titlex='E_T^{miss}',units='GeV',drawStyle="HIST")
        err['non-Zjets'][key]=ROOT.Double(0.0)
        yields['non-Zjets'][key]=h_met_nonZ.IntegralAndError(0,1+h_met_nonZ.GetNbinsX(),err['non-Zjets'][key])
        
        # MET (zjets):
        h_met=ZJets.drawTH1('met_zjets','llnunu_l2_pt',cuts[key],str(lumi*1000),50,0,500,titlex='E_T^{miss}',units='GeV',drawStyle="HIST")
        err['Zjets'][key]=ROOT.Double(0.0)
        yields['Zjets'][key]=h_met.IntegralAndError(0,1+h_met.GetNbinsX(),err['Zjets'][key])
     
    
    print 'yields = ', yields
    print 'err = ', err
    
    ### ----- Execute (print):
    if doprint:
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
    
        
        printfile.write( '*'*40+'\n{:^40}\n'.format(Channel+'channel, '+whichregion))
        printfile.write( '*'*40+'\n{:^40}\n'.format('Scale Factors')+'-'*40+'\n' )# MC stands for Z(ll)+jets only
        printfile.write( ' A/C (MC)   | %5.2f +- %5.2f\n' % (sf['sf_ac_mc'], err_ac))
        printfile.write( ' B/D (MC)   | %5.2f +- %5.2f\n' % (sf['sf_bd_mc'], err_bd))
        printfile.write( ' B/D (data) | %5.2f +- %5.2f +- %5.2f\n' % (sf['sf_bd_dt'], err_bd_dt, sys_bd_dt))
        printfile.write( '*'*40+'\n  separate sys. uncert. of B/D (data) \n'+'-'*40 +'\n')
        printfile.write( 'sys_var_corr| %.2f \nsys_nonZ_sub| %.2f\n' % (sys_sf['sys_var_corr'], sys_sf['sys_nonZ_sub']))
        
        # To print the Zjets MC, closure test and data-driven result in SR:
        zjets_mc=yields['Zjets']['CRc']*yields['Zjets']['CRb']/yields['Zjets']['CRd']
        zjets_mc_err=math.sqrt((yields['Zjets']['CRc']*err_bd)**2 + (err['Zjets']['SR']*yields['Zjets']['CRb']/yields['Zjets']['CRd'])**2 )
    
        C_data=yields['data']['CRc']-yields['non-Zjets']['CRc']
        err_C_data=math.sqrt(err['data']['CRc']**2+err['non-Zjets']['CRc']**2)
        zjets_data=C_data*B_data/D_data
        zjets_data_err=math.sqrt( (C_data*GetError(B_data, D_data))**2+ (err_C_data*B_data/D_data)**2 )
    
        zjets_data_sys=sys_bd_dt*zjets_data # FIXME
        
        printfile.write( '*'*40+'\n{:^40}\n'.format('Z+jets estimation')+'-'*40 +'\n') #'\n Z+jets estimation: \n'
        printfile.write( '          MC| %5.2f +- %5.2f\n' % (yields['Zjets']['SR'], err['Zjets']['SR']))
        printfile.write( 'closure test| %5.2f +- %5.2f\n' % (zjets_mc, zjets_mc_err))
        printfile.write( ' data-driven| %5.2f +- %5.2f +- %5.2f\n' % (zjets_data, zjets_data_err, zjets_data_sys))
        printfile.write( '*'*40+'\n')
    
        # To print the mc and data yields in each region:
        printfile.write( '-'*40+'\n')
        printfile.write( '{:^40}\n'.format('A | C'))
        printfile.write( '{:^40}\n'.format('Zjets %6.2f | %6.2f Zjets' % (yields['Zjets']['SR'], yields['Zjets']['CRc']) ))
        printfile.write( '{:^40}\n'.format('non-Z %6.2f | %6.2f non-Z' % (yields['non-Zjets']['SR'], yields['non-Zjets']['CRc'])))
        printfile.write( '{:^40}\n'.format('data %6.2f | %6.2f data' % (yields['data']['SR'], yields['data']['CRc'])))
        printfile.write( '-'*40+'\n')
        printfile.write( '{:^40}\n'.format('B | D'))
        printfile.write( '{:^40}\n'.format('Zjets %6.2f | %6.2f Zjets' % (yields['Zjets']['CRb'], yields['Zjets']['CRd'])))
        printfile.write( '{:^40}\n'.format('non-Z %6.2f | %6.2f non-Z' % (yields['non-Zjets']['CRb'], yields['non-Zjets']['CRd'])))
        printfile.write( '{:^40}\n'.format('data %6.2f | %6.2f data' % (yields['data']['CRb'], yields['data']['CRd'])))
        printfile.write( '-'*40+'\n')
    
    
printfile.close()
