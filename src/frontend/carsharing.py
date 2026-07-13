from fastapi import FastAPI

app = FastAPI()


db = [
    {"id": 1, "size": "s", "fuel": "gasoline", "doors": 3, "transmission": "manual", "price": 100},
    {"id": 2, "size": "s", "fuel": "gasoline", "doors": 3, "transmission": "manual", "price": 200},
    {"id": 3, "size": "m", "fuel": "gasoline", "doors": 5, "transmission": "auto", "price": 150},
    {"id": 4, "size": "m", "fuel": "gasoline", "doors": 3, "transmission": "auto", "price": 300},
    {"id": 5, "size": "l", "fuel": "gasoline", "doors": 5, "transmission": "auto", "price": 800},
]


@app.get("/cars")
def get_cars(size: str = None, doors: int = None, fuel: str = None, transmission: str = None):
    results = db
    if size:
        results = [car for car in results if car["size"] == size]
    if doors:
        results = [car for car in results if car["doors"] == doors]
    if fuel:
        results = [car for car in results if car["fuel"] == fuel]
    if transmission:
        results = [car for car in results if car["transmission"] == transmission]
    return results



@app.get("/")
async def health():
    return {"message": "Health to the Car Sharing API"}