# Calculadora de Integrales Definidas

Este proyecto es una **interfaz gráfica** en Python que permite calcular integrales definidas con presentación en LaTeX y un desglose (pasos) del proceso usado para obtener el resultado. El programa convierte la entrada del usuario a una expresión simbólica con `sympy`, calcula la antiderivada y la integral definida, muestra el resultado numérico y renderiza las fórmulas en imágenes usando `matplotlib` y `Pillow`.

---

## Características principales

- Entrada de funciones en una sola caja de texto (con botones rápidos para insertar `π`, `√`, `^`, `e^x`, `sin(x)`, `cos(x)`, `tan(x)` y `log(x)`).
- Especificación de límites `a` y `b` para la integral definida.
- Cálculo simbólico de la antiderivada \(F(x)\) y el valor de la integral definida \(\int_a^b f(x)\,dx\).
- Renderizado de la integral completa en LaTeX como imagen y visualización de pasos (antiderivada, evaluación en los límites, resultado numérico) en un panel desplazable.
- Manejo de errores con cuadros de diálogo (`SympifyError`, límites inválidos, excepciones generales).

---

## Requisitos (dependencias)

- Python 3.8+ (o equivalente)
- `tkinter` (viene con la mayoría de distribuciones de Python; en Debian/Ubuntu se instala con `sudo apt install python3-tk`)
- `sympy`
- `matplotlib`
- `Pillow` (PIL)

Instalación rápida de dependencias con `pip`:

```bash
pip install sympy matplotlib pillow
```

> `tkinter` normalmente no se instala con `pip`; en sistemas Linux instálalo con el gestor de paquetes si es necesario.

---

## Cómo ejecutar

Desde la terminal, en la carpeta donde esté el archivo `calculadora_IntegralesDef.py` ejecuta:

```bash
python calculadora_IntegralesDef.py
```

Se abrirá una ventana con la calculadora. Los campos principales son:

- Caja de texto principal: expresión a integrar (por defecto aparece `π*sin(√x) + e^x`).
- `Límite a` y `Límite b`: límites de integración.
- Botón `Calcular Integral`: ejecuta el proceso y muestra los resultados.

---

## Formato de entrada y atajos

El programa acepta expresiones en notación cercana a la matemática habitual. Algunas conversiones automáticas están implementadas por el preprocesador:

- `π` → `pi` (constante π de SymPy)
- `√x` o `√(x)` → `sqrt(x)` (raíces)
- `^` o `²`, `³` → `**` (potencias)
- `e^x` o `e**x` → `exp(x)` (función exponencial)
- Inserta `*` cuando haya multiplicación implícita entre número y variable, por ejemplo `2x` → `2*x`.

Atajos (botones) disponibles en la UI: `π`, `√`, `^`, `e^x`, `sin(x)`, `cos(x)`, `tan(x)`, `log(x)`.

**Variable:** el programa asume que la variable es `x`.

---

## Funciones reconocidas

Se proporcionan un conjunto de identificadores en `locals_dict` que `sympy.sympify` usará para interpretar la entrada:

- Constantes y operaciones: `pi`, `e`, `sqrt`, `exp`, `log`, `ln` (ln alias de log)
- Funciones trigonométricas: `sin`, `cos`, `tan`, `asin`, `acos`, `atan`
- Funciones hiperbólicas: `sinh`, `cosh`, `tanh`

Si necesitas ampliar el conjunto de funciones, puedes modificar `self.locals_dict` en la clase `CalculadoraIntegralLatex`.

---

## Qué hace internamente

1. **Preprocesamiento**: la función `preprocesar_funcion(texto)` limpia y transforma la entrada del usuario con varias expresiones regulares para convertir notación "amistosa" (π, √, ^, e^x, multiplicación implícita) a una forma que `sympy` entiende.

2. **Parsing simbólico**: usa `sympy.sympify(texto, locals=self.locals_dict)` para convertir la cadena en una expresión simbólica `f_sym`.

