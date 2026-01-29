# אתרי הרסטריקציה
enzymes = {
    "DsaI": ["CCGTGG", "CCATGG"],
    "SecI": ["CCGTGG", "CCATGG", "CCAGGG"],
    "Cjul": ["CACTAAAGATG", "CATTAAAAGTG", "CACTAGAAATG"]
}


def check_sequence(sequence):
    results = {}

    for enzyme in enzymes:
        sites = []
        for s in enzymes[enzyme]:
            if s in sequence:
                sites.append(s)

        if len(sites) > 0:
            results[enzyme] = sites

    return results


# פתיחת קבצים (פעם אחת בלבד!)
file = open("data/orf_coding_all.fa.txt", "r")
out = open("results/List_Yeast_ORFs_RestSites.txt", "w")

genes_counter = 0
gene_name = ""
sequence = ""

for line in file:
    line = line.strip()

    if line.startswith(">"):
        if gene_name != "":
            found = check_sequence(sequence)

            if len(found) > 0:
                genes_counter += 1
                out.write(gene_name + "\n")

                for enzyme in found:
                    out.write(
                        "There are " + str(len(found[enzyme])) + " " + enzyme + " sites:\n"
                    )
                    for site in found[enzyme]:
                        out.write(enzyme + " site: " + site + "\n")
                    out.write("\n")

        gene_name = line
        sequence = ""

    else:
        sequence += line


# טיפול בגן האחרון
found = check_sequence(sequence)
if len(found) > 0:
    genes_counter += 1
    out.write(gene_name + "\n")

    for enzyme in found:
        out.write(
            "There are " + str(len(found[enzyme])) + " " + enzyme + " sites:\n"
        )
        for site in found[enzyme]:
            out.write(enzyme + " site: " + site + "\n")
        out.write("\n")

out.write("Number of Protein with any kind of site: " + str(genes_counter))

file.close()
out.close()

