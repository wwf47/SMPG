outfile = open("./yago/concept.txt", "w")

with open("./yago/yagoSimpleTaxonomy.tsv","r") as f:
    for line in f.readlines():
        t = line.strip().split('\t')
        c = t[0]
        sub = t[2]
        print(c+'\t'+sub,sep='',file=outfile)
outfile.close()
