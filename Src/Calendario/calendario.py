from datetime import datetime
from calendar import Calendar
#from dateutil.relativedelta import relativedelta

class calendario_UESC:
    def __init__(self):
        # Data atual, util para pegar o dia, mês e ano assim que inicializar o programa 
        # e quando precisar voltar para o dia atual
        self.__dataAtual: datetime = datetime.now()

        # Data auxiliar para percorrer o calendário
        self.__dataAux: datetime = datetime.now()
        
        # Atributos referentes aos dias, mês, ano e dia da semana, inicialmente são os valores da data atual
        self.__dia: int = self.__dataAtual.day
        self.__mes: int = self.__dataAtual.month
        self.__ano: int = self.__dataAtual.year
        self.__diaSemana: int = self.__dataAtual.weekday()

        # Atributos referentes ao calendário
        self.__cal: Calendar = Calendar()
        self.__listaMes: list[list[tuple[int, int]]]= self.__cal.monthdays2calendar(self.__ano, self.__mes)
        self.__listaAno: list[list[tuple[int, int]]] = self.__cal.yeardays2calendar(self.__ano, 12)

        # Lista de eventos cadastrados
        self.__eventosAno: dict[int, dict[int, dict[int, list[(datetime, str)]]]] = {}

    '''
        self.exemplo_do_evento = {
            2021: {
                6: {
                    1: [(datetime(2021, 6, 1, 12, 0), "Reunião"), (datetime(2021, 6, 1, 15, 0), "Aula")],
                    2: [(datetime(2021, 7, 1, 12, 0), "Reunião"), (datetime(2021, 7, 1, 15, 0), "Aula")],
                },
                7: {
                    2: [(datetime(2021, 7, 1, 12, 0), "Reunião"), (datetime(2021, 7, 1, 15, 0), "Aula")],
                }
            }, 2022: {
                1: {
                    3: [(datetime(2022, 1, 1, 12, 0), "basquete"), (datetime(2022, 1, 1, 15, 0), "futebol")],
                }, 31: {

                    1: [(datetime(2022, 1, 31, 12, 0), "Curso"), (datetime(2022, 1, 31, 15, 0), "Projeto")],
                }
            }
        }
    '''

    # Método que retorna os eventos do ano, caso não tenha eventos, retorna um dicionário vazio
    def listaEventosAno(self, ano: int) -> dict[int, dict[int, list[tuple[datetime, str]]]]:
        return self.__eventosAno.get(ano, {})

    # Método que retorna os eventos do mês, caso não tenha eventos, retorna um dicionário vazio
    def listaEventosMes(self, mes: int, ano: int) -> dict[int, list[tuple[datetime, str]]]: 
        return self.listaEventosAno(ano).get(mes, {})

    # Método que retorna os eventos do dia, caso não tenha eventos, retorna uma lista None
    def listaEventosDia(self, dia: int, mes: int, ano: int) -> list[tuple[datetime, str]]:
        return self.listaEventosMes(mes, ano).get(dia, None)


    # Método auxiliar para adicionar um evento no atributo __eventosAno
    def __adicionaEvento(self, dia: int, mes: int, ano: int, evento: tuple[datetime, str]) -> None:
        # Verifica se o ano, mês e dia já estão no dicionário, caso não estejam, adiciona
        if ano not in self.__eventosAno:
            self.__eventosAno[ano] = {}
        if mes not in self.__eventosAno[ano]:
            self.__eventosAno[ano][mes] = {}
        if dia not in self.__eventosAno[ano][mes]:
            self.__eventosAno[ano][mes][dia] = []

        self.__eventosAno[ano][mes][dia].append(evento)
        

    # Método para cadastrar um evento, retorna True se foi possível cadastrar o evento e False caso contrário
    def cadastraEvento(self, dia: int, mes: int, ano: int, descricao: str = '', hora=0, minuto=0) -> bool:
        self.__dataAtual = datetime.now()
        evento = datetime(ano, mes, dia, hora, minuto)
        evento = (evento, descricao)

        # Verifica se a data do evento é maior que a data atual
        if self.__dataAtual < evento[0]:
            self.__adicionaEvento(dia, mes, ano, evento)
            return True
        
        return False
                
    
    # Método para voltar o mês, a partir de self.__mes
    def voltaMes(self) -> None:
        self.__mes -= 1
        self.__dia = 1
        if self.__mes < 1:
            self.__mes = 12
            self.__ano -= 1
        self.__dataAux = datetime(self.__ano, self.__mes, self.__dia)
        self.__diaSemana = self.__dataAux.weekday()
        self.__listaMes = self.__cal.monthdays2calendar(self.__ano, self.__mes)
        self.__listaAno = self.__cal.yeardays2calendar(self.__ano, 12)
        

    # Método para avançar o mês, a partir de self.__mes
    def avancaMes(self) -> None:
        self.__mes += 1
        self.__dia = 1
        if self.__mes > 12:
            self.__mes = 1
            self.__ano += 1
        self.__dataAux = datetime(self.__ano, self.__mes, self.__dia)
        self.__diaSemana = self.__dataAux.weekday()
        self.__listaMes = self.__cal.monthdays2calendar(self.__ano, self.__mes)
        self.__listaAno = self.__cal.yeardays2calendar(self.__ano, 12)


    # Método para voltar o ano, a partir de self.__ano
    def voltaAno(self) -> None:
        self.__ano -= 1
        self.__dia = 1
        self.__mes = 1
        self.__dataAux = datetime(self.__ano, self.__mes, self.__dia)
        self.__diaSemana = self.__dataAux.weekday()
        self.__listaMes = self.__cal.monthdays2calendar(self.__ano, self.__mes)
        self.__listaAno = self.__cal.yeardays2calendar(self.__ano, 12)


    # Método para avançar o ano, a partir de self.__ano
    def avancaAno(self) -> None:
        self.__ano += 1
        self.__dia = 1
        self.__mes = 1
        self.__dataAux = datetime(self.__ano, self.__mes, self.__dia)
        self.__diaSemana = self.__dataAux.weekday()
        self.__listaMes = self.__cal.monthdays2calendar(self.__ano, self.__mes)
        self.__listaAno = self.__cal.yeardays2calendar(self.__ano, 12)


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
    
    def getEventos(self):
        return self.__eventosAno
