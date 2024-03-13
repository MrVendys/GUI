# AsyncIO

## Library Installation
```
pip install asyncio
```
# 1) Code Execution
+ Synchronous programming
+ Asynchronous programming

## 1.1) Synchronous Programming
+ Functions are executed sequentially, each function must complete before the next one starts
### For a better illustration:
*calling functions*  
function1 🔒  
function2 🔒  
function3 🔒  

*step 1*  
function1 ▶️  
function2 🔒  
function3 🔒  

*step 2*  
function1 ✔️  
function2 ▶️  
function3 🔒  

*step 3*  
function1 ✔️  
function2 ✔️  
function3 ▶️  

*step 4*  
function1 ✔️  
function2 ✔️  
function3 ✔️  

**function1** **->** **function2** **->** **function3**

## 1.2) Asynchronous Programming
+ Functions are executed as space becomes available (one starts and if there is space another one starts)
### For better understanding:

*step 1*  
function1 ▶️  
function2 🔒  

*step 2*  
function1 🕐  
function2 ▶️  

*step 3*  
function1 ▶️  
function2 ✔️ 

*step 4*  
function1 ✔️  
function2 ✔️ 

# 2) Code Execution
+ relates to hardware

+ single-thread
+ multi-thread
+ multi-process

## 2.1) single-thread
+ all functions are executed within one thread of 'context'
+ typically for both synchronous and asynchronous models

### synchronous
| steps | CPU: Thread1       |
|------------|------------|
| 1 | function1 ▶️ |
|  | function2 🔒 |
| 2 | function1 ✔️ |
|  | function2 ▶️ |
| 3 | function1 ✔️ |
|  | function2 ✔️ |

### asynchronous
| steps | CPU: Thread1       |
|------------|------------|
| 1 | function1 ▶️ |
|  | function2 🔒 |
| 2 | function1 🕐 |
|  | function2 ▶️ |
| 3 | function1 ▶️ |
|  | function2 ✔️ |
| 4 | function1 ✔️ |
|  | function2 ✔️ |

## 2.2) multi-thread
+ functions are divided into a certain number of threads i.e., one thread executes x functions, another thread executes y functions, ....
+ functions can run in parallel (simultaneously)  
+ **! management of threads and synchronization between them**
+ **! shared memory space !**

| steps | CPU       | ...       |
|------------|------------|------------|
| ... | Thread1       | Thread2       |
| 1 | function1 ▶️ | function2 ▶️ |
| 2 | function1 ✔️ | function2 ▶️ |
| 3 | function1 ✔️ | function2 ✔️ |

## 2.3) multi-process
+ similar to multi-thread
+ instead of threads uses processes, i.e., uses processor cores  
+ **each process has its own memory space**

| steps | CPU       | ...       |
|------------|------------|------------|
| ... | CPU1       | CPU2       |
| 1 | function1 ▶️ | function2 ▶️ |
| 2 | function1 ▶️ | function2 ▶️ |
| 3 | function1 ✔️ | function2 ✔️ |

# 3) AsyncIO
### 3.1)
we import asyncio
```
import asyncio
```
### 3.2)
+ Asynchronous programming is most commonly used for I/O operations. These operations (waiting for a server response) will be simulated using the command ''*await asyncio.sleep(x)*'', where x represents time.

create an asynchronous function and run it 
```
import asyncio

async def main():
  print("A")
  await asyncio.sleep(1)
  print("B")

asyncio.run(main())
```
### 3.3)
+ The delay between printing "A" and "B" is noticeable. What if we used this delay (in practice waiting for a response during which the program does nothing) to execute another function. Let's create another asynchronous function to fill this space.
```
import asyncio

async def main():
  print("A")
  await filling_function()
  print("B")

async def filling_function():
  print("1")
  await asyncio.sleep(2)
  print("2")

asyncio.run(main())
```
### 3.4)
+ Does this seem like asynchronous execution to you? - No.  
+ By using the command "*await*" we forced the execution of the filling function - but the program waited for the filling function to complete even though there is free space (asyncio.sleep(2)).  
+ This forcing is very similar to synchronous programming, where we simply run another function during output - i.e., we're not using free space (time).

Let's then use free space over time and utilize real asynchronous programming.  
This is achieved if in the environment we prepare a task, which contains a function that will be executed if there is free time available.
```
import asyncio

async def main():
  task = asyncio.create_task(filling_function()) # prepare a function that will possibly run to fill free time space
  print("A")
  print("B")

async def filling_function():
  print("1")
  await asyncio.sleep(2)
  print("2")

asyncio.run(main())
```
### 3.5)
+ After running the function "*main()*" we found that there is free time space at the end of the function i.e., after the last operation (print("B")).  
+ Subsequently, the filling function started, but it did not finish completely - there is free space (asyncio.sleep()) and the main function does not like it.  
  
+ If we want the main function to wait for the filling function anyway we can add the command "*await task*".  
+ This command will ensure that the filling function finds at least one space for execution - typically at the end of the main function 
```
import asyncio

async def main():
  task = asyncio.create_task(filling_function()) # prepare a function that will possibly run to fill free time space
  print("A")
  print("B")
  await task

async def filling_function():
  print("1")
  await asyncio.sleep(2)
  print("2")

asyncio.run(main())
```
### 3.6)
+ A more illustrative scenario will be a situation where there is enough time space to execute at least part of the filling function.
 
