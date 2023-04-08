from PySide6.QtWidgets import QApplication
from views import main_window
from util.settings import Settings
import sys, os



os.environ["QT_FONT_DPI"] = "96" 

settings = Settings()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myapp = main_window.MyApp()
    myapp.show()
    sys.exit(app.exec())