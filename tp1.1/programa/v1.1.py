import argparse
import random
import matplotlib.pyplot as plt
import statistics as stats
import os

def simular_ruleta(tiradas):
    return [random.randint(0, 36) for _ in range(tiradas)]

def graficar_frecuencias(resultados, corrida_id):
    conteo = [resultados.count(i) for i in range(37)]
    plt.figure(figsize=(10, 5))
    plt.bar(range(37), conteo, color='royalblue')
    plt.title(f"Frecuencia de aparición por número - Corrida {corrida_id}")
    plt.xlabel("Número")
    plt.ylabel("Frecuencia absoluta")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    nombre_archivo = f"images/frecuencia_corrida_{corrida_id}.png"
    plt.savefig(nombre_archivo)
    plt.close()
    print(f"[✓] Gráfico guardado: {nombre_archivo}")

def graficar_aparicion_numero(n_analizado, apariciones, tiradas):
    plt.figure(figsize=(10, 5))
    frecuencias = [a / tiradas for a in apariciones]
    plt.plot(range(1, len(apariciones) + 1), frecuencias, marker='o', color='crimson')
    plt.axhline(y=1/37, color='gray', linestyle='--', label='Esperado (1/37)')
    plt.title(f"Frecuencia relativa del número {n_analizado} en cada corrida")
    plt.xlabel("Corrida")
    plt.ylabel("Frecuencia relativa")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    nombre_archivo = f"images/frecuencia_relativa_{n_analizado}.png"
    plt.savefig(nombre_archivo)
    plt.close()
    print(f"[✓] Gráfico guardado: {nombre_archivo}")

def main():
    parser = argparse.ArgumentParser(description="Simulación de una ruleta europea.")
    parser.add_argument("-c", "--corridas", type=int, required=True, help="Cantidad de corridas")
    parser.add_argument("-n", "--tiradas", type=int, required=True, help="Cantidad de tiradas por corrida")
    parser.add_argument("-e", "--elegido", type=int, default=17, help="Número a analizar (0 a 36)")
    args = parser.parse_args()

    if not 0 <= args.elegido <= 36:
        print("⚠ El número elegido debe estar entre 0 y 36.")
        return

    os.makedirs("images", exist_ok=True)
    apariciones_numero = []
    varianzas = []
    desvios = []

    for i in range(1, args.corridas + 1):
        resultados = simular_ruleta(args.tiradas)
        graficar_frecuencias(resultados, i)

        apariciones = resultados.count(args.elegido)
        apariciones_numero.append(apariciones)

        media = stats.mean(resultados)
        varianza = stats.variance(resultados)
        desvio = stats.stdev(resultados)

        varianzas.append(varianza)
        desvios.append(desvio)

        print(f"Corrida {i}: Media = {media:.2f} | Varianza = {varianza:.2f} | Desvío estándar = {desvio:.2f} | {args.elegido} apareció {apariciones} veces")

    graficar_aparicion_numero(args.elegido, apariciones_numero, args.tiradas)

    print("\nResumen general:")
    print(f"Promedio de varianza entre corridas: {stats.mean(varianzas):.2f}")
    print(f"Promedio de desvío estándar entre corridas: {stats.mean(desvios):.2f}")

if __name__ == "__main__":
    main()
