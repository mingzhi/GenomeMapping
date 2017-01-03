"""Dump SRA to fastq using sra-tools from NCBI"""
from __future__ import print_function
import sys
from subprocess import call
from multiprocessing import cpu_count
from os.path import join
from joblib import Parallel, delayed
from tqdm import tqdm
from Utils import read_samples

def dump_sra(sra_file, workspace):
    """Dump sra file into 3 fastq files"""
    cmd = ["fastq-dump", "--split-3", sra_file, '-O', workspace]
    call(cmd)

def main(argv):
    """Dump SRA to fastq using sra-tools from NCBI"""
    sample_file = argv[0]
    workspace = argv[1]
    workspace = "../workspace"
    samples = read_samples(sample_file)
    sra_files = [join(workspace, sample+".sra") for sample in samples]
    print("Dump SRA to fastq...")
    Parallel(n_jobs=cpu_count())(delayed(dump_sra)
                                 (sra_file, workspace) for sra_file in tqdm(sra_files))

if __name__ == "__main__":
    main(sys.argv[1:])
