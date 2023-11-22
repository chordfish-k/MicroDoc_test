import resources_rc
from PySide6.QtWidgets import QApplication
from src.views import MyApp
from src.util.settings import settings
import sys, os

os.environ["QT_FONT_DPI"] = settings.get("qt_font_dpi") 
os.environ["CUDA_VISIBLE_DEVICES"] = settings.get("cuda_visble_devices")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myapp = MyApp()
    myapp.show()
    sys.exit(app.exec())