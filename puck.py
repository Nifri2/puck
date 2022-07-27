

dec = {
    'zero': "(+all([[]]))",
    'one': "(+all([]))"
}

number = lambda x : '+'.join([str(dec['one']) for i in range(x)])

print(dec)
print(number(7))