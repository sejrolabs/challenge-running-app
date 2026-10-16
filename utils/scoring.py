import pandas as pd

COEF_TYPE = {"Course": 1.5, "Marche": 1.0}

def coef_allure_course(allure_min_km: float) -> float:
    if allure_min_km < 4: return 1.8
    if allure_min_km < 5: return 1.6
    if allure_min_km < 6: return 1.3
    if allure_min_km < 7: return 1.0
    return 0.8

def coef_allure_marche(allure_min_km: float) -> float:
    if allure_min_km < 12: return 1.2
    if allure_min_km <= 15: return 1.0
    return 0.8

def score_sortie(row: pd.Series) -> float:
    distance = float(row["Distance_km"])
    allure = float(row["Allure_min_km"])
    type_activite = str(row["Type"]).capitalize()
    coef_type = COEF_TYPE.get(type_activite, 1.0)
    coef_allure = coef_allure_course(allure) if type_activite == "Course" else coef_allure_marche(allure)
    return distance * coef_type * coef_allure

def compute_scores(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(columns=["Nom","Equipe","Nb_sorties","Nb_jours_actifs","Score_brut","Bonus_total","Score_final"])
    data = df.copy()
    data["Date"] = pd.to_datetime(data["Date"], errors="coerce")
    data["Score_sortie"] = data.apply(score_sortie, axis=1)
    rows = []
    for (nom, equipe), group in data.groupby(["Nom", "Equipe"], dropna=True):
        days = group["Date"].dt.date.nunique()
        types = set(group["Type"].astype(str).str.capitalize())
        bonus_constance = .10 if days >= 5 else (.05 if days >= 4 else 0)
        bonus_mixte = .05 if {"Course", "Marche"}.issubset(types) else 0
        raw = group["Score_sortie"].sum()
        rows.append({"Nom":nom, "Equipe":equipe, "Nb_sorties":len(group),
                     "Nb_jours_actifs":days, "Score_brut":round(raw,2),
                     "Bonus_total":bonus_constance+bonus_mixte,
                     "Score_final":round(raw*(1+bonus_constance+bonus_mixte),2)})
    return pd.DataFrame(rows).sort_values("Score_final", ascending=False).reset_index(drop=True)

def compute_team_scores(df_scores: pd.DataFrame) -> pd.DataFrame:
    if df_scores.empty:
        return pd.DataFrame(columns=["Equipe","Score_total","Score_moyen","Nb_participants"])
    return (df_scores.groupby("Equipe").agg(Score_total=("Score_final","sum"),
            Score_moyen=("Score_final","mean"), Nb_participants=("Nom","nunique"))
            .reset_index().sort_values("Score_total", ascending=False).reset_index(drop=True))
