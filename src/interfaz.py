"""
Interfaz gráfica del sistema de cataciones, construida con tkinter
(viene incluido con Python, no requiere instalación adicional).
"""
import tkinter as tk
from tkinter import ttk, messagebox
import os
 
from modelo import Catacion, RepositorioCataciones
from graficas import grafica_promedio_por_cafe, grafica_perfil_sensorial
 
# ── Paleta minimalista ──────────────────────────────────────────────
BG        = "#F7F5F2"   # fondo general, blanco cálido
CARD      = "#FFFFFF"   # fondo de campos
TEXTO     = "#1A1A1A"   # texto principal
TEXTO_SEC = "#6B6B6B"   # etiquetas secundarias
ACENTO    = "#2D2D2D"   # botón principal
ACENTO2   = "#5C5C5C"   # botones secundarios
BORDE     = "#E0DDD9"   # bordes suaves
SLIDER_BG = "#F0EDE8"   # fondo de sliders
 
 
class AppCatacion(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("☕ Sistema de Catación de Café")
        self.geometry("500x680")
        self.resizable(False, False)
        self.configure(bg=BG)
 
        self.repositorio = RepositorioCataciones()
        self._construir_widgets()
 
    def _construir_widgets(self):
        # ── Título ──────────────────────────────────────────────────
        tk.Label(
            self, text="Sistema de Catación",
            bg=BG, fg=TEXTO,
            font=("Helvetica", 17, "bold")
        ).pack(pady=(20, 2))
 
        tk.Label(
            self, text="Registra y analiza tus cataciones de café",
            bg=BG, fg=TEXTO_SEC,
            font=("Helvetica", 10)
        ).pack(pady=(0, 14))
 
        # ── Separador ───────────────────────────────────────────────
        tk.Frame(self, bg=BORDE, height=1).pack(fill="x", padx=20, pady=(0, 12))
 
        contenedor = tk.Frame(self, bg=BG)
        contenedor.pack(padx=24, fill="x")
 
        # ── Campos de texto ─────────────────────────────────────────
        self.campos_texto = {}
        for etiqueta, clave in [("Catador", "catador"), ("Café", "cafe"), ("Origen", "origen")]:
            tk.Label(
                contenedor, text=etiqueta.upper(),
                bg=BG, fg=TEXTO_SEC,
                font=("Helvetica", 8, "bold")
            ).pack(anchor="w", pady=(6, 2))
 
            entrada = tk.Entry(
                contenedor,
                font=("Helvetica", 11),
                bg=CARD, fg=TEXTO,
                insertbackground=TEXTO,
                relief="flat",
                bd=0,
                highlightthickness=1,
                highlightbackground=BORDE,
                highlightcolor=ACENTO
            )
            entrada.pack(fill="x", ipady=7)
            self.campos_texto[clave] = entrada
 
        # ── Sliders ─────────────────────────────────────────────────
        tk.Frame(self, bg=BORDE, height=1).pack(fill="x", padx=20, pady=(16, 0))
 
        tk.Label(
            contenedor, text="PUNTAJES SENSORIALES (0 – 10)",
            bg=BG, fg=TEXTO_SEC,
            font=("Helvetica", 8, "bold")
        ).pack(anchor="w", pady=(14, 6))
 
        self.sliders = {}
        for criterio in ["Acidez", "Cuerpo", "Aroma", "Dulzor", "Balance"]:
            fila = tk.Frame(contenedor, bg=BG)
            fila.pack(fill="x", pady=3)
 
            tk.Label(
                fila, text=criterio,
                width=8, anchor="w",
                bg=BG, fg=TEXTO,
                font=("Helvetica", 10)
            ).pack(side="left")
 
            slider = tk.Scale(
                fila, from_=0, to=10, resolution=0.5, orient="horizontal",
                bg=BG,
                fg=TEXTO,
                troughcolor=BORDE,
                activebackground=ACENTO,
                highlightthickness=0,
                bd=0,
                font=("Helvetica", 9)
            )
            slider.set(7)
            slider.pack(side="left", fill="x", expand=True)
            self.sliders[criterio.lower()] = slider
 
        # ── Notas ───────────────────────────────────────────────────
        tk.Label(
            contenedor, text="NOTAS ADICIONALES",
            bg=BG, fg=TEXTO_SEC,
            font=("Helvetica", 8, "bold")
        ).pack(anchor="w", pady=(14, 2))
 
        self.texto_notas = tk.Text(
            contenedor, height=3,
            font=("Helvetica", 10),
            bg=CARD, fg=TEXTO,
            insertbackground=TEXTO,
            relief="flat",
            bd=0,
            highlightthickness=1,
            highlightbackground=BORDE,
            highlightcolor=ACENTO
        )
        self.texto_notas.pack(fill="x", ipady=4, pady=(0, 12))
 
        # ── Botones ─────────────────────────────────────────────────
        tk.Button(
            contenedor, text="Guardar catación",
            command=self._guardar,
            bg=ACENTO, fg="white",
            font=("Helvetica", 11, "bold"),
            relief="flat", pady=10,
            cursor="hand2",
            activebackground="#444444",
            activeforeground="white",
            bd=0
        ).pack(fill="x", pady=(0, 8))
 
        fila_botones = tk.Frame(contenedor, bg=BG)
        fila_botones.pack(fill="x", pady=(0, 14))
 
        for texto, comando in [("Ver historial", self._ver_historial),
                                ("Generar gráficas", self._generar_graficas)]:
            tk.Button(
                fila_botones, text=texto, command=comando,
                bg=CARD, fg=TEXTO,
                font=("Helvetica", 10),
                relief="flat", pady=8,
                cursor="hand2",
                activebackground=BORDE,
                activeforeground=TEXTO,
                bd=0,
                highlightthickness=1,
                highlightbackground=BORDE
            ).pack(side="left", expand=True, fill="x", padx=(0, 4) if texto == "Ver historial" else (4, 0))
 
        # ── Historial ───────────────────────────────────────────────
        tk.Frame(self, bg=BORDE, height=1).pack(fill="x", padx=20, pady=(0, 8))
 
        self.lista_historial = tk.Listbox(
            self,
            font=("Helvetica", 10),
            bg=CARD, fg=TEXTO,
            selectbackground=ACENTO,
            selectforeground="white",
            relief="flat",
            bd=0,
            highlightthickness=0,
            activestyle="none"
        )
        self.lista_historial.pack(padx=20, pady=(0, 16), fill="both", expand=True)
 
    # ── Lógica ──────────────────────────────────────────────────────
    def _guardar(self):
        try:
            catacion = Catacion(
                catador=self.campos_texto["catador"].get(),
                cafe=self.campos_texto["cafe"].get(),
                origen=self.campos_texto["origen"].get(),
                acidez=self.sliders["acidez"].get(),
                cuerpo=self.sliders["cuerpo"].get(),
                aroma=self.sliders["aroma"].get(),
                dulzor=self.sliders["dulzor"].get(),
                balance=self.sliders["balance"].get(),
                notas=self.texto_notas.get("1.0", "end").strip()
            )
            self.repositorio.guardar(catacion)
            messagebox.showinfo("Guardado ✓", f"Puntaje total: {catacion.puntaje_total}/10")
            self._limpiar_formulario()
            self._ver_historial()
        except ValueError as error:
            messagebox.showerror("Error de validación", str(error))
 
    def _limpiar_formulario(self):
        for entrada in self.campos_texto.values():
            entrada.delete(0, "end")
        self.texto_notas.delete("1.0", "end")
        for slider in self.sliders.values():
            slider.set(7)
 
    def _ver_historial(self):
        self.lista_historial.delete(0, "end")
        datos = self.repositorio.listar_todas()
        if not datos:
            self.lista_historial.insert("end", "  No hay cataciones registradas aún")
            return
        for fila in reversed(datos):
            texto = f"  {fila['Café']}  ·  {fila['Origen']}  ·  {fila['Puntaje Total']}/10"
            self.lista_historial.insert("end", texto)
 
    def _generar_graficas(self):
        try:
            ruta = grafica_promedio_por_cafe(self.repositorio)
            messagebox.showinfo(
                "Gráfica generada ✓",
                f"Guardada en:\n{os.path.abspath(ruta)}"
            )
        except ValueError as error:
            messagebox.showwarning("Sin datos", str(error))
 
 
if __name__ == "__main__":
    app = AppCatacion()
    app.mainloop()
