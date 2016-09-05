#!/usr/bin/env python

from print_zjets import *

t=PrintZjets()
zpt,met,reg='100','200','SR'

#for channel in ['el','mu', 'inclusive']:
for channel in ['mu']:
    t.execute(channel, zpt_cut=zpt, met_cut=met, whichregion=reg, drawStack=True)

t.finalize()
