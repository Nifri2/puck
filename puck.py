import argparse
import os

# this is a shitcode project dont expect S tier python


# numbers could be done in different way, but i likehow this looks
# i could use (+all([[]])) for everything, but wheres the fun in that?

dec = {
    'zero': "(+all([[]]))",
    'one': "(+all([]))",
    'two': "(int((str(len([[],[]]))[+(+all([[]]))])))",
    'three': '(int((str(len([[],[],[]])))))',
    'four': '(int(str(len(str(eval)))[-+all([])]))'
}

number = lambda x,n : '+'.join([str(dec[n]) for i in range(x)])

#  used chars, i wanted to do a different approach initially, but it somehow morphed into this
# i think i could remove it
q = "'"
p = '"'
chars = {
    "c": f'str(str)[{number(1, "one")}]',
    "h": f"str(chr)[-({number(1, 'three')})]",
    "r": f"str(chr)[-({number(1, 'two')})]",
    "o": f'str(ord)[-({number(1, "four")})]',
    "d": f"str(ord)[-({number(1, 'two')})]",
    'n': f"str(eval)[{number(2, 'four')}]",
    'u': f"str(eval)[{number(1, 'two')}]",
    '\'': f"str(str)[{number(7, 'one')}]",
    'o': f"str(eval)[eval(str({number(1,'one')})+str({number(6,'one')}))]",
    'f': f"str(all)[{number(10, 'one')}]",
    '\n': f"(chr({number(10, 'one')}))",
    '\\': f"chr({number(23, 'four')})",
    '"': f"chr({number(17, 'two')})",
    # ':': f"chr({number(58, 'two')})",
}

def create_char(char):
    c = f"{chars['o']}+{chars['r']}+{chars['d']}"
    return f'chr(eval({q}{number(eval(eval(c)+f"({q}{char}{q})"))}{q}))'


# number selection algorithm: 
# tis purpose is to reduce the size of the code that is generated
def gen_number(n):
    c = f"{chars['o']}+{chars['r']}+{chars['d']}"
    n = ord(n)
    if n % 4 == 0:
        n //= 4
        return f'chr(eval({q}{number(n, "four")}{q}))'
    elif n % 3 == 0:
        n //= 3
        return f'chr(eval({q}{number(n, "three")}{q}))'
    elif n % 2 == 0:
        n //= 2
        return f'chr(eval({q}{number(n, "two")}{q}))'
    elif n == 0:
        return f'chr(eval({q}{number(n, "zero")}{q}))'
    else:
        return f'chr(eval({q}{number(n, "one")}{q}))'

# expected: file_name.py
def compile_file(fn):
    lines = []
    with open(fn, 'r') as f:
        lines = f.readlines()
    nf = ["import sys\n", "sys.setrecursionlimit(10**6)\n"] # this should make everyone reading this sad
    for line in lines:
        nf.append(line)
    with open(fn + ".tmp", 'w') as f: # do i need files? no i dont, im still doing it
        f.writelines(nf)
    with open(fn + ".tmp", 'r') as f:
        s = f.read()
        lf = []
        for char in s:
            if not char.isdigit() and char not in chars:
                lf.append(gen_number(char))
            elif char in chars:
                lf.append(chars[char])
            if char.isdigit():
                lf.append(gen_number(char))
        with open('pucked_' + fn, 'w') as f:
            ln = f.write(f"s=eval({p}{'+'.join(lf)}{p});exec(s)")
        print(f'compiled {ln}b to pucked_{fn}')
    os.remove(fn + ".tmp")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file', help='file to compile')
    args = parser.parse_args()
    compile_file(args.file)
    