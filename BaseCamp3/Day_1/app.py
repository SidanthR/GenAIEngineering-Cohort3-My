# import sys 
from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello World"}

@app.get("/add")
def add(x, y):
    result = float(x) + float(y)
    return {"Operation": "add", 'x': x, 'y': y, 'result': result}

@app.get("/subtract")
def subtract(x, y):
    result = float(x) - float(y)
    return {"Operation": "subtract", 'x': x, 'y': y, 'result': result}

@app.get("/multiply")
def multiply(x, y):
    result = float(x) * float(y)
    return {"Operation": "multiply", 'x': x, 'y': y, 'result': result}

@app.get("/divide")
def divide(x, y):
    try: 
        if y == 0:
            raise ZeroDivisionError
    except ZeroDivisionError:
        print("Error: Division by zero is not allowed.")
        return {"Error": "Division by zero is not allowed."}
    
    result = float(x) / float(y)
    return {"Operation": "divide", 'x': x, 'y': y, 'result': result}

# x = int(input("Enter first number: "))
# y = int(input("Enter second number: "))

# print(divide(x, y))


if __name__ == "__main__":
    # x = sys.argv[1]
    # y = sys.argv[2]
    # print( add(int(x), int(y)) )
    uvicorn.run(app, host='0.0.0.0', port=9321)
    #we can run the app using: python app.py
    #or "fastapi dev app.py" 