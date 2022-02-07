import os

import mock
from fastapi_mvc.cli.commands.run import run


DATA_DIR = os.path.abspath(
    os.path.join(
        os.path.abspath(__file__),
        "../../../data",
    )
)


def test_run_help(cli_runner):
    result = cli_runner.invoke(run, ["--help"])
    assert result.exit_code == 0


def test_run_invalid_option(cli_runner):
    result = cli_runner.invoke(run, ["--not_exists"])
    assert result.exit_code == 2


@mock.patch("fastapi_mvc.cli.commands.run.os.getcwd", return_value=DATA_DIR)
@mock.patch("fastapi_mvc.cli.commands.run.uvicorn.run", return_value=0)
def test_run_default_options(uvi_mck, os_mck, cli_runner):
    result = cli_runner.invoke(run, [])
    assert result.exit_code == 0
    os_mck.assert_called_once()
    uvi_mck.assert_called_once_with(
        "foobar.app.asgi:application",
        host="127.0.0.1",
        port=8000,
        reload=True,
        workers=1,
        log_config=None,
        access_log=True,
    )


@mock.patch("fastapi_mvc.cli.commands.run.os.getcwd", return_value=DATA_DIR)
@mock.patch("fastapi_mvc.cli.commands.run.uvicorn.run", return_value=0)
def test_run_with_options(uvi_mck, os_mck, cli_runner):
    result = cli_runner.invoke(
        run, ["--host", "10.20.30.40", "-p", 1234, "--no-reload", "-w", 2]
    )
    assert result.exit_code == 0
    os_mck.assert_called_once()
    uvi_mck.assert_called_once_with(
        "foobar.app.asgi:application",
        host="10.20.30.40",
        port=1234,
        reload=False,
        workers=2,
        log_config=None,
        access_log=True,
    )


@mock.patch("fastapi_mvc.cli.commands.run.os.path.exists", return_value=False)
def test_run_no_ini_file(os_mck, cli_runner):
    result = cli_runner.invoke(run, [])
    assert result.exit_code == 1

    os_mck.assert_called_once()


@mock.patch("fastapi_mvc.cli.commands.run.os.path.isfile", return_value=False)
@mock.patch("fastapi_mvc.cli.commands.run.os.path.exists", return_value=True)
def test_run_not_ini_file(exists_mck, isfile_mck, cli_runner):
    result = cli_runner.invoke(run, [])
    assert result.exit_code == 1

    exists_mck.assert_called_once()
    isfile_mck.assert_called_once()


@mock.patch("fastapi_mvc.cli.commands.run.os.access", return_value=False)
@mock.patch("fastapi_mvc.cli.commands.run.os.path.isfile", return_value=True)
@mock.patch("fastapi_mvc.cli.commands.run.os.path.exists", return_value=True)
def test_run_not_ini_file(exists_mck, isfile_mck, access_mck, cli_runner):
    result = cli_runner.invoke(run, [])
    assert result.exit_code == 1

    exists_mck.assert_called_once()
    isfile_mck.assert_called_once()
    access_mck.assert_called_once()