"""
Generación de gráficas y reportes a partir de las cataciones guardadas.
"""
import os
import matplotlib
matplotlib.use("Agg")  # backend sin ventana, evita problemas en distintos sistemas
import matplotlib.pyplot as plt

from modelo import RepositorioCataciones

CARPETA_REPORTES = "reportes"


def grafica_promedio_por_cafe(repositorio: RepositorioCataciones) -> str:
    """Genera un gráfico de barras con el puntaje promedio de cada café evaluado."""
    promedios = repositorio.promedio_por_cafe()
    if not promedios:
        raise ValueError("No hay cataciones registradas todavía")

    cafes = list(promedios.keys())
    puntajes = list(promedios.values())

    os.makedirs(CARPETA_REPORTES, exist_ok=True)
    ruta = os.path.join(CARPETA_REPORTES, "promedio_por_cafe.png")

    plt.figure(figsize=(8, 5))
    barras = plt.bar(cafes, puntajes, color="#6F4E37")
    plt.ylim(0, 10)
    plt.ylabel("Puntaje promedio")
    plt.title("Puntaje promedio por café")
    plt.xticks(rotation=30, ha="right")

    for barra, valor in zip(barras, puntajes):
        plt.text(barra.get_x() + barra.get_width() / 2, valor + 0.15,
                  str(valor), ha="center", fontsize=9)

    plt.tight_layout()
    plt.savefig(ruta)
    plt.close()
    return ruta


def grafica_perfil_sensorial(repositorio: RepositorioCataciones, nombre_cafe: str) -> str:
    """Genera un gráfico de radar con el perfil sensorial promedio de un café específico."""
    datos = [d for d in repositorio.listar_todas() if d["Café"] == nombre_cafe]
    if not datos:
        raise ValueError(f"No hay cataciones para el café '{nombre_cafe}'")

    criterios = ["Acidez", "Cuerpo", "Aroma", "Dulzor", "Balance"]
    promedios = [
        round(sum(d[c] for d in datos) / len(datos), 2)
        for c in criterios
    ]

    angulos = [n / float(len(criterios)) * 2 * 3.14159 for n in range(len(criterios))]
    promedios_cerrado = promedios + promedios[:1]
    angulos_cerrado = angulos + angulos[:1]

    os.makedirs(CARPETA_REPORTES, exist_ok=True)
    ruta = os.path.join(CARPETA_REPORTES, f"perfil_{nombre_cafe.replace(' ', '_')}.png")

    plt.figure(figsize=(6, 6))
    ax = plt.subplot(111, polar=True)
    ax.plot(angulos_cerrado, promedios_cerrado, color="#6F4E37", linewidth=2)
    ax.fill(angulos_cerrado, promedios_cerrado, color="#6F4E37", alpha=0.25)
    ax.set_xticks(angulos)
    ax.set_xticklabels(criterios)
    ax.set_ylim(0, 10)
    plt.title(f"Perfil sensorial: {nombre_cafe}")
    plt.tight_layout()
    plt.savefig(ruta)
    plt.close()
    return ruta
