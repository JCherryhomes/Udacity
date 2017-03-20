args = ['hello', 'there', 'you', 'silly', 'people']

def upper_case(text):
    return str.upper(text)

print(map(upper_case, args))