(main.sleep < filling_function.sleep)
```
import asyncio

async def main():
  task = asyncio.create_task(filling_function()) # prepare a function that will possibly run to fill free time space
  print("A")
  await asyncio.sleep(1) # creating enough large time space for at least part of the task to run
  print("B")

async def filling_function():
  print("1")
  await asyncio.sleep(2) # by waiting this function is already interfering with the progress of the main function (main.sleep < filling_function.sleep)
  print("2")

asyncio.run(main()
```
### 3.7)
+ Let's ask the main function to continue the filling function in more time spaces i.e., using sleep() and space at the end of the main function.
```
import asyncio

async def main():
  task = asyncio.create_task(filling_function()) # prepare a function that will possibly run to fill free time space
  print("A")
  await asyncio.sleep(1) # creating enough large time space for at least part of the task to run
  print("B")
  await task # running the rest of the filling function

async def filling_function():
  print("1")
  await asyncio.sleep(2) # by waiting this function is already interfering with the progress of the main function (main.sleep < filling_function.sleep)
  print("2")

asyncio.run(main()
```
### 3.7)
+ However, we are still awkwardly forcing time space and not utilizing "spontaneous" asynchronous execution of these functions.  
+ Let's create a scenario where no enforcement exists and functions are executed purely based on free time space.
```
import asyncio

async def main():
  task = asyncio.create_task(filling_function()) # prepare a function that will possibly run to fill free time space
  print("A")
  await asyncio.sleep(5) # creating enough large time space for the task to run
  print("B")

async def filling_function():
  print("1")
  await asyncio.sleep(2) # despite creating time space in the task there is still time for the function to fully complete
  print("2")

asyncio.run(main())
```
### 3.8)
+ If we want the filling function to return some value we use the command "*await task*"  
> ! This command is used only when we are sure that the filling function has already completed !  
> ! If the filling function has not yet completed, this command will force the execution of the filling function and will wait for it regardless of free time space !  
```
import asyncio

async def main():
  task = asyncio.create_task(filling_function())
  print("A")
  await asyncio.sleep(5) # creating enough large time space for the task to run
  print("B")
  value = await task # we are sure that the function task (filling function) has already run. If it had not, we would force its execution.

async def filling_function():
  print("1")
  await asyncio.sleep(2)
  print("2")

  return "DONE"

asyncio.run(main())
```
### 3.9)
+ In case we have multiple filling functions (tasks) that we want to run "simultaneously" i.e., the initiation is simultaneous (really, the function for which there is time space is executed - !this is not multi-thread or multi-process! we use the tool "*gather(function1,function2,function3, ....)*"  
+ await asyncio.gather(x,y) will take care of running the functions *x,y* and wait until all are completed.

This will gather the tasks and run them according to free time space -> harder maneuvering but the same essence of previous tasks
```
import asyncio

async def main():
  await asyncio.gather(
    filling_function1()
    filling_function2()
  )

async def filling_function1():
  print("1")
  await asyncio.sleep(3)
  print("2")

async def filling_function2():
  print("3")
  await asyncio.sleep(1)
  print("4")

asyncio.run(main())
```
### 3.10)
+ If we wanted to run multiple filling functions but only if there is space considering the events in the main function, we can wrap this gathering (gather) in a new function.  
-> better maneuvering than in the previous step
```
import asyncio

# Definition of two asynchronous functions
async def filling_function1():
    print("Function 1 starts")
    await asyncio.sleep(2)
    print("Function 1 ends")
    return "Result 1"

async def filling_function2():
    print("Function 2 starts")
    await asyncio.sleep(1)
    print("Function 2 ends")
    return "Result 2"

# Asynchronous function that will run function1 and function2 in parallel
async def run_all():
    result = await asyncio.gather(filling_function1(), filling_function2())
    print(f"Run all: {result}")

# Creating a task to run both functions in parallel
async def main():
    task = asyncio.create_task(run_all())
    print("A")
    await asyncio.sleep(5)
    print("B")

asyncio.run(main())
```

## 4) Summary of Commands

| command | description       |
|------------|------------|
| async def | Defines an asynchronous function |
| await | Waits for the completion of an asynchronous function, allows other tasks to run (simulate I/O operation) |
| asyncio.run() | Runs the main asynchronous function - coroutine |
| asyncio.create_task() | creates a function that will be executed in parallel i.e., when there is free time space |
| asyncio.gather() | gathers multiple asynchronous functions and automatically runs them to completion according to free time space |
| asyncio.sleep() | simulation of I/O operation - i.e., waiting |

when to use **gather()**:  
*When running several asynchronous functions where it is necessary to wait until all functions are completed (asynchronously)*  

when to use **create_task and own timing await**:  
*When there is a need for more control over individual tasks whose completion can be more flexible*

# 5) Exercise

## 5.1) Asynchronous Data Collection
>Create 3 asynchronous functions that simulate downloading data from different sources (function parameters are: source name: str, download time: int).  
>Then run these asynchronous functions in parallel.  
>+ the download time for each source should be different
>+ the bulk execution should be done using the gather() tool

**the result can be, for example, the following console output**:
```
Starting the download from Source 1...
Starting the download from Source 2...
Starting the download from Source 3...
Download from Source 3 completed.
Download from Source 1 completed.
Download from Source 2 completed.
```
<details>
  <summary>Solution</summary>

  ```
  import asyncio
  
  async def fetch_data(source, duration):
      print(f"Starting the download from {source}...")
      await asyncio.sleep(duration)
      print(f"Download from {source} completed.")
  
  async def main():
      await asyncio.gather(
          fetch_data("Source 1", 2),
          fetch_data("Source 2", 3),
          fetch_data("Source 3", 1)
      )
  
  asyncio.run(main())
  ```
</details>
