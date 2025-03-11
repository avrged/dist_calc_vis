import subprocess
import os

def generate_formula_image(formula_type, **kwargs):
    # Crear el contenido del archivo LaTeX
    latex_content = r"""
\documentclass{standalone}
\usepackage{amsmath}
\usepackage{xcolor}
\begin{document}
"""
    
    if formula_type == "BINOMIAL":
        n = kwargs.get('n')
        x = kwargs.get('x')
        p = kwargs.get('p')
        latex_content += fr"$P(X = {x}) = \binom{{{n}}}{{{x}}} ({p})^{{{x}}} (1-{p})^{{{n}-{x}}}$"
    
    elif formula_type == "HIPERGEOMETRICA":
        N = kwargs.get('N')
        K = kwargs.get('K')
        n = kwargs.get('n')
        k = kwargs.get('k')
        latex_content += fr"$P(X = {k}) = \frac{{\binom{{{K}}}{{{k}}} \binom{{{N-K}}}{{{n-k}}}}}{{\binom{{{N}}}{{{n}}}}}$"
    
    elif formula_type == "BERNOULLI":
        p = kwargs.get('p')
        x = kwargs.get('x')
        latex_content += fr"$P(X = {x}) = {p}^{{{x}}} (1-{p})^{{1-{x}}}$"
    
    elif formula_type == "GEOMETRICA":
        p = kwargs.get('p')
        x = kwargs.get('x')
        latex_content += fr"$P(X = {x}) = (1-{p})^{{{x}-1}} {p}$"
    
    elif formula_type == "POISSON":
        lam = kwargs.get('lam')
        k = kwargs.get('k')
        latex_content += fr"$P(X = {k}) = \frac{{{lam}^{k} e^{{-{lam}}}}}{{{k}!}}$"
    
    latex_content += "\n\\end{document}"
    
    # Guardar el contenido en un archivo temporal
    temp_file = f"temp_{formula_type}.tex"
    with open(temp_file, "w") as f:
        f.write(latex_content)
    
    # Compilar el archivo LaTeX
    subprocess.run(["pdflatex", temp_file])
    
    # Convertir PDF a PNG
    pdf_file = f"temp_{formula_type}.pdf"
    png_file = f"{formula_type.lower()}_formula.png"
    subprocess.run(["magick", "convert", "-density", "300", pdf_file, "-quality", "90", png_file])
    
    # Limpiar archivos temporales
    for ext in ['.tex', '.pdf', '.aux', '.log']:
        try:
            os.remove(f"temp_{formula_type}{ext}")
        except:
            pass
    
    return png_file
