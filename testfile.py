import re
from colorama import init, Fore

def view_color(tab):
    if tab[0]=="ROUGE":
        print(Fore.RED + "\t" + tab[1], end="")
    elif tab[0]=="BLEU":
        print(Fore.BLUE + "\t" + tab[1], end="")
    elif tab[0]=="VERT":
        print(Fore.GREEN + "\t" + tab[1], end="")
    elif tab[0]=="JAUNE":
        print(Fore.YELLOW + "\t" + tab[1], end="")
    elif tab[0]=="BLANC":
        print(Fore.WHITE + "\t" + tab[1], end="")
    else:
        return



init()
string = "asa has these cards : ('ROUGE', 1) ('BLEU', 4) ('JAUNE', 5) ('BLEU', 5) ('ROUGE', 3) \nasa has these cards : ('ROUGE', 1) ('BLEU', 4) ('ROUGE', 5) ('BLEU', 5) ('ROUGE', 3)\n"

lines = string.split("\n")

#remove the empty last line
lines.pop()

#search for something starting and ending with () and has a string then , then an int
pattern = re.compile(r"\('(.*?)', (\d+)\)")

for line in lines:

    parts = line.split(":")

    matches = pattern.findall(parts[1])

    print(f"{parts[0]} : ")

    for match in matches:
        view_color(match)

    print(Fore.RESET + "")

