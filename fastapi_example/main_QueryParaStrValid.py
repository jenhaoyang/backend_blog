#Query Parameters and String Validations
#Path Parameters也有類似的功能

from typing import Optional

from fastapi import FastAPI, Query

app = FastAPI()

#這個範例指定q為optinal(因為預設為None)並且限制長度為50
#Query的第一個參數是預設值
#q: Optional[str] = Query(None)  和 q: Optional[str] = None的效果是一樣的
#Query也可以使用regular expression
@app.get("/items/")
async def read_items(q: Optional[str] = Query(None, min_length=3, max_length=50, regex="^fixedquery$")):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

#同樣的我們也可以指定其他預設值
#指定預設值讓q變成可選的
@app.get("/items_default/")
async def read_items(q: str = Query("fixedquery", min_length=3)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

#如果要讓query parameter變成必填
#可以將預設值設為...
@app.get("/items/")
async def read_items(q: str = Query(..., min_length=3)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


#如果要讓 query parameter 接收list(也就是同一個參數重複出現在 query parameter )
#可以使用下面方法
#訪問網址如下
# http://localhost:8000/items/?q=foo&q=bar
from typing import List, Optional

@app.get("/items_list/")
async def read_items(q: Optional[List[str]] = Query(None)):
    query_items = {"q": q}
    return query_items

#也可以定義list的預設值
@app.get("/items_list_default/")
async def read_items(q: List[str] = Query(["foo", "bar"])):
    query_items = {"q": q}
    return query_items

#也可以直接使用list，不過文件不會去確認list裡面的型態
@app.get("/items_list_direct/")
async def read_items(q: list = Query([])):#文件不會檢查list元素的型態
    query_items = {"q": q}
    return query_items


#Query還有更多的參數可以使用
@app.get("/items_title/")
async def read_items(
    q: Optional[str] = Query(None,
                            title="Query string", #增加title，會增加到文件裡參數的說明
                            description="Query string for the items to search in the database that have a good match",#增加description，會增加到文件裡參數的說明
                            min_length=3) 
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

# 別名參數
@app.get("/items_alias/")
async def read_items(q: Optional[str] = Query(None, alias="item-query")): #設定q的別名為item-query
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

# 告知參數即將停止支援，設為deprecated
@app.get("/items_deprecated/")
async def read_items(
    q: Optional[str] = Query(
        None,
        alias="item-query",
        title="Query string",
        description="Query string for the items to search in the database that have a good match",
        min_length=3,
        max_length=50,
        regex="^fixedquery$",
        deprecated=True,
    )
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results