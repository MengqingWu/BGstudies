#!/usr/bin/env python
import os, sys, math
from ROOT import *
from python.InitializePlotter import InitializePlotter

indir='../zjetsSkim'
samples=InitializePlotter(indir=indir)
outdir='./'
fout=TFile(outdir+"cutflow.root","recreate")
test = True
fchain=TChain("tree")

if test:  sampledir=["ZZTo4L"] #BulkGravToZZToZlepZinv_narrow_1000
else:  sampledir=samples.zjetsSamples     

for sample in samples.zjetsSamples:
    status = fchain.Add(indir+'/'+sample+'.root/tree', 0)
    if status<=0: raise RuntimeError, "[cutflow.py] ERROR! Invalid tree added to fchain, please check!"
    
#---- Prepare cutflow plots and initialize
cutflow = TH1F("h_cutflow", "cutflow; cut# ; / event ",10 , 0.,10. )
cutflow_w = TH1F("h_cutflow_w", "weighted cutflow; cut# ; / yields ",10 , 0.,10. )


nll = nflags = nsublep = 0
nsiglep = nZwindow = nZpt = nmet = ndjetfakeMet = nlepfakeMet = nvar1 = nvar2 = nlepVeto =0

#--- Loop:
print fchain.GetEntriesFast(),' entries to process:'

for ientry in range(0, fchain.GetEntriesFast()):
    fchain.GetEntry(ientry)
    if ientry%2000==0: print "Entry ",ientry
    
    if fchain.nllnunu>0:
        nll+=1
        # make sure the met flags are on:
        if fchain.Flag_eeBadScFilter==1 and fchain.Flag_goodVertices==1 and fchain.Flag_EcalDeadCellTriggerPrimitiveFilter==1 and fchain.Flag_CSCTightHalo2015Filter==1 and fchain.Flag_HBHENoiseIsoFilter==1 and fchain.Flag_HBHENoiseFilter==1:
            nflags+=1
            
            # make sure subleading lepton cuts applied:
            if  (abs(fchain.llnunu_l1_l1_pdgId[0])==13 and fchain.llnunu_l1_l1_pt[0]>20 and abs(fchain.llnunu_l1_l1_eta[0])<2.4 and fchain.llnunu_l1_l2_pt[0]>20 and abs(fchain.llnunu_l1_l2_eta[0])<2.4) or (abs(fchain.llnunu_l1_l1_pdgId[0])==11 and fchain.llnunu_l1_l1_pt[0]>35 and abs(fchain.llnunu_l1_l1_eta[0])<2.5 and fchain.llnunu_l1_l2_pt[0]>35 and abs(fchain.llnunu_l1_l2_eta[0])<2.5):
                nsublep+=1
                
                # leading lepton cuts:
                if (abs(fchain.llnunu_l1_l1_pdgId[0])==13 and (fchain.llnunu_l1_l1_highPtID[0]==1 or fchain.llnunu_l1_l2_highPtID[0]==1) and ((fchain.llnunu_l1_l1_pt[0]>50 and abs(fchain.llnunu_l1_l1_eta[0])<2.1) or (fchain.llnunu_l1_l2_pt[0]>50 and abs(fchain.llnunu_l1_l2_eta[0])<2.1))) or (abs(fchain.llnunu_l1_l1_pdgId[0])==11 and ((fchain.llnunu_l1_l1_pt[0]>115 and abs(fchain.llnunu_l1_l1_eta[0])<2.5) or (fchain.llnunu_l1_l2_pt[0]>115 and abs(fchain.llnunu_l1_l2_eta[0])<2.5))):
                    nsiglep+=1
                    cutflow.Fill(0.)

                    # Z mass window:
                    if abs(fchain.llnunu_l1_mass[0] - 91.1876)<20.0:
                        nZwindow+=1
                        cutflow.Fill(1.)

                        if fchain.llnunu_l1_pt[0]>100.0:
                            nZpt+=1
                            cutflow.Fill(2.)

                            if fchain.llnunu_l2_pt[0]>100.0:
                                nmet+=1
                                cutflow.Fill(3.)

                                if fchain.dPhi_jetMet_min_a>0.4:
                                    ndjetfakeMet+=1
                                    cutflow.Fill(4.)

                                    if fchain.llnunu_l1_pt[0]/fchain.llnunu_mta[0]<0.7:
                                        nlepfakeMet+=1
                                        cutflow.Fill(5.)

                                        if abs(abs(fchain.llnunu_deltaPhi[0]) - TMath.Pi()/2)>1.5: 
                                            nvar1+=1; 
                                            cutflow.Fill(6.)
                                            if (fchain.llnunu_l2_pt[0]*(abs(fchain.llnunu_deltaPhi[0])-TMath.Pi()/2)/abs(abs(fchain.llnunu_deltaPhi[0])-TMath.Pi()/2)/fchain.llnunu_l1_pt[0])>0.2:
                                                nvar2+=1
                                                cutflow.Fill(7.)
                                                
                                                toVeto=False
                                                if (fchain.nlep>2):
                                                    for ilep in range(0,fchain.nlep):
                                                        if fchain.lep_pt[ilep] in [fchain.llnunu_l1_l1_pt[0], fchain.llnunu_l1_l2_pt[0]]: continue
                                                        else: 
                                                            if fchain.deltaR_lep[ilep]>0.4 and fchain.deltaR_jet[ilep]>0.4: toVeto=True
                                                            else: print '[info] evt==', fchain.evt 
                                                if not toVeto: nlepVeto+=1; cutflow.Fill(8.)
                                    
print 'we have ', fchain.GetEntriesFast(), 'entries.'
print 'llnunu pair:   ', nll
print 'MET Flags:     ', nflags 
print 'sub lepton:    ', nsublep
print 'lead lepton:   ', nsiglep #1
print 'Z window:      ', nZwindow #2
print 'Z pt>100:      ', nZpt #3
print 'met>100:       ', nmet #4
print 'dphi(j,met)>.4:', ndjetfakeMet #5
print 'Zpt/mT<0.7:    ', nlepfakeMet #6
print '|dphi-pi/2|>1.5:', nvar1 #7
print 'pTbalance>0.2: ', nvar2 #8
print '3rd lepton veto:',nlepVeto #9

#---- Finalize:
fout.cd()
cutflow.Write()
fout.Close()
