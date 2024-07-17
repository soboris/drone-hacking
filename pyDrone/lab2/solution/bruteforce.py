import sys
import re

regex = r"b\'([0-9A-Fa-f]{18})\'"
n = 256
tolerance = 2

def guess(series):
    prev = None
    for x in series:
        if prev is None:
            prev = x
            continue
        if x < prev or x - prev > tolerance:
            return False
        prev = x
    return True

def main():
    if len(sys.argv) > 1:
        try:
            f = open(sys.argv[1], "r")
            lines = f.readlines()
            candidates = {}
            for i in range(n):
                series = []
                for line in lines:
                    match = re.search(regex, line)
                    if match:
                        xored = match.group(1)[-2:]
                        c = [_a ^ _b for _a, _b in zip(bytearray.fromhex(xored), i.to_bytes())][0]
                        series.append(c)
                    else:
                        print("No match")
                if guess(series):
                    candidates[i] = series
            print("Potential candidates")
            print("-" * 20)
            for candidate in candidates:
                print(str(candidate) + " - " + " ".join(str(x) for x in candidates[candidate]))
        except IOError:
            print("Cannot open file")
    else:
        print("Program argument: <captured data file>")

if __name__ == "__main__":
    main()
