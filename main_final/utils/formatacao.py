def format(data:tuple | int) -> str:
    if type(data) is int:
        return f'{data}'
    if len(data) == 1:
        return f'{data[0]}'
    if data[1] - data[0] > 1:
        return f'{data[0]} a {data[1]}'
    return f'{data[0]} e {data[1]}'

def wrap_text(texto: str, tamanho_minimo = 50, tamanho_maximo = 200):
    contador = 0
    for i in range(0, len(texto) - 2):
        if texto[i] == '\n':
            contador = 0
        elif contador > tamanho_maximo and texto[i] == ' ':
            texto =  texto[:i] + '\n' + texto[i + 1:]
            contador = 0
        elif texto[i - 1] == '.' and texto[i] == ' ' and contador > tamanho_minimo:
            texto = texto[:i] + '\n' + texto[i + 1:]
            contador = 0
        elif contador > (tamanho_maximo + 10):
            texto = texto[:i] + '-\n' + texto[i + 1:]
            contador = 0
        else:
            contador += 1
    return texto

def height_text(text) -> int:
    height = 1
    for i in range(len(text)):
        if text[i] == '\n':
            height += 1
    return height
