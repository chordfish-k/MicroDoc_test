from PySide6.QtWidgets import QLineEdit, QHBoxLayout, QPushButton, QSizePolicy
from PySide6.QtCore import QRegularExpression, Signal, Qt
from PySide6.QtGui import QRegularExpressionValidator
import math
from src.components import MyQWidget
from src.util.share import ObjectManager


class PaginationWidget(MyQWidget):
    window = None
    edCurrentPage: QLineEdit = None
    lyBeforePages: QHBoxLayout = None
    lyAfterPages: QHBoxLayout = None
    btnPrevPage: QPushButton = None
    btnNextPage: QPushButton = None

    listSize: int = 4  # 左右两侧最多的页码按钮数

    pageSize: int = 10
    pageCount: int = 1
    total: int = 0
    currentPage: int = 1

    changed = Signal(int)

    def __init__(self):
        self.window = ObjectManager.get("window")
        super().__init__(name="pagination")

    def initComponents(self):
        self.edCurrentPage.editingFinished.connect(self.__textEdited)

        rx = QRegularExpression("[0-9]+$")
        validator = QRegularExpressionValidator(rx, self)
        self.edCurrentPage.setValidator(validator)

        self.lyBeforePages.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.lyAfterPages.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.btnNextPage.clicked.connect(self.toNext)
        self.btnPrevPage.clicked.connect(self.toPrev)

    def setPageParms(self, **kwargs):
        """
        kwargs:
            pageSize    :int 每页的数据条数
            pageCount   :int 总页数
            total       :int 总数据数，与pageCount同时存在时以pageCount为准
        """
        pageSize = kwargs.get("pageSize")
        pageCount = kwargs.get("pageCount")
        total = kwargs.get("total")

        self.pageSize = pageSize if pageSize else self.pageSize
        self.pageCount = pageCount if pageCount else self.pageCount
        self.total = total if total else self.total

        if not pageCount and total:
            self.pageCount = math.ceil(self.total / self.pageSize)

        self.__refreshBtns()

    def toPrev(self):
        if self.currentPage > 1:
            self.currentPage -= 1
        self.__refreshBtns()
        self.changed.emit(self.currentPage)

    def toNext(self):
        if self.currentPage < self.pageCount:
            self.currentPage += 1
        self.__refreshBtns()
        self.changed.emit(self.currentPage)

    def to(self, page: int):
        if 1 <= page <= self.pageCount:
            self.currentPage = page
        self.__refreshBtns()
        self.changed.emit(self.currentPage)

    def __refreshBtns(self):
        # 清除原有的按钮
        bp = self.lyBeforePages
        ap = self.lyAfterPages
        for i in range(bp.count()):
            bp.itemAt(i).widget().deleteLater()
        for i in range(ap.count()):
            ap.itemAt(i).widget().deleteLater()

        # 1 < k < currentPage
        page = self.currentPage
        if page > 1:
            st = 1 if page <= self.listSize else page - self.listSize
            for k in range(st, page):
                self.__addPageBtn(k, True)

        if page < self.pageCount:
            ed = self.pageCount + 1 if self.pageCount + 1 <= self.listSize + page else page + self.listSize + 1
            for k in range(page + 1, ed):
                self.__addPageBtn(k, False)

        self.edCurrentPage.setText(str(page))

    def __addPageBtn(self, page: int, isPrev: bool = True):
        ly = self.lyBeforePages if isPrev else self.lyAfterPages
        btn = QPushButton(self)
        btn.setMaximumWidth(50)
        btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Ignored)
        btn.setText("{}".format(page))

        def func(pageNo: int):
            def wrapper():
                self.to(pageNo)

            return wrapper

        btn.clicked.connect(func(page))

        ly.addWidget(btn)

    def __textEdited(self):
        page = self.edCurrentPage.text()
        if page == "":
            self.edCurrentPage.setText(str(self.currentPage))
            return
        page = int(page)
        if 1 > page > self.pageCount:
            self.edCurrentPage.setText(str(self.currentPage))
            return

        self.to(page)
