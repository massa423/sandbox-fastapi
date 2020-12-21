from fastapi import FastAPI, Query, Path, Body, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
from typing import Dict, Optional, List
from starlette.responses import Response
from starlette.status import HTTP_201_CREATED
from time import sleep
from datetime import datetime

app = FastAPI()


@app.get("/")
async def hello() -> Dict:
    return {"text": "hello world"}


@app.get("/get/{path}")
async def path_and_query_params(
    path: str, query: int, default_none: Optional[str] = None
) -> Dict:
    return {"text": f"hello, {path}, {query} and {default_none}"}


@app.get("/validation/{path}")
async def validation(
    string: str = Query(None, min_length=2, max_length=5, regex=r"[a-c]+."),
    integer: int = Query(..., gt=1, le=3),
    alias_query: str = Query("default", alias="alias-query"),
    path: int = Path(10),
) -> Dict:
    return {
        "string": string,
        "integer": integer,
        "alias_query": alias_query,
        "path": path,
    }


class Data(BaseModel):
    """
    Data
    """

    string: str
    default_none: Optional[int] = None
    lists: List[int]


@app.post("/post")
async def declare_request_body(data: Data) -> Dict:
    return {"text": f"hello, {data.string}, {data.default_none}, {data.lists}"}


@app.post("/post/embed")
async def declare_embedded_request_body(data: Data = Body(..., embed=True)) -> Dict:
    return {"text": f"hello, {data.string}, {data.default_none}, {data.lists}"}


class subDict(BaseModel):
    """
    subDict
    """

    strings: str
    integer: int


class NestedData(BaseModel):
    """
    NestedData
    """

    subData: subDict
    subDataList: List[subDict]


@app.post("/post/nested")
async def declare_nested_request_body(data: NestedData) -> Dict:
    return {"text": f"hello {data.subData}, {data.subDataList}"}


class ValidatedSubData(BaseModel):
    """
    ValidatedSubData
    """

    strings: str = Field(None, min_length=2, max_length=5, regex=r"[a-b]+.")
    integer: int = Field(..., gt=1, le=3)  # required


class ValidatedNetedData(BaseModel):
    """
    ValidatedNetedData
    """

    subData: ValidatedSubData = Field(..., example={"strings": "aaa", "integer": 2})
    subDataList: List[ValidatedSubData] = Field(...)


@app.post("/validation")
async def validation_post(data: ValidatedNetedData) -> Dict:
    return {"text": f"hello, {data.subData}, {data.subDataList}"}


class ItemOut(BaseModel):
    """
    ItemOut
    """

    strings: str
    aux: int = 1
    text: str


@app.get("/response", response_model=ItemOut)
async def response(strings: str, integer: int) -> Dict:
    return {"text": "hello world!", "strings": strings, "integer": integer}


# 辞書に存在しない場合にresponse_modelのattributesのデフォルト値を"入れない"
@app.get("/unset", response_model=ItemOut, response_model_exclude_unset=True)
async def response_exclude_unset(strings: str, integer: int) -> Dict:
    return {"text": "hello world!", "strings": strings, "integer": integer}


# response_modelの"strings", "aux"を無視 -> "text"のみ返す
@app.get("/exclude", response_model=ItemOut, response_model_exclude={"strings", "aux"})
async def response_exclude(strings: str, integer: int) -> Dict:
    return {"text": "hello world!", "strings": strings, "integer": integer}


# response_modelの"text"のみ考慮する -> "text"のみ返す
@app.get("/include", response_model=ItemOut, response_model_include={"text"})
async def response_include(strings: str, integer: int) -> Dict:
    return {"text": "hello world!", "strings": strings, "integer": integer}


@app.get("/status", status_code=200)
async def response_status_code(integer: int, response: Response) -> Dict:
    if integer > 5:
        raise HTTPException(status_code=404, detail="this is error messages")

    elif integer == 1:
        response.status_code = HTTP_201_CREATED
        return {"text": "hello world, created!"}
    else:
        return {"text": "hello world!"}


def time_bomb(count: int) -> None:
    """
    time_bomb
    """
    sleep(count)
    print(f"bomb!! {datetime.utcnow()}")


@app.get("/{count}")
async def back(count: int, background_task: BackgroundTasks) -> Dict[str, str]:
    background_task.add_task(time_bomb, count)
    return {"text": "finish"}
