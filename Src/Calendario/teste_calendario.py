from calendario import Calendario
import holidays

def main():

    """
    feriados = holidays.country_holidays('BR')
    for feriado in feriados["2024-01-01":"2024-12-31"]:
        nome_feriado = holidays.country_holidays('BR').get(feriado)
        print(feriado, nome_feriado)
    """

    calendario = Calendario()

    log = calendario.criar_evento('17/09/2024', '17/09/2024', True, 'Aniversario Teste Teste Teste')
    log2 = calendario.criar_evento('18/09/2024', '19/09/2024', False, 'Aniversario Teste Teste')
    log2 = calendario.criar_evento('18/09/2024', '19/09/2024', False, 'Zoro')
    log2 = calendario.criar_evento('18/09/2024', '19/09/2024', True, 'Luffy')
    eventos = calendario.eventos_por_mes(9)
    #print(calendario.eventos)
    print(eventos)


if __name__ == '__main__':
    main()