#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ================================================== #
# This file is a part of PYGPT package               #
# Website: https://pygpt.net                         #
# GitHub:  https://github.com/szczyglis-dev/py-gpt   #
# MIT License                                        #
# Created By  : Marcin Szczygliński                  #
# Updated Date: 2023.12.22 18:00:00                  #
# ================================================== #

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QTextBrowser

from ....utils import trans


class ChatOutput(QTextBrowser):
    def __init__(self, window=None):
        """
        Chat output

        :param window: main window
        """
        super(ChatOutput, self).__init__(window)
        self.window = window
        self.setReadOnly(True)
        self.setStyleSheet(self.window.controller.theme.get_style('chat_output'))
        self.value = self.window.config.data['font_size']
        self.max_font_size = 42
        self.min_font_size = 8

    def contextMenuEvent(self, event):
        menu = self.createStandardContextMenu()

        selected_text = self.textCursor().selectedText()
        if selected_text:
            action = menu.addAction(trans('text.context_menu.audio.read'))
            action.triggered.connect(self.audio_read_selection)
        menu.exec_(event.globalPos())

    def audio_read_selection(self):
        """
        Read selected text (audio)
        """
        self.window.controller.output.speech_selected_text(self.textCursor().selectedText())

    def wheelEvent(self, event):
        """
        Wheel event: set font size
        :param event: Event
        """
        if event.modifiers() & Qt.ControlModifier:
            if event.angleDelta().y() > 0:
                if self.value < self.max_font_size:
                    self.value += 1
            else:
                if self.value > self.min_font_size:
                    self.value -= 1

            self.window.config.data['font_size'] = self.value
            self.window.config.save()
            self.window.controller.settings.update_font_size()
            event.accept()
        else:
            super(ChatOutput, self).wheelEvent(event)
