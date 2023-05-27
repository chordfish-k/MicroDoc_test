from PySide6.QtWidgets import QApplication
from views import main_window
from util.settings import Settings
import sys, os



os.environ["QT_FONT_DPI"] = "96" 
settings = Settings()
settings.setItemIfNone('theme', "dark")
settings.setItemIfNone('last_dir_path', "")
settings.setItemIfNone('camera_flipX', "True")
settings.setItemIfNone('camera_output', "True")
settings.setItemIfNone('min_accepted_probability', "0.4")
settings.setItemIfNone('use_gpu', "False")
settings.setItemIfNone('output_duration', "4")
settings.save()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myapp = main_window.MyApp(settings)
    myapp.show()
    sys.exit(app.exec())