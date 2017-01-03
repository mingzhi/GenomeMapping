"""Util functions"""
import gzip
from sqlite3 import connect
from os.path import exists, join
from os import makedirs

def check_folder(folder_path):
    """Check if the folder exists. If not, it will create it."""
    if not exists(folder_path):
        makedirs(folder_path)

def read_samples(sample_file):
    """Read a list of sample names from a file"""
    samples = []
    with open(sample_file) as infile:
        for line in infile:
            if len(line.rstrip()) > 0:
                samples.append(line.rstrip())
    return samples

def get_file_extension(filename):
    """Get file extension."""
    terms = filename.split('.')
    return terms[len(terms)-1]

def open_file(filename):
    """Open a file according to the file type."""
    fileextension = get_file_extension(filename)
    if fileextension == 'gz':
        infile = gzip.open(filename, 'r')
    else:
        infile = open(filename, 'r')
    return infile

class Sequence(object):
    """A sequence"""
    def __init__(self, seqid, seq):
        self.seqid = seqid
        self.seq = seq

def read_fasta(filename, getid):
    """Read sequences from a fasta file."""
    infile = open_file(filename)
    records = []
    currentid = None
    seq = ""
    for line in infile:
        if line.startswith('>'):
            seqid = getid(line.rstrip())
            if seqid != currentid:
                if currentid is not None:
                    records.append(Sequence(currentid, seq))
                currentid = seqid
                seq = ""
        else:
            seq = seq + str(line.rstrip())
    if currentid != "":
        records.append(Sequence(currentid, seq))
    infile.close()
    return records

class GFFRecord(object):
    """GFF record"""
    def __init__(self, terms):
        self.genome = terms[0]
        self.source = terms[1]
        self.feature = terms[2]
        self.start = int(terms[3])
        self.end = int(terms[4])
        if terms[5] != '.':
            self.score = float(terms[5])
        else:
            self.score = 0
        self.strand = terms[6]
        self.frame = terms[7]
        self.attribute = terms[8]

    def get_protein_id(self):
        """get protein id"""
        terms = self.attribute.split(";")
        for term in terms:
            fields = term.split("=")
            key = fields[0]
            value = fields[1]
            if key == "protein_id":
                return value
        return None

def read_gff(filename):
    """Read gff records from a gff file"""
    records = []
    infile = open_file(filename)
    for line in infile:
        if line.startswith('#'):
            continue
        terms = line.rstrip().split("\t")
        if len(terms) == 9:
            gff = GFFRecord(terms)
            records.append(gff)
    infile.close()
    return records

def write_fasta(outfile, seqs):
    """Write sequences into a file in fasta format"""
    out = open(outfile, 'w')
    for seq in seqs:
        out.write(">" + seq.seqid + "\n")
        out.write(seq.seq + "\n")
    out.close()

def query_clusters(conn):
    """Query distinc cluster names from db"""
    cur = conn.cursor()
    sql = "select distinct cluster from cluster"
    cur.execute(sql)
    clusters = []
    for row in cur.fetchall():
        clusters.append(row[0])
    return clusters
