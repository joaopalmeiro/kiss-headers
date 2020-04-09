import unittest
from datetime import datetime
from datetime import timezone
from email import utils

from kiss_headers import (
    CustomHeader,
    ContentType,
    SetCookie,
    ContentLength,
    ContentDisposition,
    CrossOriginResourcePolicy,
    ReferrerPolicy,
    From,
    Allow,
    Date,
)


class MyBuilderTestCase(unittest.TestCase):
    def test_custom_header_expect(self):

        with self.assertRaises(NotImplementedError):
            k = CustomHeader("Should absolutely not work !")

    def test_content_type(self):

        self.assertEqual(
            repr(ContentType("application/json", charset="utf-8")),
            'Content-Type: application/json; charset="UTF-8"',
        )

    def test_set_cookie(self):

        dt = datetime.now()

        self.assertEqual(
            repr(SetCookie("MACHINE_IDENTIFIANT", "ABCDEFGHI", expires=dt)),
            'Set-Cookie: MACHINE_IDENTIFIANT="ABCDEFGHI"; expires="{dt}"; HttpOnly'.format(
                dt=utils.format_datetime(dt.astimezone(timezone.utc), usegmt=True)
            ),
        )

    def test_content_length(self):

        self.assertEqual(repr(ContentLength(1881)), "Content-Length: 1881")

    def test_content_disposition(self):

        self.assertEqual(
            repr(ContentDisposition("attachment", filename="test-file.json")),
            'Content-Disposition: attachment; filename="test-file.json"',
        )

    def test_value_error_builder(self):

        with self.assertRaises(ValueError):
            CrossOriginResourcePolicy("policy-not-known-yet")

        with self.assertRaises(ValueError):
            ReferrerPolicy("hello-world")

        with self.assertRaises(ValueError):
            From("not-a-valid-email.com")

        with self.assertRaises(ValueError):
            Allow("DOES-NOT-EXIST-HTTP-VERB")

    def test_verify_always_gmt(self):

        self.assertTrue(repr(Date(datetime.now())).endswith("GMT"))


if __name__ == "__main__":
    unittest.main()
