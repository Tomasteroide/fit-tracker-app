# Funciones para conectarse a Google Sheets
import gspread
import pandas as pd
from gspread_dataframe import get_as_dataframe, set_with_dataframe
from oauth2client.service_account import ServiceAccountCredentials

def get_worksheet(sheet_name="Progreso Tracker", worksheet_name="Entrenamientos"):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open(sheet_name).worksheet(worksheet_name)
    return sheet

def leer_datos(sheet):
    df = get_as_dataframe(sheet, evaluate_formulas=True).dropna(how='all')
    return df

def guardar_datos(sheet, df):
    sheet.clear()
    set_with_dataframe(sheet, df)
