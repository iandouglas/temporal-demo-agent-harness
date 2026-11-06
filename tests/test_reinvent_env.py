"""The booth's explicit empty auth values must produce an unauthenticated local client."""
import os
from unittest.mock import AsyncMock, patch
import pytest
from agent_harness_demo import config


@pytest.mark.asyncio
async def test_local_env_discards_empty_cloud_auth_without_cert_conflict():
    env = {'TEMPORAL_ADDRESS': '127.0.0.1:7233', 'TEMPORAL_NAMESPACE': 'default',
           'TEMPORAL_API_KEY': '', 'TEMPORAL_TLS': 'false',
           'TEMPORAL_TLS_CLIENT_CERT_PATH': '', 'TEMPORAL_TLS_CLIENT_CERT_DATA': '',
           'TEMPORAL_TLS_CLIENT_KEY_PATH': '', 'TEMPORAL_TLS_CLIENT_KEY_DATA': ''}
    with patch.dict(os.environ, env, clear=True), patch.object(config.Client, 'connect', new_callable=AsyncMock) as connect:
        await config.connect([])
    assert connect.call_args.kwargs['target_host'] == '127.0.0.1:7233'
    assert not connect.call_args.kwargs.get('api_key')
    assert not connect.call_args.kwargs.get('tls')
