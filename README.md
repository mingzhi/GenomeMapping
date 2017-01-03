# Genome mapping from sequencing reads.

## Pipeline:
- FetchSRA.py
    fetch read .sra files from NCBI SRA ftp site.
- DumpSRA.py
    dump .sra files to generate fastq files.
- SmaltMap.py
    map reads against a reference genome using smalt.
- InvokeFreebayes.sh
    do SNP calling using freebayes.
- ConcensusGenome
