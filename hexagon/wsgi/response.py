from typing import Any, Dict


class WsgiResponse(object):
    def __init__(self, raw_request):
        # type: (Dict[str, Any]) -> None
        self.raw_request: Dict[str, Any] = raw_request

    def body(self) -> Any:
        return self.raw_request['body']

    def status_code(self) -> int:
        return self.raw_request['statusCode']
