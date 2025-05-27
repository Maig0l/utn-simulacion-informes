import argparse
import random
import matplotlib.pyplot as plt
import numpy as np

# Secuencia Fibonacci
fibonacci_seq = [1, 1]
def next_fibonacci(index):
    while len(fibonacci_seq) <= index:
        fibonacci_seq.append(fibonacci_seq[-1] + fibonacci_seq[-2])
    return fibonacci_seq[index]

def jugar_ruleta():
    return random.randint(0, 36)

def es_rojo(numero):
    rojos = {1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36}
    return numero in rojos

def pertenece_a_docena(numero, docena):
    if docena == 1:
        return 1 <= numero <= 12
    elif docena == 2:
        return 13 <= numero <= 24
    elif docena == 3:
        return 25 <= numero <= 36
    return False

def simular_estrategia(corridas, tiradas, capital_inicial, estrategia, capital_tipo, tipo_apuesta, numero_apuesta=None, docena_apuesta=None):
    resultados = []
    bancarrotas = 0
    frecuencia_exitos_total = [0] * tiradas

    for _ in range(corridas):
        saldo = capital_inicial
        historial_saldo = [saldo]
        apuesta_inicial = 1
        apuesta = apuesta_inicial
        fib_index = 0
        exitos = []

        for t in range(tiradas):
            if capital_tipo == 'f' and saldo < apuesta:
                bancarrotas += 1
                break

            numero = jugar_ruleta()

            if tipo_apuesta == 'color':
                gano = es_rojo(numero)
                pago = 1
            elif tipo_apuesta == 'numero':
                gano = (numero == numero_apuesta)
                pago = 35
            elif tipo_apuesta == 'docena':
                gano = pertenece_a_docena(numero, docena_apuesta)
                pago = 2
            else:
                gano = False
                pago = 0

            exitos.append(1 if gano else 0)

            if gano:
                saldo += apuesta * pago
                if estrategia == 'm':
                    apuesta = apuesta_inicial
                elif estrategia == 'd':
                    apuesta = max(apuesta - 1, 1)
                elif estrategia == 'f':
                    fib_index = max(fib_index - 2, 0)
                    apuesta = next_fibonacci(fib_index)
                elif estrategia == 'o':
                    apuesta = apuesta * 2
            else:
                saldo -= apuesta
                if estrategia == 'm':
                    apuesta *= 2
                elif estrategia == 'd':
                    apuesta += 1
                elif estrategia == 'f':
                    fib_index += 1
                    apuesta = next_fibonacci(fib_index)
                elif estrategia == 'o':
                    apuesta = apuesta

            historial_saldo.append(saldo)

        for i in range(len(exitos)):
            frecuencia_exitos_total[i] += exitos[i]

        resultados.append(historial_saldo)

    frecuencia_relativa = [f / corridas for f in frecuencia_exitos_total]
    return resultados, bancarrotas, frecuencia_relativa

def graficar_resultados(resultados, estrategia, tipo_apuesta, capital_inicial, capital_tipo):
    max_len = max(map(len, resultados))
    resultados_padded = [np.pad(np.array(r, dtype=float), (0, max_len - len(r)), constant_values=0)
    for r in resultados]
    promedio_capital = np.nanmean(resultados_padded, axis=0)

    plt.plot(promedio_capital, label='Promedio del saldo')
    plt.axhline(y=capital_inicial, color='gray', linestyle='--', label='Capital inicial')
    plt.xlabel('Tiradas')
    plt.ylabel('Saldo')
    plt.title(f'{estrategia.upper()} - Promedio Capital ({tipo_apuesta})')
    plt.legend()
    plt.grid(True)
    plt.savefig(f'promedio_capital_{estrategia}_{tipo_apuesta}_{capital_tipo}.png')
    plt.show()

def graficar_frecuencia_relativa(frecuencia_relativa, estrategia, tipo_apuesta, capital_tipo):
    tipo_capital = 'Infinito' if capital_tipo == 'i' else 'Finito'
    plt.plot(frecuencia_relativa, color='green')
    plt.xlabel('Tiradas')
    plt.ylabel('Frecuencia Relativa de Éxitos')
    plt.title(f'{estrategia.upper()} - Frecuencia Relativa ({tipo_apuesta})')
    plt.grid(True)
    plt.savefig(f'frecuencia_relativa_{estrategia}_{tipo_apuesta}_{capital_tipo}.png')
    plt.show()

def graficar_boxplot(resultados, estrategia, tipo_apuesta, capital_tipo):
    tipo_capital = 'Infinito' if capital_tipo == 'i' else 'Finito'
    saldos_finales = [r[-1] for r in resultados]
    plt.boxplot(saldos_finales, vert=False)
    plt.xlabel('Saldo Final')
    plt.title(f'{estrategia.upper()} - Boxplot Saldo Final ({tipo_apuesta})')
    plt.grid(True)
    plt.savefig(f'boxplot_{estrategia}_{tipo_apuesta}_{capital_tipo}.png')
    plt.show()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', type=int, required=True, help='Número de corridas')
    parser.add_argument('-s', type=str, required=True, help='Estrategia: m, d, f, o')
    parser.add_argument('-a', type=str, required=True, help='Capital: i (infinito), f (finito)')
    parser.add_argument('-c', type=int, default=100, help='Capital inicial')
    parser.add_argument('-t', type=int, default=100, help='Tiradas por corrida')
    parser.add_argument('--tipo_apuesta', choices=['color', 'numero', 'docena'], required=True, help='Tipo de apuesta')
    parser.add_argument('--numero', type=int, help='Número elegido (si se apuesta a un número)')
    parser.add_argument('--docena', type=int, choices=[1, 2, 3], help='Docena elegida (1, 2 o 3)')

    args = parser.parse_args()

    resultados, bancarrotas, frecuencia_relativa = simular_estrategia(
        args.n, args.t, args.c, args.s, args.a,
        args.tipo_apuesta, args.numero, args.docena
    )

    print(f"\nEstrategia: {args.s.upper()} | Capital: {'Infinito' if args.a == 'i' else 'Finito'}")
    print(f"Apuesta: {args.tipo_apuesta.upper()} | Bancarrotas: {bancarrotas} en {args.n} corridas\n")


    graficar_resultados(resultados, args.s, args.tipo_apuesta, args.c, args.a)
    graficar_frecuencia_relativa(frecuencia_relativa, args.s, args.tipo_apuesta, args.a)
    graficar_boxplot(resultados, args.s, args.tipo_apuesta, args.a)

if __name__ == '__main__':
    main()
