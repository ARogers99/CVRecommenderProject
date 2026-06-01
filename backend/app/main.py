from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    text: str
    is_done: bool = False

items = []
@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/cv/upload")
async def upload_cv(file: UploadFile = File(...)):
    contents = await file.read()
    # parse PDF text here with pdfplumber or PyMuPDF
    # return extracted text or store it
@app.post("/items")
async def create_item(item: Item):
    items.append(item)
    return items
@app.get("/items/{item_id}", response_model=Item)
async def get_item(item_id: int) -> Item:
    if item_id < len(items):
        return items[item_id]
    else:
        raise HTTPException(status_code=404, detail="Item not found")