from fastapi import Request
from pydantic import AnyUrl


def get_client(request: Request) -> AnyUrl:
    host, port = request.client.host, str(request.client.port)
    return AnyUrl.build(scheme='http', host=host, port=port)
