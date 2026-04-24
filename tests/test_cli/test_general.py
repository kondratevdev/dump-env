from pathlib import Path
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from tests.conftest import DelegatorFactory

import pytest


def test_simple_usage(
    monkeypatch: pytest.MonkeyPatch,
    delegator: 'DelegatorFactory',
) -> None:
    """Check that cli shows prefixed variables."""
    monkeypatch.setenv('SOME_TT_VALUE', '1')

    variables = delegator('dump-env -p SOME_TT_')
    assert variables == 'VALUE=1\n'


def test_both_options(
    monkeypatch: pytest.MonkeyPatch,
    env_file: str,
    delegator: 'DelegatorFactory',
) -> None:
    """
    Check with template and prefix.

    CLI must show all prefixed variables by template.
    """
    monkeypatch.setenv('SOME_TT_VALUE', '1')

    variables = delegator(f'dump-env -p SOME_TT_ -t {env_file}')
    assert variables == 'NORMAL_KEY=SOMEVALUE\nVALUE=1\n'


def test_multiple_prefixes(
    monkeypatch: pytest.MonkeyPatch,
    delegator: 'DelegatorFactory',
) -> None:
    """
    Check that CLI with multiple prefixes.

    CLI must show all prefixed variables correctly.
    """
    monkeypatch.setenv('SOME_TT_VALUE', '1')
    monkeypatch.setenv('ANOTHER_TT_VALUE', '2')

    variables = delegator('dump-env -p SOME_TT_ -p ANOTHER_TT_')
    assert variables == 'VALUE=2\n'


def test_simple_usage_file_output(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    delegator: 'DelegatorFactory',
) -> None:
    """Check that CLI puts prefixed variables into file correctly."""
    monkeypatch.setenv('SOME_TT_VALUE', '1')

    output_dir = tmp_path / 'tests'
    output_dir.mkdir()
    env_file = output_dir / '.env'

    delegator(f'dump-env -p SOME_TT_ > {env_file}')
    assert env_file.read_text(encoding='utf-8') == 'VALUE=1\n'


@pytest.mark.parametrize(
    ('command', 'expected'),
    [
        ('dump-env -p SOM_TT_', 'VALUE="first second"\n'),
        ('dump-env -p SOM_TT_ --no-quote-values', 'VALUE=first second\n'),
    ],
)
def test_quote_values_option(
    monkeypatch: pytest.MonkeyPatch,
    delegator: 'DelegatorFactory',
    *,
    command: str,
    expected: str,
) -> None:
    """Check that cli quotes values depending on the selected option."""
    monkeypatch.setenv('SOM_TT_VALUE', 'first second')

    variables = delegator(command)
    assert variables == expected


def test_no_quote_values_file_output(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    delegator: 'DelegatorFactory',
) -> None:
    """Check that cli puts unquoted values into file correctly."""
    monkeypatch.setenv('SOM_TT_VALUE', 'first second')

    output_dir = tmp_path / 'tests'
    output_dir.mkdir()
    env_file = output_dir / '.env'

    delegator(f'dump-env -p SOM_TT_ --no-quote-values > {env_file}')
    assert env_file.read_text(encoding='utf-8') == 'VALUE=first second\n'
