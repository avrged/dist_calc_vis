def factorial (n):
    n = int (n)
    resultado = 1
    for i in range(1, n+1):
        resultado *= i
    return resultado
    
def permutacion (n, r):
    n = int (n)
    r = int (r)
    resultado = factorial(n) / factorial(n - r)
    return int(resultado)

def combinacion (n, r):
    n = int (n)
    r = int (r)
    resultado = permutacion (n, r) / factorial (r)
    return int(resultado)

def bernoulli(prob_exito, x):
    '''
    prob_exito: probabilidad de éxito
    x: 1 si es éxito, 0 si es fracaso
    '''
    if x not in [0, 1]:
        raise ValueError("x debe ser 0 o 1")
    resultado = (prob_exito ** x) * ((1 - prob_exito) ** (1 - x))
    return resultado

def binomial(n_eventos, x_exitos, prob_exito):
    '''
    n_eventos: es el total de eventos independientes
    x_exitos: total de exitos esperados
    prob_exito: probabilidad de que un evento sea exitoso
    '''
    p = prob_exito
    q = 1 - p
    resultado = combinacion(n_eventos, x_exitos) * (p ** x_exitos) * (q ** (n_eventos - x_exitos))
    return 100*float(resultado)

def geometrica(prob_exito, x):
    '''
    prob_exito: probabilidad de éxito
    x: número de fracasos antes del primer éxito
    '''
    p = prob_exito
    q = 1 - p
    resultado = (q ** x) * p
    return resultado

def poisson(lam, x):
    '''
    lam: tasa de ocurrencia
    x: número de ocurrencias
    '''
    e = 2.71828
    resultado = (lam ** x) * (e ** -lam) / factorial(x)
    return resultado

def hipergeometrica(N, K, n, k):
    '''
    N = poblacion
    K = exitos_poblacion
    n = muestra
    k = exitos_muestra
    '''
    fracasos_pob = N - K
    fracasos_muestra = n - k 
    resultado = combinacion (K, k)*combinacion (fracasos_pob, fracasos_muestra)/combinacion(N, n)
    return 100*(resultado)