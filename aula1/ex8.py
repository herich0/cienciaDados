def estatisticas(*args):
    if not args:
        return {}
    
    return {
        "média": sum(args) / len(args),
        "máximo": max(args),
        "mínimo": min(args)
    }

resultado_estatisticas = estatisticas(10, 25, 5, 40, 20)
print(f"O dicionário com as estatísticas dos números é: {resultado_estatisticas}")