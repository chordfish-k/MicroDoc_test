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

    def __init__(self):
        super().__init__()

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
        for i in range(0, len(self.channels)):
            self.eegCharts[i].cleanDatas()

    def updateData(self):
        for n in range(0, settings.get("output_duration", int)):
            for i in range(0, len(self.channels)):
                self.eegCharts[i].updateSeries(self.npyData[i][self.pointer])
            self.pointer += 1

