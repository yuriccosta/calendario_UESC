from datetime import datetime
from calendar import Calendar
#from dateutil.relativedelta import relativedelta

class calendario_UESC:
    def __init__(self):
        # Data atual, util para pegar o dia, mês e ano assim que inicializar o programa 
        # e quando precisar voltar para o dia atual
        self.__dataAtual: datetime = datetime.now()
        
        # Atributos referentes aos dias, mês, ano e dia da semana, inicialmente são os valores da data atual
        self.__dia: int = self.__dataAtual.day
        self.__mes: int = self.__dataAtual.month
        self.__ano: int = self.__dataAtual.year
        self.__diaSemana: int = self.__dataAtual.weekday()

        # Atributos referentes ao calendário
        self.__cal: Calendar = Calendar()
        self.__listaMes: list[list[tuple[int, int]]]= self.__cal.monthdays2calendar(self.__ano, self.__mes)
        self.__listaAno: list[list[tuple[int, int]]] = self.__cal.yeardays2calendar(self.__ano, 12)


    # Método para voltar o mês, a partir de self.__mes
    def voltaMes(self) -> None:
        self.__mes -= 1
        self.__dia = 1
        if self.__mes < 1:
            self.__mes = 12
            self.__ano -= 1
        self.__listaMes = self.__cal.monthdays2calendar(self.__ano, self.__mes)
        self.__listaAno = self.__cal.yeardays2calendar(self.__ano, 12)
        

    # Método para avançar o mês, a partir de self.__mes
    def avancaMes(self) -> None:
        self.__mes += 1
        self.__dia = 1
        if self.__mes > 12:
            self.__mes = 1
            self.__ano += 1
        self.__listaMes = self.__cal.monthdays2calendar(self.__ano, self.__mes)
        self.__listaAno = self.__cal.yeardays2calendar(self.__ano, 12)


    # Método para voltar o ano, a partir de self.__ano
    def voltaAno(self) -> None:
        self.__ano -= 1
        self.__dia = 1
        self.__mes = 1


    # Método para avançar o ano, a partir de self.__ano
    def avancaAno(self) -> None:
        self.__ano += 1
        self.__dia = 1
        self.__mes = 1


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
    def getDia(self):
        return self.__dia
    
    def getMes(self):
        return self.__mes
    
    def getAno(self):
        return self.__ano
    
    def getDiaSemana(self):
        return self.__diaSemana
    
    def getListaMes(self):
        return self.__listaMes
    
    def getListaAno(self):
        return self.__listaAno
