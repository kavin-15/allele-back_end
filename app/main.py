from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import json
import os
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers=["*"],
)

# with open("filtered_alcohol_heatmap_all_combined (1).json") as f:
#     all_data = json.load(f)

# with open("filtered_alcohol_heatmap_by_continent (1).json") as f:
#     continent_data = json.load(f)
# @app.get("/alcohol-consumption-heatmap")
# def get_heatmap(continent: Optional[str] = Query('All')):
#     if continent == "All":
#         return{"type": "multi", "data": all_data}
#     if continent in continent_data:
#         return {"type":"single","continent": continent, "data": continent_data[continent]}
#     return{
#         "error":f"continent '{continent}' not found",
#         "available": list(continent_data.keys()) + ["All"]
#     }

@app.get("/allele-frequency")
def get_allele_frequency(
    variant_id: str = Query("4-99318162-T-C")
    ):
    query = f"""
    {{
        variant(variantId: "{variant_id}", dataset: gnomad_r3){{
        genome{{
        populations{{
            id
            ac
            an
        }}
        }}
        }}
    }}
    """
    response = requests.post(
        "https://gnomad.broadinstitute.org/api",
        json={"query":query},
        headers={"Content-Type": "application/json"}
    )

    if response.status_code != 200:
        return{"error": "Failed to fetch data from gnomAD"}
    data = response.json()

    try:
        populations=data["data"]["variant"]["genome"]["populations"]
        frequencies ={}
        for pop in population:
            pop_id = pop["id"]
            ac = pop["ac"]
            an = pop["an"]
            af = round(ac/an, 6) if an != 0 else 0
            frequencies[pop_id] = af
        return{
            "variant": variant_id,
            "frequencies": frequencies
        }
    except Exception as e:
        return{
            "error": f"Error parsing gnomAD data: {e}", "raw_data": data
        }