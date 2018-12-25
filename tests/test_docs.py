import unittest.mock

import aiohttp.test_utils

import harserver.app


class DocTests(aiohttp.test_utils.AioHTTPTestCase):
    def get_app(self):
        return harserver.app._create_app(unittest.mock.Mock())

    @aiohttp.test_utils.unittest_run_loop
    async def test_that_slash_redirects_to_docs(self):
        response = await self.client.get('/')
        self.assertEqual(1, len(response.history))
        self.assertEqual('/static/index.html', response.url.path)
        self.assertEqual('text/html', response.content_type)

    @aiohttp.test_utils.unittest_run_loop
    async def test_that_openapi_is_available(self):
        response = await self.client.get('/static/openapi.yaml')
        self.assertEqual(200, response.status)
        self.assertEqual('text/x-yaml', response.content_type)
