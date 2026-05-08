def try_or_none(lista_strings):
    resultados = []
    for item in lista_strings:
        try:
            resultados.append(int(item))
        except ValueError:
            resultados.append(None)
    return resultados