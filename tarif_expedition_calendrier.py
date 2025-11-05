import streamlit as st
import pandas as pd

# --- Configuration de la page ---
st.set_page_config(page_title="Tarification d’expédition - SPCA", page_icon="📦")

# --- Style personnalisé SPCA ---
st.markdown("""
    <style>
        body {background-color: #fafafa;}
        .main-title {
            color: #ae0f27;
            font-size: 30px;
            font-weight: 700;
            text-align: center;
        }
        .subtext {
            color: #444;
            font-size: 16px;
            text-align: center;
            margin-bottom: 25px;
        }
        .result-box {
            background-color: #ffffff;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            margin-top: 15px;
        }
        table {
            border-collapse: collapse;
            width: 100%;
            margin-top: 10px;
            border-radius: 10px;
            overflow: hidden;
        }
        th {
            background-color: #f7dcdc; /* rouge clair SPCA */
            color: #6a0c15;           /* rouge plus doux */
            font-weight: 600;
            padding: 10px;
            text-align: center;
        }
        td {
            background-color: #fff;
            color: #333;
            padding: 8px;
            text-align: center;
            border-bottom: 1px solid #eee;
        }
        tbody tr:nth-child(even) td {
            background-color: #f9f9f9;
        }
        thead th:first-child, tbody td:first-child {
            background-color: #fdeaea; /* teinte rose claire pour la colonne index */
            font-weight: 600;
        }
    </style>
""", unsafe_allow_html=True)

# --- En-tête ---
st.markdown('<h1 class="main-title">📦 Tarification d’expédition – SPCA Montréal</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtext">Entrez la quantité de calendriers pour obtenir le coût total d’expédition (Postes Canada + manutention Kopel).</p>', unsafe_allow_html=True)

# --- Données officielles ---
manutention = 1.68  # coût fixe Kopel ($)
tarifs_postaux = {
    1: {"poids": 98, "poste": 2.61},
    2: {"poids": 176, "poste": 4.29},
    3: {"poids": 254, "poste": 5.98},
    4: {"poids": 332, "poste": 6.85},
    5: {"poids": 410, "poste": 7.36},
}

# --- Tableau récapitulatif ---
data = []
for qte, info in tarifs_postaux.items():
    total = info["poste"] + manutention
    data.append({
        "Quantité": qte,
        "Poids (g)": info["poids"],
        "Frais postaux ($)": f"{info['poste']:.2f}",
        "Manutention ($)": f"{manutention:.2f}",
        "Total ($)": f"{total:.2f}"
    })
df = pd.DataFrame(data)

st.subheader("📋 Grille tarifaire officielle (Postes Canada + Kopel)")
st.table(df)

# --- Fonction de calcul ---
def calculer_frais(qte):
    if qte in tarifs_postaux:
        poids = tarifs_postaux[qte]["poids"]
        frais_poste = tarifs_postaux[qte]["poste"]
        total = frais_poste + manutention
        return poids, frais_poste, manutention, total, False
    elif qte > 5:
        # Estimation linéaire pour 6+ (sans modifier la grille officielle)
        poids = 98 * qte
        frais_poste = 1.67 + 1.13 * qte
        total = frais_poste + manutention
        return round(poids), round(frais_poste, 2), manutention, round(total, 2), True
    else:
        return 0, 0, 0, 0, False

# --- Interface utilisateur ---
st.markdown("---")
qte = st.number_input("Nombre de calendriers :", min_value=1, step=1)

poids, frais_poste, frais_manut, total, estimer = calculer_frais(qte)

# --- Affichage des résultats ---
st.markdown('<div class="result-box">', unsafe_allow_html=True)
if not estimer:
    st.subheader(f"Résultat pour {qte} calendrier(s)")
else:
    st.subheader(f"Estimation pour {qte} calendriers (au-delà de 5)")

if qte <= 5:
    st.write(f"⚖️ **Poids total :** {poids} g")
else:
    st.write(f"⚖️ **Poids estimé :** ~{poids} g")

st.write(f"📮 **Frais postaux :** {frais_poste:.2f} $")
st.write(f"🏗️ **Manutention Kopel :** {frais_manut:.2f} $")
st.success(f"💰 **Total d’expédition : {total:.2f} $**")

if estimer:
    st.warning("⚠️ Montant estimé pour plus de 5 calendriers (à valider avec Kopel).")

st.markdown('</div>', unsafe_allow_html=True)

# --- Pied de page ---
st.caption("SPCA Montréal • Outil interne d’estimation des coûts d’expédition © 2025")

