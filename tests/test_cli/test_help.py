from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from tests.conftest import DelegatorFactory


def test_help_option(delegator: 'DelegatorFactory') -> None:
    """Check that cli shows help."""
    variables = delegator('dump-env --help')
    assert 'show this help message and exit' in variables
    assert '--template TEMPLATE' in variables
    assert '--prefix PREFIX' in variables
    assert '--strict' in variables
    assert '--no-quote-values' in variables
