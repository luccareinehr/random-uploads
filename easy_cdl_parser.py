import argparse, re, os

parser = argparse.ArgumentParser(description="Converts given input cdl netlist into an ngspice netlist.")
parser.add_argument("--inputCdl", "-i", required=True, help="input cdl netlist")
parser.add_argument("--stdCdl", "-s", required=True, help="standard cells CDL netlist")
parser.add_argument("--outputCdl", "-o", required=True, help="output CDL netlist")

args = parser.parse_args()

# testing --------------------------------------------
# class Args:
#     def __init__(self, stdCdl, inputCdl, outputCdl):
#         self.stdCdl = stdCdl
#         self.inputCdl = inputCdl
#         self.outputCdl = outputCdl
#
# args = Args(
#     "/home/lucca/GSoC/originalRepo/OpenFASOC/openfasoc/common/platforms/sky130hd/cdl/sky130_fd_sc_hd.spice",
#     "/home/lucca/GSoC/originalRepo/OpenFASOC/openfasoc/generators/temp-sense-gen/flow/results/sky130hd/tempsense/6_final.cdl",
#     "bacon.spice"
#     )
# testing --------------------------------------------

# since the pin order from 6_final.cdl is correct, only the file format has to be changed

with open(args.inputCdl, "r") as rf:
    filedata = rf.read()
    filedata = re.sub("r_VIN", "VIN", filedata) # header cell pin

ckt_re = re.search("(\.SUBCKT.*\n(\+.*\n)*)((.*\n)*)(\.ENDS.*)", filedata)
ckt_head = ckt_re.group(1)
ckt_cells = ckt_re.group(3)
ckt_end = ckt_re.group(5)
ckt_cells = ckt_cells.replace("\n+", "").split("\n")[:-1] # removes trailing '\n' split

with open(args.outputCdl, "w") as wf:
    wf.write(".INCLUDE '" + os.path.abspath(args.stdCdl) + "'\n") # include std cell definitions
    for cell in ckt_cells:
        wf.write(cell + "\n")
    wf.write(".end")
