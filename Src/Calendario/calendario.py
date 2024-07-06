from datetime import datetime
from calendar import TextCalendar
from eventos import Eventos
#from dateutil.relativedelta import relativedelta

class Calendario(Eventos, TextCalendar):

    def __init__(self):
        super().__init__()
        # Data atual, util para pegar o dia, mês e ano assim que inicializar o programa 
        # e quando precisar voltar para o dia atual
        self.__data_atual: datetime = datetime.now()

        # Data auxiliar para percorrer o calendário
        self.__data_aux: datetime = datetime.now()
        
        # Atributos referentes aos dias, mês, ano e dia da semana, inicialmente são os valores da data atual
        self.__dia: int = self.__data_atual.day
        self.__mes: int = self.__data_atual.month
        self.__ano: int = self.__data_atual.year
        self.__dia_semana: int = self.__data_atual.weekday()
                
    
    # Método para voltar o mês, a partir de self.__mes
    def volta_mes(self):
        self.__mes -= 1
        self.__dia = 1
        if self.__mes < 1:
            self.__mes = 12
            self.__ano -= 1
        self.__data_aux = datetime(self.__ano, self.__mes, self.__dia)
        self.__dia_semana = self.__data_aux.weekday()
        

    # Método para avançar o mês, a partir de self.__mes
    def avanca_mes(self):
        self.__mes += 1
        self.__dia = 1
        if self.__mes > 12:
            self.__mes = 1
            self.__ano += 1
        self.__data_aux = datetime(self.__ano, self.__mes, self.__dia)
        self.__dia_semana = self.__data_aux.weekday()


    # Método para voltar o ano, a partir de self.__ano
    def volta_ano(self):
        self.__ano -= 1
        self.__dia = 1
        self.__mes = 1
        self.__data_aux = datetime(self.__ano, self.__mes, self.__dia)
        self.__dia_semana = self.__data_aux.weekday()


    # Método para avançar o ano, a partir de self.__ano
    def avanca_ano(self):
        self.__ano += 1
        self.__dia = 1
        self.__mes = 1
        self.__data_aux = datetime(self.__ano, self.__mes, self.__dia)
        self.__dia_semana = self.__data_aux.weekday()


    ''' # Método utilizando o relativedelta para voltar o mês
    def voltaMes(self, k: int = 1):
        self.__dataAtual -= relativedelta(months=k)
        self.__dia = self.__dataAtual.day
        self.__mes = self.__dataAtual.month
        self.__ano = self.__dataAtual.year
        self.__diaSemana = self.__dataAtual.weekday()
        self.__listaMesAtual = self.__cal.monthdays2calendar(self.__ano, self.__mes)
        self.__listaAnoAtual = self.__cal.yeardays2calendar(self.__ano)
    '''

    # Métodos getters
    @property
    def dia(self) -> int:
        return self.__dia
    
    @property
    def mes(self) -> int:
        return self.__mes
    
    @property
    def ano(self) -> int:
        return self.__ano
    
    @property
    def dia_semana(self) -> int:
        return self.__dia_semana
    