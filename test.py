d = 'Цена 199,99 руб'
print("".join(filter(lambda d: str.isdigit(d) or d == ',', d)))
