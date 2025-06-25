from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import json
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers=["*"],
)

with open("filtered_alcohol_heatmap_all_combined (1).json") as f:
    all_data = json.load(f)

with open("filtered_alcohol_heatmap_by_continent (1).json") as f:
    continent_data = json.load(f)
@app.get("/alcohol-consumption-heatmap")
def get_heatmap(continent: Optional[str] = Query('All')):
    if continent == "All":
        return{"type": "multi", "data": all_data}
    if continent in continent_data:
        return {"type":"single","continent": continent, "data": continent_data[continent]}
    return{
        "error":f"continent '{continent}' not found",
        "available": list(continent_data.keys()) + ["All"]
    }