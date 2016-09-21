#!/bin/sh

doStep1=false
doTest=true

met=( 0 100 200)
var=( mt) #( mt mz) 
## parameters for test only:
sb=( both) #( both right)
MzWt=( 0) #( 0 1)

if [ "doStep1" = true ]; then
    ./step1_plotter.py -b
    ./step1_plotter.py 100 -b
    ./step1_plotter.py 200 -b
    
else
    echo print "Usage: ./run.py met_cut var_to_draw (sideband='both') (doMzWt=True) (dotest=False)"
    if [ "$doTest" = true ]; then
	# for closure test:
	for i in "${met[@]}";do
	    for j in "${var[@]}";do
		for k in "${sb[@]}";do
		    for l in "${MzWt[@]}";do
		    echo ./run.py $i $j $k $l 1 -b
		    ./run.py $i $j $k $l 1 -b
		    done
		done
	    done
	done

    else
	# for data-driven result:
	for i in "${met[@]}";do
	    for j in "${var[@]}";do
		echo ./run.py $i $j -b
		./run.py $i $j -b
	    done
	done
    fi
fi
