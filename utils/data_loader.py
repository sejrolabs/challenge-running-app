import pandas as pd
import streamlit as st

@st.cache_data(ttl=300)
def load_data(sheet_id: str, sheet_name: str = "Donnees") -> pd.DataFrame:
    """Charge un onglet Google Sheets public et normalise les colonnes."""
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
    try:
        df = pd.read_csv(url)
    except Exception as exc:
        st.error("Impossible de charger les données Google Sheets. Vérifie le partage du fichier et les paramètres dans .streamlit/secrets.toml.")
        st.exception(exc)
        st.stop()
    df.columns = [str(c).strip() for c in df.columns]
    required = ["Date", "Nom", "Equipe", "Type", "Distance_km", "Duree_min", "Allure_min_km"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        st.error(f"Colonnes manquantes dans l'onglet « {sheet_name} » : {', '.join(missing)}")
        st.stop()
    for col in ["Distance_km", "Duree_min", "Allure_min_km"]:
        df[col] = pd.to_numeric(df[col].astype(str).str.replace(",", ".", regex=False).str.strip(), errors="coerce")
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce", dayfirst=True)
    df["Nom"] = df["Nom"].astype(str).str.strip()
    df["Equipe"] = df["Equipe"].astype(str).str.strip().str.upper()
    df["Type"] = df["Type"].astype(str).str.strip().str.capitalize()
    df = df.dropna(subset=["Date", "Distance_km", "Duree_min", "Allure_min_km"])
    df = df[(df["Distance_km"] > 0) & (df["Duree_min"] > 0) & (df["Allure_min_km"] > 0)]
    return df.reset_index(drop=True)
