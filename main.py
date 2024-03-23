import os
from typing import Any, Dict

import httpx
from fastapi import FastAPI, Request
from starlette.background import BackgroundTask
from starlette.responses import StreamingResponse

app: FastAPI = FastAPI()


client = httpx.AsyncClient(base_url=os.environ.get("BASE_PROXY_URL"))


@app.get("{path:path}")
async def proxy(path: str, request: Request):
    url = httpx.URL(path=path, query=request.url.query.encode("utf-8"))
    rp_req = client.build_request(
        request.method,
        url,
    )
    rp_resp = await client.send(rp_req, stream=True)
    return StreamingResponse(
        rp_resp.aiter_raw(),
        status_code=rp_resp.status_code,
        headers=rp_resp.headers,
        background=BackgroundTask(rp_resp.aclose),
    )
