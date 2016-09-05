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
if Channel=="": 
    print "[info] default to use inclusive (el+mu)"
    lsChannel=['el', 'mu']
else: lsChannel.append(Channel)

mycuts=SetCuts()

tag0='ZJstudy'
outdir='test'
indir="./inds/"
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
plotter = InitializePlotter(indir=indir, addData=True, doMetCorr=True)
ZJets = plotter.ZJets
Data = plotter.Data
otherBG = plotter.NonZBG

### ----- Execute (plotting):
comb=[lsChannel, lswhichregion]
print list(product(*comb))

for Channel, whichregion in list(product(*comb)):
    
    cuts=mycuts.abcdCuts(Channel, whichregion, zpt_cut='100', met_cut='50')
    #cuts_loose=mycuts.abcdCuts(Channel, whichregion, met_cut='50')
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
        err_ac=GetError(yields['Zjets']['regA'], yields['Zjets']['regC'], err['Zjets']['regA'], err['Zjets']['regC'])
        err_bd=GetError(yields['Zjets']['regB'], yields['Zjets']['regD'], err['Zjets']['regB'], err['Zjets']['regD'])
        
        B_data=yields['data']['regB']-yields['non-Zjets']['regB']
        D_data=yields['data']['regD']-yields['non-Zjets']['regD']
        err_B_data=math.sqrt(err['data']['regB']**2+err['non-Zjets']['regB']**2)
        err_D_data=math.sqrt(err['data']['regD']**2+err['non-Zjets']['regD']**2)
        err_bd_dt=GetError(B_data, D_data, err_B_data, err_D_data)
    
        sf={}
        sf['sf_ac_mc']=yields['Zjets']['regA']/yields['Zjets']['regC']
        sf['sf_bd_mc']=yields['Zjets']['regB']/yields['Zjets']['regD']
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
        zjets_mc=yields['Zjets']['regC']*yields['Zjets']['regB']/yields['Zjets']['regD']
        zjets_mc_err=math.sqrt((yields['Zjets']['regC']*err_bd)**2 + (err['Zjets']['regA']*yields['Zjets']['regB']/yields['Zjets']['regD'])**2 )
    
        C_data=yields['data']['regC']-yields['non-Zjets']['regC']
        err_C_data=math.sqrt(err['data']['regC']**2+err['non-Zjets']['regC']**2)
        zjets_data=C_data*B_data/D_data
        zjets_data_err=math.sqrt( (C_data*GetError(B_data, D_data))**2+ (err_C_data*B_data/D_data)**2 )
    
        zjets_data_sys=sys_bd_dt*zjets_data # FIXME
        
        printfile.write( '*'*40+'\n{:^40}\n'.format('Z+jets estimation')+'-'*40 +'\n') #'\n Z+jets estimation: \n'
        printfile.write( '          MC| %5.2f +- %5.2f\n' % (yields['Zjets']['regA'], err['Zjets']['regA']))
        printfile.write( 'closure test| %5.2f +- %5.2f\n' % (zjets_mc, zjets_mc_err))
        printfile.write( ' data-driven| %5.2f +- %5.2f +- %5.2f\n' % (zjets_data, zjets_data_err, zjets_data_sys))
        printfile.write( '*'*40+'\n')
    
        # To print the mc and data yields in each region:
        printfile.write( '-'*40+'\n')
        printfile.write( '{:^40}\n'.format('A | C'))
        printfile.write( '{:^40}\n'.format('Zjets %6.2f | %6.2f Zjets' % (yields['Zjets']['regA'], yields['Zjets']['regC']) ))
        printfile.write( '{:^40}\n'.format('non-Z %6.2f | %6.2f non-Z' % (yields['non-Zjets']['regA'], yields['non-Zjets']['regC'])))
        printfile.write( '{:^40}\n'.format('data %6.2f | %6.2f data' % (yields['data']['regA'], yields['data']['regC'])))
        printfile.write( '-'*40+'\n')
        printfile.write( '{:^40}\n'.format('B | D'))
        printfile.write( '{:^40}\n'.format('Zjets %6.2f | %6.2f Zjets' % (yields['Zjets']['regB'], yields['Zjets']['regD'])))
        printfile.write( '{:^40}\n'.format('non-Z %6.2f | %6.2f non-Z' % (yields['non-Zjets']['regB'], yields['non-Zjets']['regD'])))
        printfile.write( '{:^40}\n'.format('data %6.2f | %6.2f data' % (yields['data']['regB'], yields['data']['regD'])))
        printfile.write( '-'*40+'\n')
    
    
printfile.close()
