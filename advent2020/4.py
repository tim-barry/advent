import sys

passports = [pp.strip().split() for pp in sys.stdin.read().split('\n\n')]

all_fields={"byr","iyr","eyr","hgt","hcl","ecl","pid","cid"}
req_fields = all_fields - {"cid"}

def valid(pp, part=1):
    if not ({s[:3] for s in pp}>= req_fields): return False
    if part == 1: return True
    #part 2
    for s in pp:
        f, v = s.split(":")
        if f=="byr":
            if len(v)==4 and all(map(str.isdigit,v)) and 1920<=int(v)<=2002:
                continue
        elif f=="iyr":
            if len(v)==4 and all(map(str.isdigit,v)) and 2010<=int(v)<=2020:
                continue
        elif f=="eyr":
            if len(v)==4 and all(map(str.isdigit,v)) and 2020<=int(v)<=2030:
                continue
        elif f=="hgt":
            if v.endswith("cm") and 150<=int(v[:-2])<=193:
                continue
            if v.endswith("in") and 59<=int(v[:-2])<=76:
                continue
        elif f=="hcl" and v[0]=="#" and all(c.isdigit() or c in "abcdef" for c in v[1:]):
            continue
        elif f=="ecl" and v in "amb blu brn gry grn hzl oth".split():
            continue
        elif f=="pid" and len(v)==9 and v.isdigit():
            continue
        elif f=="cid":
            continue
        return False
    return True

print(sum(map(valid, passports)))

