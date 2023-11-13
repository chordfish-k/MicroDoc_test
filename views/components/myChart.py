from PySide6.QtCharts import (QChart, QChartView, QLineSeries,
                              QValueAxis, QCategoryAxis)
from PySide6.QtGui import QColor, QPainter
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QSizePolicy, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QSpacerItem
from assets.api.report import postReportAPI

from assets.assets_loader import Assets
from util.settings import Settings

class MyChartWidget(QWidget):
    chart: QChart = None
    btn: QPushButton = None
    settings: Settings = None

    data1 = [{'x':[], 'y':[]} for _ in range(3)]
    duration = 1

    def __init__(self, parent, settings):
        super().__init__()
        self.settings = settings
        self.initComponents()
        Assets.loadQss("my_chart", self)
        self.duration = self.settings.get("output_duration", int)


    def initComponents(self):
        # 图表初始化
        fontColor: QColor = None
        if self.settings.get("theme").startswith("light"):
            fontColor = QColor(0, 0, 0)
        else:
            fontColor = QColor(255, 255, 255)
        ### 表1
        # 创建折线视图
        self.data_index = 0
        self.x_data_length = 100

        self.chart = QChart()
        # self.chart.setAnimationOptions(QChart.AnimationOption.NoAnimation)
        # self.chart.legend().hide()
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
        self.chartview = QChartView(self.chart)
        # self.chart.setTitle("简单折线图")
        self.chart.legend().setAlignment(Qt.AlignmentFlag.AlignRight)
        self.chart.legend().setLabelColor(fontColor)
        self.chartview.setRenderHint(QPainter.RenderHint.Antialiasing)  # 抗锯齿
        self.chartview.setGeometry(0, 0, 600, 600)


                ### 表2
        self.chart2 = QChart()
        self.chart2.setBackgroundVisible(False)

        self.y_Aix2 = QCategoryAxis()
        self.y_Aix2.setLinePenColor(fontColor)
        self.y_Aix2.setLabelsColor(fontColor)
        self.y_Aix2.setGridLineColor(fontColor)
        self.y_Aix2.append("Positive", 0.5)
        self.y_Aix2.append("Neutral", 1)
        self.y_Aix2.append("Negative", 1.5)
        self.y_Aix2.setRange(0,1.5)

        self.x_Aix2 = QValueAxis()
        self.x_Aix2.setLinePenColor(fontColor)
        self.x_Aix2.setRange(0.00, self.x_data_length)
        self.x_Aix2.setGridLineVisible(False)
        self.x_Aix2.setMinorGridLineVisible(False)  # 隐藏参考线
        self.x_Aix2.setLabelFormat("%u")
        self.x_Aix2.setTickCount(11)  # 10+1
        self.x_Aix2.setMinorTickCount(1)
        self.x_Aix2.setLabelsColor(fontColor)
        self.x_Aix2.setGridLineColor(fontColor)

        self.chart2.addAxis(self.y_Aix2, Qt.AlignmentFlag.AlignLeft)
        self.chart2.addAxis(self.x_Aix2, Qt.AlignmentFlag.AlignBottom)

        self.series_4 = QLineSeries()
        self.chart2.addSeries(self.series_4)
        self.series_4.attachAxis(self.x_Aix2)
        self.series_4.attachAxis(self.y_Aix2)
        

        self.chartview2 = QChartView(self.chart2)
        #self.chart2.legend().setAlignment(Qt.AlignmentFlag.AlignRight)
        self.chart2.legend().hide()
        self.chart2.legend().setLabelColor(fontColor)
        self.chartview2.setRenderHint(QPainter.RenderHint.Antialiasing)  # 抗锯齿
        self.chartview2.setGeometry(0, 0, 600, 600)


        # 添加到窗体中
        # self.__ui.lineGraphFrame.layout().addWidget(self.chartview)
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.chartview)
        layout.addWidget(self.chartview2)

        self.btn = QPushButton()
        self.btn.setText("导出")
        self.btn.clicked.connect(self.outputData)
        layout2 = QHBoxLayout()
        layout2.addWidget(self.btn)

        layout3 = QVBoxLayout()
        layout3.addItem(layout)
        layout3.addItem(layout2)
        self.setLayout(layout3)

        # 增加数据点
    def add_chartDatas(self, series, data):
        # if series.count() >= self.x_data_length:
        #     series.removePoints(0, self.x_data_length)
        series.append(self.data_index, data)
        # if series==self.series_3:
        #     print(self.data_index, data)
        


    #清除数据
    def clean_datas(self):
        self.data_index = 0
        self.series_1.clear()
        self.series_2.clear()
        self.series_3.clear()
        self.series_4.clear()
        self.data1 = [{'x':[], 'y':[]} for _ in range(3)]
        self.x_Aix.setRange(0.00, self.x_data_length)
        self.x_Aix2.setRange(0.00, self.x_data_length)


    # 更新数据
    def update_series(self, result):
        self.data_index += self.duration
        # print(result)
        self.add_chartDatas(self.series_3, result[2])
        self.add_chartDatas(self.series_2, result[1])
        self.add_chartDatas(self.series_1, result[0])

        self.data1[0]['y'].append(str.format("{:.0f}", result[2]*1000))
        self.data1[1]['y'].append(str.format("{:.0f}", result[0]*1000))
        
        # self.data1[0].append(str.format("{:.0f}", result[0]*1000))

        averge = 0.333
        for i in range(0,3):
            if result[i] > averge:
                category = ((2 - i) / 2.0) + 0.25
                self.add_chartDatas(self.series_4, category)
                self.data1[2]['y'].append(str.format("{:.0f}", category))
                break

        # 当时间轴大于现有时间轴，进行更新坐标轴，并删除之前数据
        xp2 = self.x_data_length // 2
        sub = self.data_index - self.x_data_length
        # print(self.data_index, self.x_data_length)
        if sub >= 0 and sub % xp2 <= self.duration:
            left = self.data_index - xp2
            right = self.data_index + xp2
            self.x_Aix.setRange(left, right)
            self.x_Aix2.setRange(left, right)



    def outputData(self):
        total = len(self.data1[0]['y'])
        print("total:", total)
        print("data_index:", self.data_index)
        
        self.data1[0]['x'] = self.data1[1]['x'] = self.data1[2]['x'] = \
            [str.format("{:.0f}", 1+x*self.duration) for x in range(0, total)]
        data = {
            'datas':[
                {
                    'type': 0,
                    'x': ",".join(self.data1[0]['x']),
                    'y': ",".join(self.data1[0]['y']),
                },
                {
                    'type': 1,
                    'x': ",".join(self.data1[1]['x']),
                    'y': ",".join(self.data1[1]['y']),
                },
                {
                    'type': 2,
                    'x': ",".join(self.data1[2]['x']),
                    'y': ",".join(self.data1[2]['y']),
                },
            ]
        }
        # print(data)
        res = postReportAPI(data)
        # print(res)
        pass