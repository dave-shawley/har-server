==========
HAR Server
==========
Simple programmable HTTP API server.

|build| |coverage| |docs|

The server is programmable using elements from the `HTTP Archive`_ (HAR)
specification originally developed by `Jan Odvarko`_ and the `W3C`_
web-performance working group.  It was never moved beyond draft in the
W3C.  Jan Odvarko has maintained the specification on his blog.  I created
this project after discovering the `mockbin`_ service created by `Mashape`_
(now `KongHQ`_).  Unfortunately `mockbin`_ does not meet my exact needs.

Usage
=====
The primary use case is to return programmed responses to specified
requests.  The response is POSTed to service along with a matching request.
Both are specified as HAR objects -- the request is a `HAR request`_ and
the response is a `HAR response`_ ::

   POST /responses HTTP/1.1
   Host: 127.0.0.1:8080
   Content-Type: application/json
   Content-Length: 733

   {
      "request": {
         "method": "GET",
         "url": "http://example.org/status",
         "httpVersion": "HTTP/1.1",
         "cookies": [],
         "headers": [],
         "queryString": [],
         "postData": {},
         "headersSize": -1,
         "bodySize": 0
      },
      "response": {
         "status": 200,
         "statusText": "OK",
         "httpVersion": "HTTP/1.1",
         "cookies": [],
         "headers": [
            {"name":"Content-Type", "value":"application/json"}
         ],
         "content": {
            "mimeType": "application/json",
            "encoding": "json",
            "text": {
               "service": "my-service",
               "status": "ok"
            }
         },
         "redirectURL": "",
         "headersSize": -1,
         "bodySize": -1
      }
   }

   HTTP/1.1 200 OK
   Content-Type: application/json
   Content-Length: 49
   Link: <http://127.0.0.1:8080/hosts>; rel=host-map; method=GET
   Link: <http://127.0.0.1:8080/requests>; rel=requests; method=GET
   Link: <http://127.0.0.1:8080/responses>; rel=add-response; method=POST
   Link: <http://127.0.0.1:8080/responses>; rel=clear-responses;
     method=PURGE

   {
      "effective_url": "http://127.0.0.1:32443"
   }

After this message is sent, the service will respond to ``GET /status``
on port 32443 with the registered response::

   GET /status HTTP/1.1
   Host: 127.0.0.1:32443

   HTTP/1.1 200 OK
   Content-Type: application/json

   {
     "service": "my-service",
     "status": "ok"
   }

.. _HAR request: http://www.softwareishard.com/blog/har-12-spec/#request
.. _HAR response: http://www.softwareishard.com/blog/har-12-spec/#response
.. _HTTP Archive: http://www.softwareishard.com/blog/har-12-spec/
.. _Jan Odvarko: http://www.softwareishard.com/blog/about/
.. _KongHQ: https://konghq.com/
.. _Mashape: https://en.wikipedia.org/wiki/Mashape
.. _mockbin: https://mockbin.com/
.. _W3C: https://w3c.github.io/web-performance/specs/HAR/Overview.html

.. |build| image:: https://circleci.com/gh/dave-shawley/har-server/tree/master.svg?style=svg
   :target: https://circleci.com/gh/dave-shawley/har-server/tree/master
.. |coverage| image:: https://coveralls.io/repos/github/dave-shawley/har-server/badge.svg?branch=master
   :target: https://coveralls.io/github/dave-shawley/har-server?branch=master
.. |docs| image:: https://readthedocs.org/projects/har-server/badge/?version=latest
   :target: https://har-server.readthedocs.io/en/latest/?badge=latest
