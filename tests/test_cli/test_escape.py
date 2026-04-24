import json
from typing import TYPE_CHECKING

import pytest
from syrupy.assertion import SnapshotAssertion

if TYPE_CHECKING:
    from tests.conftest import DelegatorFactory


def test_quote_escape(
    monkeypatch: pytest.MonkeyPatch,
    delegator: 'DelegatorFactory',
    snapshot: SnapshotAssertion,
) -> None:
    """Check that cli escapes."""
    multiline_value = {
        'key': 'value',
        'key2': 'multi\nline\nvalue',
    }
    monkeypatch.setenv('MULTILINE_VALUE', json.dumps(multiline_value, indent=4))

    variables = delegator('dump-env -p MULTILINE_')
    assert variables == snapshot
