#!/usr/bin/env python

import ROOT
import os
from collections import OrderedDict

### Please keep the keys same in tex_dic={}  and cuts={}
class SetCuts ():
    def __init__(self):
         
        self.Tex_dic = {'regA': 'Region A', 'regB': 'Region B','regC': 'Region C','regD': 'Region D'}
        
        self.met_pt_in=raw_input("[info] 'SetCuts' -> please give the MET cut: (enter to use default MET>100GeV)\n")
        self.met_pt='100' if self.met_pt_in=='' else self.met_pt_in

        self.var1='fabs(fabs(llnunu_deltaPhi)-TMath::Pi()/2)'
        self.var2='cos(llnunu_deltaPhi)/fabs(cos(llnunu_deltaPhi))'

        self.cut_var1 ='TMath::Pi()/4'
        self.cut_var2 ='0' 
        
        # define a cutflow for signal region
        self.cutflow=("(nllnunu>0)", #0
                      "(llnunu_l1_mass>70.0&&llnunu_l1_mass<110.0)", #1
                      "llnunu_l1_pt>100.0", #2
                      "llnunu_l2_pt>"+self.met_pt, #3
                      self.var1+'>'+self.cut_var1, #4
                      self.var2+'<'+self.cut_var2, #5
                      "nlep<3")  #6

    def GetSRCut(self, N_minus_1=''):
        """ N_minus_1 (from 1 to 5) is to choose which cut to loose to get the N-1 plots  """
        ll=['{'+str(i)+'}' for i in[0,1,2,3,4,5]]
        
        N_minus_1='{'+N_minus_1+'}'
        if N_minus_1 in ll:
            print "[Info] 'GetSRCut' says you are asking for a 'N-1' SR: "
            ll.remove(N_minus_1)
        else: print "[Info] 'GetSRCut' says you are asking for a full SR: " 
        
        cut_str = "("+ "&&".join(ll) +")"
        srCuts = cut_str.format(*self.cutflow)
        print '  ', srCuts
        return srCuts
    
    # Cuts used for alpha-method to estimate non-resonant bkgs
    def alphaCuts(self, isll=True, Zmass='inclusive', zpt_cut='', met_cut=''):
        zpt, met = 'llnunu_l1_pt>','llnunu_l2_pt>'
        zpt+=zpt_cut if zpt_cut!='' else '100.0'
        met+=met_cut if met_cut!='' else self.met_pt
                 
        astr = "({0}&&{4}&&{5}&&{6})"
        #astr = "({0}&&{4}&&{5})"
        cuts_tmp = astr.format(*self.cutflow)
        cuts_tmp+='&&'+zpt+'&&'+met

        if Zmass=='inclusive': pass
        elif Zmass=='out': cuts_tmp+="&&((llnunu_l1_mass>35.0&&llnunu_l1_mass<65.0)||(llnunu_l1_mass>115.0&&llnunu_l1_mass<200.0))"
        elif Zmass=='in': cuts_tmp+="&&(llnunu_l1_mass>70.0&&llnunu_l1_mass<110.0)"
        else: raise RuntimeError, "ERROR! I do not understand the Zmass value you put in alphaCuts(self, isll, Zmass) from SetCuts.py"

        if not isll:
            cuts_tmp = ROOT.TString(cuts_tmp)
            cuts_tmp.ReplaceAll("llnunu","elmununu")
            cuts=cuts_tmp.Data()
        else:  cuts=cuts_tmp
        
        #print cuts
        return cuts

    def GetAlphaCuts(self, zpt_cut='', met_cut=''):
        """cuts[<reg>][<zmass>]  """
        cuts = {'ll' : { 'in': self.alphaCuts(isll=True, Zmass='in', zpt_cut=zpt_cut, met_cut=met_cut),
                         'out': self.alphaCuts(isll=True, Zmass='out', zpt_cut=zpt_cut, met_cut=met_cut),
                         'inclusive': self.alphaCuts(Zmass='inclusive', zpt_cut=zpt_cut, met_cut=met_cut)
                     },
                'emu':{ 'in' : self.alphaCuts(isll=False, Zmass='in', zpt_cut=zpt_cut, met_cut=met_cut),
                        'out': self.alphaCuts(isll=False, Zmass='out', zpt_cut=zpt_cut, met_cut=met_cut),
                        'inclusive': self.alphaCuts(isll=False, Zmass='inclusive', zpt_cut=zpt_cut, met_cut=met_cut)}
            }
        #print cuts
        return cuts
    
    def abcdCuts(self, channel="", whichRegion="", isPreSelect=False, zpt_cut='', met_cut=''):
        if channel in ['el', 'mu', 'inclusive'] : Channel=channel
        else:
            Channel='inclusive'
            print "[Warning] abcdCuts(): ",channel ," is not in ['el', 'mu', 'inclusive'], choose default 'inclusive'."

        channelCut={'el':'abs(llnunu_l1_l1_pdgId)==11',
                    'mu':'abs(llnunu_l1_l1_pdgId)==13',
                    'inclusive': '(1)'}
        
        zpt=zpt_cut if zpt_cut!='' else '100.0'
        met=met_cut if met_cut!='' else self.met_pt

        #fakeMetCut='llnunu_l1_pt/llnunu_mta<0.7&&dPhi_jetMet_min_a>0.4'
        #preSelection='nllnunu>0&&(llnunu_l1_mass>70.0&&llnunu_l1_mass<110.0)&&llnunu_l1_pt>'
        prestr = "({0}&&{1}&&{6})"
        preSelection = prestr.format(*self.cutflow)
                        
        if whichRegion=="": whichRegion=raw_input("[info]' abcdCuts' -> Please choose a benchmarck Region (SR or VR): \n")
        if whichRegion=='SR':
            preSelection='('+preSelection+'&&llnunu_l1_pt>'+zpt+'&&llnunu_l2_pt>'+met+')'
        elif whichRegion=='VR':
            preSelection='('+preSelection+'&&llnunu_l1_pt>'+zpt+'&&llnunu_l2_pt<'+met+')'
        else:
            print "I do not understand your benchmark Region, should be either 'SR' for MET>"+met+"GeV or 'VR' for MET<"+met+"GeV\n"
            sys.exit(0)
            

        if isPreSelect:
            cuts='('+preSelection+'&&'+channelCut[Channel]+')'
        else:
            cuts_a='('+preSelection+'&&'+channelCut[Channel]+'&&'+self.var1+'>'+self.cut_var1+'&&'+self.var2+'<'+self.cut_var2+')'
            cuts_b='('+preSelection+'&&'+channelCut[Channel]+'&&'+self.var1+'>'+self.cut_var1+'&&'+self.var2+'>'+self.cut_var2+')'
            cuts_c='('+preSelection+'&&'+channelCut[Channel]+'&&'+self.var1+'<'+self.cut_var1+'&&'+self.var2+'<'+self.cut_var2+')'
            cuts_d='('+preSelection+'&&'+channelCut[Channel]+'&&'+self.var1+'<'+self.cut_var1+'&&'+self.var2+'>'+self.cut_var2+')'
            cuts=OrderedDict({'regA':cuts_a, 'regB':cuts_b, 'regC':cuts_c, 'regD':cuts_d})
        
        return cuts
   
