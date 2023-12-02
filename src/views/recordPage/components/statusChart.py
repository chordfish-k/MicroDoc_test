from PySide6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis
from PySide6.QtGui import QColor, QPainter
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QPushButton, QMainWindow
from src.assets.assets_loader import Assets
from src.components import MyQWidget
from src.util.settings import settings
from src.util.share import ObjectManager


class StatusChartWidget(MyQWidget):
    window: QMainWindow = None
    chart: QChart = None
    btn: QPushButton = None
    duration = 1
    last = []
    output = Signal()

    def __init__(self):
        self.chartView = None
        self.y_Aix = None
        self.x_Aix = None
        self.series_3 = None
        self.series_2 = None
        self.series_1 = None
        self.x_data_length = None
        self.data_index = None
        self.window = ObjectManager.get("window")
        super().__init__()
        self.initCharts()
        self.setObjectName("StatusChart")
        self.setMinimumHeight(200)
        Assets.loadQss("my_chart", self)
        self.duration = settings.get("output_duration", int)

    def initCharts(self):
        # 图表初始化
        fontColor: QColor
        if settings.get("theme").startswith("light"):
            fontColor = QColor(0, 0, 0)
        else:
            fontColor = QColor(255, 255, 255)
        ### 表1
        # 创建折线视图
        self.data_index = 0
        self.x_data_length = 100

        self.chart = QChart()
        # self.chart.setAnimationOptions(QChart.AnimationOption.NoAnimation)

        self.chart.setBackgroundVisible(False)

        # 曲线
        self.series_1 = QLineSeries()
        self.series_1.setName("Negative")  # 设置曲线名称
        self.series_2 = QLineSeries()
        self.series_2.setName("Neutral")
        self.series_3 = QLineSeries()
        self.series_3.setName("Positive")

        # 坐标轴
        self.x_Aix = QValueAxis()
        self.x_Aix.setRange(0.00, self.x_data_length)
        self.x_Aix.setGridLineVisible(False)
        self.x_Aix.setMinorGridLineVisible(False)  # 隐藏参考线
        self.x_Aix.setLabelFormat("%u")
        self.x_Aix.setTickCount(6)  # 5+1
        self.x_Aix.setMinorTickCount(1)
        self.x_Aix.setLabelsColor(fontColor)
        self.x_Aix.setLinePenColor(fontColor)
        self.x_Aix.setGridLineColor(fontColor)

        self.y_Aix = QValueAxis()
        self.y_Aix.setRange(0.00, 1.00)
        self.y_Aix.setGridLineVisible(False)  # 隐藏参考线
        self.y_Aix.setMinorGridLineVisible(False)
        self.y_Aix.setTickCount(5)
        self.y_Aix.setLabelsColor(fontColor)
        self.y_Aix.setLinePenColor(fontColor)
        self.y_Aix.setGridLineColor(fontColor)

        # 画坐标轴
        self.chart.addAxis(self.x_Aix, Qt.AlignmentFlag.AlignBottom)
        self.chart.addAxis(self.y_Aix, Qt.AlignmentFlag.AlignLeft)
        # 画线
        self.chart.addSeries(self.series_1)
        self.chart.addSeries(self.series_2)
        self.chart.addSeries(self.series_3)
        # 把曲线关联到坐标轴
        self.series_1.attachAxis(self.x_Aix)
        self.series_1.attachAxis(self.y_Aix)
        self.series_2.attachAxis(self.x_Aix)
        self.series_2.attachAxis(self.y_Aix)
        self.series_3.attachAxis(self.x_Aix)
        self.series_3.attachAxis(self.y_Aix)

        # 创建折线视图 窗口
        self.chartView = QChartView(self.chart)
        # self.chart.setTitle("简单折线图")
        self.chart.legend().setAlignment(Qt.AlignmentFlag.AlignBottom)
        self.chart.legend().setLabelColor(fontColor)
        self.chart.setContentsMargins(0, 0, 0, 0)
        self.chartView.setRenderHint(QPainter.RenderHint.Antialiasing)  # 抗锯齿
        self.chartView.setGeometry(0, 0, 600, 600)

        # 添加到窗体中
        # self.__ui.lineGraphFrame.layout().addWidget(self.chartview)
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.chartView)

        layout3 = QVBoxLayout()
        layout3.setContentsMargins(0, 0, 0, 0)
        layout3.addItem(layout)
        # layout3.addItem(layout2)
        self.setLayout(layout3)

        # 增加数据点

    def addChartDatas(self, series, data):
        series.append(self.data_index, data)

    def refresh(self):
        # if ObjectManager.get("refreshFlag") == self.lastRefreshTime:
        #     return
        # self.lastRefreshTime = ObjectManager.get("refreshFlag")

        fontColor: QColor
        if settings.get("theme").startswith("light"):
            fontColor = QColor(0, 0, 0)
        else:
            fontColor = QColor(255, 255, 255)

        self.chart.legend().setLabelColor(fontColor)

        self.x_Aix.setLabelsColor(fontColor)
        self.x_Aix.setLinePenColor(fontColor)
        self.x_Aix.setGridLineColor(fontColor)

        self.y_Aix.setLabelsColor(fontColor)
        self.y_Aix.setLinePenColor(fontColor)
        self.y_Aix.setGridLineColor(fontColor)

    # 清除数据
    def cleanDatas(self):
        self.data_index = 0
        self.series_1.clear()
        self.series_2.clear()
        self.series_3.clear()
        self.x_Aix.setRange(0.00, self.x_data_length)

    # 更新数据
    def updateSeries(self, result):
        self.data_index += self.duration
        # print(result)
        self.addChartDatas(self.series_3, result[2])
        self.addChartDatas(self.series_2, result[1])
        self.addChartDatas(self.series_1, result[0])

        # 当时间轴大于现有时间轴，进行更新坐标轴，并删除之前数据
        xp2 = self.x_data_length // 2
        sub = self.data_index - self.x_data_length
        # print(self.data_index, self.x_data_length)
        if sub >= 0 and sub % xp2 <= self.duration:
            left = self.data_index - xp2
            right = self.data_index + xp2
            self.x_Aix.setRange(left, right)

        self.last = [x for x in result]

    def repeatLast(self):
        if len(self.last) > 0:
            self.updateSeries(self.last)
        else:
            self.updateSeries([0, 1, 0])

    def repeatZero(self):
        self.updateSeries([0, 0, 0])
