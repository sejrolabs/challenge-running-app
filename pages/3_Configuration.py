import streamlit as st
import pandas as pd
from utils.style import appliquer_style, afficher_navigation, COULEURS

st.set_page_config(page_title="Configuration | Challenge Running",page_icon="⚙️",layout="wide")
appliquer_style(); afficher_navigation("Configuration")
st.markdown('<div class="page-eyebrow">Paramètres du challenge</div>',unsafe_allow_html=True)
st.title("⚙️ Configuration")
st.markdown('<div class="page-subtitle">Consultez les règles, les participants et les paramètres de la saison.</div>',unsafe_allow_html=True)
rules,participants,challenge=st.tabs(["📐 Règles","👥 Participants","🗓️ Challenge"])
with rules:
    st.subheader("Coefficients et bonus")
    data=[
        ["Coef_Course","2,0","Coefficient de base pour la course"],
        ["Coef_Marche","1,0","Coefficient de base pour la marche"],
        ["Bonus_Constance_5j","10 %","Au moins 5 jours actifs sur une semaine"],
        ["Bonus_Constance_4j","5 %","4 jours actifs sur une semaine"],
        ["Bonus_Equipe","5 %","Bonus collectif si l’objectif est atteint"],
        ["Bonus_Mixte","5 %","Course et marche sur la période"],
    ]
    st.dataframe(pd.DataFrame(data,columns=["Paramètre","Valeur","Description"]),use_container_width=True,hide_index=True)
    st.info("Les règles affichées servent de référence. Leur modification n’est pas encore reliée au moteur de calcul.")
    with st.expander("Barème d’allure"):
        st.markdown("**Course :** moins de 4 min/km → ×1,8 · 4–5 → ×1,6 · 5–6 → ×1,3 · 6–7 → ×1,0 · 7 et plus → ×0,8")
        st.markdown("**Marche :** moins de 12 min/km → ×1,2 · 12–15 → ×1,0 · plus de 15 → ×0,8")
with participants:
    st.subheader("Gestion des participants")
    st.info("Les participants sont actuellement récupérés depuis l’onglet Google Sheets configuré. Pour éviter toute modification non persistante, cette version propose un export plutôt qu’un faux bouton d’enregistrement.")
    try:
        sid=st.secrets["sheet_id"]; sheet=st.secrets.get("sheet_name","Donnees")
        from utils.data_loader import load_data
        df=load_data(sid,sheet)
        people=df[["Nom","Equipe"]].drop_duplicates().sort_values(["Equipe","Nom"])
        st.dataframe(people.rename(columns={"Nom":"Participant","Equipe":"Équipe"}),use_container_width=True,hide_index=True)
        st.download_button("⬇️ Exporter les participants CSV",people.to_csv(index=False).encode("utf-8-sig"),"participants.csv","text/csv")
    except Exception:
        st.warning("Renseigne d’abord la connexion Google Sheets dans `.streamlit/secrets.toml`.")
with challenge:
    st.subheader("Période du challenge")
    col1,col2=st.columns(2)
    with col1: debut=st.date_input("Date de début",value=pd.Timestamp("2026-09-28").date())
    with col2: fin=st.date_input("Date de fin",value=pd.Timestamp("2026-10-18").date())
    objectif=st.number_input("Objectif d’équipe (km, optionnel)",min_value=0,value=100,step=10)
    if fin<debut: st.error("La date de fin doit être postérieure à la date de début.")
    st.caption("Ces paramètres sont affichés localement et ne sont pas encore enregistrés dans Google Sheets.")
    if st.button("💾 Prévisualiser les paramètres",type="primary"):
        st.success(f"Période : {debut:%d/%m/%Y} – {fin:%d/%m/%Y} · Objectif : {objectif} km")
