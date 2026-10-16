import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_loader import load_data
from utils.scoring import compute_scores, compute_team_scores, score_sortie
from utils.style import appliquer_style, afficher_navigation, COULEURS

st.set_page_config(page_title="Classement | Challenge Running", page_icon="🏆", layout="wide")
appliquer_style(); afficher_navigation("Classement")
st.markdown('<div class="page-eyebrow">La compétition</div>',unsafe_allow_html=True)
st.title("🏆 Classement")
st.markdown('<div class="page-subtitle">Suivez les performances individuelles et la bataille entre équipes.</div>',unsafe_allow_html=True)
try:
    df=load_data(st.secrets["sheet_id"],st.secrets.get("sheet_name","Donnees"))
except Exception:
    st.error("Configure Google Sheets dans `.streamlit/secrets.toml`."); st.stop()
if df.empty: st.info("Aucune activité à classer pour le moment."); st.stop()
scores=compute_scores(df); teams=compute_team_scores(scores)
df["Score_sortie"]=df.apply(score_sortie,axis=1)
c1,c2=st.columns([1,1])
with c1: period=st.selectbox("Période",["Tout le challenge","7 derniers jours","14 derniers jours"])
with c2: mode=st.radio("Vue",["Par équipe","Individuel"],horizontal=True)
if period!="Tout le challenge":
    days=7 if period=="7 derniers jours" else 14
    cutoff=df["Date"].max()-pd.Timedelta(days=days-1)
    filtered=df[df["Date"]>=cutoff].copy()
else: filtered=df.copy()
if filtered.empty: st.warning("Aucune sortie pour cette période."); st.stop()
filtered_scores=compute_scores(filtered)
filtered_teams=compute_team_scores(filtered_scores)
total=max(filtered_teams["Score_total"].sum(),1)
if mode=="Par équipe":
    cols=st.columns(max(2,min(2,len(filtered_teams))))
    for i,(_,r) in enumerate(filtered_teams.iterrows()):
        letter=str(r["Equipe"]); css="a" if letter=="A" else "b"
        color=COULEURS["accents"] if letter=="A" else COULEURS["important"]
        part=filtered[filtered["Equipe"]==letter]
        pct=r["Score_total"]/total*100
        with cols[i%len(cols)]:
            st.markdown(f"""<div class="team-card {css}"><div class="team-name">🏆 Équipe {letter}</div>
            <div class="team-score" style="color:{color}">{r['Score_total']:,.0f} pts</div>
            <div class="team-meta">{r['Nb_participants']} participants • {len(part)} sorties • {part['Distance_km'].sum():.1f} km</div>
            <div class="progress-bar"><div class="progress-fill {css}" style="width:{pct:.1f}%"></div></div>
            <div class="team-meta" style="text-align:right;margin-top:5px">{pct:.1f}% des points</div></div>""",unsafe_allow_html=True)
    st.write(""); st.subheader("Comparaison des équipes")
    chart=px.bar(filtered_teams,x="Equipe",y="Score_total",color="Equipe",text_auto=".0f",
                 color_discrete_map={"A":COULEURS["accents"],"B":COULEURS["important"]})
    chart.update_layout(showlegend=False,xaxis_title="Équipe",yaxis_title="Points",height=300,
                        margin=dict(l=0,r=0,t=15,b=0),paper_bgcolor="white",plot_bgcolor="white")
    st.plotly_chart(chart,use_container_width=True)
    st.subheader("Détail par équipe")
    st.dataframe(filtered_teams.rename(columns={"Equipe":"Équipe","Score_total":"Points","Score_moyen":"Points moyens","Nb_participants":"Participants"}).round(1),use_container_width=True,hide_index=True)
else:
    st.subheader("Classement individuel")
    display=filtered_scores.copy()
    display.insert(0,"Rang",range(1,len(display)+1))
    display=display.rename(columns={"Nom":"Participant","Equipe":"Équipe","Score_final":"Points","Nb_sorties":"Sorties","Nb_jours_actifs":"Jours actifs","Score_brut":"Points bruts","Bonus_total":"Bonus"})
    display["Bonus"]=display["Bonus"].map(lambda x:f"+{x:.0%}")
    st.dataframe(display[["Rang","Participant","Équipe","Points","Sorties","Jours actifs","Bonus"]].round(1),use_container_width=True,hide_index=True)
    st.download_button("⬇️ Télécharger le classement CSV",display.to_csv(index=False).encode("utf-8-sig"),"classement_challenge.csv","text/csv")
