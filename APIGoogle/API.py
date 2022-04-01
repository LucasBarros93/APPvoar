from googleapiclient.discovery import build
from google.oauth2 import service_account
from datetime import date

def GetSheet():
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    SERVICE_ACCOUNT_FILE = 'C:/Users/lucas/Desktop/PythonApp/Voar/APIGoogle/keys.json'
    
    #creds = None
    creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    
    
    spreadsheetId = '12Z6D5AXPM0cPJo9TBYFp5aaNkr90xPmdJUYzel46cLA'
    
    service = build('sheets', 'v4', credentials=creds)
    
    # Call the Sheets API
    sheet = service.spreadsheets()
    
    return sheet, spreadsheetId


def GetActives():
    sheet, spreadsheetId = GetSheet()
    result = sheet.values().get(spreadsheetId=spreadsheetId,
                                range="ativos!1:1000",
                                majorDimension="ROWS").execute()
    
    values = result.get('values', [])
    
    actives = []
    for i in values:
        if i[0] == "FALSE":
            actives.append(i)
    
    return actives


def SetNew(tipo, sequencia, frase1, frase2,frase3):
    sheet, spreadsheetId = GetSheet()
    result = sheet.values().get(spreadsheetId=spreadsheetId,
                                range="ativos!1:1000",
                                majorDimension="ROWS").execute()
    
    values = result.get('values', [])
    
    lr = len(values)+1
    Range = "ativos!A" + str(lr)
    
    values.reverse()    
    for row in values:
        ID = row[1]
        
        if ID[0] == tipo:    
            ID = int(ID[1:])+1
            ID = f"{tipo}{ID}"
            values.reverse()
            break
        
    today = date.today().strftime("%d/%m/%Y")
    newRow = [[False, ID, tipo, sequencia, frase1, frase2, frase3, today]]
    
    sheet.values().update(spreadsheetId=spreadsheetId,
                                    range=Range,
                                    valueInputOption="USER_ENTERED",
                                    body={"values": newRow}).execute()
    
    return ID

def SetNota(ID, rotina, nota):
    sheet, spreadsheetId = GetSheet()
    result = sheet.values().get(spreadsheetId=spreadsheetId,
                                range="ativos!1:1000",
                                majorDimension="ROWS").execute()
    
    values = result.get('values', [])
    
    nota = "'+" if nota == "+" else nota
    
    lr = 1
    for row in values:
        try:
            row.index(ID)
            break
        except:
            lr += 1
            continue  #TEM Q TA VENDO PQ SE N ACHAR A LINHA 'ELE' VOLTA A ULTIMA
        
    tamanho = len(row) -8
    
    if tamanho < rotina:
        row.append(nota)
    else:
        row[rotina+7] = nota
        
    if rotina == 9:
        row[0] = True
        
    Range = "ativos!A" + str(lr)
    sheet.values().update(spreadsheetId=spreadsheetId,
                                    range=Range,
                                    valueInputOption="USER_ENTERED",
                                    body={"values": [row]}).execute()        

def returnNota(ID):
    sheet, spreadsheetId = GetSheet()
    result = sheet.values().get(spreadsheetId=spreadsheetId,
                                range="ativos!1:1000",
                                majorDimension="ROWS").execute()
    
    values = result.get('values', [])
    
    lr = 1
    for row in values:
        try:
            row.index(ID)
            break
        except:
            lr += 1
            continue  #TEM Q TA VENDO PQ SE N ACHAR A LINHA 'ELE' VOLTA A ULTIMA
            
        
    row[-1] = ''        
        
    Range = "ativos!A" + str(lr)
    sheet.values().update(spreadsheetId=spreadsheetId,
                                    range=Range,
                                    valueInputOption="USER_ENTERED",
                                    body={"values": [row]}).execute()        


#returnNota("N2")
#SetNota("N2", 2, "D+")        
#print(GetActives())
#SetNew("c","A","oi","mundo","!!!")