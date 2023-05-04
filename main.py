import sys

def print_help():
    print("Usage: python3 ./run_sp2.py -i <input file> -o <output file>")
    sys.exit()

if(len(sys.argv) != 5):
    help("Usage: python3 ./run_sp2.py -i <input file> -o <output file>")

if(sys.argv[1] != "-i" and sys.argv[3] != "-o"):
    help()

input_file = sys.argv[2].strip()
output_file = sys.argv[4].strip()

with open(input_file) as f:
    lines = f.read().splitlines()