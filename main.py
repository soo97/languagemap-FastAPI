from fastapi import FastAPI
# test deploy

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello FastAPI"}
