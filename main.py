from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import (QApplication,
                             QMainWindow,
                             QLabel,
                             QTableWidget,
                             QTableWidgetItem,
                             QHeaderView
                             )
from PyQt6.QtCore import QSize
import discordbot
import asyncio

class QMainWindow(QtWidgets.QMainWindow):
    def resizeEvent(self, event):
        table.resize(window.size() - QSize(20, 50))
        QtWidgets.QMainWindow.resizeEvent(self, event)

app = QApplication([])
window = QMainWindow()
title = QLabel(window)
table = QTableWidget(window)

def add_table_row(guild_text : str, channel_text : str, username : str, message : str):
    row_num = table.rowCount()
    table.insertRow(row_num)
    table.setItem(row_num, 0, QTableWidgetItem(guild_text))
    table.setItem(row_num, 1, QTableWidgetItem(channel_text))
    table.setItem(row_num, 2, QTableWidgetItem(username))
    table.setItem(row_num, 3, QTableWidgetItem(message))

def load_mainwindow():
    window.setAttribute(QtCore.Qt.WidgetAttribute.WA_DeleteOnClose)
    window.setWindowTitle("Status Board")
    window.resize(800, 400)
    title.setText("Status Board")
    title.move(10, 5)
    header = table.horizontalHeader()
    header.hide()
    header.setStretchLastSection(True)
    header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
    table.verticalHeader().hide()
    table.setColumnCount(4)
    add_table_row("Guild", "Channel", "Username", "Message")
    table.resize(780, 350)
    table.move(10, 40)
    table.itemChanged.connect(table.scrollToBottom)
    with open("style.css", "r") as stylesheet:
        window.setStyleSheet(stylesheet.read())

def query_guild(guild_id : str, channel_id : str):
    for guild in discordbot.GUILDS:
        if guild["id"] != guild_id: continue
        guild_name = guild["name"]
        if "channels" not in guild: guild["channels"] = discordbot.get_guild_channels(guild_id)
        for channel in guild["channels"]:
            if channel["id"] != channel_id: continue
            channel_name = channel["name"]
            return guild_name, channel_name
        return guild_name, channel_id
    return guild_id, channel_id

def message_handler(message : dict):
    data = message["d"]
    if "guild_id" not in data.keys(): return
    guild_id = data["guild_id"]
    channel_id = data["channel_id"]
    username = data["author"]["username"]
    content = data["content"]
    guild_text, channel_text = query_guild(guild_id, channel_id)
    add_table_row(guild_text, channel_text, username, content)

async def main():
    worker = discordbot.DiscordWorker()
    worker.msg_events = [message_handler]
    worker.start()
    load_mainwindow()
    window.show()
    app.exec()

if __name__ == '__main__':
    asyncio.run(main())
