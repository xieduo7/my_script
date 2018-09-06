#!/usr/bin/env python
# coding utf-8
"""Duo Xie(modified from the code from biopython)
Usage:
 ncbi_download.py (--term=<term>) (--email=<address>)(--name=<filename>)[--db=<database>] [--rettype=<type>] [--retmax=<number>] [--retmode=<type>]

 Options:
  --term=<term> Entrez text query.
  --email=<address> Always tell NCBI who you are.
  --rettype=<type> the format of output,The rettype parameter must be used in conjunction with retmode.
  --retmode=<type> Retrieval mode,The retmode parameter must be used in conjunction with rettype.
  --retmax=<number> Total number of records from the input set to be retrieved.
  --db=<database>   Database from which to retrieve records.		
  --name=<filename> The name of output	
"""
from docopt import docopt
from Bio import Entrez
import sys
from urllib2 import HTTPError  # for Python 2

def _esearch(word,email,database):
	Entrez.email = "history."+email
	search_handle = Entrez.esearch(db="nucleotide",term=word,usehistory="y", idtype="acc")
	results = Entrez.read(search_handle)
	search_handle.close()
	return results
def _efetch(search_results,datatype,datamode,maxbatch,databse,name):
	acc_list = search_results["IdList"]
	count = int(search_results["Count"])
	webenv = search_results["WebEnv"]
	query_key = search_results["QueryKey"]
	batch_size = maxbatch
	out_handle = open(name+"."+datatype, "w")
	for start in range(0, count, batch_size):
		end = min(count, start+batch_size)
		print("Going to download record %i to %i" % (start+1, end))	    
		attempt = 0
	        while attempt < 3:
			attempt += 1
			try:
				fetch_handle = Entrez.efetch(db=databse,
                                         rettype=datatype, retmode=datamode,
                                         retstart=start, retmax=batch_size,
                                         webenv=webenv, query_key=query_key,
                                         idtype="acc")
			except HTTPError as err:
				if 500 <= err.code <= 599:
					print("Received error from server %s" % err)
					print("Attempt %i of 3" % attempt)
					time.sleep(15)
				else:
					raise
		data = fetch_handle.read()
		fetch_handle.close()
		out_handle.write(data)
	out_handle.close()







if __name__=='__main__':
	arguments =docopt(__doc__)
	term=arguments["--term"]
	email=arguments["--email"]
	if (arguments["--rettype"]):
		rettype=arguments["--rettype"]
	else:
		rettype="fasta"
	if (arguments["--retmode"]):
		retmode=arguments["--retmode"]
	else:
		retmode="text"
	if (arguments["--retmax"]):
		retmax=arguments["--retmax"]
	else:
		retmax=3
	if (arguments["--db"]):
		db=arguments["--db"]
	else:
		db="nucleotide"
	name=arguments["--name"]
	search_results=_esearch(term,email,db)
	_efetch(search_results,rettype,retmode,retmax,db,name)
