# Challenge Running — interface modernisée

Application Streamlit de suivi d'un challenge course/marche. La structure initiale est conservée :
- `app.py` : tableau de bord
- `pages/1_Classement.py` : classement par équipe ou individuel
- `pages/2_Stats_Individuelles.py` : profil et historique
- `pages/3_Configuration.py` : règles, participants et paramètres
- `utils/data_loader.py` : chargement Google Sheets
- `utils/scoring.py` : calcul des points
- `utils/style.py` : thème et navigation

## Installation (Windows)

Dans le dossier du projet :

```bat
py -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Connexion à Google Sheets

1. Crée le fichier `.streamlit/secrets.toml` en copiant `.streamlit/secrets.example.toml`.
2. Renseigne l'identifiant de ton Google Sheet et le nom exact de l'onglet qui contient les sorties.
3. Le fichier Google Sheets doit être accessible en lecture à l'application (par exemple publié en CSV ou partagé en lecture selon la configuration utilisée).

Exemple :

```toml
sheet_id = "ID_DE_VOTRE_GOOGLE_SHEET"
sheet_name = "Donnees"
```

L'identifiant est la partie entre `/d/` et `/edit` dans l'URL Google Sheets. Ne partage jamais `secrets.toml` publiquement.

## Lancer l'application

```bat
python -m streamlit run app.py
```

## Notes

- Le design a été modernisé avec une palette bleu marine/bleu/vert/orange/rouge et des cartes, graphiques Plotly et navigation cohérente.
- Les calculs de points existants sont conservés dans leur logique principale. Le bonus d'équipe affiché dans la maquette reste à connecter à une définition d'objectif métier précise.
- La configuration permet de consulter les règles et de prévisualiser les paramètres, mais ne prétend pas sauvegarder des modifications dans Google Sheets sans mécanisme d'écriture.
