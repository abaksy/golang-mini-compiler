import sys

filename = sys.argv[1]
tac_file = filename.split(".")[0]+"_three_addr_code.txt"
code = []
with open(tac_file, "r") as f:
    tac = f.read().split("\n")
    tac = [eval(line) for line in tac if line != '']
print(tac)    

