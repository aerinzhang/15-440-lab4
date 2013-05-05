15-440-lab4  
K-Means

Boya Yang (boyay)           					Shikun Zhang (shikunz)
======================================================================
Submission incluse:
- pdf file:
	- report.pdf

- shell scripts:
	- runSample
		runs a sample data of size 5000 with k=5 using both 
		algorithms (use 8 processors for parallel)

	First Step: generate Data
	- dataGenerator
		generates datasets for both DNA and Points using a combination
		of different k's and p's, saves file into folder /data/
		k ranges from 2 to 10; p is in [10, 100, 1000, 10000, 100000]
		also generate the solution file, the original k centroids

	- runSequential
		runs sequential algorithms on two types of datasets generated 
		by the dataGenerator with profiling information

	- runParallel
		runs parallel algorithms on two types of datasets generated 
		by the dataGenerator by using 2, 4, 8 or 12 processors with
		profiling information


- python files (used in the shell scripts):
	
	-k # of clusters
	-e value of epsilon 
	-i input file
	-o output file
	-p number of points aruond centroid
	-l length of DNA strand, default = 50
	-r range of coordinates, default = 1000000

	- PointGenerator.py   -k <int> -p <int> -o <outfile> [-r <int>]
	- PointSequential.py  -k <int> -e <float> -i <infile> -o <outfile> 
	- PointParallel.py    -k <int> -e <fliat> -i <infile> -o <outfile>

	- DNAGenerator.py     -k <int> -p <int> -o <outfile> [-l <int>]
	- DNASequential.py    -k <int> -e <float> -i <infile> -o <outfile> 
	- DNAParallel.py      -k <int> -e <float> -i <infile> -o <outfile>
======================================================================