from lista_eventos import ListaEventos
import holidays

def main():

    """
    feriados = holidays.country_holidays('BR')
    for feriado in feriados["2024-01-01":"2024-12-31"]:
        nome_feriado = holidays.country_holidays('BR').get(feriado)
        print(feriado, nome_feriado)
    """

    calendario = ListaEventos()

    log = calendario.criar_evento('17/09/2024', '17/09/2024', 'Aniversario Teste Teste Teste', True)
    log2 = calendario.criar_evento('18/09/2024', '19/09/2024', 'Aniversario Teste Teste', False)
    log2 = calendario.criar_evento('18/09/2024', '19/09/2024', 'Zoro', False)
    log2 = calendario.criar_evento('18/09/2024', '19/09/2024', 'Luffy', True)
    log2 = calendario.criar_evento('18/10/2024', '19/10/2024', 'Luffyssss', True)
    log2 = calendario.criar_evento('18/10/2024', '25/10/2024', 'Inscricao estagio', True)
    eventos = calendario.busca_eventos()
    print(eventos)


if __name__ == '__main__':
    main()