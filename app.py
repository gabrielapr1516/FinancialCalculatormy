import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication

from ui.main_window import MainWindow


def main() -> int:
    # Habilita escalado automático según DPI del monitor
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)

    # Obtener geometría de la pantalla principal
    screen = app.primaryScreen()
    screen_geometry = screen.availableGeometry()
    dpi = screen.logicalDotsPerInch()

    window = MainWindow(screen_geometry=screen_geometry, screen_dpi=dpi)
    window.show()
    return app.exec_()


if __name__ == "__main__":
    raise SystemExit(main())
