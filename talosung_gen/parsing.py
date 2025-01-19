import re
print("start")

f = open("./Tanach.txt/TextFiles/Amos.txt", "r")
for line in f.readlines():
    print(line.strip())
    #noDashes = re.sub("(-){1,3}", " ", line.replace("\u202c", "").replace("\xa0\xa0\xa0", "").replace("‪xxxx‬", ""))
    print(
        line
        .replace("\u202c", "")
        .replace("\xa0\xa0\xa0", "")
        .replace("‪xxxx‬", "")
        .strip()
    )
    #print(re.findall("(\d+)(.*)", noDashes), "\n")
