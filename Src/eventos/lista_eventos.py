from datetime import datetime, timedelta
from collections import defaultdict

class ListaEventos:

    formatacao_data = '%d/%m/%Y'

    def __init__(self):
        self.__eventos = defaultdict(set)
        self.__carregar_eventos()


    @property
    def eventos(self) -> defaultdict:
        return self.__eventos
    

    def remover_evento(self):
        pass

    def eventos_por_mes(self, mes: int, ano: int = 2024) -> list[list]:
        """
        O método retorna todos os eventos referentes a determinado mês/ano.
        Por padrão se apenas passar o mês, vai entender que está se referindo ao mês de 2024.
        """
        lista_eventos = self.__lista_datas_eventos()
        lista = []
        for i, aux in enumerate(lista_eventos):
            if int(aux[1]) == mes and int(aux[2]) == ano:
                data = f'{lista_eventos[i][0]}/{lista_eventos[i][1]}/{lista_eventos[i][2]}'
                for evento in self.__eventos[data]:
                    descricao_evento, nao_funciona, dias = evento.split('-')
                    descricao_evento = descricao_evento[0:-1]
                    nao_funciona = nao_funciona[1:-1]
                    print(nao_funciona)
                    data_final = self.__calcula_tempo_evento(data, int(dias))
                    lista.append([data, data_final, descricao_evento, nao_funciona])
        lista.sort(key = lambda x: x[0])

        return lista
    
    def __lista_datas_eventos(self) -> list[list]:
        lista_eventos = []
        for data in self.__eventos:
            aux = data.split('/')
            lista_eventos.append(aux)
        
        lista_eventos.sort(key = lambda eventos: (eventos[2], eventos[1], eventos[0]))
        return lista_eventos


    def __calcula_tempo_evento(self, data_inicial: str, dias: int) -> str:
        data = datetime.strptime(data_inicial, ListaEventos.formatacao_data).date()
        ano, mes, dia = str(data + timedelta(dias)).split('-')
        data_final = f'{dia}/{mes}/{ano}'
        return data_final


    def criar_evento(self, data_inicial: str, data_final: str, evento: str, nao_funciona: bool) -> str:
        """
        Cria um novo evento e retorna uma string para ser usado no front.
        """
        if self.__verifica_data(data_inicial, data_final):
            data_inicial_formatada = datetime.strptime(data_inicial, ListaEventos.formatacao_data).date()
            data_final_formatada = datetime.strptime(data_final, ListaEventos.formatacao_data).date()
            dias = data_final_formatada - data_inicial_formatada
            self.__eventos[data_inicial].add(f'{nao_funciona} - {evento} - {dias.days}')
            self.__salvar_eventos()
            return 'Evento registrado com sucesso!'
        else:
            return 'Data invalida! Digite a data atual ou futura!'          


    def __verifica_data(self, data_str1: str, data_str2: str) -> bool:
        """
        Verifica se a data é do dia ou futura, caso contrário retorna Falso.
        """
        try:
            data_inicial = datetime.strptime(data_str1, ListaEventos.formatacao_data).date()
            data_final = datetime.strptime(data_str2, ListaEventos.formatacao_data).date()
            data_atual = datetime.now().date()
            return data_inicial >= data_atual <= data_final
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
                    data, nao_funciona, evento, dias  = line.strip().split(' - ')
                    self.__eventos[data].add(f'{nao_funciona} - {evento} - {dias}')
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