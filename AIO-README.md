# AsyncIO 


## Instalace knihovny
```
pip install asyncio
```
# 1) Vykonávání kódu
+ Synchronní programování
+ Asynchronní programování

## 1.1) Synchronní programování
+ Funkce se spouští postupně, každá funkce musí být dokončena než začne následující
### Pro lepší představení:
*zavolání funkcí*  
funkce1 🔒  
funkce2 🔒  
funkce3 🔒  

*krok 1*  
funkce1 ▶️  
funkce2 🔒  
funkce3 🔒  

*krok 2*  
funkce1 ✔️  
funkce2 ▶️  
funkce3 🔒  

*krok 3*  
funkce1 ✔️  
funkce2 ✔️  
funkce3 ▶️  

*krok 4*  
funkce1 ✔️  
funkce2 ✔️  
funkce3 ✔️  

**funkce1** **->** **funkce2** **->** **funkce3**

## 1.2) Asynchronní programování
+ Funkce se spouští dle volného prostoru (spustí se jedna a pokud je prostor spustí se jiná)
### Pro lepší pochopení:

*krok 1*  
funkce1 ▶️  
funkce2 🔒  

*krok 2*  
funkce1 🕐  
funkce2 ▶️  

*krok 3*  
funkce1 ▶️  
funkce2 ✔️ 

*krok 4*  
funkce1 ✔️  
funkce2 ✔️ 

# 2) Spouštění kódu
+ váže se na hardware

+ single-thread
+ multi-thread
+ multi-process

## 2.1) single-thread
+ všechny funkce se spouští v rámci jednoho vlákna 'kontextu'
+ typicky pro synchronní ale i asynchronní model

### sychronní
| kroky | CPU: Thread1       |
|------------|------------|
| 1 | funkce1 ▶️ |
|  | funkce2 🔒 |
| 2 | funkce1 ✔️ |
|  | funkce2 ▶️ |
| 3 | funkce1 ✔️ |
|  | funkce2 ✔️ |

### asynchronní
| kroky | CPU: Thread1       |
|------------|------------|
| 1 | funkce1 ▶️ |
|  | funkce2 🔒 |
| 2 | funkce1 🕐 |
|  | funkce2 ▶️ |
| 3 | funkce1 ▶️ |
|  | funkce2 ✔️ |
| 4 | funkce1 ✔️ |
|  | funkce2 ✔️ |

## 2.2) multi-thread
+ funkce jsou rozdělený do určitého počtu vláken tj. jedno vlákno spouští x funkcí, druhé vlákno spouští y funkcí, ....
+ funkce se mohou spouštět paralélně (najednou)  
+ **! správa vláken a synchronizace mezi nimi**
+ **! společný paměťový prostor !**

| kroky | CPU       | ...       |
|------------|------------|------------|
| ... | Thread1       | Thread2       |
| 1 | funkce1 ▶️ | funkce2 ▶️ |
| 2 | funkce1 ✔️ | funkce2 ▶️ |
| 3 | funkce1 ✔️ | funkce2 ✔️ |

## 2.3) multi-process
+ podobné multi-thread
+ místo vláken využívá procesy, tj. využívá jádra procesoru  
+ **každý proces má svůj paměťový prostor**

| kroky | CPU       | ...       |
|------------|------------|------------|
| ... | CPU1       | CPU2       |
| 1 | funkce1 ▶️ | funkce2 ▶️ |
| 2 | funkce1 ▶️ | funkce2 ▶️ |
| 3 | funkce1 ✔️ | funkce2 ✔️ |

# 3) AsyncIO
### 3.1)
importujeme asyncio
```
import asyncio
```
### 3.2)
+ ''*await asyncio.sleep(x)*''

