import aiohttp.web


def handler(request):
    """Simply redirect to the static HTML file."""
    return aiohttp.web.Response(
        status=302,
        headers={'Location': '/static/index.html'},
    )
