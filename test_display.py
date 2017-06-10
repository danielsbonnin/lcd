import display
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("line")
parser.add_argument("-v", "--vertical", help="vertical scrolling", action="store_true")
parser.add_argument("-r", "--reps", help="number of reps", type=int)
args = parser.parse_args()
d = display.Display()
reps = 1
if args.reps:
    reps = int(args.reps)
if args.vertical == True:
    d.verticalscroll(args.line, reps)
else:
    d.linescroll(args.line, reps)
