import re

de_verses = "/Users/harega/Desktop/net-copy.txt"
f = open(de_verses, "r")

csv_lines = [
    "time,ms",
]

first_line = f.readline().replace("(", "").replace(")", "").replace(":", "").strip()
[ping, address, ip, size, str1, str2] = first_line.split(" ")

for line in f.readlines():
    newLine = ""
    if line.replace("Request timeout for", "") is line:
        parts = line.split(" ")
        newLine = "\"{date}\",\"{ms}\"".format(date=parts[0], ms=parts[-2].replace("time=", ""))
    else:
        # request timeout
        # newLine = line.replace("", "").strip()
        newLine = "-,10000"

    csv_lines.append(newLine)


print("\n".join(csv_lines))


with open("/Users/harega/Desktop/net-copy.csv", "w") as f:
    for line in csv_lines:
        f.write(line)
        f.write("\n")

# print("\n".join(csv_lines))
