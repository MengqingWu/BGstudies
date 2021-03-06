#!/usr/bin/env python

import ROOT
import os
from math import *
from itertools import combinations, product
from python.TreePlotter import TreePlotter
from python.MergedPlotter import MergedPlotter
from python.StackPlotter import StackPlotter
from python.SimplePlot import *
from python.SetCuts import SetCuts
from python.InitializePlotter import InitializePlotter

printfile = open('num_nonRes.txt', 'a')

Channel=raw_input("Please choose a channel (el or mu): \n")
lsChannel=[]
if Channel=="": lsChannel=['el', 'mu']
else: lsChannel.append(Channel)

tag0='nonResStudy'
outdir='test'
indir="../../AnalysisRegion_nonRes"
lumi=2.318278305
doprint=False

if not os.path.exists(outdir): os.system('mkdir '+outdir)

tag = tag0+'_'+'test'
outTag=outdir+'/'+tag

whichregion=raw_input("Please choose a benchmarck Region (SR or VR): \n")
lswhichregion=[]
if whichregion=="": lswhichregion=['SR', 'VR']
else: lswhichregion.append(whichregion)

#  ll in Z | ll out Z
# --------------------  M_out [35,65] U [115,120]
#  eu in Z | eu out Z
#  M_in (70,110)

### ----- Initialize (samples):

plotter_ll=InitializePlotter(addSig=False, addData=False,doRatio=False)
plotter_eu=InitializePlotter(addSig=False, addData=False,doRatio=False, doElMu=True)
setcuts=SetCuts()
print "I am cuts_ll:"
cuts_ll=setcuts.alphaCuts(inclusive=True)
print "I am cuts_eu:"
cuts_eu=setcuts.alphaCuts(isll=False, inclusive=True)

exit(0)
### ----- Execute (plotting):
print product(lsChannel, lswhichregion)

for Channel, whichregion in product(lsChannel, lswhichregion):
    
    cuts=mycuts.abcdCuts(Channel, whichregion)
    print cuts
    
    ROOT.gROOT.ProcessLine('.x tdrstyle.C')
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
    fout = ROOT.TFile(outTag+'.root','recreate')
    
    canvas = ROOT.TCanvas('c1', 'c1', 600,630)
    canvas.Print(outTag+'.ps[')
    
    for key in tex_dic:
        # MET (data):
        h_met_dt=Data.drawTH1('met_pt',cuts[key],"1",50,0,500,titlex='E_T^{miss}',units='GeV',drawStyle="HIST")
        err['data'][key]=ROOT.Double(0.0)
        yields['data'][key]=h_met_dt.IntegralAndError(0,1+h_met_dt.GetNbinsX(),err['data'][key])
        
        # MET (non-zjets):
        h_met_nonZ=otherBG.drawTH1('met_pt',cuts[key],str(lumi*1000),50,0,500,titlex='E_T^{miss}',units='GeV',drawStyle="HIST")
        err['non-Zjets'][key]=ROOT.Double(0.0)
        yields['non-Zjets'][key]=h_met_nonZ.IntegralAndError(0,1+h_met_nonZ.GetNbinsX(),err['non-Zjets'][key])
        
        # MET (zjets):
        h_met=ZJets.drawTH1('met_pt',cuts[key],str(lumi*1000),50,0,500,titlex='E_T^{miss}',units='GeV',drawStyle="HIST")
        err['Zjets'][key]=ROOT.Double(0.0)
        yields['Zjets'][key]=h_met.IntegralAndError(0,1+h_met.GetNbinsX(),err['Zjets'][key])
        
        canvas.Clear()
        h_met.Draw()
        canvas.Print(outTag+'.ps')
        h_met.SetName("zjets_MET_"+key);
        h_met.Write()
    
        # deltaR_ll (zjets):
        hdRZmm=ZJets.drawTH1('llnunu_l1_deltaR',cuts[key],str(lumi*1000),50,0,5,titlex='#Delta R(#mu,#mu)',units='',drawStyle="HIST")
        hdRZmm.SetName("zjets_hdRZmm_"+key)
        hdRZmm.GetYaxis().SetTitle("Events")
    
        canvas.Clear()
        hdRZmm.Draw()
        canvas.Print(outTag+'.ps')
        hdRZmm.Write()
    
    ### ----- Finalizing:
    canvas.Print(outTag+'.ps]')
    os.system('ps2pdf '+outTag+'.ps '+outTag+'.pdf')    
    fout.Close()
    
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
        printfile.write( '{:^40}\n'.format('ll in | ll out'))
        printfile.write( '{:^40}\n'.format('nonRes %6.2f | %6.2f nonRes' % (yields['Zjets']['SR'], yields['Zjets']['CRc']) ))
        printfile.write( '{:^40}\n'.format('Res %6.2f | %6.2f Res' % (yields['non-Zjets']['SR'], yields['non-Zjets']['CRc'])))
        printfile.write( '{:^40}\n'.format('data %6.2f | %6.2f data' % (yields['data']['SR'], yields['data']['CRc'])))
        printfile.write( '-'*40+'\n')
        printfile.write( '{:^40}\n'.format('eu in | eu out'))
        printfile.write( '{:^40}\n'.format('nonRes %6.2f | %6.2f nonRes' % (yields['Zjets']['CRb'], yields['Zjets']['CRd'])))
        printfile.write( '{:^40}\n'.format('Res %6.2f | %6.2f Res' % (yields['non-Zjets']['CRb'], yields['non-Zjets']['CRd'])))
        printfile.write( '{:^40}\n'.format('data %6.2f | %6.2f data' % (yields['data']['CRb'], yields['data']['CRd'])))
        printfile.write( '-'*40+'\n')
    
    
printfile.close()
