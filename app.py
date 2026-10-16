import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.data_loader import load_data
from utils.scoring import compute_scores, compute_team_scores, score_sortie
from utils.style import appliquer_style, afficher_navigation, COULEURS

st.set_page_config(page_title="Challenge Running", page_icon="🏃", layout="wide")
appliquer_style()
afficher_navigation("App")

st.markdown('<div class="page-eyebrow">Tableau de bord</div>', unsafe_allow_html=True)
st.title("🏃 Challenge Running")
st.markdown('<div class="page-subtitle">Vue d’ensemble du challenge, des équipes et de votre progression.</div>', unsafe_allow_html=True)

try:
    sheet_id = st.secrets["sheet_id"]
    sheet_name = st.secrets.get("sheet_name", "Donnees")
except Exception:
    st.error("La configuration Google Sheets est absente. Crée le fichier `.streamlit/secrets.toml` et renseigne `sheet_id` et `sheet_name` (voir README.md).")
    st.stop()

df = load_data(sheet_id, sheet_name)
if df.empty:
    st.warning("Aucune activité valide n’est disponible pour le moment.")
    st.stop()
scores = compute_scores(df)
teams = compute_team_scores(scores)
df["Score_sortie"] = df.apply(score_sortie, axis=1)

c1,c2,c3,c4 = st.columns(4)
metrics = [
    ("🏃","Sorties",f"{len(df):,}".replace(","," ")),
    ("📍","Distance totale",f"{df['Distance_km'].sum():,.1f} km".replace(","," ")),
    ("⏱️","Temps total",f"{int(df['Duree_min'].sum())//60}h {int(df['Duree_min'].sum())%60:02d}"),
    ("👥","Participants",str(scores["Nom"].nunique())),
]
for col,(icon,label,value) in zip([c1,c2,c3,c4],metrics):
    col.markdown(f'<div class="kpi-card"><div class="kpi-icon">{icon}</div><div><div class="kpi-value">{value}</div><div class="kpi-label">{label}</div></div></div>',unsafe_allow_html=True)

st.write("")
st.subheader("La compétition entre équipes")
team_cols = st.columns(max(2, min(len(teams), 2)))
total_score = max(float(teams["Score_total"].sum()), 1)
for i,(_,team) in enumerate(teams.iterrows()):
    letter = str(team["Equipe"])
    css = "a" if letter == "A" else "b"
    color = COULEURS["accents"] if letter == "A" else COULEURS["important"]
    pct = float(team["Score_total"])/total_score*100
    n_part = int(team["Nb_participants"])
    distance = df.loc[df["Equipe"] == letter, "Distance_km"].sum()
    outings = int((df["Equipe"] == letter).sum())
    with team_cols[i % len(team_cols)]:
        st.markdown(f"""<div class="team-card {css}">
        <div class="team-name">🏆 Équipe {letter}</div>
        <div class="team-score" style="color:{color}">{team['Score_total']:,.0f} pts</div>
        <div class="team-meta">{n_part} participants &nbsp;•&nbsp; {outings} sorties &nbsp;•&nbsp; {distance:.1f} km</div>
        <div class="progress-bar"><div class="progress-fill {css}" style="width:{pct:.1f}%"></div></div>
        <div class="team-meta" style="text-align:right;margin-top:5px">{pct:.1f}% des points</div></div>""",unsafe_allow_html=True)

st.write("")
left,right = st.columns([1.55,1])
with left:
    st.markdown('<div class="section-card">',unsafe_allow_html=True)
    st.subheader("📈 Évolution des scores cumulés")
    evolution = df.copy()
    evolution["Date"] = pd.to_datetime(evolution["Date"]).dt.normalize()
    daily = evolution.groupby(["Date","Equipe"],as_index=False)["Score_sortie"].sum()
    dates = pd.date_range(daily["Date"].min(),daily["Date"].max(),freq="D")
    all_teams = sorted(daily["Equipe"].dropna().unique())
    full = pd.MultiIndex.from_product([dates,all_teams],names=["Date","Equipe"]).to_frame(index=False)
    daily = full.merge(daily,on=["Date","Equipe"],how="left").fillna({"Score_sortie":0})
    daily["Score cumulé"] = daily.groupby("Equipe")["Score_sortie"].cumsum()
    fig = px.line(daily,x="Date",y="Score cumulé",color="Equipe",markers=True,
                  color_discrete_map={"A":COULEURS["accents"],"B":COULEURS["important"]})
    fig.update_layout(margin=dict(l=0,r=0,t=8,b=0),height=300,legend_title_text="",paper_bgcolor="white",
                      plot_bgcolor="white",font=dict(color=COULEURS["principal"]),yaxis_title="Points",xaxis_title="")
    fig.update_xaxes(showgrid=False); fig.update_yaxes(gridcolor="#E8EEF6")
    st.plotly_chart(fig,use_container_width=True)
    st.markdown('</div>',unsafe_allow_html=True)
with right:
    st.markdown('<div class="section-card">',unsafe_allow_html=True)
    st.subheader("🥧 Répartition des activités")
    counts = df["Type"].value_counts().reindex(["Course","Marche"],fill_value=0).reset_index()
    counts.columns = ["Type","Sorties"]
    fig = px.pie(counts,names="Type",values="Sorties",hole=.66,
                 color="Type",color_discrete_map={"Course":COULEURS["accents"],"Marche":COULEURS["succes"]})
    fig.update_traces(textposition="outside",textinfo="percent+label",hole=.66)
    fig.update_layout(showlegend=False,margin=dict(l=5,r=5,t=8,b=8),height=300,paper_bgcolor="white")
    st.plotly_chart(fig,use_container_width=True)
    st.caption(f"{len(df)} sorties enregistrées • {int((df['Type']=='Course').sum())} courses • {int((df['Type']=='Marche').sum())} marches")
    st.markdown('</div>',unsafe_allow_html=True)

st.write("")
st.subheader("⭐ Les participants en tête")
top = scores[["Nom","Equipe","Score_final","Nb_sorties","Nb_jours_actifs"]].head(5).copy()
top.insert(0,"Rang",range(1,len(top)+1))
top.columns = ["Rang","Participant","Équipe","Points","Sorties","Jours actifs"]
st.dataframe(top,use_container_width=True,hide_index=True)
