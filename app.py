import io

from pydantic import BaseModel

from master_call import make_master_call
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

class Args(BaseModel):
    lat: str
    lon: str
    time: str
    type: str
    zoom: int

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello from API!"}

@app.get("/default")
def default_request():
    geo_coords = "50.45466 30.5238"  # Kyiv

    lat = float(geo_coords.split(" ")[0])
    lon = float(geo_coords.split(" ")[1])

    # 250m geographic_with_clouds
    # 1km vegetation
    # 2km temp

    matrix_type = "250m"

    img = make_master_call(lat, lon, matrix_type, 3, "2012-07-09")

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)

    return StreamingResponse(buf, media_type="image/png")

@app.get("/at")
def get_at(args: Args):
    img = make_master_call(args.lat, args.lon, args.type, args.zoom, args.time)

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)

    return StreamingResponse(buf, media_type="image/png")