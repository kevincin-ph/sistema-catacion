"""
Tests del módulo modelo.py usando pytest.

Para ejecutar: pytest tests/ -v
"""
import os
import sys
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from modelo import Catacion, RepositorioCataciones


# ---------- Tests de la clase Catacion ----------

def test_puntaje_total_se_calcula_correctamente():
    catacion = Catacion(
        catador="Juan", cafe="Castillo", origen="La Mina",
        acidez=8, cuerpo=6, aroma=6, dulzor=9, balance=7
    )
    assert catacion.puntaje_total == 7.2


def test_catacion_asigna_fecha_automatica_si_no_se_da():
    catacion = Catacion(
        catador="Juan", cafe="Castillo", origen="La Mina",
        acidez=8, cuerpo=6, aroma=6, dulzor=9, balance=7
    )
    assert catacion.fecha != ""


def test_catacion_rechaza_puntaje_fuera_de_rango():
    with pytest.raises(ValueError, match="debe estar entre 0 y 10"):
        Catacion(
            catador="Juan", cafe="Castillo", origen="La Mina",
            acidez=15, cuerpo=6, aroma=6, dulzor=9, balance=7
        )


def test_catacion_rechaza_catador_vacio():
    with pytest.raises(ValueError, match="catador no puede estar vacío"):
        Catacion(
            catador="", cafe="Castillo", origen="La Mina",
            acidez=8, cuerpo=6, aroma=6, dulzor=9, balance=7
        )


def test_catacion_rechaza_nombre_cafe_vacio():
    with pytest.raises(ValueError, match="café no puede estar vacío"):
        Catacion(
            catador="Juan", cafe="", origen="La Mina",
            acidez=8, cuerpo=6, aroma=6, dulzor=9, balance=7
        )


def test_a_fila_devuelve_lista_con_orden_correcto():
    catacion = Catacion(
        catador="Juan", cafe="Castillo", origen="La Mina",
        acidez=8, cuerpo=6, aroma=6, dulzor=9, balance=7, notas="seco"
    )
    fila = catacion.a_fila()
    assert fila[1] == "Juan"
    assert fila[2] == "Castillo"
    assert fila[-1] == "seco"
    assert fila[-2] == 7.2


# ---------- Tests del RepositorioCataciones (usan un archivo temporal) ----------

@pytest.fixture
def repositorio_temporal(tmp_path):
    ruta = tmp_path / "test_cataciones.xlsx"
    return RepositorioCataciones(ruta_archivo=str(ruta))


def test_repositorio_crea_archivo_al_inicializar(repositorio_temporal):
    assert os.path.exists(repositorio_temporal.ruta_archivo)


def test_guardar_y_listar_una_catacion(repositorio_temporal):
    catacion = Catacion(
        catador="Ana", cafe="Geisha", origen="Finca El Roble",
        acidez=9, cuerpo=7, aroma=9, dulzor=8, balance=8
    )
    repositorio_temporal.guardar(catacion)

    resultados = repositorio_temporal.listar_todas()
    assert len(resultados) == 1
    assert resultados[0]["Café"] == "Geisha"
    assert resultados[0]["Puntaje Total"] == 8.2


def test_listar_todas_devuelve_vacio_si_no_hay_datos(repositorio_temporal):
    assert repositorio_temporal.listar_todas() == []


def test_promedio_por_cafe_agrupa_correctamente(repositorio_temporal):
    repositorio_temporal.guardar(Catacion(
        catador="Ana", cafe="Geisha", origen="Finca El Roble",
        acidez=9, cuerpo=7, aroma=9, dulzor=8, balance=8  # promedio 8.2
    ))
    repositorio_temporal.guardar(Catacion(
        catador="Luis", cafe="Geisha", origen="Finca El Roble",
        acidez=7, cuerpo=7, aroma=7, dulzor=7, balance=7  # promedio 7.0
    ))

    promedios = repositorio_temporal.promedio_por_cafe()
    assert promedios["Geisha"] == pytest.approx((8.2 + 7.0) / 2, rel=1e-2)
