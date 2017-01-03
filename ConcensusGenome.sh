module load parallel
module load samtools
export sample_file=$1
export genome=$2
export workspace=$3
concensus() {
    read=$1
    # samtools mpileup -q 30 -f ${genome} ${read}.sorted.bam | concensus_genome --fna_file ${genome} --out_file ${read}.pileup.fasta
    samtools mpileup -q 30 -f ${genome} ${workspace}/${read}.sorted.bam | genome_construct --fasta_file ${genome} --vcf_file ${workspace}/${read}.freebayes.vcf --out_file ${workspace}/${read}.freebayes.fasta --sample ${read}
    echo ${read}
}
export -f concensus
parallel concensus :::: ${sample_file}

