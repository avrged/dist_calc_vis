# Codigo por EMN / @avrged
import importlib
import tkinter as tk
import stats_functions as stfn
import matplotlib.pyplot as plt
from tkinter import Label, Button, Frame, ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.stats import binom, hypergeom, bernoulli, geom, poisson
from matplotlib.figure import Figure

importlib.reload(stfn)

class Style:
    # Paleta de colores utilizada
    # Fueron elegidos gracias a su facilidad de lectura y contraste

    PRIMARY = "#2C3E50"      # Azul marino (para barras resaltadas y elementos principales)
    SECONDARY = "#B3C6E7"    # Azul grisáceo claro (para barras normales y elementos secundarios)
    BG_PRIMARY = "#F5F7FA"   # Gris muy claro (fondo general)
    BG_SECONDARY = "#FFFFFF" # Blanco (fondo de elementos)
    TEXT_PRIMARY = "#2C3E50" # Azul marino (texto principal)
    TEXT_SECONDARY = "#7F8C8D" # Gris (texto secundario)
    HOVER = "#34495E"        # Azul marino más oscuro (para hover de botones)

    # Fuentes utilizadas
    FONT_FAMILY = "Segoe UI"
    FONT_TITLE = (FONT_FAMILY, 16, "bold")
    FONT_SUBTITLE = (FONT_FAMILY, 12, "bold")
    FONT_TEXT = (FONT_FAMILY, 10)
    FONT_BUTTON = (FONT_FAMILY, 9, "bold")
    
    # Estilo de botones
    BUTTON_CONFIG = {
        "font": FONT_BUTTON,
        "bg": PRIMARY,       
        "fg": BG_SECONDARY,  
        "relief": tk.FLAT,
        "padx": 15,
        "pady": 5,
        "cursor": "hand2"
    }
    
    # Estilo de etiquetas
    LABEL_CONFIG = {
        "font": FONT_TEXT,
        "bg": BG_PRIMARY,
        "fg": TEXT_PRIMARY,
        "padx": 5,
        "pady": 5
    }
    
    # Estilo de frames
    FRAME_CONFIG = {
        "bg": BG_PRIMARY,    
        "relief": tk.FLAT,
        "padx": 10,
        "pady": 10
    }
    
    # Estilo de las entradas de datos
    ENTRY_CONFIG = {
        "font": FONT_TEXT,
        "relief": tk.SOLID,
        "bd": 1,
        "bg": BG_SECONDARY
    }
    
    # Estilo de las graficas hechas con matplotlib
    PLOT_STYLE = {
        "figure.facecolor": BG_PRIMARY,
        "axes.facecolor": BG_PRIMARY,
        "axes.edgecolor": TEXT_SECONDARY,
        "axes.labelcolor": TEXT_PRIMARY,
        "axes.titlecolor": PRIMARY,
        "xtick.color": TEXT_SECONDARY,
        "ytick.color": TEXT_SECONDARY,
        "grid.color": SECONDARY,
        "grid.alpha": 0.1
    }
    
    # Estilo de la caja de probabilidad segun los casos 
    PROB_BOX_STYLE = {
        "boxstyle": "round,pad=0.5",
        "facecolor": BG_PRIMARY,
        "edgecolor": PRIMARY,
        "alpha": 0.95,
        "linewidth": 2
    }

# Estilo de la libreria matplotlib
plt.style.use(Style.PLOT_STYLE)

# Funcion que crea las formulas base de cada caso, utilizando LaTeX
def create_base_formula(text):
    fig = Figure(figsize=(6, 1.5))
    ax = fig.add_subplot(111)
    
    if text == "BINOMIAL":
        formula = r"$P(X = x) = \binom{n}{x} p^x (1-p)^{n-x}$"
    elif text == "HIPERGEOMETRICA":
        formula = r"$P(X = k) = \frac{\binom{K}{k} \binom{N-K}{n-k}}{\binom{N}{n}}$"
    elif text == "BERNOULLI":
        formula = r"$P(X = x) = p^x (1-p)^{1-x}$"
    elif text == "GEOMETRICA":
        formula = r"$P(X = x) = (1-p)^{x-1} p$"
    elif text == "POISSON":
        formula = r"$P(X = k) = \frac{\lambda^k e^{-\lambda}}{k!}$"
    
    ax.text(0.5, 0.5, formula, fontsize=14, ha='center', va='center')
    ax.axis('off')
    fig.tight_layout()
    return fig

