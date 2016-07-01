#!/usr/bin/env python
from stack_nonResDD import *

t=StackDataDriven()

toplot={('llnunu_l1_mass', 'elmununu_l1_mass'): (40, 0.0, 200.0, "M_{Z}^{ll}", "GeV", 70.0, 110.0),
        ('llnunu_l2_pt', 'elmununu_l2_pt'): (50, 0.0, 500.0, "E_{T}^{miss}", "GeV", 0.0, 500.0)}
for var in toplot:
    t.drawDataDrivenStack(var[0], var[1], toplot[var][0], toplot[var][1], toplot[var][2], toplot[var][3], toplot[var][4],
                          xcutmin=toplot[var][5], xcutmax=toplot[var][6])
