# AsynchIO
## Návod na instalaci


# FastApi
## Návod na instalaci
```
```
Vytvoření virtuálního prostředí
```
python -m venv venv
```
Aktivace virtuálního prostředí, aby se nám všechny knihovny instalovali sem
```
venv\scripts\activate
```

Nainstalování knihoven fastapi a uvicorn
```
pip install fastapi uvicorn[standard]
```

Teď si vytvoříme python soubor a naimportujeme FastAPI
```
from fastapi import FastAPI

app = FastAPI()
```
### Spouštění aplikace
```
uvicorn {jmeno python souboru}:{jmeno FastAPI instance} --reload
```
V mém případě: 
```
uvicorn main:app --reload
```

## Programování
Jakmile máme připravené pracovní prostředí, je čas programovat

### Endpoint GET


```


```
```
fake_names_db = [
    "Elon Muskrat",
    "Johnny Dippity-Doo",
    "Taylor Swiftly Running Away",
    "Brad Pitstop",
    "Angelina Joliet",
    "Kim Carcrashian",
    "Leonardo DiCapuccino",
    "Oprah Windfury",
    "Beyoncé Knows-all",
    "Dwayne 'The Rocking Chair' Johnson"
]

@app.get("/names/")
async def get_names():
    return fake_names_db

```

### Endpoint POST

### Endpoint PUT

### Endpoint DELETE


