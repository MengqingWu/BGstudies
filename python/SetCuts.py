#!/usr/bin/env python

import ROOT
import os

### Please keep the keys same in tex_dic={}  and cuts={}
class SetCuts ():
    def __init__(self):
         
        self.Tex_dic = {'SR': 'Region A', 'CRb': 'Region B','CRc': 'Region C','CRd': 'Region D'}
        
        self.met_pt_in=raw_input("[info] 'SetCuts' -> please give the MET cut: (enter to use default MET>100GeV)\n")
        self.met_pt='100' if self.met_pt_in=='' else self.met_pt_in
        # define a cutflow for signal region
        self.cutflow=("abs(llnunu_l1_mass-91.1876)<20.0",
                      "llnunu_l1_pt>100.0",
                      "llnunu_l2_pt>"+self.met_pt,
                      "sin(llnunu_deltaPhi)<0.3",
                      "((llnunu_l2_pt*cos(llnunu_deltaPhi)+llnunu_l1_pt)/llnunu_l1_pt)<0.7")
        
    # Cuts used for alpha-method to estimate non-resonant bkgs
    def alphaCuts(self, isll=True, Zmass='inclusive'):
        astr = "({0}&&{1}&&{2}&&{3}&&{4})"
        #astr = "({0}&&{1}&&{2})"  
        cuts = astr.format(*self.cutflow)

        cuts_tmp= ROOT.TString(cuts)

        if Zmass=='inclusive': cuts_tmp.ReplaceAll("abs(llnunu_l1_mass-91.1876)<20.0&&","")
        elif Zmass=='out': cuts_tmp.ReplaceAll("91.1876)<20.0","91.1876)<=55.0&&abs(llnunu_l1_mass-91.1876)>=25.0")
        elif Zmass=='in': pass
        else: raise RuntimeError, "ERROR! I do not understand the Zmass value you put in alphaCuts(self, isll, Zmass) from SetCuts.py"

        if not isll:
            #cuts_tmp.ReplaceAll("&&llnunu_deltaPhi>2.5&&llnunu_l1_deltaR<0.6","")
            cuts_tmp.ReplaceAll("llnunu","elmununu")
            
        cuts=cuts_tmp.Data()
        
        print cuts
        return cuts

    def GetAlphaCuts(self):
        
        cuts = {'llin' : self.alphaCuts(isll=True, Zmass='in'),
                'llout': self.alphaCuts(isll=True, Zmass='out'),
                'euin' : self.alphaCuts(isll=False, Zmass='in'),
                'euout': self.alphaCuts(isll=False, Zmass='out')}
        #print cuts
        return cuts
    
    def abcdCuts(self,channel, whichRegion="", isPreSelect=False, zpt_cut='', met_cut=''):
        zpt=zpt_cut if zpt_cut!='' else '100.0'
        met=met_cut if met_cut!='' else self.met_pt
        if whichRegion=="": whichRegion=raw_input("[info]' abcdCuts' -> Please choose a benchmarck Region (SR or VR): \n")
        if whichRegion=='SR':
            preSelection='(nllnunu>0&&abs(llnunu_l1_mass-91.1876)<20.0&&llnunu_l1_pt>'+zpt+'&&llnunu_l2_pt>'+met+')'
        elif whichRegion=='VR':
            preSelection='(nllnunu>0&&abs(llnunu_l1_mass-91.1876)<20.0&&llnunu_l1_pt>'+zpt+'&&llnunu_l2_pt<'+met+')'
        else:
            print "I do not understand your benchmark Region, should be either 'SR' for MET>"+met+"GeV or 'VR' for MET<"+met+"GeV\n"
            sys.exit(0)
            
        pdgID={'el':'11','mu':'13' }
        if isPreSelect:
            cuts='('+preSelection+'&&abs(llnunu_l1_l1_pdgId)=='+pdgID[channel]+')'
        else:
            cut_var1='1.5'
            cut_var2='0.4' 
            var1='abs(llnunu_deltaPhi-TMath::Pi()/2)'
            var2='(llnunu_l2_pt*(llnunu_deltaPhi-TMath::Pi()/2)/abs(llnunu_deltaPhi-TMath::Pi()/2)/llnunu_l1_pt)'
            
            cuts_a='('+preSelection+'&&abs(llnunu_l1_l1_pdgId)=='+pdgID[channel]+'&&'+var1+'>'+cut_var1+'&&'+var2+'>'+cut_var2+')'
            cuts_b='('+preSelection+'&&abs(llnunu_l1_l1_pdgId)=='+pdgID[channel]+'&&'+var1+'>'+cut_var1+'&&'+var2+'<'+cut_var2+')'
            cuts_c='('+preSelection+'&&abs(llnunu_l1_l1_pdgId)=='+pdgID[channel]+'&&'+var1+'<'+cut_var1+'&&'+var2+'>'+cut_var2+')'
            cuts_d='('+preSelection+'&&abs(llnunu_l1_l1_pdgId)=='+pdgID[channel]+'&&'+var1+'<'+cut_var1+'&&'+var2+'<'+cut_var2+')'
            cuts={'SR':cuts_a, 'CRb':cuts_b, 'CRc':cuts_c, 'CRd':cuts_d}
        
        return cuts
   
