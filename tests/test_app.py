import asyncio
import unittest.mock

import aiohttp.web
import asynctest.mock

from harserver import app


class PatchingMixin(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self._patchers = []

    def tearDown(self):
        super().tearDown()
        for patcher in self._patchers:
            patcher.stop()
        self._patchers.clear()

    def add_patch(self, target, **kwargs):
        patcher = unittest.mock.patch(target, **kwargs)
        self._patchers.append(patcher)
        return patcher.start()


class EntryPointTests(PatchingMixin, unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.argparse_patch = self.add_patch('harserver.app.argparse')
        self.asyncio_patch = self.add_patch('harserver.app.asyncio')
        self.main_patch = self.add_patch('harserver.app._main')
        self.add_patch('harserver.app.logging')

    def test_that_main_uses_argument_parser(self):
        app.entry_point()

        self.argparse_patch.ArgumentParser.assert_called()
        parser = self.argparse_patch.ArgumentParser.return_value
        parser.parse_args.assert_called_once_with()

    def test_that_main_adds_debug_parameter(self):
        app.entry_point()

        parser = self.argparse_patch.ArgumentParser.return_value
        parser.add_argument.assert_any_call(
            '--debug',
            '-d',
            action='store_true',
            help=unittest.mock.ANY,
            default=unittest.mock.ANY)

    def test_that_main_adds_listen_parameter(self):
        app.entry_point()

        parser = self.argparse_patch.ArgumentParser.return_value
        parser.add_argument.assert_any_call(
            '--listen',
            '-l',
            type=str,
            default=unittest.mock.ANY,
            help=unittest.mock.ANY)

    def test_that_main_adds_port_parameter(self):
        app.entry_point()

        parser = self.argparse_patch.ArgumentParser.return_value
        parser.add_argument.assert_any_call(
            '--port-number',
            '-p',
            type=int,
            default=unittest.mock.ANY,
            help=unittest.mock.ANY)

    def test_that_main_adds_verbose_parameter(self):
        app.entry_point()

        parser = self.argparse_patch.ArgumentParser.return_value
        parser.add_argument.assert_any_call(
            '--verbose',
            '-v',
            action='store_true',
            help=unittest.mock.ANY,
            default=unittest.mock.ANY)

    def test_that_log_leveL_defaults_to_info(self):
        parser = self.argparse_patch.ArgumentParser.return_value
        parser.parse_args.return_value.debug = False
        parser.parse_args.return_value.verbose = False

        app.entry_point()

        app.logging.basicConfig.assert_called_once_with(
            level=app.logging.INFO, format=unittest.mock.ANY)

    def test_that_debug_option_sets_log_level(self):
        parser = self.argparse_patch.ArgumentParser.return_value
        parser.parse_args.return_value.debug = True
        parser.parse_args.return_value.verbose = False

        app.entry_point()

        app.logging.basicConfig.assert_called_once_with(
            level=app.logging.DEBUG, format=unittest.mock.ANY)

    def test_that_verbose_option_sets_log_level(self):
        parser = self.argparse_patch.ArgumentParser.return_value
        parser.parse_args.return_value.debug = False
        parser.parse_args.return_value.verbose = True

        app.entry_point()

        app.logging.getLogger.assert_any_call('harserver')
        logger = app.logging.getLogger.return_value
        logger.setLevel.assert_called_once_with(app.logging.DEBUG)

    def test_that_entry_point_runs_application(self):
        parser = self.argparse_patch.ArgumentParser.return_value
        opts = parser.parse_args.return_value

        app.entry_point()

        self.main_patch.assert_called_once_with(opts)
        self.asyncio_patch.run.assert_called_once_with(
            self.main_patch.return_value, debug=opts.debug)


class CreateAppTests(unittest.TestCase):
    def test_that_create_app_returns_application(self):
        maybe_app = app._create_app(unittest.mock.Mock())
        self.assertIsInstance(maybe_app, aiohttp.web.Application)

    def test_that_finished_event_is_added(self):
        app_instance = app._create_app(unittest.mock.Mock())
        self.assertIsInstance(app_instance['finished'], asyncio.Event)


class MainTests(PatchingMixin, asynctest.TestCase):
    def setUp(self):
        super().setUp()
        self.opts = unittest.mock.Mock()
        self.opts.listen = '0.0.0.0'
        self.opts.port_number = 0
        self.app_instance = app._create_app(self.opts)
        self.app_instance['finished'].set()  # stop the app immediately

        self.add_patch(
            'harserver.app._create_app', return_value=self.app_instance)

    async def test_running_application(self):
        await app._main(self.opts)

    async def test_that_run_uses_app_runner(self):
        runner_cls = self.add_patch('harserver.app.aiohttp.web.AppRunner')
        runner = runner_cls.return_value
        runner.setup = asynctest.mock.CoroutineMock()

        await app._main(self.opts)
        runner_cls.assert_called_once_with(
            self.app_instance, handle_signals=True)
        self.assertIs(runner, self.app_instance['runner'])

    async def test_that_run_adds_initial_site(self):
        site_cls = self.add_patch('harserver.app.aiohttp.web.TCPSite')
        site = site_cls.return_value
        site.start = asynctest.mock.CoroutineMock()

        await app._main(self.opts)
        site_cls.assert_called_once_with(
            self.app_instance['runner'],
            host=self.opts.listen,
            port=self.opts.port_number)
        site.start.assert_called_once_with()
