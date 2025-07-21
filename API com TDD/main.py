# StoreAPI/main.py
from fastapi import FastAPI
from core.database import db_client

app = FastAPI(title="Store API")

@app.on_event("startup")
async def startup_event():
    await db_client.connect()

@app.on_event("shutdown")
async def shutdown_event():
    await db_client.close()

@app.get("/")
def read_root():
    return {"message": "Bem-vindo à Store API!"}

# Importaremos e incluiremos os routers aqui mais tarde
# from routers.product_router import router as product_router
# app.include_router(product_router, prefix="/products", tags=["Products"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)