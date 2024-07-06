from datetime import datetime
from collections import defaultdict

class Eventos:

    def __init__(self) -> None:
        self.__eventos = defaultdict(set)
        self.__carregar_eventos()

    @property
    def eventos(self):
        return self.__eventos
    

    def eventos_por_mes(self, mes: int, ano: int = 2024):
        """
        O método retorna todos os eventos referentes a determinado mês/ano.
        Por padrão se apenas passar o mês, vai entender que está se referindo ao mês de 2024.
        """
        lista_eventos_mes = []
        for data in self.__eventos:
            aux = data.split('/')
            lista_eventos_mes.append(aux)

        lista = []
        for i, aux in enumerate(lista_eventos_mes):
            if int(aux[1]) == mes and int(aux[2]) == ano:
                data = f'{lista_eventos_mes[i][0]}/{lista_eventos_mes[i][1]}/{lista_eventos_mes[i][2]}'
                for evento in self.__eventos[data]:
                    lista.append([data, evento])

        return lista


    def criar_evento(self, data: str, evento: str):
        """
        Cria um novo evento e retorna uma string para ser usado no front.
        """
        if self.__verifica_data(data):
            self.__eventos[data].add(evento)
            self.__salvar_eventos()
            return 'Evento registrado com sucesso!'
        else:
            return 'Data invalida! Digite uma data atual ou futura!'


    def __verifica_data(self, data_str: str):
        """
        Verifica se a data é do dia ou futura, caso contrário retorna Falso.
        """
        formato_data = '%d/%m/%Y'

        try:
            data = datetime.strptime(data_str, formato_data).date()
            data_atual = datetime.now().date()
            return data >= data_atual
        except ValueError:
            print('Data invalida!')
            return False


    def __carregar_eventos(self):
        """
        Tenta inicializar um arquivo de texto de eventos, se não existir o dicionário
        já será inicializado vazio.
        """
        try:
            with open('eventos.txt', 'r') as file:
                for line in file:
                    data, evento = line.strip().split(' - ')
                    self.__eventos[data].add(evento)
        except FileNotFoundError:
            pass

    
    def __salvar_eventos(self):
        """
        Método auxiliar ao método cria_eventos, apenas salva um novo evento no arquivo txt.
        """
        with open('eventos.txt', 'w') as file:
            for data, eventos in self.__eventos.items():
                for evento in eventos:
                    file.write(f'{data} - {evento}\n')