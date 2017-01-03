module load parallel
export sample_file=$1
export reference=$2
export workspace=$3
freebayes_vcf() {
    read=$1
    freebayes -f ${reference} --ploidy 1 ${workspace}/${read}.sorted.bam > ${workspace}/${read}.freebayes.vcf
    echo ${read}
}
export -f freebayes_vcf
parallel freebayes_vcf :::: ${sample_file}