# Función para crear fórmulas con valores sustituidos utilizando LaTeX
def create_formula(text, **kwargs):
    fig = Figure(figsize=(6, 1.5))
    ax = fig.add_subplot(111)
    
    if text == "BINOMIAL":
        n = kwargs.get('n', '')
        x = kwargs.get('x', '')
        p = kwargs.get('p', '')
        formula = f"$P(X = {x}) = \\binom{{{n}}}{{{x}}} ({p})^{{{x}}} (1-{p})^{{{n}-{x}}}$"
    elif text == "HIPERGEOMETRICA":
        N = kwargs.get('N', '')
        K = kwargs.get('K', '')
        n = kwargs.get('n', '')
        k = kwargs.get('k', '')
        formula = f"$P(X = {k}) = \\frac{{\\binom{{{K}}}{{{k}}} \\binom{{{N-K}}}{{{n-k}}}}}{{\\binom{{{N}}}{{{n}}}}}$"
    elif text == "BERNOULLI":
        p = kwargs.get('p', '')
        x = kwargs.get('x', '')
        formula = f"$P(X = {x}) = {p}^{{{x}}} (1-{p})^{{1-{x}}}$"
    elif text == "GEOMETRICA":
        p = kwargs.get('p', '')
        x = kwargs.get('x', '')
        formula = f"$P(X = {x}) = (1-{p})^{{{x}-1}} {p}$"
    elif text == "POISSON":
        lam = kwargs.get('lam', '')
        k = kwargs.get('k', '')
        formula = f"$P(X = {k}) = \\frac{{{lam}^{k} e^{{-{lam}}}}}{{{k}!}}$"
    
    ax.text(0.5, 0.5, formula, fontsize=14, ha='center', va='center')
    ax.axis('off')
    fig.tight_layout()
    return fig

