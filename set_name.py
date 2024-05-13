'''import gspread
from oauth2client.service_account import ServiceAccountCredentials

def ajouter_nom_to_sheet(nom):
    # Configuration de l'authentification avec la clé API
    scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]    
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    
    # Autorisation du client avec les identifiants
    client = gspread.authorize(creds)
    
    # Sélection de la feuille à modifier
    sheet = client.open("caller's names").sheet1  # Utilisez sheet2, sheet3, etc. pour une autre feuille
    
    # Insérer le nom dans la feuille de calcul
    new_row = [nom]  # Créez une liste avec le nom à ajouter
    sheet.append_row(new_row)  # Ajoutez cette liste en tant que nouvelle ligne à la fin de la feuille

# Utilisation de la fonction pour ajouter un nom spécifiqu
nom_a_ajouter = "Ema ema"
ajouter_nom_to_sheet(nom_a_ajouter)

print("Le nom a été ajouté avec succès à la feuille.")'''


from fastapi import FastAPI
from pydantic import BaseModel
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = FastAPI()

# Modèle Pydantic pour représenter les données attendues dans le corps de la requête
class NomInput(BaseModel):
    nom: str

# Configuration de l'authentification avec la clé API Google Sheets
def authorize_google_sheets():
    scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)
    return client.open("caller's names").sheet1

# Fonction pour ajouter un nom à la feuille de calcul Google Sheets
def ajouter_nom_to_sheet(nom: str):
    sheet = authorize_google_sheets()
    new_row = [nom]
    sheet.append_row(new_row)

# Endpoint FastAPI pour ajouter un nom à la feuille de calcul
@app.post("/ajouter_nom/")
def ajouter_nom(nom_input: NomInput):
    try:
        ajouter_nom_to_sheet(nom_input.nom)
        return {"message": f"Le nom '{nom_input.nom}' a été ajouté avec succès à notre liste callers."}
    except Exception as e:
        return {"error": f"Une erreur s'est produite lors de l'ajout du nom : {str(e)}"}
