import unittest
from typing import Optional

from httpx import get as _next_get
from requests import get, Response

from kiss_headers import parse_it


class MyHttpTestKissHeaders(unittest.TestCase):

    HTTPBIN_GET: Optional[Response] = None
    HTTPBIN_RESPONSE_HEADER: Optional[Response] = None
    HTTPBIEN_GET_HTTPX: Optional[Response] = None

    def setUp(self) -> None:

        MyHttpTestKissHeaders.HTTPBIN_GET = get("https://httpbin.org/get")
        MyHttpTestKissHeaders.HTTPBIEN_GET_HTTPX = _next_get("https://httpbin.org/get")
        MyHttpTestKissHeaders.HTTPBIN_RESPONSE_HEADER = get(
            "https://httpbin.org/response-headers",
            params={
                "freeform": 'application/kiss; format="flowed"; expires=Thu, 12 Mar 2020 03:18:25 -0700 (PDT)'
            },
        )

    def test_httpbin_raw_headers(self):
        # HTTPResponse().

        headers = parse_it(
            """Host: developer.mozilla.org
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:50.0) Gecko/20100101 Firefox/50.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Referer: https://developer.mozilla.org/testpage.html
Connection: keep-alive
Upgrade-Insecure-Requests: 1
If-Modified-Since: Mon, 18 Jul 2016 02:36:04 GMT
If-None-Match: "c561c68d0ba92bbeb8b0fff2a9199f722e3a621a"
Cache-Control: max-age=0""".encode(
                "utf-8"
            )
        )

        self.assertEqual(17, len(headers))

        self.assertEqual(
            "c561c68d0ba92bbeb8b0fff2a9199f722e3a621a", headers.if_none_match
        )

        self.assertIn("text/html", headers.accept[0])

        self.assertNotIn("text/htm", headers.accept[0])

        self.assertIn("q", headers.accept[-1])

        self.assertEqual("0", headers.cache_control.max_age)

    def test_parse_response(self):

        headers = parse_it(MyHttpTestKissHeaders.HTTPBIN_GET)

        self.assertEqual(headers.content_type, "application/json")

        self.assertIn("application/json", headers.content_type)

        self.assertNotIn("charset", headers.content_type)

        with self.assertRaises(AttributeError):
            headers.user_agent

    def test_httpbin_get(self):

        response_headers = MyHttpTestKissHeaders.HTTPBIN_GET.headers
        headers = parse_it(response_headers)

        self.assertEqual(headers.content_type, "application/json")

        self.assertIn("application/json", headers.content_type)

        self.assertNotIn("charset", headers.content_type)

        with self.assertRaises(AttributeError):
            headers.user_agent

    def test_httpbin_freeform(self):

        response_headers = MyHttpTestKissHeaders.HTTPBIN_RESPONSE_HEADER.headers
        headers = parse_it(response_headers)

        self.assertIn("freeform", headers)

        self.assertEqual(
            {
                "application/kiss": None,
                "format": "flowed",
                "expires": "Thu, 12 Mar 2020 03:18:25 -0700 (PDT)",
            },
            dict(headers.freeform),
        )

        self.assertIn("application/kiss", headers.freeform)

    def test_httpx_requests_parse_it_eq(self):

        headers = parse_it(MyHttpTestKissHeaders.HTTPBIN_GET)

        for header in parse_it(MyHttpTestKissHeaders.HTTPBIEN_GET_HTTPX):
            self.assertIn(header.name, headers)


if __name__ == "__main__":
    unittest.main()