vytvoříme asynchronní funkci a spustíme ji 
```
import asyncio

async def main():
  print("A")
  await asyncio.sleep(1)
  print("B")

asyncio.run(main())
```
### 3.3)
+ Pojďme vytvořit další asynchronní funkci, která volné časové místo vyplní.
```
import asyncio

async def main():
  print("A")
  await vyplnujici_funkce()
  print("B")

async def vyplnujici_funkce():
  print("1")
  await asyncio.sleep(2)
  print("2")

asyncio.run(main())
```
### 3.4)
+ Vynutily jsme spuštění a počkání na vyplňující funcki
+ Pojďme docílit spuštění bez explicitního vynucení a čekání - vytvoříme task, ten obsahuje funkci, která se spustí jestliže na spuštění bude volný časový prostor.
```
import asyncio

async def main():
  task = asyncio.create_task(vyplnujici_funkce()) # připravíme funkci, která se případně spustí, aby vyplnila volný časový prostor
  print("A")
  print("B")

async def vyplnujici_funkce():
  print("1")
  await asyncio.sleep(2)
  print("2")

asyncio.run(main())
```
### 3.5)
+ Jestliže chceme, aby hlavní funkce na vyplňující funkci i tak počkala můžeme přidat příkaz "*await task*".  
+ Tento příkaz se postará o to, aby si vyplňující funkce našla alespoň jeden prostor na spuštění - typicky na konci hlavní funkce 
```
import asyncio

async def main():
  task = asyncio.create_task(vyplnujici_funkce()) # připravíme funkci, která se případně spustí, aby vyplnila volný časový prostor
  print("A")
  print("B")
  await task

async def vyplnujici_funkce():
  print("1")
  await asyncio.sleep(2)
  print("2")

asyncio.run(main())
```
### 3.6)
+ Názornějším scénářem nám bude situace, kde je časový prostor na spuštění alespoň části vyplňující funkce.
 
(main.sleep < vyplnujici_funkce.sleep)
```
import asyncio

async def main():
  task = asyncio.create_task(vyplnujici_funkce()) # připravíme funkci, která se případně spustí, aby vyplnila volný časový prostor
  print("A")
  await asyncio.sleep(1) # vytvoreni dostatecne velkeho casoveho prostoru pro spusteni alespoň části tasku
  print("B")

async def vyplnujici_funkce():
  print("1")
  await asyncio.sleep(2) # timto cekanim uz vyplnujici funkce narusuje prubeh hlavni funkce (main.sleep < vyplnujici_funkce.sleep)
  print("2")

asyncio.run(main()
```
### 3.7)
+ Pojďme hlavní funkci požádat o pokračování vyplnujici funkce ve více časových prostorech tj. využití sleep() a prostoru na konci hlavní funkce.
```
import asyncio

async def main():
  task = asyncio.create_task(vyplnujici_funkce()) # připravíme funkci, která se případně spustí, aby vyplnila volný časový prostor
  print("A")
  await asyncio.sleep(1) # vytvoreni dostatecne velkeho casoveho prostoru pro spusteni alespoň části tasku
  print("B")
  await task # spusteni zbytku vyplnujici funkce

async def vyplnujici_funkce():
  print("1")
  await asyncio.sleep(2) # timto cekanim uz vyplnujici funkce narusuje prubeh hlavni funkce (main.sleep < vyplnujici_funkce.sleep)
  print("2")

asyncio.run(main()
```
### 3.8)  
+ Pojďme vytvořit scénář, kde žádne vynucování neexistuje a funkce se spouští číste vzhledem k volnému časovému prostoru.
```
import asyncio

async def main():
  task = asyncio.create_task(vyplnujici_funkce()) # připravíme funkci, která se případně spustí, aby vyplnila volný časový prostor
  print("A")
  await asyncio.sleep(5) # vytvoreni dostatecne velkeho casoveho prostoru pro spusteni tasku
  print("B")

async def vyplnujici_funkce():
  print("1")
  await asyncio.sleep(2) # i pres vytvoreni casoveho prostoru v tasku je porad cas aby se funkce plne dokoncila
  print("2")

asyncio.run(main())
```
### 3.9)
+ Pokud chceme, aby vyplňující funkce vracela nějakou hodnotu použijeme příkaz "*await task*"  
> ! Tento přikaz použijeme jen když jsme si jisti, že vyplňující funkce byla již dokončena !  
> ! Pokud vyplňující funkce ještě nebyla dokončena tento příkaz vynutí spuštění vyplňující funkce a bude na ni čekat nehledě na volný časový prostor !  
```
import asyncio

async def main():
  task = asyncio.create_task(vyplnujici_funkce())
  print("A")
  await asyncio.sleep(5) # vytvoreni dostatecne velkeho casoveho prostoru pro spusteni tasku
  print("B")
  hodnota = await task # jsme si jisti, že funkce task (vyplnujici funkce) jiz probehla. Pokud by neprobehla vynutili bychom jeji spusteni.

async def vyplnujici_funkce():
  print("1")
  await asyncio.sleep(2)
  print("2")

  return "HOTOVO"

asyncio.run(main())
```
### 3.10)
+ await asyncio.gather(x,y) se postará o to, aby se funkce *x,y* spustily a počká než se tyto funkce dokončí (vzájemně se střídají o prostor).
```
import asyncio

async def main():
  await asyncio.gather(
    vyplnujici_funkce1()
    vyplnujici_funkce2()
  )

async def vyplnujici_funkce1():
  print("1")
  await asyncio.sleep(3)
  print("2")

async def vyplnujici_funkce2():
  print("3")
  await asyncio.sleep(1)
  print("4")

asyncio.run(main())
```
### 3.11)
+ Pokud bychom chtěli spouštět více vyplňujících funkcích, ale jen v případě, že na ně bude prostor vzhledem k dění v hlavní funkci, můžeme toto shromaždění (gather) zaobalit v nove funkci.  
-> lepší manévrování než v předešlém kroku
```
import asyncio

# Definice dvou asynchronních funkcí
async def vyplnujici_funkce1():
    print("Funkce 1 začíná")
    await asyncio.sleep(2)
    print("Funkce 1 končí")
    return "Výsledek 1"

async def vyplnujici_funkce2():
    print("Funkce 2 začíná")
    await asyncio.sleep(1)
    print("Funkce 2 končí")
    return "Výsledek 2"

# Asynchronní funkce, která spustí funkce1 a funkce2 paralelně
async def spustit_vse():
    vysledek = await asyncio.gather(vyplnujici_funkce1(), vyplnujici_funkce2())
    print(f"Spustit vše: {vysledek}")

# Vytvoření úlohy pro spuštění obou funkcí paralelně
async def main():
    task = asyncio.create_task(spustit_vse())
    print("A")
    await asyncio.sleep(5)
    print("B")

asyncio.run(main())
```

