class Evento:

    def __init__(self, data_inicial: str, data_final: str, nao_funciona: bool) -> None:
        self.__data_inicial = data_inicial
        self.__data_final = data_final
        self.__nao_funciona = bool