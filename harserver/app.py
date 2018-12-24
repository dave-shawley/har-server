import argparse
import asyncio
import logging

import aiohttp.web


def entry_point():
    """
    Application entry point.

    This function creates a server, parses command-line arguments, and
    runs the server until terminated.

    """
    opts = _parse_arguments()
    logging.basicConfig(
        level=logging.DEBUG if opts.debug else logging.INFO,
        format='%(levelname)1.1s %(name)s: %(message)s',
    )
    if opts.verbose:
        logging.getLogger(__package__).setLevel(logging.DEBUG)

    asyncio.run(_main(opts), debug=opts.debug)


async def _main(opts):
    """Create the application and run it on the event loop.

    :param argparse.Namespace opts: parsed command-line options

    N.B. we need to create the application **after** the event loop
    is running to ensure that :class:`asyncio.Event` is associated with
    the appropriate event loop.

    """
    app = _create_app(opts)
    app.on_shutdown.append(app['finished'].set)

    runner = aiohttp.web.AppRunner(app, handle_signals=True)
    await runner.setup()
    app['runner'] = runner

    site = aiohttp.web.TCPSite(runner, host=opts.listen, port=opts.port_number)
    await site.start()
    await app['finished'].wait()


def _parse_arguments():
    """Parse command-line parameters.

    :return: parsed command-line parameters
    :rtype: argparse.Namespace

    """
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '--listen',
        '-l',
        type=str,
        default='0.0.0.0',
        help='local IP address to listen on')
    parser.add_argument(
        '--port-number',
        '-p',
        type=int,
        default=8080,
        help='port number to bind to')
    parser.add_argument(
        '--debug',
        '-d',
        action='store_true',
        default=False,
        help='enable global debug logging')
    parser.add_argument(
        '--verbose',
        '-v',
        action='store_true',
        default=False,
        help='enable application-level debug logging')

    return parser.parse_args()


def _create_app(opts):
    """Create the application instance.

    :param argparse.Namespace opts: parsed command-line options
    :return: application instance with routes configured
    :rtype: aiohttp.web.Application

    A :class:`asyncio.Event` instance is stored in the application under
    the *finished* key.  This event will be set when the application is
    going to terminate.

    """
    app = aiohttp.web.Application()
    app['finished'] = asyncio.Event()
    return app
