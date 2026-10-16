import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_loader import load_data
from utils.scoring import compute_scores, score_sortie
from utils.style import appliquer_style, afficher_navigation, COULEURS

st.set_page_config(page_title="Stats individuelles | Challenge Running",page_icon="📊",layout="wide")
appliquer_style(); afficher_navigation("Stats individuelles")
st.markdown('<div class="page-eyebrow">Votre progression</div>',unsafe_allow_html=True)
st.title("📊 Statistiques individuelles")
st.markdown('<div class="page-subtitle">Un aperçu détaillé des efforts et de la progression de chaque participant.</div>',unsafe_allow_html=True)
try: df=load_data(st.secrets["sheet_id"],st.secrets.get("sheet_name","Donnees"))
except Exception: st.error("Configure Google Sheets dans `.streamlit/secrets.toml`."); st.stop()
if df.empty: st.info("Aucune activité à afficher."); st.stop()
scores=compute_scores(df)
participant=st.selectbox("Choisir un participant",scores["Nom"].tolist())
info=scores[scores["Nom"]==participant].iloc[0]
perso=df[df["Nom"]==participant].copy()
perso["Score_sortie"]=perso.apply(score_sortie,axis=1)
distance=perso["Distance_km"].sum()
minutes=perso["Duree_min"].sum()
allure=minutes/distance if distance else 0
st.markdown(f"""<div class="team-card {'a' if info['Equipe']=='A' else 'b'}">
<div class="team-name">👤 &nbsp; {participant}</div><div class="team-meta">Équipe {info['Equipe']} · {len(perso)} sorties enregistrées</div></div>""",unsafe_allow_html=True)
st.write("")
cols=st.columns(4)
metrics=[("Points",f"{info['Score_final']:,.0f} pts"),("Sorties",f"{len(perso)}"),("Distance",f"{distance:.1f} km"),("Allure moyenne",f"{allure:.2f} min/km")]
for c,(label,val) in zip(cols,metrics): c.metric(label,val)
left,right=st.columns(2)
perso["Date"]=pd.to_datetime(perso["Date"])
perso["Semaine"]=perso["Date"].dt.to_period("W").apply(lambda p:p.start_time)
with left:
    st.markdown('<div class="section-card">',unsafe_allow_html=True)
    st.subheader("📅 Distance par semaine")
    weekly=perso.groupby("Semaine",as_index=False)["Distance_km"].sum()
    fig=px.bar(weekly,x="Semaine",y="Distance_km",text_auto=".1f",color_discrete_sequence=[COULEURS["accents"]])
    fig.update_layout(xaxis_title="",yaxis_title="Distance (km)",height=310,margin=dict(l=0,r=0,t=10,b=0),paper_bgcolor="white",plot_bgcolor="white")
    st.plotly_chart(fig,use_container_width=True)
    st.markdown('</div>',unsafe_allow_html=True)
with right:
    st.markdown('<div class="section-card">',unsafe_allow_html=True)
    st.subheader("🥧 Répartition des activités")
    repartition=perso["Type"].value_counts().reindex(["Course","Marche"],fill_value=0).reset_index()
    repartition.columns=["Type","Sorties"]
    fig=px.pie(repartition,names="Type",values="Sorties",hole=.62,color="Type",
               color_discrete_map={"Course":COULEURS["accents"],"Marche":COULEURS["succes"]})
    fig.update_layout(height=310,margin=dict(l=0,r=0,t=10,b=0),paper_bgcolor="white",showlegend=True)
    st.plotly_chart(fig,use_container_width=True)
    st.markdown('</div>',unsafe_allow_html=True)
st.write(""); st.subheader("🧾 Historique des sorties")
historique=perso.sort_values("Date",ascending=False)[["Date","Type","Distance_km","Duree_min","Allure_min_km","Score_sortie"]].copy()
historique["Date"]=historique["Date"].dt.strftime("%d/%m/%Y")
historique=historique.rename(columns={"Date":"Date","Type":"Activité","Distance_km":"Distance (km)","Duree_min":"Durée (min)","Allure_min_km":"Allure (min/km)","Score_sortie":"Points"})
st.dataframe(historique.round(2),use_container_width=True,hide_index=True)
st.download_button("⬇️ Télécharger mon historique",historique.to_csv(index=False).encode("utf-8-sig"),"historique_running.csv","text/csv")
