import linecache, re, sys

pattern = re.compile(r'^(n\d+) (.*)$')

def get_label(i):
    line = linecache.getline('synset_words.txt', i+1).strip()
    m = pattern.match(line)
    if m:
        return (m.group(1), [i.strip() for i in m.group(2).split(',')])

if __name__ == "__main__":
    if len(sys.argv)>1:
        print get_label(int(sys.argv[1]))
