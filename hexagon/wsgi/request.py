class WsgiRequestBuilder(object):
    def __init__(self):
        # type: () -> None
        self.method: str = 'GET'
        self.path: str = '/'
        self.protocol: str = 'http'
        self.proxies: [str] = ['1.2.3.4']
        self.query_params: dict[str, str] = {}

    def render(self):
        # type: () -> dict[str, Any]
        return {
            'httpMethod': self.method,
            'headers': {
                'x-forwarded-for': self.proxies,
                'x-forwarded-proto': self.protocol,
            },
            'path': self.path,
            'queryStringParameters': self.query_params
        }

    def make(self, handler):
        # type: (Callable[[dict, Any], Any]) -> Any
        return handler(self.render(), None)


def start() -> WsgiRequestBuilder:
    return WsgiRequestBuilder()
