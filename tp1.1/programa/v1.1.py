import random
import argparse
import matplotlib.pyplot as plt
import numpy as np

def simular_ruleta(corridas, tiradas_por_corrida, numero_elegido):
    frecuencias_relativas = []

    for i in range(corridas):
        tiradas = [random.randint(0, 36) for _ in range(tiradas_por_corrida)]
        aciertos = tiradas.count(numero_elegido)
        frecuencia_relativa = aciertos / tiradas_por_corrida
        frecuencias_relativas.append(frecuencia_relativa)

    return frecuencias_relativas

def mostrar_graficos(frecuencias_relativas, numero_elegido):
    media = np.mean(frecuencias_relativas)
    varianza = np.var(frecuencias_relativas)

    print(f"\nResultados estadísticos:")
    print(f"- Media de frecuencias relativas: {media:.4f}")
    print(f"- Varianza: {varianza:.6f}")
    print(f"- Frecuencia teórica esperada: {1/37:.4f}")

    # Gráfico de líneas
    plt.figure(figsize=(10,5))
    plt.plot(frecuencias_relativas, marker='o', label='Frecuencia relativa')
    plt.axhline(y=1/37, color='r', linestyle='--', label='Esperado (1/37)')
    plt.title(f'Frecuencia relativa del número {numero_elegido} por corrida')
    plt.xlabel('Corrida')
    plt.ylabel('Frecuencia relativa')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('frecuencia.png')
    plt.show()

    # Histograma
    plt.figure(figsize=(8,5))
    plt.hist(frecuencias_relativas, bins=10, edgecolor='black')
    plt.title('Histograma de frecuencias relativas')
    plt.xlabel('Frecuencia relativa')
    plt.ylabel('Cantidad de corridas')
    plt.tight_layout()
    plt.savefig('histograma.png')
    plt.show()

def main():
    parser = argparse.ArgumentParser(description="Simulación del plato de una ruleta")
    parser.add_argument('-c', type=int, required=True, help='Cantidad de corridas')
    parser.add_argument('-n', type=int, required=True, help='Cantidad de tiradas por corrida')
    parser.add_argument('-e', type=int, required=True, help='Número elegido (entre 0 y 36)')
    args = parser.parse_args()

    if args.e < 0 or args.e > 36:
        print("Error: El número elegido debe estar entre 0 y 36.")
        return

    frecuencias_relativas = simular_ruleta(args.c, args.n, args.e)
    mostrar_graficos(frecuencias_relativas, args.e)

if __name__ == '__main__':
    main()
