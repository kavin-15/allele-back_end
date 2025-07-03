from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
# from typing import Optional
# import json
# import os
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

# @app.get("/allele-frequency-multi")
# def get_allele_frequency():
#     variant_list = [
#     "1-11796321-G-A",      # rs1229984 (ADH1B)
#     "11-5227002-T-A",      # rs334 (HBB)
#     "1-169549811-C-T",     # rs6025 (Factor V Leiden)
#     "19-44908822-C-T",     # rs7412 (APOE)
#     "19-44908684-T-C",     # rs429358 (APOE)
#     "12-111803962-G-A"     # rs671 (ALDH2)
#     ]

#     result = {}

#     def map_pop_to_continent(pop_id):
#         pop_id_lower = pop_id.lower()
#         if any(k in pop_id_lower for k in ["afr", "gwd", "esn", "msl", "lwk", "yri", "acb", "asw"]):
#             return "AFR"
#         elif any(k in pop_id_lower for k in ["amr", "clm", "mxl", "pel", "pur"]):
#             return "AMR"
#         elif any(k in pop_id_lower for k in ["eas", "jpt", "chb", "chs", "cdx", "khv"]):
#             return "EAS"
#         elif any(k in pop_id_lower for k in ["nfe", "fin", "ceu", "gbr", "tsi", "ibs"]):
#             return "NFE"
#         elif any(k in pop_id_lower for k in ["sas", "gih", "pjl", "beb", "stu", "itu"]):
#             return "SAS"
#         else:
#             return None
#     for variant_id in variant_list:

#         continent_freqs = {"AFR": [], "AMR": [], "EAS": [], "NFE": [], "SAS": []}


#         query = f"""
#         {{
#         variant(variantId: "{variant_id}", dataset: gnomad_r3) {{
#             genome {{
#             populations {{
#                 id
#                 ac
#                 an
#             }}
#             }}
#         }}
#         }}
#         """

#         response = requests.post(
#             "https://gnomad.broadinstitute.org/api",
#             json={"query": query},
#             headers={"Content-Type": "application/json"}
#         )

#         if response.status_code != 200:
#             return {"error": "Failed to fetch data from gnomAD", "status": response.status_code}

#         data = response.json()

#         try:
#             populations = data["data"]["variant"]["genome"]["populations"]

#             for pop in populations:
#                 pop_id = pop.get("id")
#                 ac = pop.get("ac", 0)
#                 an = pop.get("an", 0)

#                 af = ac / an if an != 0 else 0

#                 continent = map_pop_to_continent(pop_id)
#                 if continent:
#                     continent_freqs[continent].append(af)

#             # Compute mean per continent
#             mean_freqs = {}
#             for continent, freqs in continent_freqs.items():
#                 if freqs:
#                     mean_freqs[continent] = round(sum(freqs) / len(freqs), 6)
#                 else:
#                     mean_freqs[continent] = 0

#             return {
#                 "variant": variant_id,
#                 "frequencies": mean_freqs
#             }

#         except Exception as e:
#             result[variant_id] = {
#                 "error": f"Error parsing gnomAD data: {e}",
#                 "raw_data": data
#             }
#     return result
@app.get("/allele-frequency-multi")
def get_allele_frequency():
    variant_list = [
        "1-11796321-G-A",      # rs1229984 (ADH1B)
        "11-5227002-T-A",      # rs334 (HBB)
        "1-169549811-C-T",     # rs6025 (Factor V Leiden)
        "19-44908822-C-T",     # rs7412 (APOE)
        "19-44908684-T-C",     # rs429358 (APOE)
        "12-111803962-G-A"     # rs671 (ALDH2)
    ]

    result = {}

    def map_pop_to_continent(pop_id):
        pop_id_lower = pop_id.lower()
        if any(k in pop_id_lower for k in ["afr", "gwd", "esn", "msl", "lwk", "yri", "acb", "asw"]):
            return "AFR"
        elif any(k in pop_id_lower for k in ["amr", "clm", "mxl", "pel", "pur"]):
            return "AMR"
        elif any(k in pop_id_lower for k in ["eas", "jpt", "chb", "chs", "cdx", "khv"]):
            return "EAS"
        elif any(k in pop_id_lower for k in ["nfe", "fin", "ceu", "gbr", "tsi", "ibs"]):
            return "NFE"
        elif any(k in pop_id_lower for k in ["sas", "gih", "pjl", "beb", "stu", "itu"]):
            return "SAS"
        else:
            return None

    for variant_id in variant_list:
        continent_freqs = {"AFR": [], "AMR": [], "EAS": [], "NFE": [], "SAS": []}

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
            result[variant_id] = {"error": f"Failed to fetch data from gnomAD (status {response.status_code})"}
            continue

        data = response.json()

        try:
            populations = data["data"]["variant"]["genome"]["populations"]

            for pop in populations:
                pop_id = pop.get("id")
                ac = pop.get("ac", 0)
                an = pop.get("an", 0)
                af = ac / an if an != 0 else 0
                continent = map_pop_to_continent(pop_id)
                if continent:
                    continent_freqs[continent].append(af)

            mean_freqs = {}
            for continent, freqs in continent_freqs.items():
                mean_freqs[continent] = round(sum(freqs) / len(freqs), 6) if freqs else 0

            # Store in the result dictionary
            result[variant_id] = mean_freqs

        except Exception as e:
            result[variant_id] = {
                "error": f"Error parsing gnomAD data: {e}",
                "raw_data": data
            }

    # Return the collected results for all variants
    return result