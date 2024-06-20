from calendario import calendarioEventos

cal = calendarioEventos()


# cal começa com a data atual
print(f'''
    Dia: {cal.getDia()}
    Mês: {cal.getMes()}
    Ano: {cal.getAno()}
    Eventos: {cal.getEventos()}''')
'''
# cal volta 10 meses
for c in range(10):
    cal.voltaMes()

'''
print("Tentativas de cadastro de eventos")
'''print(cal.cadastraEvento(20, 6, 2024, 'Dia do Cinema Brasileiro', 14, 30))
print(cal.cadastraEvento(1, 1, 2024, 'Ano Novo'))
print(cal.cadastraEvento(25, 12, 2024, 'Natal'))
print(cal.cadastraEvento(20, 6 , 2024, 'Prova', 22, 48))'''

print(f'''
    Dia: {cal.getDia()}
    Mês: {cal.getMes()}
    Ano: {cal.getAno()}
    Eventos: {cal.getEventos()}
    Eventos do mes: {cal.getEventosMes(12, 2030)}
    Evento do dia: {cal.getEventosDia(20, 6, 2024)}''')


cal.salvarEventos()


