# coding:utf-8
import os
from PySide6.QtCore import Qt, Signal, QSize, QPoint, QRect, QUrl
from PySide6.QtWidgets import QWidget, QHBoxLayout

from qfluentwidgets import (IconWidget, BodyLabel, FluentIcon, InfoBarIcon, ComboBox,
                            PrimaryPushButton, LineEdit, GroupHeaderCardWidget, PushButton,
                            CompactSpinBox, SwitchButton, IndicatorPosition, PlainTextEdit)

from ..common.icon import Logo
from ..common.config import cfg
from ..service.m3u8dl_service import M3U8DLCommand


class M3U8GroupHeaderCardWidget(GroupHeaderCardWidget):

    def addSwitchOption(self, icon, title, content, config: M3U8DLCommand, checked=False):
        button = SwitchButton(self.tr("Off"), self, IndicatorPosition.RIGHT)
        button.setOnText(self.tr("On"))
        button.setOffText(self.tr("Off"))
        button.setProperty("config", config)
        button.setChecked(checked)

        self.addGroup(icon, title, content, button)
        return button


class BasicConfigCard(GroupHeaderCardWidget):
    """ Basic config card """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle(self.tr("Basic Settings"))

        self.urlLineEdit = LineEdit()
        self.fileNameLineEdit = LineEdit()
        self.saveFolderButton = PushButton(self.tr("Choose"))
        self.threadCountSpinBox = CompactSpinBox()
        self.retryCountSpinBox = CompactSpinBox()

        self.hintIcon = IconWidget(InfoBarIcon.INFORMATION, self)
        self.hintLabel = BodyLabel(
            self.tr("Click the download button to start downloading") + ' 👉')
        self.downloadButton = PrimaryPushButton(
            self.tr("Download"), self, FluentIcon.PLAY_SOLID)

        self.toolBarLayout = QHBoxLayout()

        self.__initWidgets()

    def __initWidgets(self):
        self.hintIcon.setFixedSize(16, 16)
        self.setBorderRadius(8)

        self.urlLineEdit.setFixedWidth(300)
        self.fileNameLineEdit.setFixedWidth(300)
        self.saveFolderButton.setFixedWidth(120)
        self.threadCountSpinBox.setFixedWidth(120)
        self.retryCountSpinBox.setFixedWidth(120)

        self.urlLineEdit.setClearButtonEnabled(True)
        self.fileNameLineEdit.setClearButtonEnabled(True)

        self.urlLineEdit.setPlaceholderText(self.tr("Please enter the url of m3u8 file"))
        self.fileNameLineEdit.setPlaceholderText(self.tr("Please enter the name of downloaded file"))

        self.threadCountSpinBox.setRange(1, 1000)
        self.threadCountSpinBox.setValue(os.cpu_count())

        self.retryCountSpinBox.setRange(1, 1000)
        self.retryCountSpinBox.setValue(3)

        self.__initLayout()
        self.__connectSignalToSlot()

    def __initLayout(self):
        # add widget to group
        self.addGroup(
            icon=Logo.GLOBE,
            title=self.tr("Download URL"),
            content=self.tr("The URL of m3u8 file"),
            widget=self.urlLineEdit
        )
        self.addGroup(
            icon=Logo.FILM,
            title=self.tr("File Name"),
            content=self.tr("The name of downloaded file"),
            widget=self.fileNameLineEdit
        )
        self.saveFolderGroup = self.addGroup(
            icon=Logo.FOLDER,
            title=self.tr("Save Folder"),
            content=cfg.get(cfg.saveFolder),
            widget=self.saveFolderButton
        )
        self.addGroup(
            icon=Logo.KNOT,
            title=self.tr("Download Threads"),
            content=self.tr("Set the number of concurrent download threads"),
            widget=self.threadCountSpinBox
        )
        group = self.addGroup(
            icon=Logo.JOYSTICK,
            title=self.tr("Retry Count"),
            content=self.tr(
                "Set the retry count for each shard download exception"),
            widget=self.retryCountSpinBox
        )
        group.setSeparatorVisible(True)

        # add widgets to bottom toolbar
        self.toolBarLayout.setContentsMargins(24, 15, 24, 20)
        self.toolBarLayout.setSpacing(10)
        self.toolBarLayout.addWidget(
            self.hintIcon, 0, Qt.AlignmentFlag.AlignLeft)
        self.toolBarLayout.addWidget(
            self.hintLabel, 0, Qt.AlignmentFlag.AlignLeft)
        self.toolBarLayout.addStretch(1)
        self.toolBarLayout.addWidget(
            self.downloadButton, 0, Qt.AlignmentFlag.AlignRight)
        self.toolBarLayout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        self.vBoxLayout.addLayout(self.toolBarLayout)

    def __connectSignalToSlot(self):
        pass

    def parseOptions(self):
        """ Returns the m3u8dl options """
        options = [
            self.urlLineEdit.text(),
            M3U8DLCommand.SAVE_NAME.command(self.fileNameLineEdit.text()),
            M3U8DLCommand.SAVE_DIR.command(self.saveFolderGroup.content()),
            M3U8DLCommand.THREAD_COUNT.command(self.threadCountSpinBox.value()),
            M3U8DLCommand.DOWNLOAD_RETRY_COUNT.command(self.retryCountSpinBox.value()),
        ]
        return options


