from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int): #指定item_id型態為int
    return {"item_id": item_id} # 會收到 {"item_id":3}，注意這裡的3已經被自動轉成int而不是str


#預先定義path parameter
from enum import Enum

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName): #這裡指定model_name型態為預設的ModelName
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet": #也可以使用value取出model_name的值
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}


# Query parameters
# route function的非path parameter會自動被視為path parameter

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]


#定義Optional parameters
from typing import Optional

@app.get("/items_id/{item_id}")                                                  #FastAPI知道q是選擇性的是因為q預設為None，而不是因為q:Optional
async def read_item(item_id: str, q: Optional[str] = None, short: bool = False): #這裡的Optional是用來幫助尋找錯誤用的
    item = {"item_id": item_id}                                                  #Optional parameters也可以指定型態
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item


#多path 和 query parameters
@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, q: Optional[str] = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item


#設定必填的query parameters
@app.get("/items_needy/{item_id}")
async def read_user_item(item_id: str, needy: str):
    item = {"item_id": item_id, "needy": needy}
    return item
