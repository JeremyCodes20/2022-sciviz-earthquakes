INTERSTATES = {'I-5', 'I-280', 'I-880 ', 'I-40', 'I-15', 'I-80', 'I-405 ', 'I-80BR', 'I-10', 'I-405', 'I-210', 'I-680',
               'I-305', 'I-580', 'I-580 ', 'I-210 ', 'I-110', 'I-8', 'I-710 ', 'I-280 ', 'I-605', 'I-680 '}

HIGHWAYS = {'ST-134', 'ST-14', 'ST-2', 'ST-92', 'ST-156', 'ST-139', 'ST-84', 'ST-135', 'ST-33', 'ST-22', 'ST-17 ',
            'ST-1', 'ST-18', 'ST-62', 'ST-3', 'ST-118', 'ST-58', 'ST-7', 'ST-99', 'ST-17', 'ST-178', 'ST-16',
            'ST-36', 'ST-85', 'ST-140', 'ST-113', 'ST-70 ', 'ST-14 ', 'ST-99 ', 'ST-166', 'ST-79', 'ST-46', 'ST-120',
            'ST-43', 'ST-299', 'ST-12', 'ST-51', 'ST-20', 'ST-116', 'ST-128', 'ST-162', 'ST-138', 'ST-23', 'ST-89'}

US_HIGHWAYS = {'US-50 ', 'US-50', 'US-101', 'US-395', 'US-95'}


def main():
    create_files()
    f = open("../data/ca_hiwys.main.asc")
    files = [open("../data/highways/all.csv", "w+")]
    files[0].write("X,Y\n")
    files[0].close()
    files = [open("../data/highways/all.csv", "a")]
    for line in f:
        if "segment" in line:
            continue
            for f in files:
                f.close()
            highways_in_segment = get_highways(line)
            files = open_files(highways_in_segment)
            files.append(open("../data/highways/all.csv", "a"))
        else:
            if "X Y" in line: continue
            for f in files:
                if len(files) > 1:
                    print("\tadding", line[:-1], "to", f.name)
                f.write(line.lstrip().replace(" ", ","))


def open_files(highways):
    files = []
    for name in highways:
        files.append(open("../data/highways/" + name + ".csv", "a"))
    return files

def create_files():
    for i in INTERSTATES:
        f = open("../data/highways/" + i + ".csv", "w+")
        f.write("X,Y\n")
        f.close()
    for s in HIGHWAYS:
        f = open("../data/highways/" + s + ".csv", "w+")
        f.write("X,Y\n")
        f.close()
    for u in US_HIGHWAYS:
        f = open("../data/highways/" + u + ".csv", "w+")
        f.write("X,Y\n")
        f.close()

def get_highways(line):
    highways_in_segment = line.split(",")[0].split("&")
    filter_highways(highways_in_segment)
    return highways_in_segment

def filter_highways(highways):
    for i in range(len(highways)):
        highways[i] = highways[i].strip("segment ")
        if "Š" in highways[i]:
            highways[i] = highways[i][0:highways[i].find("Š")].strip()
    while "" in highways:
        highways.remove("")


main()
