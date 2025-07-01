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
      variant(variantId: "{variant_id}", dataset: gnomad_r3) {{
        genome {{
          populations {{
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
        json={"query": query},
        headers={"Content-Type": "application/json"}
    )

    if response.status_code != 200:
        return {"error": "Failed to fetch data from gnomAD", "status": response.status_code}

    data = response.json()

    try:
        populations = data["data"]["variant"]["genome"]["populations"]

        # Mapping function
        def map_pop_to_continent(pop_id):
            pop_id_lower = pop_id.lower()
            if "afr" in pop_id_lower or "gwd" in pop_id_lower or "esn" in pop_id_lower or "msl" in pop_id_lower or "lwk" in pop_id_lower or "yri" in pop_id_lower or "acb" in pop_id_lower or "asw" in pop_id_lower:
                return "AFR"
            elif "amr" in pop_id_lower or "clm" in pop_id_lower or "mxl" in pop_id_lower or "pel" in pop_id_lower or "pur" in pop_id_lower:
                return "AMR"
            elif "eas" in pop_id_lower or "jpt" in pop_id_lower or "chb" in pop_id_lower or "chs" in pop_id_lower or "cdx" in pop_id_lower or "khv" in pop_id_lower:
                return "EAS"
            elif "nfe" in pop_id_lower or "fin" in pop_id_lower or "ceu" in pop_id_lower or "gbr" in pop_id_lower or "tsi" in pop_id_lower or "ibs" in pop_id_lower:
                return "NFE"
            elif "sas" in pop_id_lower or "gih" in pop_id_lower or "pjl" in pop_id_lower or "beb" in pop_id_lower or "stu" in pop_id_lower or "itu" in pop_id_lower:
                return "SAS"
            else:
                return None  # Ignore 'oth', 'asj', 'mid', etc. for clarity

        # Initialize groups
        continent_freqs = { "AFR": [], "AMR": [], "EAS": [], "NFE": [], "SAS": [] }

        for pop in populations:
            pop_id = pop.get("id")
            ac = pop.get("ac", 0)
            an = pop.get("an", 0)

            af = ac / an if an != 0 else 0

            continent = map_pop_to_continent(pop_id)
            if continent:
                continent_freqs[continent].append(af)

        # Compute mean per continent
        mean_freqs = {}
        for continent, freqs in continent_freqs.items():
            if freqs:
                mean_freqs[continent] = round(sum(freqs) / len(freqs), 6)
            else:
                mean_freqs[continent] = 0

        return {
            "variant": variant_id,
            "frequencies": mean_freqs
        }

    except Exception as e:
        return {
            "error": f"Error parsing gnomAD data: {e}",
            "raw_data": data
        }
