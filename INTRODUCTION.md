## Co je API
 - API (Application Programming Interface) je soubor pravidel, protokolů a nástrojů, které umožňují různým softwarovým aplikacím vzájemně komunikovat.

# Jak to funguje
Při používání se aplikace připojí k internetu a odesílá data na server. Server pak data zpracuje a odešle je zpět do aplikace. 
Aplikace pak data interpretuje a prezentuje vám je v čitelné podobě. 
![alt text](https://images.datacamp.com/image/upload/v1664210695/A_simple_API_architecture_design_f98bfad9ce.png)


## Co je FastAPI
 - Vysoce výkonný webový framework pro vytváření rozhraní API v jazyce Python.
### Jak to funguje
 - FastAPI a obecně API pracujou s "operacemi cest" (Path). Myslí se tím část URL za první **/**
```
https://example.com/items/foo
```
"Path" je :
```
/items/foo
```  
>[!HINT] 
> Dále to budu nazývat endpointy, ale je to to samé.  

FastAPI používá "operace", což zde odkazuje na HTTP metody:

- POST : Vytvoří data
- GET : Vrátí data
- PUT : Upraví data
- DELETE : Smaže data

Další zajimavé informace:
- OPTIONS
- HEAD
- PATCH
- TRACE

## Pydantic
 FastAPI je založena na knihovně Pydantic, která slouží pro validaci dat. 
 Jestli jsou ve správném formátu, správném typu aj.
 Blíže se s ní seznámíme dále

 
### Proč ho používat?

 Nápověda pro typy 
 Rychlá validace dat  
 Kompatibilní s JSON  
 Chybové hlášky  

### Podobnost s Flask
Ukázak kodu 
FastAPI
```
app = FastAPI()

@app.get("/hello/{name}")
async def get_hello(name: str):
    return {"message": f"Hello, {name}!"}
```
Flask
```
app = Flask(__name__)

@app.route("/hello/<name>")
def get_hello(name):
    return {"message": f"Hello, {name}!"}
```

## Výhody FastAPI
 -:white_check_mark: Rychlejší (přispívá k tomu možnost asynchroního běhu)
 -:white_check_mark: Nápovědy k typům a ověřování dat (Pydantic)
 -:white_check_mark: Automatická dokumentace (Swagger UI)
 -:white_check_mark: Vestavěné vyhytávky (Flask si je muže přidat)
 -:white_check_mark: Založeno na OpenAPI

## Nevýhody FastAPI
 -:negative_squared_cross_mark: Těžší na naučení
 -:negative_squared_cross_mark: Méně rozšíření třetích stran
Translated with DeepL.com (free version)



