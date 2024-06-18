from calendario import calendario_UESC

cal = calendario_UESC()

# cal começa com a data atual
print(f'''
    Dia: {cal.getDia()}
    Mês: {cal.getMes()}
    Ano: {cal.getAno()}''')

for c in range(10):
    cal.voltaMes()

# cal volta 10 meses
print(f'''
    Dia: {cal.getDia()}
    Mês: {cal.getMes()}
    Ano: {cal.getAno()}''')
