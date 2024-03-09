## What is API
 - API (Application Programming Interface) is a set of rules, protocols, and tools that allows different software applications to communicate with each other.

# How it works
When you use an application on your phone, the application connects to the Internet and sends data to a server. The server then processes the data and sends it back to your phone. 
The application on your phone then interprets the data and presents it to you in a readable way. 
![alt text](https://images.datacamp.com/image/upload/v1664210695/A_simple_API_architecture_design_f98bfad9ce.png)


## What is FastAPI
 - A high-performing web framework for building APIs with Python
### How it works
 - FastAPI and general APIs work with "path operations". When we talk about "Path" we mean the part of the URL after the first **/**
```
https://example.com/items/foo
```
"Path" is :
```
/items/foo
```
FastAPI uses "operations", which here refers to HTTP methods:

- POST : Creates data
- GET : Returns the data.
- PUT : Modify the data
- DELETE : Delete data

Other interesting:
- OPTIONS
- HEAD
- PATCH
- TRACE

## Benefits of FastAPI
 - Fast
 - Easy to use
 - Robust
 - OpenAPI based

Translated with DeepL.com (free version)