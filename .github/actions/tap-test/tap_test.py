import unittest
from unittest import TestCase

import requests
from defusedxml import ElementTree


class TestWebsite(TestCase):

    def test_apex_to_www_redirect(self):
        resp = requests.head("http://davidbyrne.io") # won't auto-redirect from https apex, see https://github.community/t5/GitHub-Pages/Does-GitHub-Pages-Support-HTTPS-for-www-and-subdomains/td-p/7116/page/4
        self.assertEqual(301, resp.status_code)
        self.assertEqual("https://www.davidbyrne.io/", resp.headers["Location"])

    def test_http_www_to_https_www_redirect(self):
        resp = requests.head("http://www.davidbyrne.io")
        self.assertEqual(301, resp.status_code)
        self.assertEqual("https://www.davidbyrne.io/", resp.headers["Location"])

    def test_www_ok(self):
        resp = requests.head("https://www.davidbyrne.io")
        self.assertEqual(200, resp.status_code)
        self.assertEqual("text/html; charset=utf-8", resp.headers["Content-Type"])
        self.assertGreater(int(resp.headers["Content-Length"]), 1000, "Expected the response to at least be 1000 bytes")

    def test_site_content(self):
        resp = requests.get("https://www.davidbyrne.io")
        self.assertEqual(200, resp.status_code)
        self.assertIn("David Byrne", resp.text)
        self.assertIn("Software Engineer", resp.text)
        self.assertIn("david.dbyrne@gmail.com", resp.text)
        self.assertIn("https://www.linkedin.com/in/david-d-byrne", resp.text)


class TestFilesSite(TestCase):

    def test_http_to_https_redirect(self):
        resp = requests.head("http://files.davidbyrne.io")
        self.assertEqual(301, resp.status_code)
        self.assertEqual("https://files.davidbyrne.io/", resp.headers["Location"])

    def test_root_404s(self):
        resp = requests.get("https://files.davidbyrne.io")
        self.assertEqual(404, resp.status_code)
        self.assertIn("404", resp.text)
        self.assertIn(r"¯\_(ツ)_/¯", resp.text)

    def test_fyp_is_available(self):
        resp = requests.head("https://files.davidbyrne.io/FYP")
        self.assertEqual(200, resp.status_code)
        self.assertGreater(int(resp.headers["Content-Length"]), 1400000, "Expected the response to at least be 1400000 bytes")
        self.assertEqual("application/pdf", resp.headers["Content-Type"])
        self.assertIn("1b5866d5cc69a8247b5498936b232667-ssl", resp.headers["Etag"])


class TestBlog(TestCase):
    def test_http_to_https_redirect(self):
        resp = requests.head("http://blog.davidbyrne.io")
        self.assertEqual(301, resp.status_code)
        self.assertEqual("https://blog.davidbyrne.io/", resp.headers["Location"])

    def test_main_page_content(self):
        resp = requests.get("https://blog.davidbyrne.io")
        self.assertEqual(200, resp.status_code)
        self.assertIn("David Byrne", resp.text)
        self.assertIn("david.dbyrne@gmail.com", resp.text)
        self.assertIn("/feed.xml", resp.text)

    def test_rss_feed(self):
        resp = requests.get("https://blog.davidbyrne.io/feed.xml")
        self.assertEqual(200, resp.status_code)
        feed = ElementTree.fromstring(resp.text)
        self.assertGreater(len(feed.findall("{http://www.w3.org/2005/Atom}entry")), 4, "Expected there to be more than 4 blog entries in the RSS")


class TestDevSite(TestCase):

    def test_apex_redirect_to_main_site(self):
        resp = requests.head("https://davidbyrne.dev")
        self.assertEqual(301, resp.status_code)
        self.assertEqual("https://www.davidbyrne.io/", resp.headers["Location"])

    def test_www_redirect_to_main_site(self):
        resp = requests.head("https://www.davidbyrne.dev")
        self.assertEqual(301, resp.status_code)
        self.assertEqual("https://www.davidbyrne.io/", resp.headers["Location"])

if __name__ == '__main__':
    unittest.main()
