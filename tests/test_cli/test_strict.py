from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from tests.conftest import DelegatorFactory


@pytest.mark.parametrize(
    'strict_options',
    [
        '--strict=SOME_TT_KEY',
        '--strict=SOME_TT_KEY --strict=SOME_TT_VALUE',
    ],
)
def test_strict_vars(
    monkeypatch: pytest.MonkeyPatch,
    delegator: 'DelegatorFactory',
    strict_options: str,
) -> None:
    """Check that cli works correctly with strict vars."""
    monkeypatch.setenv('SOME_TT_VALUE', '1')
    monkeypatch.setenv('SOME_TT_KEY', '2')

    variables = delegator(f'dump-env -p SOME_TT_ {strict_options}')
    assert variables == 'KEY=2\nVALUE=1\n'


def test_strict_missing_vars1(delegator: 'DelegatorFactory') -> None:
    """Check that cli raises errors for missing strict keys."""
    variables = delegator('dump-env -p SOME_TT_ --strict=SOME_TT_KEY')
    assert variables == (1, 'Missing env vars: SOME_TT_KEY\n')


def test_strict_missing_vars2(delegator: 'DelegatorFactory') -> None:
    """Check that cli raises errors for missing strict keys."""
    variables = delegator(
        'dump-env -p SOME_TT_ --strict=SOME_TT_KEY --strict=SOME_TT_VALUE',
    )
    assert variables[0] == 1
    variables_err = variables[1]
    assert 'SOME_TT_VALUE' in variables_err
    assert 'SOME_TT_KEY' in variables_err
