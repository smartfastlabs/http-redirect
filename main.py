import os
from typing import Any, Dict

import httpx
from fastapi import FastAPI, Request
from starlette.background import BackgroundTask
from starlette.responses import StreamingResponse

app: FastAPI = FastAPI()

try:
    BASE_URL: str = os.environ["BASE_PROXY_URL"]
except KeyError:
    raise ValueError("BASE_PROXY_URL is not set")

client: httpx.AsyncClient = httpx.AsyncClient(base_url=BASE_URL)


@app.get("{path:path}")
async def proxy(path: str, request: Request):
    url: httpx.URL = httpx.URL(
        path=path,
        query=request.url.query.encode("utf-8"),
    )
    rp_req: httpx.Request = client.build_request(
        request.method,
        url,
    )
    rp_resp: httpx.Response = await client.send(rp_req, stream=True)
    return StreamingResponse(
        rp_resp.aiter_raw(),
        status_code=rp_resp.status_code,
        headers=rp_resp.headers,
        background=BackgroundTask(rp_resp.aclose),
    )
