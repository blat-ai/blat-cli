from email.message import EmailMessage
from typing import Optional
from urllib.parse import urljoin

import httpx
from pydantic import AnyHttpUrl
from pydantic import BaseModel
from pydantic_core import Url


class Harvester(BaseModel):
    json_schema: str
    content: str
    start_url: AnyHttpUrl
    file_content: bytes
    file_name: Optional[str]


class BlatClient:
    def __init__(self, blat_endpoint: str, client_timeout_s: int = 300, api_key: Optional[str] = None):
        self.blat_endpoint = blat_endpoint
        self.client_timeout_s = client_timeout_s
        self.api_key = api_key

    def harvester_generate(self, schema: str, content: str, start_url: str) -> Harvester:
        file_name = "harvester.zip"
        headers = {"X-API-KEY": self.api_key} if self.api_key else {}
        resp = httpx.post(
            urljoin(self.blat_endpoint, "/harvester/generate"),
            json={"json_schema": schema, "content": content, "start_url": start_url},
            headers=headers,
            timeout=self.client_timeout_s,
        )
        resp.raise_for_status()

        if "Content-Disposition" in resp.headers:
            msg = EmailMessage()
            msg["content-type"] = resp.headers["Content-Disposition"]
            file_name = msg["content-type"].params.get("filename", file_name) or file_name

        return Harvester(
            json_schema=schema,
            content=content,
            start_url=Url(start_url),
            file_content=resp.content,
            file_name=file_name,
        )
