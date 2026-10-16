
import streamlit as st
import base64
from pathlib import Path

COULEURS = {
    "principal": "#0F172A",
    "accents": "#2563EB",
    "succes": "#10B981",
    "alerte": "#F59E0B",
    "important": "#EF4444",
    "fond": "#F1F5F9",
    "texte_secondaire": "#64748B",
    "bordure": "#DCE5F1",
}


def appliquer_style():
    """Applique le style général et l'image de fond de la barre latérale."""

    # Image placée à la racine du projet, à côté de app.py.
    image_path = Path(__file__).resolve().parent.parent / "sidebar-running.png"

    image_base64 = ""
    if image_path.exists():
        image_base64 = base64.b64encode(
            image_path.read_bytes()
        ).decode("utf-8")
    else:
        st.warning(
            "Image de fond introuvable. Vérifie que "
            "sidebar-running.png se trouve à la racine du projet."
        )

    # Dégradé + photo. En l'absence de photo, le fond reste bleu marine.
    if image_base64:
        sidebar_background = f"""
            background-image:
                linear-gradient(
                    180deg,
                    rgba(15, 23, 42, 0.98) 0%,
                    rgba(15, 42, 70, 0.94) 48%,
                    rgba(15, 42, 70, 0.45) 100%
                ),
                url("data:image/png;base64,{image_base64}");
        """
    else:
        sidebar_background = """
            background-image:
                linear-gradient(
                    180deg,
                    #0F172A 0%,
                    #102A46 100%
                );
        """

    css = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    :root {{
        --navy: #0F172A;
        --blue: #2563EB;
        --green: #10B981;
        --orange: #F59E0B;
        --red: #EF4444;
        --bg: #F1F5F9;
    }}

    /* ==============================
       STYLE GENERAL
    ============================== */

    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif;
    }}

    .stApp {{
        background: var(--bg);
        color: var(--navy);
    }}

    [data-testid="stHeader"] {{
        background: rgba(241, 245, 249, 0.92);
    }}

    .block-container {{
        padding-top: 1.7rem;
        padding-bottom: 2rem;
        max-width: 1450px;
    }}

    h1, h2, h3 {{
        color: var(--navy);
        letter-spacing: -0.025em;
    }}

    h1 {{
        font-size: 2rem !important;
        font-weight: 800 !important;
    }}

    h2 {{
        font-size: 1.35rem !important;
        font-weight: 750 !important;
    }}

    h3 {{
        font-size: 1.05rem !important;
        font-weight: 700 !important;
    }}

    p, label {{
        color: var(--navy);
    }}

    /* ==============================
       BARRE LATERALE
    ============================== */

    /* Masquer la navigation automatique de Streamlit.
       La navigation personnalisée reste active. */
    [data-testid="stSidebarNav"] {{
        display: none !important;
    }}

    [data-testid="stSidebar"] {{
        background-color: #0F172A;
        {sidebar_background}
        background-repeat: no-repeat, no-repeat;

        /* Photo ancrée en bas, avec le sujet vers la gauche */
        background-position: center, left bottom;

        /* Le dégradé remplit la barre ; la photo occupe sa hauteur */
        background-size: cover, auto 100%;

        border-right: 1px solid #1E3554;
    }}

    /* Couleurs du texte dans la barre latérale */
    [data-testid="stSidebar"] {{
        color: #F8FAFC;
    }}

    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {{
        color: #F8FAFC;
        font-size: 0.94rem;
    }}

    [data-testid="stSidebar"] [data-testid="stCaptionContainer"] {{
        color: #CBD5E1 !important;
        opacity: 1 !important;
    }}

    [data-testid="stSidebar"] a {{
        color: #F8FAFC !important;
    }}

    .brand-block {{
        padding: 0.5rem 0.2rem 1rem;
    }}

    .brand-block .brand-title {{
        font-size: 1.12rem;
        font-weight: 800;
        color: #FFFFFF;
        line-height: 1.2;
    }}

    .brand-block .brand-sub {{
        font-size: 0.78rem;
        color: #CBD5E1;
        margin-top: 0.3rem;
    }}

    /* ==============================
       TITRES DE PAGE
    ============================== */

    .page-eyebrow {{
        color: var(--blue);
        font-weight: 700;
        font-size: 0.78rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }}

    .page-subtitle {{
        color: #64748B;
        margin-top: -0.65rem;
        margin-bottom: 1.2rem;
    }}

    /* ==============================
       CARTES KPI
    ============================== */

    .kpi-card {{
        background: #FFFFFF;
        border: 1px solid #E2EAF4;
        border-radius: 16px;
        padding: 16px 17px;
        box-shadow: 0 4px 14px rgba(15, 23, 42, 0.045);
        min-height: 104px;
        display: flex;
        align-items: center;
        gap: 12px;
    }}

    .kpi-icon {{
        width: 42px;
        height: 42px;
        border-radius: 13px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 21px;
        background: #DBEAFE;
        flex-shrink: 0;
    }}

    .kpi-value {{
        color: var(--navy);
        font-size: 1.45rem;
        font-weight: 800;
        line-height: 1.25;
    }}

    .kpi-label {{
        color: #64748B;
        font-size: 0.78rem;
        font-weight: 500;
        margin-top: 3px;
    }}

    /* ==============================
       CARTES EQUIPES
    ============================== */

    .team-card {{
        border-radius: 16px;
        padding: 18px 20px;
        background: #FFFFFF;
        border: 1px solid #DCE5F1;
        box-shadow: 0 4px 14px rgba(15, 23, 42, 0.04);
    }}

    .team-card.a {{
        background: linear-gradient(115deg, #EFF6FF, #DBEAFE);
        border-color: #BFDBFE;
    }}

    .team-card.b {{
        background: linear-gradient(115deg, #FFF1F2, #FFE4E6);
        border-color: #FECDD3;
    }}

    .team-name {{
        font-weight: 750;
        font-size: 1rem;
    }}

    .team-score {{
        font-size: 1.9rem;
        font-weight: 800;
        line-height: 1.3;
        margin: 0.25rem 0;
    }}

    .team-meta {{
        color: #475569;
        font-size: 0.8rem;
    }}

    .progress-bar {{
        height: 9px;
        background: #D7E2EF;
        border-radius: 99px;
        overflow: hidden;
        margin-top: 12px;
    }}

    .progress-fill {{
        height: 100%;
        border-radius: 99px;
    }}

    .progress-fill.a {{
        background: var(--blue);
    }}

    .progress-fill.b {{
        background: var(--red);
    }}

    /* ==============================
       CARTES DE CONTENU
    ============================== */

    .section-card {{
        background: #FFFFFF;
        border: 1px solid #E2EAF4;
        border-radius: 16px;
        padding: 16px 18px;
        box-shadow: 0 4px 14px rgba(15, 23, 42, 0.035);
    }}

    /* ==============================
       METRIQUES STREAMLIT
    ============================== */

    [data-testid="stMetric"] {{
        background: #FFFFFF;
        border: 1px solid #E2EAF4;
        border-radius: 14px;
        padding: 13px 15px;
    }}

    [data-testid="stMetricLabel"] {{
        color: #64748B;
    }}

    [data-testid="stMetricValue"] {{
        color: var(--navy);
        font-weight: 800;
    }}

    /* ==============================
       ONGLETS
    ============================== */

    div[data-testid="stTabs"] button[role="tab"] {{
        border-radius: 10px 10px 0 0;
        font-weight: 650;
    }}

    div[data-testid="stTabs"] button[aria-selected="true"] {{
        color: var(--blue);
    }}

    /* ==============================
       BOUTONS
    ============================== */

    .stButton > button,
    .stDownloadButton > button {{
        border-radius: 10px;
        border: 0;
        font-weight: 700;
        padding: 0.55rem 1rem;
    }}

    .stButton > button[kind="primary"] {{
        background: var(--blue);
        color: #FFFFFF;
    }}

    .stButton > button:hover {{
        border-color: var(--blue);
        color: var(--blue);
    }}

    /* ==============================
       TABLEAUX
    ============================== */

    [data-testid="stDataFrame"] {{
        border: 1px solid #E2EAF4;
        border-radius: 12px;
        overflow: hidden;
    }}

    hr {{
        border-color: #DCE5F1;
    }}

    /* ==============================
       RESPONSIVE
    ============================== */

    @media (max-width: 760px) {{
        .block-container {{
            padding: 1rem 0.8rem;
        }}

        h1 {{
            font-size: 1.55rem !important;
        }}

        .kpi-value {{
            font-size: 1.15rem;
        }}
    }}
    </style>
    """

    st.markdown(css, unsafe_allow_html=True)


def afficher_navigation(active="App"):
    """
    Affiche la navigation personnalisée dans la barre latérale.
    La navigation automatique de Streamlit est masquée par le CSS.
    """

    with st.sidebar:
        st.markdown(
            """
            <div class="brand-block">
                <div style="font-size: 2rem;">🏃🏻‍♂️</div>
                <div class="brand-title">
                    Challenge<br>Running
                </div>
                <div class="brand-sub">
                    Bouger ensemble, progresser ensemble
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("---")

        pages = [
            ("🏠", "App", "app.py"),
            ("🏆", "Classement", "pages/1_Classement.py"),
            (
                "📊",
                "Stats individuelles",
                "pages/2_Stats_Individuelles.py",
            ),
            (
                "⚙️",
                "Configuration",
                "pages/3_Configuration.py",
            ),
        ]

        for emoji, label, path in pages:
            if label == active:
                st.markdown(
                    f"""
                    <div style="
                        background: #2563EB;
                        padding: 10px 12px;
                        border-radius: 9px;
                        font-weight: 700;
                        margin: 4px 0;
                    ">
                        {emoji} &nbsp; {label}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                st.page_link(
                    path,
                    label=f"{emoji}  {label}",
                )

        st.markdown("---")
        st.caption("Challenge • Saison automne 2026")
