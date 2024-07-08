from Src.eventos.lista_eventos import ListaEventos

def main():
    """
    Utilize este arquivo para testar funcionalidades especificas da classe eventos.
    """
    v = ListaEventos()

    v.criar_evento('09/07/2024', 'Encerramento semestre 2024/1')
    v.criar_evento('10/07/2024', 'Trabalho de Prog')
    v.criar_evento('12/08/2024', 'Inicio semestre 2024/2')

    lista_eventos_mes = v.eventos_por_mes(7, 2024)
    print(lista_eventos_mes)
    
    """
    for data in v.eventos:
        print(data)
        for evento in v.eventos[data]:
            print(evento)
    """
    

if __name__ == '__main__':
    main()