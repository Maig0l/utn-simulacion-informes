import random
import argparse
import matplotlib.pyplot as plt
import numpy as np

def simular_ruleta(corridas, tiradas_por_corrida, numero_elegido):
    todas_fr = []
    todas_vp = []
    todas_vd = []
    todas_vv = []

    for _ in range(corridas):
        tiradas = [random.randint(0, 36) for _ in range(tiradas_por_corrida)]

        fr = []
        vp = []
        vd = []
        vv = []

        aciertos = 0
        for i in range(1, tiradas_por_corrida + 1):
            if tiradas[i - 1] == numero_elegido:
                aciertos += 1
            muestra = tiradas[:i]
            fr.append(aciertos / i)
            vp.append(np.mean(muestra))
            vd.append(np.std(muestra))
            vv.append(np.var(muestra))

        todas_fr.append(fr)
        todas_vp.append(vp)
        todas_vd.append(vd)
        todas_vv.append(vv)

    # Promedios por cada índice de tirada
    promedio_fr = np.mean(todas_fr, axis=0)
    promedio_vp = np.mean(todas_vp, axis=0)
    promedio_vd = np.mean(todas_vd, axis=0)
    promedio_vv = np.mean(todas_vv, axis=0)

    return promedio_fr, promedio_vp, promedio_vd, promedio_vv, tiradas_por_corrida

def mostrar_graficos(fr, vp, vd, vv, numero_elegido, tiradas_totales):
    import os 
    output_dir = os.path.join("..","informe","img")
    os.makedirs(output_dir, exist_ok=True)


    n = list(range(1, tiradas_totales + 1))
    
    fre_esperada = 1 / 37
    vpe = np.mean(range(37))
    vde = np.std(range(37))
    vve = np.var(range(37))

    # Frecuencia relativa
    plt.figure()
    plt.plot(n, fr, label='frn (frecuencia relativa)', color='red')
    plt.axhline(y=fre_esperada, color='blue', linestyle='--', label='fre (esperada)')
    plt.xlabel('n (número de tiradas)')
    plt.ylabel('fr (frecuencia relativa)')
    plt.title(f'Frecuencia relativa promedio del número {numero_elegido}')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'frecuencia_relativa.png'))
    plt.close()

    # Promedio
    plt.figure()
    plt.plot(n, vp, label='vpn (valor promedio)', color='red')
    plt.axhline(y=vpe, color='blue', linestyle='--', label='vpe (esperado)')
    plt.xlabel('n (número de tiradas)')
    plt.ylabel('vp (valor promedio)')
    plt.title('Valor promedio de las tiradas')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'promedio.png'))
    plt.close()

    # Desvío estándar
    plt.figure()
    plt.plot(n, vd, label='vdn (desvío)', color='red')
    plt.axhline(y=vde, color='blue', linestyle='--', label='vde (esperado)')
    plt.xlabel('n (número de tiradas)')
    plt.ylabel('vd (valor del desvío)')
    plt.title('Desvío estándar de las tiradas')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'desvio.png'))
    plt.close()

    # Varianza
    plt.figure()
    plt.plot(n, vv, label='vvn (varianza)', color='red')
    plt.axhline(y=vve, color='blue', linestyle='--', label='vve (esperada)')
    plt.xlabel('n (número de tiradas)')
    plt.ylabel('vv (valor de la varianza)')
    plt.title('Varianza de las tiradas')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'varianza.png'))
    plt.close()

    print("\nValores esperados:")
    print(f"- Frecuencia esperada: {fre_esperada:.4f}")
    print(f"- Promedio esperado: {vpe:.2f}")
    print(f"- Desvío esperado: {vde:.2f}")
    print(f"- Varianza esperada: {vve:.2f}")
    print("Gráficos guardados como imágenes PNG.")

def main():
    parser = argparse.ArgumentParser(description="Simulación de ruleta")
    parser.add_argument('-c', type=int, required=True, help='Cantidad de corridas')
    parser.add_argument('-n', type=int, required=True, help='Cantidad de tiradas por corrida')
    parser.add_argument('-e', type=int, required=True, help='Número elegido (entre 0 y 36)')
    args = parser.parse_args()

    if not (0 <= args.e <= 36):
        print("Error: El número elegido debe estar entre 0 y 36.")
        return

    fr, vp, vd, vv, tiradas_totales = simular_ruleta(args.c, args.n, args.e)
    mostrar_graficos(fr, vp, vd, vv, args.e, tiradas_totales)

if __name__ == '__main__':
    main()