## 4) Souhrn příkazů

| příkaz | popis       |
|------------|------------|
| async def | Definuje asynchronní funkci |
| await | Čeká na dokončení asynchronní funkce, umožňuje jiným úlohám běžet (simulovat I/O operaci) |
| asyncio.run() | Spustí hlavní asynchronní funkci - coroutine |
| asyncio.create_task() | vytvoří funkci, která bude vykonávána paralélně tj. až na ni bude volný časový prostor |
| asyncio.gather() | shromáždí více asynchronních funkcí a spouští je automaticky do dokončení dle volného časového prostoru |
| asyncio.sleep() | simulace I/O operace - tj. čekání |

kdy použít **gather()**:  
*Při spuštění několika asynchronních funkcích, kde je potřeba počkat než se všechny funkce dokonají (asynchronně)*  

kdy použít **create_task a vlastní načasování await**:  
*Při nutnosti větší kontroly nad jednotlivými úlohami, jejichž dokončení může být flexibilnější*

# 5) Cvičení

## 5.1) Asynchronní sběr dat
>Vytvořte 3 asynchronní funkce, které simulují stahování dat z různých zdrojů (parametry funkce jsou: název zdroje: str, doba stahování: int).  
>Následně tyto asynchronní funkce parálélně spusťte.  
>+ doba stahování pro každý zdroj by měla být jiná
>+ hromadné spuštění uskutečnětě pomocí nástroje gather()

**výsledkem může být například následující výpis v konzoli**:
```
Zahajuje se stahování z Zdroj 1...
Zahajuje se stahování z Zdroj 2...
Zahajuje se stahování z Zdroj 3...
Stahování z Zdroj 3 dokončeno.
Stahování z Zdroj 1 dokončeno.
Stahování z Zdroj 2 dokončeno.
```
<details>
  <summary>Řešení</summary>

  ```
  import asyncio
  
  async def fetch_data(source, duration):
      print(f"Zahajuje se stahování z {source}...")
      await asyncio.sleep(duration)
      print(f"Stahování z {source} dokončeno.")
  
  async def main():
      await asyncio.gather(
          fetch_data("Zdroj 1", 2),
          fetch_data("Zdroj 2", 3),
          fetch_data("Zdroj 3", 1)
      )
  
  asyncio.run(main())
  ```
</details>

