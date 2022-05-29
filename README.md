# RESTFUL_API

## Introduction
This restful api is created using python and mysql.   
The key value contains different languages and special symbols.


## Demand  
1. POST /key   
    `success: return 201 `  
    `exist: return 400`
2. GET /key  
    `success: return 200 and response all keys`  
3. GET /key/{key}  
  `success: return 200`  
  `not found: return 404`  
4. PUT /key/{key}  
  `new create key: return 201`  
  `exist and update: return 200`  
5. DELETE /key/{key}  
  `success: return 200`  
  
## Database schema    

| key(255) | value(255) |  
|---|---|
| test| 123|

## Input format  
```  
curl -X POST http://127.0.0.1:5000/key -H 'Content-Type: application/json' -d '{"key":"111","value":"3331"}' #1
curl -X GET http://127.0.0.1:5000/key -H 'Content-Type: application/json' #2
curl -X GET http://127.0.0.1:5000/key/111q -H 'Content-Type: application/json' #3
curl -X PUT http://127.0.0.1:5000/key/111 -H 'Content-Type: application/json' -d '{"value":"331opop31"}' #4
curl -X DELETE http://127.0.0.1:5000/key/111 -H "Accept: application/json" #5
```
