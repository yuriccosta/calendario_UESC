from calendario import Calendario

def main():
    calendario = Calendario()

    log = calendario.criar_evento('15/09/2024', 'Aniversario Beltrano')
    eventos = calendario.eventos_por_mes(9)
    print(eventos)


if __name__ == '__main__':
    main()