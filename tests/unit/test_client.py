import json
import uuid
from urllib.parse import urljoin

import pytest
from httpx import Response
from pydantic_core import Url

from blat_cli.client import BlatClient
from blat_cli.client import Harvester


@pytest.fixture
def blat_client() -> BlatClient:
    return BlatClient("http://test.blat.ai", str(uuid.uuid4()))


def test_generate_harvester(blat_client, respx_mock):
    schema = '{"name": "test", "type": "string"}'
    content = "<html><body>content</body></html>"
    url = "https://www.example.com"
    file_content = b"thisshouldbeazipfile"

    route = respx_mock.post(urljoin(blat_client.blat_endpoint, "/harvester/generate")).mock(
        return_value=Response(
            200, content=file_content, headers={"Content-Disposition": "attachment; filename=test.zip"}
        )
    )

    result = blat_client.harvester_generate(schema, content, url)

    assert route.called
    assert json.loads(route.calls.last.request.content.decode()) == {
        "json_schema": schema,
        "content": content,
        "start_url": url,
    }
    assert route.calls.last.request.headers["X-API-KEY"] == blat_client.api_key
    assert result == Harvester(
        json_schema=schema, content=content, start_url=Url(url), file_content=file_content, file_name="test.zip"
    )
