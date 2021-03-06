from Bio import SeqIO
import os
import pandas as pd
import numpy as np
from fuzzywuzzy import process

FUZZY_CUTOFF = 60

# Specify data location
homedir = "/work/data/refseq"

file_count = 0
for root, dirs, files in os.walk(homedir):
    for file in files:
        filepath = os.path.join(root, file)
        if filepath.endswith(".gbff"):
            file_count = file_count + 1

f = open('resistance.csv', 'w')
current_file = 0
for root, dirs, files in os.walk(homedir):
    for file in files:
        filepath = os.path.join(root, file)
        if filepath.endswith(".gbff"):
            current_file = current_file + 1
            if current_file % 10 == 0:
                #print("{0:.2f}% complete ({} of {} files)".format((current_file / file_count) * 100, current_file, file_count))
                print("{}% complete ({} of {} files)".format((current_file / file_count) * 100, current_file, file_count))
            for seq_record in SeqIO.parse(filepath, "genbank"):
                locus = seq_record.id
                organism = seq_record.annotations["organism"]
                if "structured_comment" in seq_record.annotations:
                    sc = seq_record.annotations["structured_comment"]
                    for keys in sc.keys():
                    	low_1=keys.lower()
                    	if low_1 in ['metadata']:
                            meta = sc[keys]
                            for keys in meta.keys():
                            	low_2 = keys.lower()
                            	if low_2 in ['temperature range','temperature optimum','optimum temperature']:
                            		t_write = meta[keys]
                            		f.write(str('{},{},{}\n'.format(organism,locus,t_write)))
                            		f.flush()
                            	else:
                            		pass
                            		
                #for annotation in seq_record.annotations:
                #    print(f"{annotation} = {seq_record.annotations[annotation]}")


f.close()
