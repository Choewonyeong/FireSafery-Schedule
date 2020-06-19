from PyQt5.QtWidgets import QApplication
from component.main.Loading import Loading
from component.dialog.DialogMassage import DialogMassage
from sys import argv


def run():
    app = QApplication(argv)
    try:
        from component.main.Login import Login
        loading = Loading()
        login = Login(app)
        login.show()
        loading.finish(login)
        app.exec_()
    except Exception as e:
        DialogMassage(f'접근 권한이 없습니다.\n개발자에게 문의바랍니다.\n\n○ Error : {e}')
        app.quit()


if __name__ == "__main__":
    run()
