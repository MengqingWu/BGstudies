#!/usr/bin/env python

import ROOT
import os
from collections import OrderedDict

### Please keep the keys same in tex_dic={}  and cuts={}
class SetCuts ():
    def __init__(self):
         
        self.Tex_dic = {'regA': 'Region A', 'regB': 'Region B','regC': 'Region C','regD': 'Region D'}
        self.ZjetsTex = {'regTrg': 'Target Region', 'regCtrl': 'Control Region',
                         'basecut': 'Pre-selected Region'}
        self.met_pt_in=raw_input("[info] 'SetCuts' -> please give the MET cut: (enter to use default MET>100GeV)\n")
        self.met_pt='100' if self.met_pt_in=='' else self.met_pt_in

        #self.var1='fabs(fabs(llnunu_deltaPhi)-TMath::Pi()/2)'
        #self.var2='cos(llnunu_deltaPhi)/fabs(cos(llnunu_deltaPhi))'
        self.zj_var = 'fabs(llnunu_deltaPhi)'
        
        #self.cut_var1 ='TMath::Pi()/4'
        #self.cut_var2 ='0' 
        self.cut_zj_var = ['0', 'TMath::Pi()/4', 'TMath::Pi()/2','3*TMath::Pi()/4']
        
        # define a cutflow for signal region
        self.cutflow=("(nllnunu>0)", #0
                      "(llnunu_l1_mass>70.0&&llnunu_l1_mass<110.0)", #1
                      "llnunu_l1_pt>100.0", #2
                      "llnunu_l2_pt>"+self.met_pt, #3
                      "nlep<3", #4
                      self.zj_var+'>'+self.cut_zj_var[3], #5
                      #self.var1+'>'+self.cut_var1, #4
                      #self.var2+'<'+self.cut_var2, #5
                      ) 

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
                 
        astr = "({0}&&{4}&&{5})"
        cuts_tmp = astr.format(*self.cutflow)
        cuts_tmp+='&&'+zpt+'&&'+met

        if Zmass=='inclusive': pass
        elif Zmass=='out': cuts_tmp+="&&((llnunu_l1_mass>35.0&&llnunu_l1_mass<65.0)||(llnunu_l1_mass>115.0&&llnunu_l1_mass<180.0))"
        elif Zmass=='in': cuts_tmp+="&&(llnunu_l1_mass>70.0&&llnunu_l1_mass<110.0)"
        else: raise RuntimeError, "[ERROR]! I do not understand the Zmass region you asked in alphaCuts(isll, Zmass) from SetCuts.py"

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
                         'inclusive': self.alphaCuts(isll=True, Zmass='inclusive', zpt_cut=zpt_cut, met_cut=met_cut)
                     },
                'emu':{ 'in' : self.alphaCuts(isll=False, Zmass='in', zpt_cut=zpt_cut, met_cut=met_cut),
                        'out': self.alphaCuts(isll=False, Zmass='out', zpt_cut=zpt_cut, met_cut=met_cut),
                        'inclusive': self.alphaCuts(isll=False, Zmass='inclusive', zpt_cut=zpt_cut, met_cut=met_cut)}
            }
        #print cuts
        return cuts
    
    def GetZjetsCuts(self, whichRegion="", zpt_cut='', met_cut='', extra_cut=''):
        channelCut={'el':'abs(llnunu_l1_l1_pdgId)==11',
                    'mu':'abs(llnunu_l1_l1_pdgId)==13',
                    'inclusive': '(1)'}
                
        zpt='llnunu_l1_pt>'
        if whichRegion=="":
            whichRegion=raw_input("[info]' abcdCuts' -> Please choose a benchmarck Region (SR or VR): \n")
            if whichRegion not in ['SR','VR']: whichRegion='SR'; print "[Warning] invalid 'whichRegion' input, choose default = 'SR'."
            
        if whichRegion=='SR': met='llnunu_l2_pt>'
        elif whichRegion=='VR': met='llnunu_l2_pt>50.0&&llnunu_l2_pt<'
        else:
            print "I do not understand your benchmark Region, should be either 'SR' for MET>"+met+"GeV or 'VR' for 50.0<MET<"+met+"GeV\n"
            sys.exit(0)

        zpt=zpt+zpt_cut if zpt_cut!='' else zpt+'100.0'
        met=met+met_cut if met_cut!='' else met+self.met_pt
        
        basecut_str = "{0}&&{1}&&{4}".format(*self.cutflow)
        basecut_ls = [basecut_str, zpt, met ]
        if extra_cut: basecut_ls.append(extra_cut)
        
        cuts=OrderedDict()
        for channel in channelCut:
            basecut= basecut_ls+ [channelCut[channel]]
            regTrgcut = basecut + [self.zj_var + '>' + self.cut_zj_var[3]]
            regCtrlcut = basecut + [self.zj_var + '>' + self.cut_zj_var[0], self.zj_var + '<=' + self.cut_zj_var[3]]
            cuts[channel]={'basecut': '('+'&&'.join(basecut)+')',
                           'regTrg':  '('+'&&'.join(regTrgcut)+')',
                           'regCtrl': '('+'&&'.join(regCtrlcut)+')'}
        return cuts
    
    def abcdCuts(self, channel="", whichRegion="", isPreSelect=False, zpt_cut='', met_cut='', extra_cut=''):
        if channel in ['el', 'mu', 'inclusive'] : Channel=channel
        else:
            Channel='inclusive'
            print "[Warning] abcdCuts(): invalid value for 'channel', choose default = 'inclusive'."

        channelCut={'el':'abs(llnunu_l1_l1_pdgId)==11',
                    'mu':'abs(llnunu_l1_l1_pdgId)==13',
                    'inclusive': '(1)'}

        zpt='llnunu_l1_pt>'
        
        if whichRegion=="":
            whichRegion=raw_input("[info]' abcdCuts' -> Please choose a benchmarck Region (SR or VR): \n")
            if whichRegion not in ['SR','VR']: whichRegion='SR'; print "[Warning] invalid 'whichRegion' input, choose default = 'SR'."
            
        if whichRegion=='SR': met='llnunu_l2_pt>'
        elif whichRegion=='VR': met='llnunu_l2_pt>50.0&&llnunu_l2_pt<'
        else:
            print "I do not understand your benchmark Region, should be either 'SR' for MET>"+met+"GeV or 'VR' for 50.0<MET<"+met+"GeV\n"
            sys.exit(0)

        zpt=zpt+zpt_cut if zpt_cut!='' else zpt+'100.0'
        met=met+met_cut if met_cut!='' else met+self.met_pt

        #fakeMetCut='llnunu_l1_pt/llnunu_mta<0.7&&dPhi_jetMet_min_a>0.4'
        #preSelection='nllnunu>0&&(llnunu_l1_mass>70.0&&llnunu_l1_mass<110.0)&&llnunu_l1_pt>'
        
        preSelection = "{0}&&{1}&&{4}".format(*self.cutflow)
        regPreSelect=[preSelection, zpt, met, channelCut[Channel]]
        if extra_cut: regPreSelect.append(extra_cut)

        if isPreSelect:
            cuts='('+'&&'.join(regPreSelect)+')'
        else:
            cuts_a=regPreSelect + [self.zj_var + '>' +self.cut_zj_var[3]]
            cuts_b=regPreSelect + [self.zj_var + '>' +self.cut_zj_var[2], self.zj_var + '<=' + self.cut_zj_var[3]]
            cuts_c=regPreSelect + [self.zj_var + '>' +self.cut_zj_var[1], self.zj_var + '<=' + self.cut_zj_var[2]]
            cuts_d=regPreSelect + [self.zj_var + '>' +self.cut_zj_var[0], self.zj_var + '<=' + self.cut_zj_var[1]]
            cuts=OrderedDict({'regA': '(' + '&&'.join(cuts_a) + ')',
                              'regB': '(' + '&&'.join(cuts_b) + ')',
                              'regC': '(' + '&&'.join(cuts_c) + ')',
                              'regD': '(' + '&&'.join(cuts_d) + ')'})
        
        return cuts
   
