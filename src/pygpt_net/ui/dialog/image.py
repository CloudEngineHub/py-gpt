#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ================================================== #
# This file is a part of PYGPT package               #
# Website: https://pygpt.net                         #
# GitHub:  https://github.com/szczyglis-dev/py-gpt   #
# MIT License                                        #
# Created By  : Marcin Szczygliński                  #
# Updated Date: 2024.03.20 06:00:00                  #
# ================================================== #

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QCheckBox, QSizePolicy, QMenuBar

from pygpt_net.ui.widget.dialog.image import ImageDialog
from pygpt_net.ui.widget.image.display import ImageLabel
from pygpt_net.utils import trans


class Image:
    def __init__(self, window=None):
        """
        Image dialog

        :param window: Window instance
        """
        self.window = window
        self.path = None

    def setup(self):
        """Setup image dialog"""
        id = 'image'
        self.window.ui.nodes['dialog.image.pixmap'] = {}

        for i in range(0, 4):
            self.window.ui.nodes['dialog.image.pixmap'][i] = ImageLabel(self.window, self.path)
            self.window.ui.nodes['dialog.image.pixmap'][i].setMaximumSize(512, 512)

        row_one = QHBoxLayout()
        row_one.addWidget(self.window.ui.nodes['dialog.image.pixmap'][0])
        row_one.addWidget(self.window.ui.nodes['dialog.image.pixmap'][1])

        row_two = QHBoxLayout()
        row_two.addWidget(self.window.ui.nodes['dialog.image.pixmap'][2])
        row_two.addWidget(self.window.ui.nodes['dialog.image.pixmap'][3])

        state = False
        if self.window.core.config.has('img_dialog_open'):
            state = bool(self.window.core.config.get('img_dialog_open'))
        self.window.ui.nodes['dialog.image.open.toggle'] = QCheckBox(trans('settings.img_dialog_open'), self.window)
        self.window.ui.nodes['dialog.image.open.toggle'].setChecked(state)
        self.window.ui.nodes['dialog.image.open.toggle'].clicked.connect(
            lambda: self.toggle_dialog_auto_open())

        layout = QVBoxLayout()
        layout.addLayout(row_one)
        layout.addLayout(row_two)
        layout.addWidget(self.window.ui.nodes['dialog.image.open.toggle'])

        self.window.ui.dialog[id] = ImageDialog(self.window, id)
        self.window.ui.dialog[id].setLayout(layout)
        self.window.ui.dialog[id].setWindowTitle(trans("dialog.image.title"))

    def toggle_dialog_auto_open(self):
        """Toggle dialog auto open"""
        if self.window.ui.nodes['dialog.image.open.toggle'].isChecked():
            value = True
        else:
            value = False
        self.window.core.config.set('img_dialog_open', value)

        # update checkbox in config dialog
        self.window.controller.config.checkbox.apply('config', 'img_dialog_open', {'value': value})


class ImagePreview:
    def __init__(self, window=None):
        """
        Image preview dialog

        :param window: Window instance
        """
        self.window = window
        self.path = None
        self.id = 'image_preview'

    def setup_menu(self) -> QMenuBar:
        """Setup dialog menu"""
        self.menu_bar = QMenuBar()
        self.file_menu = self.menu_bar.addMenu(trans("menu.file"))
        self.actions = {}

        # open
        self.actions["open"] = QAction(QIcon(":/icons/folder.svg"), trans("action.open"))
        self.actions["open"].triggered.connect(self.window.tools.viewer.open_file)

        # save as
        self.actions["save_as"] = QAction(QIcon(":/icons/save.svg"), trans("action.save_as"))
        self.actions["save_as"].triggered.connect(
            lambda: self.window.tools.viewer.save(self.window.ui.nodes['dialog.image.preview.pixmap'].path)
        )

        # exit
        self.actions["exit"] = QAction(QIcon(":/icons/logout.svg"), trans("menu.file.exit"))
        self.actions["exit"].triggered.connect(self.window.tools.viewer.close_preview)

        # add actions
        self.file_menu.addAction(self.actions["open"])
        self.file_menu.addAction(self.actions["save_as"])
        self.file_menu.addAction(self.actions["exit"])
        return self.menu_bar

    def setup(self):
        """Setup image dialog"""
        self.window.ui.nodes['dialog.image.preview.pixmap.source'] = ImageLabel(self.window, self.path)
        self.window.ui.nodes['dialog.image.preview.pixmap.source'].setVisible(False)
        self.window.ui.nodes['dialog.image.preview.pixmap'] = ImageLabel(self.window, self.path)

        row = QHBoxLayout()
        row.addWidget(self.window.ui.nodes['dialog.image.preview.pixmap'])

        sizePolicy = QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.window.ui.nodes['dialog.image.preview.pixmap'].setSizePolicy(sizePolicy)

        layout = QVBoxLayout()
        layout.setMenuBar(self.setup_menu())
        layout.addLayout(row)

        self.window.ui.dialog[self.id] = ImageDialog(self.window, self.id)
        self.window.ui.dialog[self.id].setLayout(layout)
        self.window.ui.dialog[self.id].resizeEvent = self.onResizeEvent  # resize event to adjust the pixmap

    def onResizeEvent(self, event):
        """
        Resize event to adjust the pixmap on window resizing

        :param event: resize event
        """
        source = self.window.ui.nodes['dialog.image.preview.pixmap.source']
        label = self.window.ui.nodes['dialog.image.preview.pixmap']
        if source.pixmap() and not source.pixmap().isNull():
            label.setPixmap(source.pixmap().scaled(label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        super(ImageDialog, self.window.ui.dialog[self.id]).resizeEvent(event)
