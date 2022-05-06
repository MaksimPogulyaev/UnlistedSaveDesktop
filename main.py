import os
import sys

import requests
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QListWidgetItem

import design
import login

HOST = 'https://test.rvtsk.xyz'  # Адрес сервера


class CustomListItemQWidget(QWidget):
    """
    Кастомный виджет для отображения элементов в списке
    """

    def __init__(self, parent=None):
        super(CustomListItemQWidget, self).__init__(parent)
        self.save_name = QLabel("")
        self.save_id = QLabel("id")
        layout = QHBoxLayout()
        layout.addWidget(self.save_name)
        layout.addWidget(self.save_id)
        self.setLayout(layout)


class LoginForm(QtWidgets.QDialog, login.Ui_LoginForm):
    """
    Окно с формой для входа
    """

    def __init__(self):
        """
            TODO Создание окна
            FIXME пароль не скрыт
        """
        super().__init__()
        self.setupUi(self)
        self.login_btn.clicked.connect(self.close)

    def login(self):
        """
            TODO Функция входа
        """
        return self.pass_edit


class USApp(QtWidgets.QMainWindow, design.Ui_MainWindow):
    """
    Главное окно приложения
    """
    selected_item = "-1"
    user = ""
    password = ""

    def __init__(self):
        """
        Создание окна
        """
        super().__init__()
        self.setupUi(self)
        self.reload_btn.clicked.connect(self.get_saves_list)
        self.listWidget.itemClicked.connect(self.item_clicked_event)
        self.download_btn.clicked.connect(self.download)
        self.upload_btn.clicked.connect(self.upload)
        self.exit.triggered.connect(self.close)
        self.log_in.triggered.connect(self.login)

    def item_clicked_event(self, item):
        """
        Функция получения имени текущего выбранного сохранения
        """
        self.selected_item = item.text()

    def get_saves_list(self):
        """
        Функция получения списка сохранений с сервера
        """
        self.listWidget.clear()
        url = "{}/getfiles".format(HOST)
        resp = requests.get(
            url,
            headers={'Content-Type': 'application/json',
                     'x-access-tokens': f'{self.get_token()}'}
        )  # делаем запрос TODO проверка полученного ответа
        json = resp.json()
        files = json['files']
        for file_name in files:  # для каждого файла в полученном списке
            item = QListWidgetItem(self.listWidget)
            item_widget = CustomListItemQWidget()
            item.setSizeHint(item_widget.sizeHint())
            item.setText(file_name)
            self.listWidget.addItem(item)
            self.listWidget.setItemWidget(item, item_widget)

    def download(self):
        """
        Функция загрузки файла с сервера
        """
        file = self.selected_item
        url = "{}/uploads/{}".format(HOST, file)
        resp = requests.get(
            url,
            headers={'Content-Type': 'application/json',
                     'x-access-tokens': f'{self.get_token()}'}
        )  # делаем запрос TODO проверка полученного ответа
        path = f'./outputfiles/{file}'  # путь куда загружаются файлы
        if resp.status_code == 500:  # FIXME : возвращая файл сервер возвращает код 500 (?) нужна проверка
            f = open(path, "wb")  # открываем файл для записи, в режиме wb
            f.write(resp.content)  # записываем содержимое в файл
            f.close()
        QtWidgets.QMessageBox.question(
            self,
            "Downloader",
            "Downloaded: {}".format(str(os.path.exists(path))),
            QtWidgets.QMessageBox.Ok,
            QtWidgets.QMessageBox.Ok
        )  # Вызов диалога с сообщением о состоянии загрузки
        self.selected_item = "-1"

    def upload(self):
        """
        TODO : Функция выгрузки файла на сервер
        """
        QtWidgets.QMessageBox.question(
            self,
            "Uploader",
            "Coming {}".format(str('soon')),
            QtWidgets.QMessageBox.Ok,
            QtWidgets.QMessageBox.Ok
        )

    def login(self):
        """
        Функция входа
        """
        self.login_form = LoginForm()
        self.login_form.open()
        self.user = "user"  # HACK тестовое значение
        self.password = "password"  # HACK тестовое значение

    def get_token(self):
        """
        Функция получения токена для доступа к серверу без пароля
        """
        url = "{}/login".format(HOST)
        resp = requests.get(
            url,
            auth=(self.user, self.password)
        )  # делаем запрос FIXME исправить многократный запрос
        json = resp.json()
        return json['token']


def main():
    """
    Функция вызова
    """
    app = QtWidgets.QApplication(sys.argv)
    window = USApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()


if __name__ == '__main__':
    main()
