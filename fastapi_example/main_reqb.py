# Request body
# Request body 是client 傳送給API的資料，通常會藉由Post, PUT, DELETE 或 PATCH來傳送
# 這裡學習如何定義request body

from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel #import BaseModel


class Item(BaseModel): # 定義data model，所有的attribute都用標準python資料型態
    name: str #沒有預設值為必填
    description: Optional[str] = None #Optional 要指定預設值為None
    price: float
    tax: Optional[float] = None


app = FastAPI()


@app.post("/items/") #post 方法傳送request body
async def create_item(item: Item):
    return item


# Request body + path parameters
@app.put("/items/{item_id}")
async def create_item(item_id: int, item: Item):
    return {"item_id": item_id, **item.dict()}

# Request body + path + query parameters
@app.put("/items/{item_id}")
async def create_item(item_id: int, item: Item, q: Optional[str] = None):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result