class AdvanceConfigCard(M3U8GroupHeaderCardWidget):
    """ Advance config card """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle(self.tr("Advance Settings"))

        self.httpTimeoutSpinBox = CompactSpinBox()
        self.httpHeaderEdit = PlainTextEdit()
        self.speedSpinBox = CompactSpinBox()
        self.speedComboBox = ComboBox()
        self.subtitleComboBox = ComboBox()

        self.__initWidgets()

    def __initWidgets(self):
        self.setBorderRadius(8)

        self.httpTimeoutSpinBox.setRange(5, 100000)
        self.httpTimeoutSpinBox.setValue(100)
        self.httpTimeoutSpinBox.setFixedWidth(120)

        self.httpHeaderEdit.setFixedSize(300, 56)
        self.httpHeaderEdit.setPlaceholderText("User-Agent: iOS\nCookie: mycookie")

        self.speedSpinBox.setRange(-1, 1000000000)
        self.speedSpinBox.setValue(-1)
        self.speedComboBox.addItems(["Mbps", "Kbps"])

        self.subtitleComboBox.setFixedWidth(120)
        self.subtitleComboBox.addItems(["SRT", "VTT"])

        self.__initLayout()

    def __initLayout(self):
        self.addGroup(
            icon=Logo.COOKIE,
            title=self.tr("Header"),
            content=self.tr("Set custom headers for HTTP requests"),
            widget=self.httpHeaderEdit
        )

        speedGroup = self.addGroup(
            icon=Logo.ROCKET,
            title=self.tr("Max Speed"),
            content=self.tr("Set maximum download speed, -1 indicates no speed limit"),
            widget=self.speedSpinBox
        )
        speedGroup.addWidget(self.speedComboBox)

        self.addGroup(
            icon=Logo.HOURGLASS,
            title=self.tr("Request Timeout"),
            content=self.tr("Set timeout for HTTP requests (in seconds)"),
            widget=self.httpTimeoutSpinBox
        )

        self.addGroup(
            icon=Logo.SCROLL,
            title=self.tr("Subtitle Format"),
            content=self.tr("Set the output type of subtitle"),
            widget=self.subtitleComboBox
        )

        self.addSwitchOption(
            icon=Logo.ALEMBIC,
            title=self.tr("Auto Select"),
            content=self.tr("Automatically select the best track of all types"),
            config=M3U8DLCommand.AUTO_SELECT,
        )
        self.addSwitchOption(
            icon=Logo.CARD_FILE_BOX,
            title=self.tr("Binary Merge"),
            content=self.tr("Merge ts files directly through binary copy connections"),
            config=M3U8DLCommand.BINARY_MERGE
        )
        self.addSwitchOption(
            icon=Logo.WASTEBASKET,
            title=self.tr("Delete After Done"),
            content=self.tr("Delete temporary files after downloading is complete"),
            config=M3U8DLCommand.DEL_AFTER_DONE,
            checked=True
        )
        self.addSwitchOption(
            icon=Logo.LINK,
            title=self.tr("Append URL Params"),
            content=self.tr("Adding the Params of the input URL to the shard"),
            config=M3U8DLCommand.APPEND_URL_PARAMS,
        )
        self.addSwitchOption(
            icon=Logo.CALENDAR,
            title=self.tr("Date Info"),
            content=self.tr("Do not write date information when mixing"),
            config=M3U8DLCommand.NO_DATE_INFO,
        )
        self.addSwitchOption(
            icon=Logo.INBOX,
            title=self.tr("Concurrent"),
            content=self.tr("Concurrent download of selected audio, video, and subtitles"),
            config=M3U8DLCommand.CONCURRENT_DOWNLOAD,
        )

    def parseOptions(self):
        """ Returns the m3u8dl options """
        options = [
            M3U8DLCommand.HTTP_REQUEST_TIMEOUT.command(self.httpTimeoutSpinBox.value()),
            M3U8DLCommand.SUB_FORMAT.command(self.subtitleComboBox.currentText()),
        ]

        if self.httpHeaderEdit.toPlainText():
            options.append(M3U8DLCommand.HEADER.command(self.httpHeaderEdit.toPlainText()))

        if self.speedSpinBox.value() > 0:
            speed = str(self.speedSpinBox.value()) + self.speedComboBox.currentText()
            options.append(M3U8DLCommand.MAX_SPEED.command(speed))

        for button in self.findChildren(SwitchButton):
            config = button.property("config")
            if config:
                options.append(config.command(button.isChecked()))

        return options


class ProxyConfigCard(M3U8GroupHeaderCardWidget):
    """ Proxy config card """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle(self.tr("Proxy Settings"))

        self.proxyLineEdit = LineEdit()

        self.__initWidgets()

    def __initWidgets(self):
        self.setBorderRadius(8)

        self.proxyLineEdit.setFixedWidth(300)
        self.proxyLineEdit.setPlaceholderText("http://127.0.0.1:8080")
        self.proxyLineEdit.setEnabled(False)

        self.__initLayout()
        self.__connectSignalToSlot()

    def __initLayout(self):
        self.systemProxyButton = self.addSwitchOption(
            icon=Logo.PLANET,
            title=self.tr("System Proxy"),
            content=self.tr("Use system default proxy"),
            config=M3U8DLCommand.USE_SYSTEM_PROXY,
            checked=True
        )
        self.addGroup(
            icon=Logo.AIRPLANE,
            title=self.tr("Custom Proxy"),
            content=self.tr("Set the http request proxy to be used"),
            widget=self.proxyLineEdit
        )

    def __connectSignalToSlot(self):
        self.systemProxyButton.checkedChanged.connect(self.proxyLineEdit.setDisabled)

    def parseOptions(self):
        """ Returns the m3u8dl options """
        if self.systemProxyButton.isChecked():
            return []

        options = [M3U8DLCommand.USE_SYSTEM_PROXY.command(False)]

        if self.proxyLineEdit.text():
            options.append(M3U8DLCommand.CUSTOM_PROXY.command(self.proxyLineEdit.text()))

        return options
