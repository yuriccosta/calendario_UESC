from datetime import datetime, timedelta
from collections import defaultdict
from utils.meses import meses_por_indice

class ListaEventos:

    formatacao_data = '%d/%m/%Y'

    def __init__(self):
        self.__eventos = defaultdict(set)
        self.__carregar_eventos()


    @property
    def eventos(self) -> defaultdict:
        return self.__eventos
    

    def remover_evento(self, data: str, descricao_evento: str) -> str:
        """
        Remove um evento por data e descrição do evento.
        """
        try:
            eventos_do_dia = self.__eventos[data]
            evento_para_remover = None
            for evento in eventos_do_dia:
                nao_funciona, descricao, dias = evento.split(' - ')
                if descricao == descricao_evento:
                    evento_para_remover = evento
                    break

            if evento_para_remover:
                self.__eventos[data].remove(evento_para_remover)
                if not self.__eventos[data]:  # Se não houver mais eventos na data, remova a chave
                    del self.__eventos[data]
                self.__salvar_eventos()
                return 'Evento removido com sucesso!'
            else:
                return 'Evento não encontrado.'
        except KeyError:
            return 'Data não encontrada.'


    def busca_eventos(self):
        lista_eventos = self.__lista_datas_eventos()
        eventos_dict = {}
        
        for i, _ in enumerate(lista_eventos):
            data = f'{lista_eventos[i][0]}/{lista_eventos[i][1]}/{lista_eventos[i][2]}'
            ano = int(lista_eventos[i][2])
            mes = meses_por_indice[int(lista_eventos[i][1])]
            
            if ano not in eventos_dict:
                eventos_dict[ano] = {}
            if mes not in eventos_dict[ano]:
                eventos_dict[ano][mes] = []

            for evento in self.__eventos[data]:
                nao_funciona, descricao_evento, dias = evento.split(' - ')
                nao_funciona = True if int(nao_funciona) == 1 else False
                dias = int(dias)
                dia_evento = int(lista_eventos[i][0])
                if dias > 0:
                    dia_final = int(self.__calcula_tempo_evento(data, dias))
                    eventos_dict[ano][mes].append([[dia_evento, dia_final], nao_funciona, descricao_evento])
                else:
                    eventos_dict[ano][mes].append([[dia_evento], nao_funciona, descricao_evento])

        return eventos_dict
    
    
    def __lista_datas_eventos(self) -> list[list]:
        lista_eventos = []
        for data in self.__eventos:
            aux = data.split('/')
            lista_eventos.append(aux)
        
        lista_eventos.sort(key = lambda eventos: (eventos[2], eventos[1], eventos[0]))
        return lista_eventos


    def __calcula_tempo_evento(self, data_inicial: str, dias: int) -> str:
        data = datetime.strptime(data_inicial, ListaEventos.formatacao_data).date()
        _, _, dia = str(data + timedelta(dias)).split('-')
        return dia


    def criar_evento(self, data_inicial: str, data_final: str, evento: str, nao_funciona: bool) -> str:
        """
        Cria um novo evento e retorna uma string para ser usado no front.
        """
        if self.__verifica_data(data_inicial, data_final):
            data_inicial_formatada = datetime.strptime(data_inicial, ListaEventos.formatacao_data).date()
            data_final_formatada = datetime.strptime(data_final, ListaEventos.formatacao_data).date()
            dias = data_final_formatada - data_inicial_formatada

            nao_funciona_evento = 1 if nao_funciona else 0

            # Verifica se o evento ja esta cadastrado com maiscula ou nao
            aux = f'{nao_funciona} - {evento} - {dias.days}'.lower()
            for auxevento in self.__eventos[data_inicial]:
                if aux == auxevento.lower():
                    return 'Evento já registrado'

            self.__eventos[data_inicial].add(f'{nao_funciona_evento} - {evento} - {dias.days}')
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
            with open('resources/eventos.txt', 'r') as file:
                for line in file:
                    data, nao_funciona, evento, dias  = line.strip().split(' - ')
                    self.__eventos[data].add(f'{nao_funciona} - {evento} - {dias}')
        except FileNotFoundError:
            pass

    
    def __salvar_eventos(self):
        """
        Método auxiliar ao método cria_eventos, apenas salva um novo evento no arquivo txt.
        """
        with open('resources/eventos.txt', 'w') as file:
            for data, eventos in self.__eventos.items():
                for evento in eventos:
                    file.write(f'{data} - {evento}\n')