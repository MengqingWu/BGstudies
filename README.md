# xzz2l2v BG studies based on 76X samples:

**Private package to do background estimation in xzz2l2v analysis**

1. Zjets background: (so many different versions to do)

   - current methodology:
    
    	Since the dphi(Z, met) is now better modulated to have a good data/MC agreement, so we can do the methodology below. <br/>
	Simply revert the cut of dphi(Z, met)>3PI/4 to define a CR, compute a scale factor between CR and Target Region (TR, which is SR) using MC,
	apply this scale factor to the non-resonant bkg subtracted (use MC) CR data: <br/>
	N_TR^dt = N_CR^{dt,sub} * (N_TR^mc / N_TR^mc).

   - validation:
     
     	a validation region constructed in a lower MET region (from 50 up to SR met cut), repeat the above methodology and open the TR data to validate the technique.

	The code for zjets is out of data, but updated in the 80x branch.

   **FIXME**: Many previous estimation method to be documented. (2016 Sep 29)
    
2. non-Resolution background:
    codes under 'bkgStudies/nonResBG'
    
    - methodology: using emu control samples
    
    - an inclusive alpha computed from SB regions of ll/emu samples to account for the differences in branching ratios, acceptance and efficiency: 
    	alpha = N_emu(SB)/N_ll(SB)
	
    - since the electron and muon offline cuts are so different, leading to large selection efficiency differed from ll to emu pairs;
    	an event-by-event shape reweight based on Mz is applied to emu samples before the alpha is computed:
	
    	f(non_res, data_ll) =  f(res+non_res, data_eu) * f(non_res, mc_ll)/f(res+non_res, mc_eu)
        
    - code documentations:
    
    	simply use ./run.sh to configure:
	
	    - doStep1=true:
	
		   make the step1_plotter.py run to have the table of yields printed in './out_step1/num_out.txt'
		   (even the final yield estimate will be given with shape reweight applied). <br/>
	   	   './out_step1/shape_correction_metx.root', where x=0,100,200 is the met cut applied,
	   	   are produced to apply the Mz-reweight weights to data and MC samples.
	
	     - doTest=true:
	
		  you can do a MC closure test (NOTE: MC samples needs Mz-reweight), with output in './closure_step2'
	
	     - doTest=false:
	
		  data-driven plots with other background from MC stacked to compare with data (Note: Mt(ZZ) blinded w/ MET>200), will be produced in './out_step2'.

    FIXME: some code updates to be perfected. (2016 Sep 29)