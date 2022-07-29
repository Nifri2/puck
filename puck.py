import argparse

# you can do everythingusing one and zero, but the other numbers reduce file size and partially prenvent recursion errors
# the goal is to keep them smaller then the only ones counterpart
dec = {
    'zero': "(+all([[]]))",
    'one': "(+all([]))",
    'two': "(len([[],[]]))",
    'three': '(+all([])+(len([[],[]])))',
    'four': '(len([[],[]])+len([[],[]]))',
    'five': '(len([[],[]])+(+all([])+(len([[],[]]))))',
    'nine': "(len([[],[],[],[],[],[],[],[],[]]))"
}

number = lambda x,n : '+'.join([str(dec[n]) for i in range(x)])

q = "'"
p = '"'

# characters that get used a lot, shortend. otherwise a char would be the lenght of like 500 chars
# greatly reduces file size and recursion errors

chars = {
    '\n':   f"(chr({number(10, 'one')}))",
    '"':    f"chr({number(17, 'two')})",
    "'":    f"str(str)[{number(7, 'one')}]",
    '\\':   f"chr({number(23, 'four')})",
    'a':    f"str(set)[{number(1, 'three')}]",
    'c':    f'str(str)[{number(1, "one")}]',
    'd':    f"str(ord)[-({number(1, 'two')})]",
    'e':    f"str(set)[-{number(1, 'four')}]",
    'f':    f"str(all)[{number(10, 'one')}]",
    'h':    f"str(chr)[-({number(1, 'three')})]",
    'i':    f"str(list)[-({number(1, 'four')}+{number(1, 'one')})]",
    'n':    f"str(eval)[{number(2, 'four')}]",
    'o':    f"str(eval)[eval(str({number(1,'one')})+str({number(2,'three')}))]",
    'r':    f"str(chr)[-({number(1, 'two')})]",
    's':    f"str(str)[{number(1, 'four')}]",
    't':    f"str(list)[-{number(1, 'three')}]",
    'u':    f"str(eval)[{number(1, 'two')}]",
    "#":    f"chr({number(7, 'five')})",
    '[':    f"chr(int(str({number(1, 'nine')})+str({number(1, 'one')})))",
 }

# this aswell reduces file size and recursion errors
def gen_number(n):
    n = ord(n)
    if  n % 9 == 0:
        n //= 9
        return f'chr(eval({q}{number(n, "nine")}{q}))'
    elif  n % 5 == 0:
        n //= 5
        return f'chr(eval({q}{number(n, "five")}{q}))'
    elif n % 4 == 0:
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
    nf = "import sys\nsys.setrecursionlimit(8**10)\n"
    lf = []
    for char in nf:
        if not char.isdigit() and char not in chars:
            lf.append(gen_number(char))
        elif char in chars:
            lf.append(chars[char])
        if char.isdigit():
            lf.append(gen_number(char))
    with open('pucked_' + fn, 'w') as f:
            ln = f.write(f"s=eval({p}{'+'.join(lf)}{p});exec(s);")
    lf = []
    with open(fn, 'r') as f:
        s = f.read()
        for char in s:
            if not char.isdigit() and char not in chars:
                lf.append(gen_number(char))
            elif char in chars:
                lf.append(chars[char])
            if char.isdigit():
                lf.append(gen_number(char))
        with open('pucked_' + fn, 'a') as f:
            ln = f.write(f"s=eval({p}{'+'.join(lf)}{p});exec(s)")
        print(f'compiled {ln}b to pucked_{fn}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file', help='file to compile')
    args = parser.parse_args()
    compile_file(args.file)
    