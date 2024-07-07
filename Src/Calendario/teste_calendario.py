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

    log = calendario.criar_evento('17/09/2024', '17/09/2024', 'Aniversario Teste Teste Teste')
    eventos = calendario.eventos_por_mes(9)
    print(eventos)


if __name__ == '__main__':
    main()