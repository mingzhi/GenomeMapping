"""Dump SRA to fastq using sra-tools from NCBI"""
from __future__ import print_function
import sys
from os import remove
from multiprocessing import cpu_count
from subprocess import call
from os.path import join, exists
from tqdm import tqdm

def smalt_map(reference, read, workspace):
    """smalt mapping"""
    read1 = join(workspace, read + "_1.fastq")
    read2 = join(workspace, read + "_2.fastq")
    outfile = join(workspace, read + ".sam")
    cpus = cpu_count()

    if exists(read1) and exists(read2):
        cmd = ['smalt', 'map', '-n', str(cpus), '-o', outfile, reference, read1, read2]
        call(cmd)
    else:
        single = join(workspace, read + ".fastq")
        cmd = ['smalt', 'map', '-n', str(cpus), '-o', outfile, reference, single]
        call(cmd)

def sam_sort(read, workspace):
    sam_file = join(workspace, read + '.sam')
    bam_file = join(workspace, read + '.sorted.bam')
    cmd = ['samtools', 'sort', '-@', '20', '-T', '/tmp/sort'+read, '-o', bam_file, sam_file]
    call(cmd)
    cmd = ['samtools', 'index', bam_file]
    call(cmd)
    remove(sam_file)

def main(argv):
    """Dump SRA to fastq using sra-tools from NCBI"""
    sample_file = argv[0]
    reference = argv[1]
    workspace = argv[2]
    with open(sample_file) as f:
        samples = [line.rstrip() for line in f]
    for read in tqdm(samples):
        smalt_map(reference, read, workspace)
        sam_sort(read, workspace)

if __name__ == "__main__":
    main(sys.argv[1:])
