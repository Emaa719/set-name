
from fastapi import FastAPI, Response, status, Request
from pydantic import BaseModel
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # List of origins that are allowed to make requests
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*", "x-vapi-secret"],  # Allow all headers including 'x-vapi-secret'
)

@app.options("/{full_path:path}")
async def options_handler(request: Request, full_path: str):
    """
    Handle OPTIONS requests for any path
    """
    response = Response()
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Authorization, Content-Type, x-vapi-secret'
    return response

class NomInput(BaseModel):
    nom: str

def authorize_google_sheets():
    scope = [
        "https://www.googleapis.com/auth/spreadsheets", 
        "https://www.googleapis.com/auth/drive.file", 
        "https://www.googleapis.com/auth/drive"
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)
    return client.open("caller's names").sheet1

def ajouter_nom_to_sheet(nom: str):
    sheet = authorize_google_sheets()
    new_row = [nom]
    sheet.append_row(new_row)

@app.post("/ajouter_nom/")
def ajouter_nom(nom_input: NomInput):
    try:
        ajouter_nom_to_sheet(nom_input.nom)
        return {"message": f"Le nom '{nom_input.nom}' a été ajouté avec succès à notre liste callers."}
    except Exception as e:
        return {"error": f"Une erreur s'est produite lors de l'ajout du nom : {str(e)}"}
