#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ================================================== #
# This file is a part of PYGPT package               #
# Website: https://pygpt.net                         #
# GitHub:  https://github.com/szczyglis-dev/py-gpt   #
# MIT License                                        #
# Created By  : Marcin Szczygliński                  #
# Updated Date: 2024.05.01 17:00:00                  #
# ================================================== #

from unittest.mock import MagicMock

from tests.mocks import mock_window
from pygpt_net.controller.chat.output import Output
from pygpt_net.item.ctx import CtxItem


def test_handle(mock_window):
    """Test handle output"""
    output = Output(mock_window)
    output.handle_complete = MagicMock()

    ctx = CtxItem()
    output.handle(ctx, 'chat', stream_mode=False)

    mock_window.core.dispatcher.dispatch.assert_called_once()  # should dispatch event: ctx.after
    mock_window.controller.chat.render.append_output.assert_called_once_with(ctx)
    mock_window.controller.chat.render.append_extra.assert_called_once_with(ctx, True)
    output.handle_complete.assert_called_once_with(ctx)


def test_handle_complete(mock_window):
    """Test handle complete"""
    output = Output(mock_window)
    mock_window.core.config.data['mode'] = 'chat'
    mock_window.core.config.data['store_history'] = True
    mock_window.core.ctx.post_update = MagicMock()
    mock_window.core.ctx.store = MagicMock()
    mock_window.controller.ctx.update_ctx = MagicMock()
    mock_window.ui.status = MagicMock()

    ctx = CtxItem()
    output.handle_complete(ctx)

    mock_window.core.ctx.post_update.assert_called_once()
    mock_window.core.ctx.store.assert_called_once()
    mock_window.controller.ctx.update_ctx.assert_called_once()
    mock_window.ui.status.assert_called_once()


def test_handle_cmd(mock_window):
    """Test handle cmd: all commands"""
    output = Output(mock_window)
    mock_window.core.config.data['cmd'] = True  # enable all cmd execution
    mock_window.controller.plugins.apply_cmds = MagicMock()
    mock_window.controller.plugins.apply_cmds_inline = MagicMock()
    mock_window.ui.status = MagicMock()
    cmds = [
        {'cmd': 'cmd1', 'params': {'param1': 'value1'}},
        {'cmd': 'cmd2', 'params': {'param2': 'value2'}},
    ]
    mock_window.core.command.extract_cmds = MagicMock(return_value=cmds)
    mock_window.controller.agent.experts.enabled = MagicMock(return_value=False)

    ctx = CtxItem()
    output.handle_cmd(ctx)

    mock_window.controller.plugins.apply_cmds.assert_called_once()
    mock_window.controller.plugins.apply_cmds_inline.assert_not_called()
    mock_window.ui.status.assert_called_once()


def test_handle_cmd_only(mock_window):
    """Test handle cmd: only inline commands"""
    output = Output(mock_window)
    mock_window.core.config.data['cmd'] = False  # disable cmd execution, allow only 'inline' commands
    mock_window.controller.plugins.apply_cmds = MagicMock()
    mock_window.controller.plugins.apply_cmds_inline = MagicMock()
    mock_window.ui.status = MagicMock()
    cmds = [
        {'cmd': 'cmd1', 'params': {'param1': 'value1'}},
        {'cmd': 'cmd2', 'params': {'param2': 'value2'}},
    ]
    mock_window.core.command.extract_cmds = MagicMock(return_value=cmds)
    mock_window.controller.agent.experts.enabled = MagicMock(return_value=False)

    ctx = CtxItem()
    output.handle_cmd(ctx)

    mock_window.controller.plugins.apply_cmds_inline.assert_called_once()
    mock_window.controller.plugins.apply_cmds.assert_not_called()


def test_handle_cmd_no_cmds(mock_window):
    """Test handle cmd: empty commands"""
    output = Output(mock_window)
    mock_window.core.config.data['cmd'] = True  # enable all cmd execution
    mock_window.controller.plugins.apply_cmds = MagicMock()
    mock_window.controller.plugins.apply_cmds_inline = MagicMock()
    mock_window.ui.status = MagicMock()

    cmds = []
    mock_window.core.command.extract_cmds = MagicMock(return_value=cmds)

    ctx = CtxItem()
    output.handle_cmd(ctx)

    mock_window.controller.plugins.apply_cmds.assert_not_called()
    mock_window.controller.plugins.apply_cmds_inline.assert_not_called()
    mock_window.ui.status.assert_not_called()