3. **Cálculo simbólico**:

   - `F = integrate(f_sym, x)` calcula una antiderivada simbólica \(F(x)\).
   - `resultado_integral = integrate(f_sym, (x, a, b))` calcula la integral definida simbólicamente.
   - `valor_decimal = float(resultado_integral.evalf())` obtiene una aproximación numérica (decimal) del resultado.

4. **Renderizado LaTeX**:

   - Genera imágenes PNG con `matplotlib` usando `matplotlib.use("Agg")` (backend no interactivo) y guarda dos tipos de imágenes:
     - `resultado_latex.png`: la fórmula completa de la integral con su resultado.
     - `paso_temp.png`: imágenes temporales para cada paso que luego se añaden al `Frame` desplazable.
   - Las imágenes se abren con `PIL.Image` y se muestran en la ventana `tkinter`.

5. **Interfaz de pasos**:

   - Se construye una lista de pasos que contiene las expresiones LaTeX (integral, antiderivada, evaluación en los límites y resultado numérico) y se limita a 8 pasos.
   - Cada paso se renderiza como imagen y se añade a un `Frame` dentro de un `Canvas` con scrollbar vertical para poder desplazar cuando hay muchos pasos.

---

## Salidas y archivos temporales

- Imágenes generadas (por defecto) en la misma carpeta: `resultado_latex.png` y `paso_temp.png` (se sobrescriben en cada renderizado).
- Resultado principal mostrado como texto aproximado (ej. `≈ 1.234567`) y como imagen renderizada en LaTeX.

Si deseas guardar cada paso con nombre único en vez de sobrescribir, modifica la generación de `ruta` en `agregar_paso_latex` (por ejemplo añadiendo un sufijo con el índice del paso o un timestamp).

---

## Manejo de errores y mensajes al usuario

- `SympifyError`: se muestra un `messagebox` indicando que la función no es válida (ejemplo sugerido en el código: `sin(x) + π`).
- `ValueError`: se muestra un `messagebox` indicando que los límites son inválidos.
- Cualquier otra excepción se muestra en un `messagebox` con el mensaje de error.

---

## Limitaciones y consideraciones

- La variable está fijada a `x`. No hay soporte para integrar respecto de otra variable sin modificar el código.
- El preprocesador intenta cubrir casos comunes pero no garantiza parseo correcto para expresiones muy exóticas o mal formateadas.
- Para integrales impropias o con singularidades la evaluación numérica (`float(...)`) puede fallar o dar `inf`/`nan`.
- El renderizado usa archivos PNG temporales; si necesitas evitar archivos en disco usa `BytesIO` para generar imágenes en memoria.
- Aunque `sympy.sympify` se usa con un diccionario de `locals`, siempre hay que ser cauteloso al evaluar entradas arbitrarias en entornos no confiables.

---

## Posibles mejoras

- Añadir soporte para múltiples variables y selección de variable de integración.
- Mejorar el preprocesador para detectar casos complejos de multiplicación implícita.
- Guardar un histórico de cálculos y permitir exportar pasos a PDF o LaTeX.
- Usar `io.BytesIO` para evitar crear archivos temporales en disco.
- Añadir modo "paso a paso" con explicaciones simbólicas más detalladas (p. ej. reglas aplicadas).
- Manejar integrales impropias con chequeos de convergencia y avisos.

---

## Ejemplos de uso

- `π*sin(√x) + e^x` con límites `0` y `1` (valor por defecto en la interfaz).
- `sin(x)` con límites `0` y `π` → resultado aproximadamente `2.0`.
- `x^2` con límites `0` y `3` → antiderivada `x**3/3`, resultado `9.0`.
- `√x` (puedes escribir `√x` o `sqrt(x)`) con límites `0` y `1` → resultado `2/3 ≈ 0.666667`.

---

## Archivo principal

El código fuente principal se encuentra en `calculadora_IntegralesDef.py`.

---

## Licencia

Proyecto perteneciente a Osvaldo Fabian Ramiro Balboa, Georgina Reta Limas

