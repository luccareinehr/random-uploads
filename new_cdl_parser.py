import argparse, re

parser = argparse.ArgumentParser(description="Converts given input cdl netlist into an ngspice netlist.")
parser.add_argument("--inputCdl", "-i", required=True, help="input cdl netlist")
parser.add_argument("--stdCdl", "-s", required=True, help="standard cells CDL netlist")
parser.add_argument("--outputCdl", "-o", required=True, help="output CDL netlist")

args = parser.parse_args()

# testing --------------------------------------------
class Args:
    def __init__(self, stdCdl, inputCdl):
        self.stdCdl = stdCdl
        self.inputCdl = inputCdl

args = Args(
    "/home/lucca/GSoC/originalRepo/OpenFASOC/openfasoc/common/platforms/sky130hd/cdl/sky130_fd_sc_hd.spice",
    "/home/lucca/GSoC/originalRepo/OpenFASOC/openfasoc/generators/temp-sense-gen/flow/results/sky130hd/tempsense/6_final.cdl"
    )
# testing --------------------------------------------

# get actual pin order from stdCdl netlist
with open(args.stdCdl, "r") as rf:
    filedata = rf.read()

stdCdl_pin_order = {}
std_cells_re = re.findall("\.subckt (.*)", filedata)
for std_cell in std_cells_re:
    std_cell_info = std_cell.split(" ")
    # std_cell_info = 'SubcktName': [N1 N2 ... Nn]
    stdCdl_pin_order[std_cell_info[0]] = std_cell_info[1:]

# get pin order from inputCdl netlist
with open(args.inputCdl, "r") as rf:
    filedata = rf.read()

ckt_re = re.search("(\.SUBCKT.*\n(\+.*\n)*)((.*\n)*)(\.ENDS.*)", filedata)
ckt_head = ckt_re.group(1)
ckt_cells = ckt_re.group(3)
ckt_end = ckt_re.group(5)
ckt_cells = ckt_cells.replace("\n+", "").split("\n")[:-1] # removes trailing '\n' split

inputCdl_cells = {}
for cell in ckt_cells:
    cell_info = cell.split(" ")
    # cell_info = 'CompName': {'pins': [N1 N2 ... Nn], 'subckt': SubcktName}
    inputCdl_cells[cell_info[0]] = {
        'pins': cell_info[1:-1],
        'subckt': cell_info[-1]
        }

outputCdl_cells = inputCdl_cells
for cell in outputCdl_cells:
    cell_pin_order = outputCdl_cells[cell]['pins']
    std_pin_order = stdCdl_pin_order[outputCdl_cells[cell]['subckt']] # std pin order for the cell

    std_pin_order # we want this order
    cell_pin_order # with these pin names
    # but what's the equivalence between them? (don't insert it manually)
