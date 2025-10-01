import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ===============================
# Registrace fontu DejaVu Sans
# ===============================
pdfmetrics.registerFont(TTFont('DejaVu', 'DejaVuSans.ttf'))

# ===============================
# TITULEK A POPIS
# ===============================
st.title("Body na kružnici")
st.write("Zadej parametry a vykresli body na kružnici.")

# ===============================
# VSTUPNÍ PARAMETRY
# ===============================
st.sidebar.header("Nastavení parametrů")

# Souřadnice středu
x_center = st.sidebar.number_input("Souřadnice středu X", value=0.0, step=1.0)
y_center = st.sidebar.number_input("Souřadnice středu Y", value=0.0, step=1.0)

# Poloměr – číselný vstup
radius = st.sidebar.number_input("Poloměr kružnice", min_value=1.0, max_value=1000.0, value=5.0, step=1.0)

# Počet bodů
num_points = st.sidebar.number_input("Počet bodů na kružnici", min_value=3, max_value=200, value=10, step=1)

# Barva bodů
color = st.sidebar.color_picker("Vyber barvu bodů", "#ff0000")

# Jednotka na osách
unit = st.sidebar.text_input("Jednotka os", "m")

# ===============================
# VÝPOČET SOUŘADNIC BODŮ
# ===============================
angles = np.linspace(0, 2*np.pi, num_points, endpoint=False)
x_points = x_center + radius * np.cos(angles)
y_points = y_center + radius * np.sin(angles)

# ===============================
# VYKRESLENÍ GRAFU
# ===============================
fig, ax = plt.subplots()
ax.scatter(x_points, y_points, c=color, label="Body")
ax.add_patch(plt.Circle((x_center, y_center), radius, fill=False, linestyle="--", color="gray", label="Kružnice"))
ax.set_aspect("equal", "box")
ax.set_xlabel(f"X [{unit}]")
ax.set_ylabel(f"Y [{unit}]")
ax.grid(True)
ax.legend()

st.subheader("Bodový graf")
st.pyplot(fig)

# ===============================
# TABULKA SOUŘADNIC (číslování 1-n)
# ===============================
st.subheader("Souřadnice bodů")
data = {
    "Bod": list(range(1, num_points + 1)),  # čísla od 1
    "X": np.round(x_points, 2),
    "Y": np.round(y_points, 2)
}
st.table(data)

# ===============================
# GENEROVÁNÍ PDF
# ===============================
def create_pdf():
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Použití DejaVu Sans pro češtinu
    c.setFont("DejaVu", 14)
    c.drawString(50, height - 50, "Výsledky - Body na kružnici")

    c.setFont("DejaVu", 12)
    c.drawString(50, height - 100, f"Střed kružnice: ({x_center}, {y_center})")
    c.drawString(50, height - 120, f"Poloměr: {radius} {unit}")
    c.drawString(50, height - 140, f"Počet bodů: {num_points}")
    c.drawString(50, height - 160, f"Barva bodů: {color}")
    c.drawString(50, height - 180, "Autor: Jakub Jungman")
    c.drawString(50, height - 200, "Kontakt: 277941@vutbr.cz")

    c.drawString(50, height - 240, "Souřadnice bodů:")
    y_pos = height - 260
    for i in range(num_points):
        c.drawString(60, y_pos, f"Bod {i+1}: X={round(x_points[i],2)}, Y={round(y_points[i],2)}")
        y_pos -= 20
        if y_pos < 50:  # nová strana
            c.showPage()
            c.setFont("DejaVu", 12)
            y_pos = height - 50

    c.save()
    buffer.seek(0)
    return buffer

if st.button("Stáhnout výsledky do PDF"):
    pdf = create_pdf()
    st.download_button("📥 Stáhnout PDF", data=pdf, file_name="body_na_kruznici.pdf", mime="application/pdf")

# ===============================
# INFO O TECHNOLOGIÍCH
# ===============================
with st.expander("ℹ️ Použité technologie"):
    st.write("""
    - **Python**
    - **Streamlit** (web aplikace)
    - **NumPy** (výpočty)
    - **Matplotlib** (vykreslení grafu)
    - **ReportLab** (generování PDF)
    """)

# ===============================
# INFORMACE O AUTOROVI
# ===============================
st.subheader("Informace o autorovi")
st.write("**Jméno:** Jan Novotný") 
st.write("**Kontakt:** 278193@vutbr.cz")
