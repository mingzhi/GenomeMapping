"""Fetch SRA data from NCBI ftp"""
from __future__ import print_function
import sys
from os.path import join
from ftplib import FTP
from progressbar import ProgressBar
from Utils import check_folder, read_samples

def main(argv):
    """Fetch SRA data from NCBI ftp"""
    sample_file = argv[0]
    workspace = argv[1]
    samples = read_samples(sample_file)

    ftp = FTP("ftp.ncbi.nlm.nih.gov")
    ftp.login("anonymous", "mingzhi9@gmail.com")
    ftp.cwd("sra/sra-instant/reads/ByRun/sra")

    print("Fetching SRA from NCBI ftp...")
    pbar = ProgressBar()
    for sample in pbar(samples):
        dir_path = "%s/%s/%s" % (sample[:3], sample[:6], sample)
        run_path = dir_path + "/" + sample + ".sra"
        local_file_path = join(workspace, sample + ".sra")
        local_file = open(local_file_path, 'wb')
        ftp.retrbinary('RETR %s' % run_path, local_file.write)
        local_file.close()
    ftp.quit()

if __name__ == "__main__":
    main(sys.argv[1:])
