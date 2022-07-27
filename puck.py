

dec = {
    'zero': "(+all([[]]))",
    'one': "(+all([]))"
}

number = lambda x : '+'.join([str(dec['one']) for i in range(x)])

q = "'"
chars = {
    "c": f'str(str)[{number(1)}]',
    "h": f"str(chr)[-({number(3)})]",
    "r": f"str(chr)[-({number(2)})]",
    "o": f'str(ord)[-({number(4)})]',
    "d": f"str(ord)[-({number(2)})]",
}

def create_char(char):
    c = f"{chars['o']}+{chars['r']}+{chars['d']}"
    return f'chr(eval({q}{number(eval(eval(c)+f"({q}{char}{q})"))}{q}))'


print(chars)
print(dec)  
print(number(7))