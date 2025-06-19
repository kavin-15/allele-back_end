from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers=["*"],
)
@app.get("/")
def root():
    return {"message": "Allele backend is running."}

@app.get("/heatmap-data")
def get_heatmap_data():
    return{
        "xLabels":["SNP_A","SNP_B","SNP_C","SNP_D"],
        "yLabels":["Sample1","Sample2","Sample3"],
        "data":[
            [0,1,2,1],
            [1,0,2,0],
            [2,1,0,1]
        ]
    }
@app.get("/test")
def test():
    return{"status":"Backend working perfectly"}