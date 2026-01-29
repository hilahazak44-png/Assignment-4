# מילון שמכיל את אנזימי הרסטריקציה ואת אתרי החיתוך שלהם
enzymes = {
    "DsaI": ["CCGTGG", "CCATGG"],
    "SecI": ["CCGTGG", "CCATGG", "CCAGGG"],
    "Cjul": ["CACTAAAGATG", "CATTAAAAGTG", "CACTAGAAATG"]
}


# פונקציה שבודקת רצף גנטי ומחזירה את אתרי הרסטריקציה שנמצאו בו
def check_sequence(sequence):
    results = {}  # מילון לשמירת התוצאות

    # מעבר על כל אנזים
    for enzyme in enzymes:
        sites = []  # רשימה לאתרים שנמצאו
        # מעבר על כל אתר חיתוך של האנזים
        for s in enzymes[enzyme]:
            if s in sequence:  # בדיקה אם האתר נמצא ברצף
                sites.append(s)

        # אם נמצאו אתרים , שמירה במילון התוצאות
        if len(sites) > 0:
            results[enzyme] = sites

    return results  # החזרת התוצאות


# פתיחת קובץ הקלט לקריאה וקובץ הפלט לכתיבה
file = open("data/orf_coding_all.fa.txt", "r")
out = open("results/List_Yeast_ORFs_RestSites.txt", "w")

genes_counter = 0      # מונה גנים עם לפחות אתר רסטריקציה אחד
gene_name = ""         # משתנה לשמירת שם הגן
sequence = ""          # משתנה לשמירת רצף הגן

# קריאה כל שורה מקובץ הפסטה
for line in file:
    line = line.strip()  # הסרת רווחים מיותרים

    # אם השורה מתחילה ב">" זהו גן חדש
    if line.startswith(">"):
        if gene_name != "":
            # בדיקת רצף הגן הקודם
            found = check_sequence(sequence)

            # אם נמצאו אתרים
            if len(found) > 0:
                genes_counter += 1
                out.write(gene_name + "\n")

                # הדפסת התוצאות לכל אנזים
                for enzyme in found:
                    out.write(
                        "There are " + str(len(found[enzyme])) + " " + enzyme + " sites:\n"
                    )
                    for site in found[enzyme]:
                        out.write(enzyme + " site: " + site + "\n")
                    out.write("\n")

        # התחלת גן חדש
        gene_name = line
        sequence = ""

    else:
        # הוספת השורה לרצף הגן
        sequence += line


# טיפול בגן האחרון בקובץ
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

# (הדפסת סיכום (מספר הגנים עם לפחות אתר רסטריקציה אחד
out.write("Number of Protein with any kind of site: " + str(genes_counter))

# סגירת הקבצים
file.close()
out.close()
