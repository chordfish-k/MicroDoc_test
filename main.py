from PySide6.QtWidgets import QApplication
from views import main_window
from util.settings import settings
import sys, os

os.environ["QT_FONT_DPI"] = "96" 
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myapp = main_window.MyApp(settings)
    myapp.show()
    sys.exit(app.exec())