import os
import sys
from contextlib import contextmanager
from typing import Optional
from unittest import mock

from golem_sci.chains import MAINNET

from golem.config.environments import ENVIRONMENT_VARIABLE
from golem.core.variables import PROTOCOL_CONST


@contextmanager
def mock_config(net: Optional[str] = None, patch_active: bool = True) -> None:

    protocol_const = mock.Mock(ID=PROTOCOL_CONST.ID,
                               NUM=PROTOCOL_CONST.NUM,
                               POSTFIX=PROTOCOL_CONST.POSTFIX)

    config_module_name = 'golem.config.active'
    config_module = mock.Mock()

    org_module = sys.modules[config_module_name]

    os_environ = dict(os.environ)
    os_environ.update({ENVIRONMENT_VARIABLE: net})

    sys_modules = dict(sys.modules)
    sys.modules.update({config_module_name: config_module})

    with mock.patch.dict('os.environ', os_environ):
        with mock.patch.dict('sys.modules', sys_modules):

            if patch_active:

                config_module.PROTOCOL_CONST = protocol_const

                if net == MAINNET:
                    from golem.config.environments import mainnet as module
                else:
                    from golem.config.environments import testnet as module

            else:

                module = org_module

            for name, value in module.__dict__.items():
                if name == 'PROTOCOL_CONST':
                    continue
                setattr(config_module, name, value)

            yield
