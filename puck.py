import argparse


dec = {
    'zero': "(+all([[]]))",
    'one': "(+all([]))",
    'two': "(len(([[],[]])))",
}

number = lambda x : '+'.join([str(dec['one']) for i in range(x)])

#unused
def gen_number(n):
    if n % 2 == 0:
        # even
        pass
    else:
        # odd
        pass

q = "'"
p = '"'
chars = {
    "c": f'str(str)[{number(1)}]',
    "h": f"str(chr)[-({number(3)})]",
    "r": f"str(chr)[-({number(2)})]",
    "o": f'str(ord)[-({number(4)})]',
    "d": f"str(ord)[-({number(2)})]",
    'n': f"str(eval)[{number(8)}]",
    'u': f"str(eval)[{number(2)}]",
    '\'': f"str(str)[{number(7)}]",
    'o': f"str(eval)[eval(str({number(1)})+str({number(6)}))]",
    'f': f"str(all)[{number(10)}]",
    '\n': f"(chr({number(10)}))",
    '\\': f"chr({number(92)})",
}

def create_char(char):
    c = f"{chars['o']}+{chars['r']}+{chars['d']}"
    return f'chr(eval({q}{number(eval(eval(c)+f"({q}{char}{q})"))}{q}))'



# expected: file_name.py
def compile_file(fn):
    with open(fn, 'r') as f:
        s = f.read()
        lf = []
        for char in s:
            if not char.isdigit() and char not in chars:
                lf.append(create_char(char))
            elif char in chars:
                lf.append(chars[char])
            if char.isdigit():
                lf.append(create_char(char))
        with open(fn + '.puck', 'w') as f:
            ln = f.write(f"s=eval({p}{'+'.join(lf)}{p});exec(s)")
        print(f'compiled {ln}b to {fn}.puck')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file', help='file to compile')
    args = parser.parse_args()
    compile_file(args.file)
    