# Función para actualizar la fórmula en la interfaz con los valores dados
def update_formula(fig):
    for widget in formula_frame.winfo_children():
        widget.destroy()
    canvas = FigureCanvasTkAgg(fig, master=formula_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

def show_random_samples(dist_type, **params):
    # Crear nueva ventana
    samples_window = tk.Toplevel()
    samples_window.title("Histograma de Muestras Aleatorias")
    samples_window.configure(bg=Style.BG_PRIMARY)
    
    # Generar muestras según la distribución
    try:
        if dist_type == "BINOMIAL":
            samples = binom.rvs(n=params['n'], p=params['p'], size=1000)
        elif dist_type == "HIPERGEOMETRICA":
            samples = hypergeom.rvs(M=params['N'], n=params['n'], N=params['K'], size=1000)
        elif dist_type == "BERNOULLI":
            samples = bernoulli.rvs(p=params['p'], size=1000)
        elif dist_type == "GEOMETRICA":
            samples = geom.rvs(p=params['p'], size=1000)
        elif dist_type == "POISSON":
            samples = poisson.rvs(mu=params['lam'], size=1000)
        
        # Crear figura
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.hist(samples, bins='auto', color=Style.SECONDARY, edgecolor=Style.PRIMARY)
        
        # Estilo del histograma
        ax.set_title('Histograma de 1000 Muestras Aleatorias', 
                     color=Style.PRIMARY, 
                     pad=20)
        ax.set_xlabel('Valores', color=Style.TEXT_SECONDARY)
        ax.set_ylabel('Frecuencia', color=Style.TEXT_SECONDARY)
        
        # Configurar estilo
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color(Style.TEXT_SECONDARY)
        ax.spines['bottom'].set_color(Style.TEXT_SECONDARY)
        
        # Mostrar en la nueva ventana
        canvas = FigureCanvasTkAgg(fig, master=samples_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
    except Exception as e:
        messagebox.showerror("Error", f"Error al generar las muestras: {str(e)}")
        samples_window.destroy()

# Funcion para los procesos a realizar con el boton de calcular (submit)
def on_button_click(text):
    def submit():
        buscar = int(buscar_entry.get())
        condicion = condicion_combobox.get()
        
        if text == "BINOMIAL":
            n = int(n_entry.get())
            x = int(x_entry.get())
            p = float(p_entry.get())
            prob = stfn.binomial(n, x, p)
            result_label.config(text=f"n={n}, x={x}, p={p}\nProbabilidad: {prob}")
            formula_fig = create_formula(text, n=n, x=x, p=p)
            update_formula(formula_fig)
            plot_binomial(n, p, buscar, condicion)
            
            # Agregar botón de muestras aleatorias
            Button(input_frame, 
                   text="Cálculo con muestras aleatorias", 
                   command=lambda: show_random_samples("BINOMIAL", n=n, p=p),
                   **Style.BUTTON_CONFIG).grid(row=7, column=0, columnspan=2, pady=5)
            
        elif text == "HIPERGEOMETRICA":
            N = int(N_entry.get())
            K = int(K_entry.get())
            n = int(n_entry.get())
            k = int(k_entry.get())
            prob = stfn.hipergeometrica(N, K, n, k)
            result_label.config(text=f"N={N}, K={K}, n={n}, k={k}\nProbabilidad: {prob}")
            formula_fig = create_formula(text, N=N, K=K, n=n, k=k)
            update_formula(formula_fig)
            plot_hipergeometrica(N, K, n, buscar, condicion)
            
            # Agregar botón de muestras aleatorias
            Button(input_frame, 
                   text="Cálculo con muestras aleatorias",
                   command=lambda: show_random_samples("HIPERGEOMETRICA", N=N, K=K, n=n),
                   **Style.BUTTON_CONFIG).grid(row=7, column=0, columnspan=2, pady=5)
            
        elif text == "BERNOULLI":
            p = float(p_entry.get())
            x = int(x_entry.get())
            if x not in [0, 1]:
                result_label.config(text="Error: x debe ser 0 o 1 para la distribución Bernoulli")
                return
            prob = stfn.bernoulli(p, x)
            result_label.config(text=f"p={p}, x={x}\nProbabilidad: {prob}")
            formula_fig = create_formula(text, p=p, x=x)
            update_formula(formula_fig)
            plot_bernoulli(p, buscar, condicion)
            
            # Agregar botón de muestras aleatorias
            Button(input_frame, 
                   text="Cálculo con muestras aleatorias",
                   command=lambda: show_random_samples("BERNOULLI", p=p),
                   **Style.BUTTON_CONFIG).grid(row=7, column=0, columnspan=2, pady=5)
            
        elif text == "GEOMETRICA":
            p = float(p_entry.get())
            x = int(x_entry.get())
            prob = stfn.geometrica(p, x)
            result_label.config(text=f"p={p}, x={x}\nProbabilidad: {prob}")
            formula_fig = create_formula(text, p=p, x=x)
            update_formula(formula_fig)
            plot_geometrica(p, buscar, condicion)
            
            # Agregar botón de muestras aleatorias
            Button(input_frame, 
                   text="Cálculo con muestras aleatorias",
                   command=lambda: show_random_samples("GEOMETRICA", p=p),
                   **Style.BUTTON_CONFIG).grid(row=7, column=0, columnspan=2, pady=5)
            
        elif text == "POISSON":
            lam = float(lam_entry.get())
            k = int(k_entry.get())
            prob = stfn.poisson(lam, k)
            result_label.config(text=f"λ={lam}, k={k}\nProbabilidad: {prob}")
            formula_fig = create_formula(text, lam=lam, k=k)
            update_formula(formula_fig)
            plot_poisson(lam, buscar, condicion)
            
            # Agregar botón de muestras aleatorias
            Button(input_frame, 
                   text="Cálculo con muestras aleatorias",
                   command=lambda: show_random_samples("POISSON", lam=lam),  # Changed from 'lambda' to 'lam'
                   **Style.BUTTON_CONFIG).grid(row=7, column=0, columnspan=2, pady=5)
    
    for widget in variable_frame.winfo_children():
        widget.destroy()

# Crear subframes para entradas y fórmulas
    input_frame = Frame(variable_frame, **Style.FRAME_CONFIG)
    input_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
    
    formula_container = Frame(variable_frame, **Style.FRAME_CONFIG)  # Cambiado de input_frame a variable_frame
    formula_container.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")  # Columna 1 para ponerlo a la derecha
    
    # Etiquetas para las fórmulas
    Label(formula_container, 
          text="Fórmula general:",
          font=Style.FONT_SUBTITLE,
          bg=Style.BG_PRIMARY,
          fg=Style.TEXT_PRIMARY).pack(anchor="w", padx=5)
    
    global formula_frame
    formula_frame = Frame(formula_container, **Style.FRAME_CONFIG, width=300, height=60)
    formula_frame.pack(fill="both", expand=True)
    formula_frame.pack_propagate(False)
    
    # Frame para resultados debajo de la fórmula
    result_container = Frame(formula_container, **Style.FRAME_CONFIG)
    result_container.pack(fill="x", expand=False, pady=(5,0))
    
    global result_label
    result_label = Label(result_container, 
                        text="", 
                        font=(Style.FONT_FAMILY, 12, "bold"),
                        bg=Style.BG_PRIMARY,
                        fg=Style.PRIMARY)
    result_label.pack(anchor="center")
    
    # Configurar pesos de columnas para mantener proporciones
    variable_frame.grid_columnconfigure(0, weight=3)  
    variable_frame.grid_columnconfigure(1, weight=2)

    # Crear entradas de datos (parámetros) según el tipo de distribución
    if text == "BINOMIAL":
        Label(input_frame, text="Número de ensayos (n):", **Style.LABEL_CONFIG).grid(row=0, column=0, padx=5, pady=5)
        n_entry = tk.Entry(input_frame, **Style.ENTRY_CONFIG)
        n_entry.grid(row=0, column=1)

        Label(input_frame, text="Número de éxitos (x):", **Style.LABEL_CONFIG).grid(row=1, column=0, padx=5, pady=5)
        x_entry = tk.Entry(input_frame, **Style.ENTRY_CONFIG)
        x_entry.grid(row=1, column=1, padx=5, pady=5)

        Label(input_frame, text="Probabilidad de éxito (p):", **Style.LABEL_CONFIG).grid(row=2, column=0, padx=5, pady=5)
        p_entry = tk.Entry(input_frame, **Style.ENTRY_CONFIG)
        p_entry.grid(row=2, column=1, padx=5, pady=5)

    elif text == "HIPERGEOMETRICA":
        Label(input_frame, text="Tamaño de la población (N):", **Style.LABEL_CONFIG).grid(row=0, column=0, padx=5, pady=5)
        N_entry = tk.Entry(input_frame, **Style.ENTRY_CONFIG)
        N_entry.grid(row=0, column=1, padx=5, pady=5)

        Label(input_frame, text="Número de éxitos en la población (K):", **Style.LABEL_CONFIG).grid(row=1, column=0, padx=5, pady=5)
        K_entry = tk.Entry(input_frame, **Style.ENTRY_CONFIG)
        K_entry.grid(row=1, column=1, padx=5, pady=5)

        Label(input_frame, text="Tamaño de la muestra (n):", **Style.LABEL_CONFIG).grid(row=2, column=0, padx=5, pady=5)
        n_entry = tk.Entry(input_frame, **Style.ENTRY_CONFIG)
        n_entry.grid(row=2, column=1, padx=5, pady=5)

        Label(input_frame, text="Número de éxitos en la muestra (k):", **Style.LABEL_CONFIG).grid(row=3, column=0, padx=5, pady=5)
        k_entry = tk.Entry(input_frame, **Style.ENTRY_CONFIG)
        k_entry.grid(row=3, column=1, padx=5, pady=5)

    elif text == "BERNOULLI":
        Label(input_frame, text="Probabilidad de éxito (p):", **Style.LABEL_CONFIG).grid(row=0, column=0, padx=5, pady=5)
        p_entry = tk.Entry(input_frame, **Style.ENTRY_CONFIG)
        p_entry.grid(row=0, column=1, padx=5, pady=5)

        Label(input_frame, text="Número de éxitos (x):", **Style.LABEL_CONFIG).grid(row=1, column=0, padx=5, pady=5)
        x_entry = tk.Entry(input_frame, **Style.ENTRY_CONFIG)
        x_entry.grid(row=1, column=1, padx=5, pady=5)

    elif text == "GEOMETRICA":
        Label(input_frame, text="Probabilidad de éxito (p):", **Style.LABEL_CONFIG).grid(row=0, column=0, padx=5, pady=5)
        p_entry = tk.Entry(input_frame, **Style.ENTRY_CONFIG)
        p_entry.grid(row=0, column=1, padx=5, pady=5)

        Label(input_frame, text="Número de ensayos hasta el primer éxito (x):", **Style.LABEL_CONFIG).grid(row=1, column=0, padx=5, pady=5)
        x_entry = tk.Entry(input_frame, **Style.ENTRY_CONFIG)
        x_entry.grid(row=1, column=1, padx=5, pady=5)

    elif text == "POISSON":
        Label(input_frame, text="Tasa de éxito promedio (λ):", **Style.LABEL_CONFIG).grid(row=0, column=0, padx=5, pady=5)
        lam_entry = tk.Entry(input_frame, **Style.ENTRY_CONFIG)
        lam_entry.grid(row=0, column=1, padx=5, pady=5)

        Label(input_frame, text="Número de éxitos (k):", **Style.LABEL_CONFIG).grid(row=1, column=0, padx=5, pady=5)
        k_entry = tk.Entry(input_frame, **Style.ENTRY_CONFIG)
        k_entry.grid(row=1, column=1, padx=5, pady=5)

    Label(input_frame, text="Valor a buscar:", **Style.LABEL_CONFIG).grid(row=4, column=0, padx=5, pady=5)
    buscar_entry = tk.Entry(input_frame, **Style.ENTRY_CONFIG)
    buscar_entry.grid(row=4, column=1, padx=5, pady=5)

    Label(input_frame, text="Condición:", **Style.LABEL_CONFIG).grid(row=5, column=0, padx=5, pady=5)
    condicion_combobox = ttk.Combobox(input_frame, values=["Igual", "Menor", "Mayor", "Menor o igual", "Mayor o igual", "Indiferente"])
    condicion_combobox.grid(row=5, column=1, padx=5, pady=5)
    condicion_combobox.set("Indiferente")

    Button(input_frame, text="Calcular", command=submit, **Style.BUTTON_CONFIG).grid(row=6, column=0, columnspan=2, pady=10)

    # Mostrar fórmula base inicial
    initial_fig = create_base_formula(text)
    update_formula(initial_fig)

# Funciones para poder graficar los resultados dados utilizando matplotlib y scipy
def plot_binomial(n, p, buscar, condicion):
    x_posibles = list(range(n + 1))
    resultados = [stfn.binomial(n, x, p) for x in x_posibles]
    plot_distribution(x_posibles, resultados, "", buscar, condicion)

def plot_hipergeometrica(N, K, n, buscar, condicion):
    x_posibles = list(range(min(K, n) + 1))
    resultados = [stfn.hipergeometrica(N, K, n, x) for x in x_posibles]
    plot_distribution(x_posibles, resultados, "", buscar, condicion)

def plot_bernoulli(p, buscar, condicion):
    x_posibles = [0, 1]
    resultados = [stfn.bernoulli(p, x) for x in x_posibles]
    plot_distribution(x_posibles, resultados, "", buscar, condicion)

def plot_geometrica(p, buscar, condicion):
    x_posibles = list(range(1, 11))
    resultados = [stfn.geometrica(p, x) for x in x_posibles]
    plot_distribution(x_posibles, resultados, "", buscar, condicion)

def plot_poisson(lam, buscar, condicion):
    x_posibles = list(range(20))
    resultados = [stfn.poisson(lam, x) for x in x_posibles]
    plot_distribution(x_posibles, resultados, "", buscar, condicion)

def plot_distribution(x, y, title, buscar, condicion):
    for widget in plot_frame.winfo_children():
        widget.destroy()

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.bar(x, y, color='#B3C6E7', edgecolor=None)
    fig.subplots_adjust(bottom=0.15)  
    ax.bar(x, y, color='#B3C6E7', edgecolor=None)

    # Calcular la probabilidad acumulada según la condición
    if condicion == "Igual":
        indices = [i for i, val in enumerate(x) if val == buscar]
        prob_acum = sum(y[i] for i in indices)
        prob_text = f"P(X = {buscar}) = {prob_acum:.4f}%"
    elif condicion == "Menor":
        indices = [i for i, val in enumerate(x) if val < buscar]
        prob_acum = sum(y[i] for i in indices)
        prob_text = f"P(X < {buscar}) = {prob_acum:.4f}%"
    elif condicion == "Mayor":
        indices = [i for i, val in enumerate(x) if val > buscar]
        prob_acum = sum(y[i] for i in indices)
        prob_text = f"P(X > {buscar}) = {prob_acum:.4f}%"
    elif condicion == "Menor o igual":
        indices = [i for i, val in enumerate(x) if val <= buscar]
        prob_acum = sum(y[i] for i in indices)
        prob_text = f"P(X ≤ {buscar}) = {prob_acum:.4f}%"
    elif condicion == "Mayor o igual":
        indices = [i for i, val in enumerate(x) if val >= buscar]
        prob_acum = sum(y[i] for i in indices)
        prob_text = f"P(X ≥ {buscar}) = {prob_acum:.4f}%"
    elif condicion == "Indiferente":
        indices = [i for i, val in enumerate(x) if val != buscar]
        prob_acum = sum(y[i] for i in indices)
        prob_text = f"P(X ≠ {buscar}) = {prob_acum:.4f}%"
    else:
        indices = range(len(x))
        prob_acum = sum(y)
        prob_text = f"Probabilidad total = {prob_acum:.4f}%"

    # Colorear las barras según la condición
    for i in indices:
        ax.bar(x[i], y[i], color=Style.PRIMARY, edgecolor=None)

    # Agregar cuadro de texto con la probabilidad
    ax.text(0.95, 0.95, prob_text, 
            transform=ax.transAxes,
            fontsize=10,
            fontweight='bold',
            verticalalignment='top',
            horizontalalignment='right',
            bbox=Style.PROB_BOX_STYLE,
            color=Style.PRIMARY)
    
    # Etiquetas de los ejes con padding ajustado
    ax.set_xlabel('Valores', fontsize=10, color=Style.TEXT_SECONDARY, labelpad=10)
    ax.set_ylabel('Probabilidad', fontsize=10, color=Style.TEXT_SECONDARY)
    
    # Estilo de la gráfica
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(Style.TEXT_SECONDARY)
    ax.spines['bottom'].set_color(Style.TEXT_SECONDARY)
    
    # Ajustar layout con márgenes específicos
    plt.tight_layout(pad=1.5, rect=[0.05, 0.1, 0.95, 0.95])

    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

def show_random_samples(dist_type, **params):
    # Crear nueva ventana
    samples_window = tk.Toplevel()
    samples_window.title("Histograma de Muestras Aleatorias")
    samples_window.configure(bg=Style.BG_PRIMARY)
    
    # Generar muestras según la distribución
    if dist_type == "BINOMIAL":
        samples = binom.rvs(n=params['n'], p=params['p'], size=1000)
    elif dist_type == "HIPERGEOMETRICA":
        samples = hypergeom.rvs(M=params['N'], n=params['n'], N=params['K'], size=1000)
    elif dist_type == "BERNOULLI":
        samples = bernoulli.rvs(p=params['p'], size=1000)
    elif dist_type == "GEOMETRICA":
        samples = geom.rvs(p=params['p'], size=1000)
    elif dist_type == "POISSON":
        samples = poisson.rvs(mu=params['lambda'], size=1000)
    
    # Crear figura
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.hist(samples, bins='auto', color=Style.SECONDARY, edgecolor=Style.PRIMARY)
    
    # Estilo del histograma
    ax.set_title('Histograma de 1000 Muestras Aleatorias', 
                 color=Style.PRIMARY, 
                 pad=20)
    ax.set_xlabel('Valores', color=Style.TEXT_SECONDARY)
    ax.set_ylabel('Frecuencia', color=Style.TEXT_SECONDARY)
    
    # Configurar estilo
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(Style.TEXT_SECONDARY)
    ax.spines['bottom'].set_color(Style.TEXT_SECONDARY)
    
    # Mostrar en la nueva ventana
    canvas = FigureCanvasTkAgg(fig, master=samples_window)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Funcion para darle estilo a la GUI y crearla
def create_gui():
    global root, variable_frame, result_label, plot_frame, formula_frame, container
    root = tk.Tk()
    root.title("Distribuciones de Probabilidad")
    
    # Centrar la ventana en la pantalla
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    # Ajustar el tamaño de la ventana con parametros maximos (reducir el factor de ancho)
    window_width = int(screen_width * 0.6)  
    window_height = int(screen_height * 0.8)
    window_width = max(800, min(window_width, 1000))  
    window_height = max(600, min(window_height, 900))
    position_top = int(screen_height / 2 - window_height / 2)
    position_right = int(screen_width / 2 - window_width / 2)
    root.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')
    # Permitir redimensionamiento vertical pero no horizontal
    root.resizable(False, True)
    root.configure(bg=Style.BG_PRIMARY)
    
    # Ajustar tamaños de fuente basados en la resolución
    scale_factor = min(window_width/1000, window_height/900)  # Factor de escala basado en la resolución base
    Style.FONT_TITLE = (Style.FONT_FAMILY, int(16 * scale_factor), "bold")
    Style.FONT_SUBTITLE = (Style.FONT_FAMILY, int(12 * scale_factor), "bold")
    Style.FONT_TEXT = (Style.FONT_FAMILY, int(10 * scale_factor))
    Style.FONT_BUTTON = (Style.FONT_FAMILY, int(9 * scale_factor), "bold")
    
    # Actualizar configuraciones que dependen de las fuentes
    Style.BUTTON_CONFIG.update({"font": Style.FONT_BUTTON})
    Style.LABEL_CONFIG.update({"font": Style.FONT_TEXT})
    Style.ENTRY_CONFIG.update({"font": Style.FONT_TEXT})
    
    # Título principal (reducido el padding vertical)
    title_label = Label(root, 
                       text="Calculadora de distribuciones de probabilidad",
                       font=Style.FONT_TITLE,
                       bg=Style.BG_PRIMARY,
                       fg=Style.PRIMARY)
    title_label.pack(pady=int(5 * scale_factor))
     
    # Contenedor principal
    container = Frame(root, **Style.FRAME_CONFIG)
    container.pack(pady=int(5 * scale_factor), fill=tk.BOTH, expand=True)
    
    # Centrar los botones y dar peso igual a todas las columnas
    for i in range(5):
        container.grid_columnconfigure(i, weight=1)
     
    discreta_label = Label(container,
                          text="Distribuciones discretas",
                          font=Style.FONT_SUBTITLE,
                          bg=Style.BG_PRIMARY,
                          fg=Style.PRIMARY)
    discreta_label.grid(row=0, column=0, columnspan=5, pady=(0, int(5 * scale_factor)))
    
    # Frame para botones
    button_frame = Frame(container, bg=Style.BG_PRIMARY)
    button_frame.grid(row=1, column=0, columnspan=5, pady=int(5 * scale_factor))
    
    # Botones para elegir distribución discreta
    discreta_buttons = ["BERNOULLI", "BINOMIAL", "GEOMETRICA", "POISSON", "HIPERGEOMETRICA"]
    
    for i, text in enumerate(discreta_buttons):
        btn = Button(button_frame, text=text, **Style.BUTTON_CONFIG,
                    command=lambda t=text: on_button_click(t))
        btn.pack(side=tk.LEFT, padx=1)
        
        btn.bind("<Enter>", lambda e, btn=btn: btn.configure(bg=Style.HOVER))
        btn.bind("<Leave>", lambda e, btn=btn: btn.configure(bg=Style.PRIMARY))

    # Frame para las variables
    variable_frame = Frame(container, **Style.FRAME_CONFIG)
    variable_frame.grid(row=2, column=0, columnspan=5, pady=10, sticky="ew")  # Reducido pady de 20 a 10
    
    # Label para mostrar resultados
    result_label = Label(container, text="", **Style.LABEL_CONFIG)
    result_label.grid(row=3, column=0, columnspan=5, pady=5, sticky="ew")  # Reducido pady de 10 a 5
    
    # Frame para mostrar gráficos
    plot_frame = Frame(container, **Style.FRAME_CONFIG)
    plot_frame.grid(row=4, column=0, columnspan=5, pady=5, sticky="nsew")  # Reducido pady de 10 a 5
    container.grid_rowconfigure(4, weight=1)
    
    root.mainloop()
create_gui()