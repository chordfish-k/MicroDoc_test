from src.components import MyQWidget
from .eegChart import *
from src.util.logger import logger
import numpy as np


class EEGChartGroup(MyQWidget):
    layout: QVBoxLayout = None
    npyPath = ""
    npyData = None

    eegCharts = []
    channels = []
    pointer = 0
    duration = 4

    dataBuf = []

    def __init__(self):
        super().__init__()
        self.duration = settings.get("output_duration", int)

    def initComponents(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)

        self.addChart(0, QColor(50, 50, 250))
        self.addChart(1, QColor(50, 250, 50))
        self.addChart(2, QColor(50, 250, 250))

    def setNpyDataSource(self, path: str):
        self.npyPath = path
        self.npyData = np.load(path)
        self.pointer = 0
        logger.info(self.npyData.shape)

    def addChart(self, channel: int, color: QColor):

        eegChart = EEGChartWidget()
        eegChart.setSeriesColor(color)
        self.layout.addWidget(eegChart)
        self.channels.append(channel)
        self.eegCharts.append(eegChart)

    def cleanAll(self):
        self.pointer = 0
        self.dataBuf = []
        for i in range(0, len(self.channels)):
            self.eegCharts[i].cleanDatas()
            self.dataBuf.append({'x': [], 'y': []})

    def updateData(self):
        for n in range(0, self.duration):
            for i in range(0, len(self.channels)):
                y = self.npyData[self.channels[i]][self.pointer]
                self.eegCharts[i].updateSeries(y)
                self.dataBuf[i]["y"].append(str.format("{:.0f}", y*1000))
            self.pointer += 1

    def refresh(self):
        for chart in self.eegCharts:
            chart.refresh()

    def getData(self):
        total = self.pointer
        # print("total:", total)
        # print("data_index:", self.data_index)
        data = []
        for d in self.dataBuf:
            d['x'] = [str.format("{:.0f}", 1 + x * self.duration) for x in range(0, total)]

            dataPiece = {
                    'type': 3,
                    'x': ",".join(d['x']),
                    'y': ",".join(d['y']),
                }

            data.append(dataPiece)
        return data
