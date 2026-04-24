from typing import TYPE_CHECKING

import pytest
from syrupy.assertion import SnapshotAssertion

if TYPE_CHECKING:
    from tests.conftest import DelegatorFactory


def test_simple_multiline(
    monkeypatch: pytest.MonkeyPatch,
    delegator: 'DelegatorFactory',
    snapshot: SnapshotAssertion,
) -> None:
    """Check that cli works with simple multiline inputs."""
    monkeypatch.setenv('MULTILINE_VALUE', '1\n2\n3')

    variables = delegator('dump-env -p MULTILINE_')
    assert variables == snapshot
