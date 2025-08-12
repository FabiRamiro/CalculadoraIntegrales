import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
import matplotlib
import re
from sympy import (
    symbols,
    sympify,
    integrate,
    pi,
    E,
    sqrt,
    sin,
    cos,
    tan,
    log,
    exp,
    asin,
    acos,
    atan,
    sinh,
    cosh,
    tanh,
    SympifyError,
    latex,
)

matplotlib.use("Agg")  # Backend no interactivo para renderizar imágenes


def preprocesar_funcion(texto):
    texto = texto.replace(" ", "")
    texto = texto.replace("π", "pi")
    texto = texto.replace("²", "**2").replace("³", "**3")
    texto = texto.replace("^", "**")
    texto = re.sub(r"√(\w+)", r"sqrt(\1)", texto)
    texto = re.sub(r"√\((.*?)\)", r"sqrt(\1)", texto)
    texto = re.sub(r"e\*\*(\w+)", r"exp(\1)", texto)
    texto = re.sub(r"e\*\*\((.*?)\)", r"exp(\1)", texto)
    texto = re.sub(r"(\d)([a-zA-Z\(])", r"\1*\2", texto)
    texto = re.sub(r"(\))(\w)", r"\1*\2", texto)
    return texto


class CalculadoraIntegralLatex(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculadora de Integrales")
        self.geometry("750x750")
        self.configure(bg="#f8f6ff")
        self.resizable(True, True)

        self.funcion = tk.StringVar(value="π*sin(√x) + e^x")
        self.limite_a = tk.StringVar(value="0")
        self.limite_b = tk.StringVar(value="1")
        self.resultado = tk.StringVar(value="Resultado decimal")

        self.locals_dict = {
            "pi": pi,
            "e": E,
            "sqrt": sqrt,
            "sin": sin,
            "cos": cos,
            "tan": tan,
            "asin": asin,
            "acos": acos,
            "atan": atan,
            "sinh": sinh,
            "cosh": cosh,
            "tanh": tanh,
            "log": log,
            "ln": log,
            "exp": exp,
        }

        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure(
            "TButton",
            padding=6,
            relief="flat",
            background="#b497ff",
            foreground="white",
            font=("Segoe UI", 11),
        )
        self.style.map("TButton", background=[("active", "#a07bff")])

        self.style.configure("TEntry", padding=5, relief="flat", font=("Segoe UI", 12))
        self.style.configure("TLabel", background="#f8f6ff", font=("Segoe UI", 12))

        self.construir_ui()

    def construir_ui(self):
        fuente_titulo = ("Segoe UI", 18, "bold")

        frame_main = tk.Frame(self, bg="#f8f6ff")
        frame_main.pack(expand=True, fill="both", padx=15, pady=15)

        tk.Label(
            frame_main,
            text="Calculadora de Integrales Definidas",
            font=fuente_titulo,
            bg="#f8f6ff",
            fg="#6f42c1",
        ).pack(pady=10)

        ttk.Entry(frame_main, textvariable=self.funcion, width=50).pack(
            pady=8, fill="x"
        )

        botones = [
            ("π", "π"),
            ("√", "√("),
            ("^", "^"),
            ("e^x", "e^x"),
            ("sin(x)", "sin(x)"),
            ("cos(x)", "cos(x)"),
            ("tan(x)", "tan(x)"),
            ("log(x)", "log(x)"),
        ]
        frame_botones = tk.Frame(frame_main, bg="#f8f6ff")
        frame_botones.pack(pady=5)
        for texto, valor in botones:
            ttk.Button(
                frame_botones, text=texto, command=lambda val=valor: self.agregar(val)
            ).pack(side="left", padx=3, pady=3)

        frame_limites = tk.Frame(frame_main, bg="#f8f6ff")
        frame_limites.pack(pady=10)
        tk.Label(frame_limites, text="Límite a:", bg="#f8f6ff").pack(side="left")
        ttk.Entry(frame_limites, textvariable=self.limite_a, width=6).pack(
            side="left", padx=5
        )
        tk.Label(frame_limites, text="Límite b:", bg="#f8f6ff").pack(side="left")
        ttk.Entry(frame_limites, textvariable=self.limite_b, width=6).pack(
            side="left", padx=5
        )

        ttk.Button(frame_main, text="Calcular Integral", command=self.calcular).pack(
            pady=12
        )

        tk.Label(
            frame_main,
            textvariable=self.resultado,
            font=("Segoe UI", 13, "bold"),
            bg="#f8f6ff",
            fg="#343a40",
        ).pack()

        self.imagen_latex = tk.Label(frame_main, bg="#f8f6ff")
        self.imagen_latex.pack(pady=10, expand=False)

        # Frame para pasos
        self.frame_pasos = tk.Frame(frame_main, bg="#f8f6ff", bd=1, relief="sunken")
        self.frame_pasos.pack(fill="both", expand=True, pady=10)

        self.canvas = tk.Canvas(self.frame_pasos, bg="#f8f6ff", highlightthickness=0)
        self.v_scroll = ttk.Scrollbar(
            self.frame_pasos, orient="vertical", command=self.canvas.yview
        )
        self.canvas.configure(yscrollcommand=self.v_scroll.set)

        self.v_scroll.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.inner_frame = tk.Frame(self.canvas, bg="#f8f6ff")
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

        self.inner_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )

    def agregar(self, valor):
        self.funcion.set(self.funcion.get() + valor)

    def calcular(self):
        try:
            x = symbols("x")
            texto = preprocesar_funcion(self.funcion.get())
            f_sym = sympify(texto, locals=self.locals_dict)

            a_expr = sympify(self.limite_a.get(), locals=self.locals_dict)
            b_expr = sympify(self.limite_b.get(), locals=self.locals_dict)
            a = float(a_expr.evalf())
            b = float(b_expr.evalf())

            # Calcular integral y antiderivada
            F = integrate(f_sym, x)
            resultado_integral = integrate(f_sym, (x, a, b))
            valor_decimal = float(resultado_integral.evalf())
            self.resultado.set(f"≈ {valor_decimal:.6f}")

            # Mostrar resultado principal
            integral_latex = (
                r"\int_{"
                + str(a)
                + r"}^{"
                + str(b)
                + r"} "
                + latex(f_sym)
                + r"\, dx = "
                + latex(resultado_integral)
            )
            self.render_latex(integral_latex)

            # Mostrar pasos
            self.mostrar_pasos(f_sym, F, a, b, resultado_integral, valor_decimal)

        except SympifyError:
            messagebox.showerror("Error", "Función no válida. Ejemplo: sin(x) + π")
        except ValueError:
            messagebox.showerror("Error", "Límites inválidos. Usa números reales.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error:\n{str(e)}")

    def mostrar_pasos(self, f_sym, F, a, b, resultado, valor_decimal):
        # Limpiar pasos previos
        for widget in self.inner_frame.winfo_children():
            widget.destroy()

        pasos = [
            rf"\int_{{{a}}}^{{{b}}} {latex(f_sym)}\,dx",
            rf"F(x) = {latex(F)}",
            rf"F({b}) - F({a})",
            rf"{latex(F.subs('x', b))} - {latex(F.subs('x', a))}",
            rf"{latex(F.subs('x', b) - F.subs('x', a))}",
            rf"\approx {valor_decimal:.6f}",
        ]

        # Limitar a 8 pasos
        pasos = pasos[:8]

        for i, paso in enumerate(pasos, start=1):
            self.agregar_paso_latex(f"Paso {i}: {paso}")

    def agregar_paso_latex(self, latex_expr):
        plt.figure(figsize=(7, 0.8))
        plt.text(0, 0.5, f"${latex_expr}$", fontsize=16, ha="left", va="center")
        plt.axis("off")
        plt.tight_layout()
        ruta = "paso_temp.png"
        plt.savefig(ruta, dpi=150, bbox_inches="tight", transparent=True)
        plt.close()

        imagen = Image.open(ruta)
        img_tk = ImageTk.PhotoImage(imagen)
        label_img = tk.Label(self.inner_frame, image=img_tk, bg="#f8f6ff")
        label_img.image = img_tk
        label_img.pack(anchor="w", pady=3)

    def render_latex(self, latex_expr):
        plt.figure(figsize=(6, 1.2))
        plt.text(0.5, 0.5, f"${latex_expr}$", fontsize=20, ha="center", va="center")
        plt.axis("off")
        plt.tight_layout()
        ruta = "resultado_latex.png"
        plt.savefig(ruta, dpi=150, bbox_inches="tight", transparent=True)
        plt.close()

        imagen = Image.open(ruta)
        imagen_tk = ImageTk.PhotoImage(imagen)
        self.imagen_latex.configure(image=imagen_tk)
        self.imagen_latex.image = imagen_tk


if __name__ == "__main__":
    app = CalculadoraIntegralLatex()
    app.mainloop()
