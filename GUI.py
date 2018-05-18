# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!
import copy2dir
import algorithms
import map_loader
import maps
import high_potential_area
import os
import re
import subprocess
import pcraster
import cost_optimization
import map_merge
from distutils.dir_util import copy_tree
from shutil import copytree

import datetime

from config import read_config
import time
from PyQt4 import *
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QFileDialog, QStringListModel
import errno
# import arcpy, arcinfo
# from arcpy.sa import *
import sys
from ExecutePre import ExecutePre
from ExecuteMod import ExecuteMod
# import psutil
import json
import codecs

import map_merge

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8


    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)
import shutil

_D_GENARAL_MAPS = {}
_Current = os.getcwd()

_OUTPUT_DIR = os.path.join(os.getcwd(), "output")
_files = []
_ERRONED_PRE = []


# settings ={'folder_number' : len(os.listdir('C:/TMP')), 'available':[], 'associations':{}}
# for i in range(1, len(os.listdir('C:/TMP'))+1):
#    settings['available'].append(i)
def read_settings():
    try:
        with open('sett.cfg', 'r') as settings_file:
            settings = json.load(settings_file)

    except:
        settings = {'folder_number': 0, 'available': [], 'associations': []}

    return settings


def save_settings(settings):
    output_file = codecs.open("sett.cfg", "w", encoding="utf-8")
    json.dump(settings, output_file, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False)


class Ui_Dialog(object):
    def setupUi(self, Dialog, main):
        self.main = main
        Dialog.setObjectName(_fromUtf8("Dialog"))

        Dialog.resize(800, 600)
        self.groupBox_9 = QtGui.QGroupBox(Dialog)
        self.groupBox_9.setGeometry(QtCore.QRect(380, 10, 400, 491))
        self.groupBox_9.setObjectName(_fromUtf8("groupBox_9"))
        self.btn_DefinePara = QtGui.QPushButton(self.groupBox_9)
        self.btn_DefinePara.setGeometry(QtCore.QRect(40, 22, 281, 51))
        self.btn_DefinePara.setObjectName(_fromUtf8("btn_DefinePara"))
        self.btn_RunPre = QtGui.QPushButton(self.groupBox_9)
        self.btn_RunPre.setGeometry(QtCore.QRect(40, 90, 281, 51))
        self.btn_RunPre.setObjectName(_fromUtf8("btn_RunPre"))
        self.label = QtGui.QLabel(self.groupBox_9)
        self.label.setGeometry(QtCore.QRect(20, 190, 370, 51))
        self.label.setObjectName(_fromUtf8("label"))
        self.le_subsrerun = QtGui.QLineEdit(self.groupBox_9)
        self.le_subsrerun.setGeometry(QtCore.QRect(270, 220, 81, 20))
        self.le_subsrerun.setObjectName(_fromUtf8("le_subsrerun"))
        self.btn_define = QtGui.QPushButton(self.groupBox_9)
        self.btn_define.setGeometry(QtCore.QRect(30, 250, 151, 41))
        self.btn_define.setObjectName(_fromUtf8("btn_define"))
        self.groupBox_gen = QtGui.QGroupBox(self.groupBox_9)
        self.groupBox_gen.setGeometry(QtCore.QRect(20, 310, 360, 161))
        self.groupBox_gen.setObjectName(_fromUtf8("groupBox_gen"))
        self.lv_parammap = QtGui.QListView(self.groupBox_gen)
        self.lv_parammap.setGeometry(QtCore.QRect(10, 20, 171, 91))
        self.lv_parammap.setObjectName(_fromUtf8("lv_parammap"))
        self.btn_show_m = QtGui.QPushButton(self.groupBox_gen)
        self.btn_show_m.setGeometry(QtCore.QRect(100, 120, 91, 31))
        self.btn_show_m.setObjectName(_fromUtf8("btn_show_m"))

        self.le_SubNn = QtGui.QLineEdit(self.groupBox_gen)
        self.le_SubNn.setGeometry(QtCore.QRect(200, 60, 51, 20))
        self.le_SubNn.setObjectName(_fromUtf8("le_SubN"))
        self.label_1n = QtGui.QLabel(self.groupBox_gen)
        self.label_1n.setGeometry(QtCore.QRect(200, 20, 145, 16))
        self.label_1n.setObjectName(_fromUtf8("label_1"))

        self.groupBox = QtGui.QGroupBox(Dialog)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 361, 550))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.groupBox_2 = QtGui.QGroupBox(self.groupBox)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 20, 341, 41))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.tb_DEM = QtGui.QToolButton(self.groupBox_2)
        self.tb_DEM.setGeometry(QtCore.QRect(310, 20, 25, 19))
        self.tb_DEM.setObjectName(_fromUtf8("tb_DEM"))
        self.le_DEM = QtGui.QLineEdit(self.groupBox_2)
        self.le_DEM.setGeometry(QtCore.QRect(20, 20, 281, 20))
        self.le_DEM.setObjectName(_fromUtf8("le_DEM"))
        self.groupBox_3 = QtGui.QGroupBox(self.groupBox)
        self.groupBox_3.setGeometry(QtCore.QRect(10, 60, 341, 41))
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.tb_Landuse = QtGui.QToolButton(self.groupBox_3)
        self.tb_Landuse.setGeometry(QtCore.QRect(310, 20, 25, 19))
        self.tb_Landuse.setObjectName(_fromUtf8("tb_Landuse"))
        self.le_Landuse = QtGui.QLineEdit(self.groupBox_3)
        self.le_Landuse.setGeometry(QtCore.QRect(20, 20, 281, 20))
        self.le_Landuse.setObjectName(_fromUtf8("le_Landuse"))
        self.groupBox_4 = QtGui.QGroupBox(self.groupBox)
        self.groupBox_4.setGeometry(QtCore.QRect(10, 100, 341, 41))
        self.groupBox_4.setObjectName(_fromUtf8("groupBox_4"))
        self.tb_Soil = QtGui.QToolButton(self.groupBox_4)
        self.tb_Soil.setGeometry(QtCore.QRect(310, 20, 25, 19))
        self.tb_Soil.setObjectName(_fromUtf8("tb_Soil"))
        self.le_Soil = QtGui.QLineEdit(self.groupBox_4)
        self.le_Soil.setGeometry(QtCore.QRect(20, 20, 281, 20))
        self.le_Soil.setObjectName(_fromUtf8("le_Soil"))
        self.groupBox_5 = QtGui.QGroupBox(self.groupBox)
        self.groupBox_5.setGeometry(QtCore.QRect(10, 140, 341, 41))
        self.groupBox_5.setObjectName(_fromUtf8("groupBox_5"))
        self.tb_Watershed = QtGui.QToolButton(self.groupBox_5)
        self.tb_Watershed.setGeometry(QtCore.QRect(310, 20, 25, 19))
        self.tb_Watershed.setObjectName(_fromUtf8("tb_Watershed"))
        self.le_Watershed = QtGui.QLineEdit(self.groupBox_5)
        self.le_Watershed.setGeometry(QtCore.QRect(20, 20, 281, 20))
        self.le_Watershed.setObjectName(_fromUtf8("le_Watershed"))
        self.groupBox_6 = QtGui.QGroupBox(self.groupBox)
        self.groupBox_6.setGeometry(QtCore.QRect(10, 180, 341, 41))
        self.groupBox_6.setObjectName(_fromUtf8("groupBox_6"))
        self.btn_evaporation = QtGui.QToolButton(self.groupBox_6)
        self.btn_evaporation.setGeometry(QtCore.QRect(310, 20, 25, 19))
        self.btn_evaporation.setObjectName(_fromUtf8("btn_evaporation"))
        self.le_evaporation = QtGui.QLineEdit(self.groupBox_6)
        self.le_evaporation.setGeometry(QtCore.QRect(20, 20, 281, 20))
        self.le_evaporation.setObjectName(_fromUtf8("le_evaporation"))
        self.groupBox_7 = QtGui.QGroupBox(self.groupBox)
        self.groupBox_7.setGeometry(QtCore.QRect(10, 220, 341, 41))
        self.groupBox_7.setObjectName(_fromUtf8("groupBox_7"))
        self.btn_precipitation = QtGui.QToolButton(self.groupBox_7)
        self.btn_precipitation.setGeometry(QtCore.QRect(310, 20, 25, 19))
        self.btn_precipitation.setObjectName(_fromUtf8("btn_precipitation"))
        self.le_precipitation = QtGui.QLineEdit(self.groupBox_7)
        self.le_precipitation.setGeometry(QtCore.QRect(20, 20, 281, 20))
        self.le_precipitation.setObjectName(_fromUtf8("le_precipitation"))

        self.groupBox_OpenLAI = QtGui.QGroupBox(self.groupBox)
        self.groupBox_OpenLAI.setGeometry(QtCore.QRect(10, 260, 341, 41))
        self.groupBox_OpenLAI.setObjectName(_fromUtf8("groupBox_OpenLAI"))
        self.btn_OpenLAI = QtGui.QToolButton(self.groupBox_OpenLAI)
        self.btn_OpenLAI.setGeometry(QtCore.QRect(310, 20, 25, 19))
        self.btn_OpenLAI.setObjectName(_fromUtf8("btn_OpenLAI"))
        self.le_OpenLAI = QtGui.QLineEdit(self.groupBox_OpenLAI)
        self.le_OpenLAI.setGeometry(QtCore.QRect(20, 20, 281, 20))
        self.le_OpenLAI.setObjectName(_fromUtf8("le_OpenLAI"))

        self.groupBox_8 = QtGui.QGroupBox(self.groupBox)
        self.groupBox_8.setGeometry(QtCore.QRect(10, 400, 331, 131))
        self.groupBox_8.setObjectName(_fromUtf8("groupBox_8"))
        self.le_SubN = QtGui.QLineEdit(self.groupBox_8)
        self.le_SubN.setGeometry(QtCore.QRect(200, 20, 51, 20))
        self.le_SubN.setObjectName(_fromUtf8("le_SubN"))
        self.label_1 = QtGui.QLabel(self.groupBox_8)
        self.label_1.setGeometry(QtCore.QRect(20, 20, 150, 16))
        self.label_1.setObjectName(_fromUtf8("label_1"))
        self.cb_SoilMap = QtGui.QCheckBox(self.groupBox_8)
        self.cb_SoilMap.setGeometry(QtCore.QRect(30, 60, 101, 17))
        self.cb_SoilMap.setObjectName(_fromUtf8("cb_SoilMap"))
        self.cb_LanduseMap = QtGui.QCheckBox(self.groupBox_8)
        self.cb_LanduseMap.setGeometry(QtCore.QRect(30, 80, 101, 17))
        self.cb_LanduseMap.setObjectName(_fromUtf8("cb_LanduseMap"))
        self.cb_ElevationMap = QtGui.QCheckBox(self.groupBox_8)
        self.cb_ElevationMap.setGeometry(QtCore.QRect(30, 100, 101, 17))
        self.cb_ElevationMap.setObjectName(_fromUtf8("cb_ElevationMap"))
        self.btn_ShowResult = QtGui.QPushButton(self.groupBox_8)
        self.btn_ShowResult.setGeometry(QtCore.QRect(230, 90, 91, 31))
        self.btn_ShowResult.setObjectName(_fromUtf8("btn_ShowResult"))
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(20, 320, 170, 16))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.le_NSubs = QtGui.QLineEdit(self.groupBox)
        self.le_NSubs.setGeometry(QtCore.QRect(200, 320, 51, 20))
        self.le_NSubs.setText(_fromUtf8(""))
        self.le_NSubs.setObjectName(_fromUtf8("le_NSubs"))
        self.btn_Map_Generation = QtGui.QPushButton(self.groupBox)
        self.btn_Map_Generation.setGeometry(QtCore.QRect(30, 350, 291, 31))
        self.btn_Map_Generation.setObjectName(_fromUtf8("btn_Map_Generation"))
        self.btn_runagain = QtGui.QPushButton(self.groupBox_9)
        self.btn_runagain.setGeometry(QtCore.QRect(190, 250, 151, 41))
        self.btn_runagain.setObjectName(_fromUtf8("btn_runagain"))

        self.groupBox_2.raise_()
        self.groupBox_3.raise_()
        self.groupBox_5.raise_()
        self.groupBox_4.raise_()
        self.groupBox_6.raise_()
        self.groupBox_7.raise_()
        self.groupBox_8.raise_()
        self.groupBox_9.raise_()
        self.label_2.raise_()
        self.le_NSubs.raise_()
        self.btn_Map_Generation.raise_()

        self.retranslateUi(Dialog)
        self.SetUpActions()

        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.closeEvent = self.closeEvent

    def closeEvent(self, diag):
        self.main.show()

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Wetspa_Urban", None))
        self.groupBox.setTitle(_translate("Dialog", "Inputs", None))
        self.groupBox_2.setTitle(_translate("Dialog", "Open DEM ascii", None))
        self.tb_DEM.setText(_translate("Dialog", "...", None))
        self.groupBox_3.setTitle(_translate("Dialog", "Open Landuse ascii", None))
        self.tb_Landuse.setText(_translate("Dialog", "...", None))
        self.groupBox_4.setTitle(_translate("Dialog", "Open Soil ascii", None))
        self.tb_Soil.setText(_translate("Dialog", "...", None))
        self.groupBox_5.setTitle(_translate("Dialog", "Open Watershed ascii", None))
        self.tb_Watershed.setText(_translate("Dialog", "...", None))
        self.groupBox_6.setTitle(_translate("Dialog", "Evapotranspiration", None))
        self.btn_evaporation.setText(_translate("Dialog", "...", None))
        self.groupBox_7.setTitle(_translate("Dialog", "Precipitation", None))
        self.btn_precipitation.setText(_translate("Dialog", "...", None))
        self.groupBox_8.setTitle(_translate("Dialog", "See Results : ", None))
        self.groupBox_OpenLAI.setTitle(_translate("Dialog", "Open LAI maps", None))
        self.btn_OpenLAI.setText(_translate("Dialog", "...", None))

        self.label_1.setText(_translate("Dialog", "Subcatchments Number :", None))
        self.cb_SoilMap.setText(_translate("Dialog", "Soil Map", None))
        self.cb_LanduseMap.setText(_translate("Dialog", "Landuse Map", None))
        self.cb_ElevationMap.setText(_translate("Dialog", "Elevation Map", None))
        self.btn_ShowResult.setText(_translate("Dialog", "Show Results", None))
        self.label_2.setText(_translate("Dialog", " Number of Subcatchments :", None))
        self.btn_Map_Generation.setText(_translate("Dialog", "Map Generation", None))
        self.groupBox_9.setTitle(_translate("Dialog", "Preprocessing", None))
        self.btn_DefinePara.setText(_translate("Dialog", "Define parameters", None))
        self.btn_RunPre.setText(_translate("Dialog", "Run Preprocessing", None))
        self.label.setText(_translate("Dialog", "in case of any errors in the subcatchements ,set the parametres\n"
                                                "\n"
                                                " individually for following subcatchements : ", None))
        self.label_1n.setText(_translate("Dialog", "Subcatchments Number :", None))
        self.btn_define.setText(_translate("Dialog", "Define", None))
        self.groupBox_gen.setTitle(_translate("Dialog", "See the generated maps", None))
        self.btn_runagain.setText(_translate("Dialog", "Rerun", None))
        self.btn_show_m.setText(_translate("Dialog", "List maps", None))

    def setLEDEM(self):
        fname = QFileDialog.getOpenFileName(None, 'Open file',
                                            os.getcwd(), "ascii maps (*.asc)")
        self.le_DEM.setText(fname)

    def setLE_precipitation(self):
        fname = QFileDialog.getOpenFileName(None, 'Open file',
                                            os.getcwd(), "tss files (*.tss)")
        self.le_precipitation.setText(fname)

    def setLE_evaporation(self):
        fname = QFileDialog.getOpenFileName(None, 'Open file',
                                            os.getcwd(), "tss files (*.tss)")
        self.le_evaporation.setText(fname)

    def setLESoil(self):
        fname = QFileDialog.getOpenFileName(None, 'Open file',
                                            os.getcwd(), "ascii maps (*.asc)")
        self.le_Soil.setText(fname)

    def setLEWhatershed(self):
        fname = QFileDialog.getOpenFileName(None, 'Open file',
                                            os.getcwd(), "ascii maps (*.asc)")
        self.le_Watershed.setText(fname)

    def setLELanduse(self):
        fname = QFileDialog.getOpenFileName(None, 'Open file',
                                            os.getcwd(), "ascii maps (*.asc)")
        self.le_Landuse.setText(fname)

    def setLAImaps(self):
        fname = QFileDialog.getOpenFileName(None, 'Open file',
                                            os.getcwd())
        self.le_OpenLAI.setText(fname)

    def listmaps(self):
        Continue = False

        if self.le_SubNn.text() == "":
            Continue = False
        Sub_path = os.path.join("C:\\TMP", str(self.le_SubNn.text()), "Runner\\catchment\\parammaps")
        print(Sub_path)

        if not os.path.isdir(Sub_path):
            choice = QtGui.QMessageBox.question(None, 'Subs not found',
                                                "Please, Check the sub path if it exist or wait for program to finish generation",
                                                QtGui.QMessageBox.Ok)

        else:
            files = [f for f in os.listdir(Sub_path)
                     if os.path.isfile(os.path.join(Sub_path, f))]
            model = QStringListModel()
            model.setStringList(files)
            self.lv_parammap.setModel(model)

    def showmap(self, selected):
        Sub_path = os.path.join("C:\\TMP", str(self.le_SubNn.text()), "Runner\\catchment\\parammaps")
        a = (str(self.lv_parammap.model().data(selected, 0).toString()))
        pathss = os.path.join(Sub_path, a)
        agrus = "aguila {}".format(pathss)
        subprocess.Popen(agrus)

    def getLAImaps_from_folder(self):
        path = str(self.le_OpenLAI.text())

        l = [0]
        while (1):
            index = path.find("/", max(l), len(path) - 1)
            if index == -1:
                break
            else:
                l.append(index + 1)

        folder_path = path[0:max(l) - 1]  # folder that contains LAIs
        print folder_path

        files_list_LAIs = os.listdir(folder_path)

        watershed = map_loader.MapLoader()
        watershed = watershed.load_map(maps.WaterShedMap, "watershed.asc")

        for file in files_list_LAIs:

            LAI_path = os.path.join(folder_path, file)

            LAI_map = map_loader.MapLoader()
            # LAImap = LAImap.load_dot_map(maps.BasicMap, LAI_path)
            LAI_map = LAI_map.load_map(maps.BasicMap, LAI_path)

            sub_range = []
            i = 1
            while (i < 40):
                sub_range.append(str(i))
                i += 1

            path_tmp = "C:\\tmp"
            list_subs = os.listdir(path_tmp)

            for sub in sub_range:
                for i in range(len(watershed.map.matrix)):
                    for j in range(len(watershed.map.matrix[i])):
                        if watershed.map.matrix[i][j] == sub:
                            LAI_map.map.matrix[i][j] = 1
                        elif watershed.map.matrix[i][j] == watershed.map.no_data_value:
                            LAI_map.map.matrix[i][j] = LAI_map.map.no_data_value
                        else:
                            LAI_map.map.matrix[i][j] == 0

                sub_path = os.path.join(path_tmp, sub,
                                        "Runner\catchment")  # agha nahad ino takmil konid ! (Runner\catchment)

                LAI_map.map.to_file(file, sub_path)

            # copy2dir.copy2dir(os.path.join(folder_path,file),"parammaps")

            pass

    def GenerateMaps(self):
        arcpy.CheckOutExtension('Spatial')

        do = True
        if (
                                    self.le_Landuse.text() == "" or self.le_Watershed.text() == "" or self.le_Soil.text() == "" or self.le_DEM.text() == "" or self.le_NSubs.text() == ""):
            choice = QtGui.QMessageBox.question(None, 'Invalid parametre',
                                                "Please, make sure you chose all maps before generation",
                                                QtGui.QMessageBox.Ok)
            do = False
        _Nsubs = 0
        try:
            _Nsubs = int(self.le_NSubs.text())
        except Exception as e:
            choice = QtGui.QMessageBox.question(None, 'Invalid parametre',
                                                "Subs Number has to be an integer",
                                                QtGui.QMessageBox.Ok)
            do = False
        print("ff")

        if (do):
            _D_GENARAL_MAPS['elevation'] = str(self.le_DEM.text())
            _D_GENARAL_MAPS['soil'] = str(self.le_Soil.text())
            _D_GENARAL_MAPS['watershed'] = str(self.le_Watershed.text())
            _D_GENARAL_MAPS['landuse'] = str(self.le_Landuse.text())
            print(_D_GENARAL_MAPS)

            arcpy.ASCIIToRaster_conversion(_D_GENARAL_MAPS['landuse'], os.path.join(_OUTPUT_DIR, "landuser"), "INTEGER")
            arcpy.ASCIIToRaster_conversion(os.path.join(_D_GENARAL_MAPS['soil']), os.path.join(_OUTPUT_DIR, "soilr"),
                                           "INTEGER")
            arcpy.ASCIIToRaster_conversion(os.path.join(_D_GENARAL_MAPS['elevation']),
                                           os.path.join(_OUTPUT_DIR, "elevationr"), "FLOAT")
            arcpy.ASCIIToRaster_conversion(os.path.join(_D_GENARAL_MAPS['watershed']),
                                           os.path.join(_OUTPUT_DIR, "watershedr"), "INTEGER")

            landuse_raster = Raster(os.path.join(_OUTPUT_DIR, "landuser"))
            watershed_raster = Raster(os.path.join(_OUTPUT_DIR, "watershedr"))
            soil_raster = Raster(os.path.join(_OUTPUT_DIR, "soilr"))
            elevation_raster = Raster(os.path.join(_OUTPUT_DIR, "elevationr"))
            for i in xrange(1, _Nsubs + 1):
                make_sure_path_exists(os.path.join(_OUTPUT_DIR, str(i)))
                landuse1 = Con(watershed_raster == i, landuse_raster)
                arcpy.RasterToASCII_conversion(landuse1, os.path.join(_OUTPUT_DIR, str(i), "landuse.asc"))
                soil1 = Con(watershed_raster == i, soil_raster)
                arcpy.RasterToASCII_conversion(soil1, os.path.join(_OUTPUT_DIR, str(i), "soil.asc"))
                elevation1 = Con(watershed_raster == i, elevation_raster)
                arcpy.RasterToASCII_conversion(elevation1, os.path.join(_OUTPUT_DIR, str(i), "elevation.asc"))
                _files.append(os.path.join(_OUTPUT_DIR, str(i), "landuse.asc"))
                _files.append(os.path.join(_OUTPUT_DIR, str(i), "soil.asc"))
                _files.append(os.path.join(_OUTPUT_DIR, str(i), "elevation.asc"))
                Dic = {}  # to save data read from files
                FinalDic = {}
                Dirs = {}
                #### read first 5 lines of each file
            for _file in _files:  # for each file
                Dic[_file] = []  # prepare a list to save values in
                f = open(_file, 'r')  # open the file
                for i in range(5):  # file lines
                    line = f.next().strip()
                    Dic[_file].append({line.split()[0]: line.split()[-1]})
                f.close()
                if 'soil' in _file.split("""\\""")[-1]:
                    a = _file.split("""\\""")
                    b = a[:-1]
                    print(b)
                    print(_file)
                    Dirs["""\\""".join(b)] = Dic[_file]
            for Map in Dirs:
                argss = "mapattr {} -s -S -R {} -C {} -x {} -y {} -l {}  ".format(os.path.join(Map, "CloneScalar"),
                                                                                  Dirs[Map][1]["nrows"],
                                                                                  Dirs[Map][0]["ncols"],
                                                                                  Dirs[Map][2]["xllcorner"], str(
                        int(Dirs[Map][3]["yllcorner"]) + (int(Dirs[Map][1]["nrows"]) * int(Dirs[Map][4]["cellsize"]))),
                                                                                  Dirs[Map][4]["cellsize"])
                subprocess.Popen(argss)
                argss = "mapattr {} -s -N -R {} -C {} -x {} -y {} -l {}  ".format(os.path.join(Map, "CloneNominal"),
                                                                                  Dirs[Map][1]["nrows"],
                                                                                  Dirs[Map][0]["ncols"],
                                                                                  Dirs[Map][2]["xllcorner"], str(
                        int(Dirs[Map][3]["yllcorner"]) + (int(Dirs[Map][1]["nrows"]) * int(Dirs[Map][4]["cellsize"]))),
                                                                                  Dirs[Map][4]["cellsize"])
                subprocess.Popen(argss)

            for Map in Dic:
                C = Map
                C = C.split("""\\""")[:-1]
                agrsing = ''
                if 'elevation' in Map:
                    output_map = []
                    CS = []
                    for item in C:
                        output_map.append(item)
                        CS.append(item)
                    output_map.append('elevation_start.map')
                    CS.append('CloneScalar')

                    agrsing = """asc2map -a "{}" {} --clone {}""".format(Map, """\\""".join(output_map),
                                                                         """\\""".join(CS))
                elif 'soil' in Map:
                    output_map = []
                    CS = []
                    for item in C:
                        output_map.append(item)
                        CS.append(item)
                    output_map.append('soil_start.map')
                    CS.append('CloneNominal')
                    agrsing = """asc2map -a "{}" {} --clone {}""".format(Map, """\\""".join(output_map),
                                                                         """\\""".join(CS))
                elif 'landuse' in Map:
                    output_map = []
                    CS = []
                    for item in C:
                        output_map.append(item)
                        CS.append(item)
                    output_map.append('landuse_start.map')
                    CS.append('CloneNominal')
                    agrsing = """asc2map -a "{}" {} --clone {}""".format(Map, """\\""".join(output_map),
                                                                         """\\""".join(CS))
                print(agrsing)
                subprocess.Popen(agrsing)
                time.sleep(1)
            arcpy.CheckInExtension('Spatial')
        pass

        self.getLAImaps_from_folder()

    def SeeSub(self):
        Continue = False

        if self.le_SubN.text() == "":
            Continue = False
        Sub_path = os.path.join(_OUTPUT_DIR, str(self.le_SubN.text()))
        print(Sub_path)

        if not os.path.isdir(Sub_path):
            choice = QtGui.QMessageBox.question(None, 'Subs not found',
                                                "Please, Check the sub path if it exist or wait for program to finish generation",
                                                QtGui.QMessageBox.Ok)
        else:
            Continue = True
        if Continue:
            TMP_ASCII_MAPS = []
            # let's check if there are Start maps to see them
            files = [f for f in os.listdir(Sub_path)
                     if os.path.isfile(os.path.join(Sub_path, f))]
            for f in files:
                if '_start' in f:
                    TMP_ASCII_MAPS.append(f)
            if len(TMP_ASCII_MAPS) == 0:
                choice = QtGui.QMessageBox.question(None, 'Subs not found',
                                                    "There's no maps in this sub!",
                                                    QtGui.QMessageBox.Ok)
            print(TMP_ASCII_MAPS)
            if len(TMP_ASCII_MAPS) != 0:
                print('gg')
                print(self.cb_ElevationMap.isChecked())
                if self.cb_ElevationMap.isChecked():
                    for Map in TMP_ASCII_MAPS:
                        print(Map)
                        if 'elevation' in Map:
                            agrsing = """aguila {}\\{} """.format(Sub_path, Map)
                            print(agrsing)
                            subprocess.Popen(agrsing)
                            time.sleep(2)
                if self.cb_SoilMap.isChecked():
                    for Map in TMP_ASCII_MAPS:
                        if 'soil' in Map:
                            agrsing = """aguila {}\\{} """.format(Sub_path, Map)
                            print(agrsing)
                            subprocess.Popen(agrsing)
                            time.sleep(2)
                if self.cb_LanduseMap.isChecked():
                    for Map in TMP_ASCII_MAPS:
                        if 'landuse' in Map:
                            agrsing = """aguila {}\\{} """.format(Sub_path, Map)
                            print(agrsing)
                            subprocess.Popen(agrsing)
                            time.sleep(2)

    def OpenUserinput(self):
        os.chdir(_Current)
        subprocess.Popen("notepad userinput.ini")

    def Runpre(self):
        ff = []
        files = [f for f in os.listdir(_OUTPUT_DIR)
                 if not os.path.isfile(os.path.join(_OUTPUT_DIR, f))]
        for f in files:
            try:
                if int(f):
                    ff.append(f)
            except Exception as e:
                continue
        ff = sorted(ff)
        ##### Check meteo tss files and save them into a list
        _list_meteo = []
        if self.le_evaporation.text() != "":
            # "c/TMP/1/Runner/catchment/meteo/e.tss"

            _list_meteo.append(str(self.le_evaporation.text()))

            # Added by Taha
            path_evaporation = str(self.le_evaporation.text())
            copy2dir.copy2dir(path_evaporation, "meteo/evapotranspiration.tss")
            # ----------------
            pass
        if self.le_precipitation.text() != "":
            # "c/TMP/1/Runner/catchment/meteo/N.tss"
            _list_meteo.append(str(self.le_precipitation.text()))

            # Added by Taha
            path_precipitation = str(self.le_precipitation.text())
            copy2dir.copy2dir(path_precipitation, "meteo/precipitation.tss")
            # ----------------
            pass

        # if self.le_OpenLAI.text() != "":


        #### copy files
        dbconfig = read_config(section='config')
        if (len(_list_meteo) != 0):
            for tssfile in _list_meteo:
                # we'll copy to every sub
                for sub in ff:
                    shutil.copy(tssfile, os.path.join(dbconfig['tmp'], str(sub), dbconfig['meteo']))
        Threads = []
        userinputdic = read_config(filename="userinput.ini", section="userinput")
        for count, sub in enumerate(ff):
            print("Processing Sub {0}".format(sub))
            a = ExecutePre(sub, userinputdic)
            Threads.append(a)

        for T in Threads:
            T.start()
            T.join()
            if T.erroned:
                _ERRONED_PRE.append(str(T.sub))
        print(_ERRONED_PRE)

        Message = ''
        if len(_ERRONED_PRE) != 0:
            for a in _ERRONED_PRE:
                Message += " {}".format(str(a))

        choice = QtGui.QMessageBox.question(None, 'Erroned Subs',
                                            "these Subs are erroned : {} ".format(Message),
                                            QtGui.QMessageBox.Ok)

        pass

    def ReRunPre(self):
        do = False
        os.chdir(_Current)
        print(_Current)
        userinputdic = read_config(filename=os.path.join(_Current, "userinput.ini"), section="userinput")
        if (self.le_subsrerun.text() == ""):
            choice = QtGui.QMessageBox.question(None, 'Erroned Subs',
                                                " Please include at least one sub",
                                                QtGui.QMessageBox.Ok)

        else:
            do = True

        if do:

            l = str(self.le_subsrerun.text()).split(',')
            Threads = []
            os.chdir(_Current)
            userinputdic = read_config(filename=os.path.join(_Current, "userinput.ini"), section="userinput")
            for count, sub in enumerate(l):
                print("Processing Sub {0}".format(sub))
                a = ExecutePre(sub, userinputdic)
                Threads.append(a)

            for T in Threads:
                T.start()
                T.join()
                if T.erroned:
                    if T.sub not in _ERRONED_PRE:
                        _ERRONED_PRE.append(str(T.sub))

            Message = ""
            if len(_ERRONED_PRE) != 0:
                for a in _ERRONED_PRE:
                    Message += " {}".format(str(a))
            bb = "these Subss are erroned : {} ".format((Message))
            print(type(bb))
            choice = QtGui.QMessageBox.question(None, 'Erroned Subs',
                                                "these Subs are erroned : {} ".format(str(Message)),
                                                QtGui.QMessageBox.Ok)

    def SetUpActions(self):
        self.tb_DEM.clicked.connect(self.setLEDEM)
        self.tb_Landuse.clicked.connect(self.setLELanduse)
        self.tb_Soil.clicked.connect(self.setLESoil)
        self.tb_Watershed.clicked.connect(self.setLEWhatershed)
        self.btn_Map_Generation.clicked.connect(self.GenerateMaps)
        self.btn_ShowResult.clicked.connect(self.SeeSub)
        self.btn_DefinePara.clicked.connect(self.OpenUserinput)
        self.btn_RunPre.clicked.connect(self.Runpre)
        self.btn_define.clicked.connect(self.OpenUserinput)
        self.btn_runagain.clicked.connect(self.ReRunPre)
        self.btn_show_m.clicked.connect(self.listmaps)
        self.btn_OpenLAI.clicked.connect(self.setLAImaps)

        self.lv_parammap.doubleClicked.connect(self.showmap)
        self.btn_precipitation.clicked.connect(self.setLE_precipitation)
        self.btn_evaporation.clicked.connect(self.setLE_evaporation)


dbconfig = read_config(section='config')
_WORKING_DIR = os.getcwd()


class Ui_Dialogone(object):
    def setupUi(self, Dialog, main):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        self.main = main

        Dialog.resize(752, 600)

        self.groupBox = QtGui.QGroupBox(Dialog)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 361, 281))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(20, 20, 46, 21))
        self.label.setObjectName(_fromUtf8("label"))
        self.le_Kep = QtGui.QLineEdit(self.groupBox)
        self.le_Kep.setGeometry(QtCore.QRect(80, 20, 113, 20))
        self.le_Kep.setObjectName(_fromUtf8("le_Kep"))
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(20, 40, 46, 21))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.le_k_run = QtGui.QLineEdit(self.groupBox)
        self.le_k_run.setGeometry(QtCore.QRect(80, 40, 113, 20))
        self.le_k_run.setObjectName(_fromUtf8("le_k_run"))
        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(20, 60, 46, 21))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.label_4 = QtGui.QLabel(self.groupBox)
        self.label_4.setGeometry(QtCore.QRect(20, 80, 46, 21))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.le_kss = QtGui.QLineEdit(self.groupBox)
        self.le_kss.setGeometry(QtCore.QRect(80, 80, 113, 20))
        self.le_kss.setObjectName(_fromUtf8("le_kss"))
        self.le_p_max = QtGui.QLineEdit(self.groupBox)
        self.le_p_max.setGeometry(QtCore.QRect(80, 60, 113, 20))
        self.le_p_max.setObjectName(_fromUtf8("le_p_max"))
        self.label_5 = QtGui.QLabel(self.groupBox)
        self.label_5.setGeometry(QtCore.QRect(20, 100, 46, 21))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.label_6 = QtGui.QLabel(self.groupBox)
        self.label_6.setGeometry(QtCore.QRect(20, 160, 46, 21))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.label_7 = QtGui.QLabel(self.groupBox)
        self.label_7.setGeometry(QtCore.QRect(20, 120, 46, 21))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.le_g_max = QtGui.QLineEdit(self.groupBox)
        self.le_g_max.setGeometry(QtCore.QRect(80, 140, 113, 20))
        self.le_g_max.setObjectName(_fromUtf8("le_g_max"))
        self.label_8 = QtGui.QLabel(self.groupBox)
        self.label_8.setGeometry(QtCore.QRect(20, 140, 46, 21))
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.le_go = QtGui.QLineEdit(self.groupBox)
        self.le_go.setGeometry(QtCore.QRect(80, 120, 113, 20))
        self.le_go.setObjectName(_fromUtf8("le_go"))
        self.le_ki = QtGui.QLineEdit(self.groupBox)
        self.le_ki.setGeometry(QtCore.QRect(80, 100, 113, 20))
        self.le_ki.setObjectName(_fromUtf8("le_ki"))
        self.le_kg = QtGui.QLineEdit(self.groupBox)
        self.le_kg.setGeometry(QtCore.QRect(80, 160, 113, 20))
        self.le_kg.setObjectName(_fromUtf8("le_kg"))
        self.label_9 = QtGui.QLabel(self.groupBox)
        self.label_9.setGeometry(QtCore.QRect(10, 190, 171, 41))
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.le_SubsN = QtGui.QLineEdit(self.groupBox)
        self.le_SubsN.setGeometry(QtCore.QRect(10, 230, 113, 20))
        self.le_SubsN.setObjectName(_fromUtf8("le_SubsN"))
        self.btn_define = QtGui.QPushButton(self.groupBox)
        self.btn_define.setGeometry(QtCore.QRect(220, 210, 131, 41))
        self.btn_define.setObjectName(_fromUtf8("btn_define"))
        self.groupBox_2 = QtGui.QGroupBox(Dialog)
        self.groupBox_2.setGeometry(QtCore.QRect(380, 10, 361, 491))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.label_13 = QtGui.QLabel(self.groupBox_2)
        self.label_13.setGeometry(QtCore.QRect(20, 30, 170, 16))
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.le_NSubSee = QtGui.QLineEdit(self.groupBox_2)
        self.le_NSubSee.setGeometry(QtCore.QRect(200, 30, 81, 20))
        self.le_NSubSee.setObjectName(_fromUtf8("le_NSubSee"))
        self.btn_waterbalanec = QtGui.QPushButton(self.groupBox_2)
        self.btn_waterbalanec.setGeometry(QtCore.QRect(100, 70, 131, 31))
        self.btn_waterbalanec.setObjectName(_fromUtf8("btn_waterbalanec"))
        self.groupBox_4 = QtGui.QGroupBox(self.groupBox_2)
        self.groupBox_4.setGeometry(QtCore.QRect(10, 150, 341, 151))
        self.groupBox_4.setObjectName(_fromUtf8("groupBox_4"))
        self.groupBox_5 = QtGui.QGroupBox(self.groupBox_4)
        self.groupBox_5.setGeometry(QtCore.QRect(0, 0, 341, 151))
        self.groupBox_5.setObjectName(_fromUtf8("groupBox_5"))
        self.lv_showseries = QtGui.QListView(self.groupBox_5)
        self.lv_showseries.setGeometry(QtCore.QRect(20, 20, 161, 91))
        self.lv_showseries.setObjectName(_fromUtf8("lv_showseries"))
        self.btn_showseries = QtGui.QPushButton(self.groupBox_5)
        self.btn_showseries.setGeometry(QtCore.QRect(30, 120, 75, 23))
        self.btn_showseries.setObjectName(_fromUtf8("btn_showseries"))
        self.groupBox_6 = QtGui.QGroupBox(self.groupBox_2)
        self.groupBox_6.setGeometry(QtCore.QRect(10, 300, 341, 151))
        self.groupBox_6.setObjectName(_fromUtf8("groupBox_6"))
        self.lv_showmaps = QtGui.QListView(self.groupBox_6)
        self.lv_showmaps.setGeometry(QtCore.QRect(20, 20, 161, 91))
        self.lv_showmaps.setObjectName(_fromUtf8("lv_showmaps"))
        self.btn_showmaps = QtGui.QPushButton(self.groupBox_6)
        self.btn_showmaps.setGeometry(QtCore.QRect(30, 120, 75, 23))
        self.btn_showmaps.setObjectName(_fromUtf8("btn_showmaps"))

        self.groupBox_LAI = QtGui.QGroupBox(Dialog)
        self.groupBox_LAI.setGeometry(QtCore.QRect(10, 300, 361, 100))
        self.groupBox_LAI.setObjectName(_fromUtf8("groupBox_LAI"))
        self.le_LAImin = QtGui.QLineEdit(self.groupBox_LAI)
        self.le_LAImin.setGeometry(QtCore.QRect(60, 40, 113, 30))
        self.le_LAImin.setObjectName(_fromUtf8("le_LAImin"))
        self.btn_LAImin = QtGui.QPushButton(self.groupBox_LAI)
        self.btn_LAImin.setGeometry(QtCore.QRect(180, 40, 100, 30))
        self.btn_LAImin.setObjectName(_fromUtf8("btn_LAImin"))

        self.groupBox_3 = QtGui.QGroupBox(Dialog)
        self.groupBox_3.setGeometry(QtCore.QRect(10, 400, 361, 191))
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.le_timesteps = QtGui.QLineEdit(self.groupBox_3)
        self.le_timesteps.setGeometry(QtCore.QRect(130, 30, 113, 20))
        self.le_timesteps.setObjectName(_fromUtf8("le_timesteps"))
        self.label_11 = QtGui.QLabel(self.groupBox_3)
        self.label_11.setGeometry(QtCore.QRect(10, 50, 111, 21))
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.label_12 = QtGui.QLabel(self.groupBox_3)
        self.label_12.setGeometry(QtCore.QRect(10, 70, 61, 21))
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.label_10 = QtGui.QLabel(self.groupBox_3)
        self.label_10.setGeometry(QtCore.QRect(10, 30, 71, 21))
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.le_start_date = QtGui.QLineEdit(self.groupBox_3)
        self.le_start_date.setGeometry(QtCore.QRect(130, 70, 113, 20))
        self.le_start_date.setObjectName(_fromUtf8("le_start_date"))
        self.le_Ntimesteps = QtGui.QLineEdit(self.groupBox_3)
        self.le_Ntimesteps.setGeometry(QtCore.QRect(130, 50, 113, 20))
        self.le_Ntimesteps.setObjectName(_fromUtf8("le_Ntimesteps"))
        self.btn_run = QtGui.QPushButton(self.groupBox_3)
        self.btn_run.setGeometry(QtCore.QRect(60, 130, 131, 41))
        self.btn_run.setObjectName(_fromUtf8("btn_run"))
        self.le_NSUBSTORUN = QtGui.QLineEdit(self.groupBox_3)
        self.le_NSUBSTORUN.setGeometry(QtCore.QRect(130, 90, 113, 20))
        self.le_NSUBSTORUN.setObjectName(_fromUtf8("le_NSUBSTORUN"))
        self.label_14 = QtGui.QLabel(self.groupBox_3)
        self.label_14.setGeometry(QtCore.QRect(10, 90, 61, 21))
        self.label_14.setObjectName(_fromUtf8("label_14"))
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        self.SetActions()
        Dialog.closeEvent = self.closeEvent

    def closeEvent(self, diag):
        self.main.show()

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Wetspa_Urban", None))
        self.groupBox.setTitle(_translate("Dialog", "Global Paramters", None))
        self.label.setText(_translate("Dialog", "Kep", None))
        self.label_2.setText(_translate("Dialog", "k_run", None))
        self.label_3.setText(_translate("Dialog", "P_max", None))
        self.label_4.setText(_translate("Dialog", "kss", None))
        self.label_5.setText(_translate("Dialog", "ki", None))
        self.label_6.setText(_translate("Dialog", "kg", None))
        self.label_7.setText(_translate("Dialog", "g0", None))
        self.label_8.setText(_translate("Dialog", "g_max", None))
        self.label_9.setText(_translate("Dialog", "Set these parameters for\n"
                                                  " these subcatchments individually :", None))
        self.btn_define.setText(_translate("Dialog", "Define", None))
        self.groupBox_2.setTitle(_translate("Dialog", "Results", None))
        self.label_13.setText(_translate("Dialog", "Set the catchments number :", None))
        self.btn_waterbalanec.setText(_translate("Dialog", "Water Balance", None))
        self.groupBox_4.setTitle(_translate("Dialog", "Series :", None))
        self.groupBox_5.setTitle(_translate("Dialog", "Series :", None))
        self.btn_showseries.setText(_translate("Dialog", "Show", None))
        self.groupBox_6.setTitle(_translate("Dialog", "Maps :", None))
        self.btn_showmaps.setText(_translate("Dialog", "Show", None))
        self.groupBox_3.setTitle(_translate("Dialog", "Simulation Options", None))
        self.label_11.setText(_translate("Dialog", "Number of timesteps", None))
        self.label_12.setText(_translate("Dialog", "Start Date", None))
        self.label_10.setText(_translate("Dialog", "Timesteps", None))
        self.btn_run.setText(_translate("Dialog", "Run", None))
        self.label_14.setText(_translate("Dialog", "Subs Number to run", None))
        self.groupBox_LAI.setTitle(_translate("Dialog", "LAI min", None))
        self.btn_LAImin.setText(_translate("Dialog", "OK", None))

    def definepara(self):
        Continue = True
        if (
                                                self.le_g_max.text() == "" and self.le_go.text() == "" and self.le_k_run.text() == "" and self.le_Kep.text() == ""
                            and self.le_kg.text() == "" and self.le_ki.text() == "" and self.le_p_max.text() == "" and self.le_kss.text() == ""):
            choice = QtGui.QMessageBox.question(None, 'Subs not found',
                                                "Please, Check the sub path if it exist or wait for program to finish generation",
                                                QtGui.QMessageBox.Ok)
            Continue = False

        if (Continue):
            ListLe = {}
            ListLe['Kep'] = (self.le_Kep)
            ListLe['K_run'] = (self.le_k_run)
            ListLe['P_max'] = (self.le_g_max)
            ListLe['Kss'] = (self.le_kss)
            ListLe['Ki'] = (self.le_ki)
            ListLe['g0'] = (self.le_go)
            ListLe['g_max'] = (self.le_p_max)
            ListLe['Kg'] = (self.le_kg)
            for a in ListLe:
                # print(str(ListLe[a].text()))
                pass
            ####### Read current file
            readconf = read_config(section='config')
            subs = str(self.le_SubsN.text()).split(',')
            for sub in subs:
                paths = os.path.join(readconf['tmp'], sub, readconf['configparametersets'])
                print(paths)
                f = open(paths, 'r')
                old = f.read().strip()
                f.close()
                dic_start_index = old.find('{')
                dic_string = old[dic_start_index + 1:-1]
                dic_list = dic_string.split(',')
                dic_old = {}
                for item in dic_list:
                    a = item.split(':')

                    dic_old[a[0].split("'")[1]] = a[1].strip()

                #######Buildding the file
                strings = """"""
                strings += """#WetSpa parameters
    WETSPAclassic.paramset1::{"""
                for a in ListLe:
                    if (ListLe[a].text() != ""):
                        strings += """'{}':{}, """.format(a, str(ListLe[a].text()))
                    else:
                        strings += """'{}':{}, """.format(a, dic_old[a])
                strings = strings[:-2] + "}"
                print(strings)
                f = open(paths, 'w')
                f.write(strings)
                f.close()

    def showbalance(self):
        _C = True
        if (self.le_NSubSee.text() == ""):
            choice = QtGui.QMessageBox.question(None, 'Prvide sub',
                                                "Please, write down the number of sub in the right position.",
                                                QtGui.QMessageBox.Ok)
            _C = False
        if (_C):
            print(os.getcwd())
            os.chdir(_WORKING_DIR)
            _db = read_config(section='config')
            agruing = "notepad {}".format(os.path.join(_db['tmp'], str(self.le_NSubSee.text()), _db['balance']))
            subprocess.Popen(agruing)

    def lisseries(self):
        Continue = False

        if self.le_NSubSee.text() == "":
            Continue = False
        Sub_path = os.path.join("C:\\TMP", str(self.le_NSubSee.text()), "Runner\\catchment\\")
        print(Sub_path)

        if not os.path.isdir(Sub_path):
            choice = QtGui.QMessageBox.question(None, 'Subs not found',
                                                "Please, Check the sub path if it exist or wait for program to finish generation",
                                                QtGui.QMessageBox.Ok)

        else:
            files = [f for f in os.listdir(Sub_path)
                     if os.path.isfile(os.path.join(Sub_path, f))]
            filing = []
            for f in files:
                print(f)
                if 'tss' in f:
                    filing.append(f)

            model = QStringListModel()
            model.setStringList(filing)
            self.lv_showseries.setModel(model)

    def showseries(self, selected):
        Sub_path = os.path.join("C:\\TMP", str(self.le_NSubSee.text()), "Runner\\catchment")
        a = (str(self.lv_showseries.model().data(selected, 0).toString()))
        pathss = os.path.join(Sub_path, a)
        agrus = "notepad {}".format(pathss)
        subprocess.Popen(agrus)

    def listmapss(self):
        Continue = False

        if self.le_NSubSee.text() == "":
            Continue = False
        Sub_path = os.path.join("C:\\TMP", str(self.le_NSubSee.text()), "Runner\\catchment\\output\\")
        print(Sub_path)

        if not os.path.isdir(Sub_path):
            choice = QtGui.QMessageBox.question(None, 'Subs not found',
                                                "Please, Check the sub path if it exist or wait for program to finish generation",
                                                QtGui.QMessageBox.Ok)

        else:
            files = [f for f in os.listdir(Sub_path)
                     if os.path.isfile(os.path.join(Sub_path, f))]
            filing = []
            for f in files:
                print(f)
                _l = f.split('.')
                itsamap = True
                try:
                    int(_l[-1])
                except:
                    itsamap = False
                if itsamap:
                    filing.append(f)

            model = QStringListModel()
            model.setStringList(filing)
            self.lv_showmaps.setModel(model)

    def showmaps(self, selected):
        Sub_path = os.path.join("C:\\TMP", str(self.le_NSubSee.text()), "Runner\\catchment\\output")
        a = (str(self.lv_showmaps.model().data(selected, 0).toString()))
        pathss = os.path.join(Sub_path, a)
        agrus = "aguila {}".format(pathss)
        subprocess.Popen(agrus)

    def runpro(self):

        self.le_Ntimesteps.text()
        self.le_timesteps.text()
        self.le_start_date.text()
        dic_old = {}
        if self.le_Ntimesteps.text() != "":
            dic_old['NRTIMESTEPS'] = str(self.le_Ntimesteps.text())
        if self.le_timesteps.text() != "":
            dic_old['TIMESTEPS'] = str(self.le_timesteps.text())
        if self.le_start_date.text() != "":
            dic_old['SIMULATION_START_DATE'] = str(self.le_start_date.text())
        _C = True
        if (self.le_NSUBSTORUN.text() == ""):
            _C = False
        if (_C):
            dbconfig = read_config(section='config')
            Threads = []
            if len(dic_old) == 0:
                for a in xrange(1, int(self.le_NSUBSTORUN.text()) + 1):
                    b = ExecuteMod(a)
                    Threads.append(b)
                Dialog.setWindowState(QtCore.Qt.WindowMinimized)
                self.CheckThreads(Threads)


            ##
            ##                    freemom = psutil.virtual_memory()[-1]/1024/1024/1024 #in GB
            ##                    print("Current Free Memory : {} Gb".format(freemom))
            ##                    if ( freemom> int(dbconfig['memorythreads'])):
            ##
            ##                            try:
            ##                                print(os.path.join(dbconfig['tmp'],str(a),dbconfig['catchment'],dbconfig['runframework']))
            ##                                print("Executing the Model {}".format(a))
            ##                                os.chdir(os.path.join(dbconfig['tmp'],str(a),dbconfig['catchment']))
            ##                                subprocess.Popen(os.path.join(dbconfig['tmp'],str(a),dbconfig['catchment'],dbconfig['runframework']), shell=True,stdin=None, stdout=None, stderr=None, close_fds=True)
            ##                                #self.output = subprocess.check_output(os.path.join(dbconfig['tmp'],str(a),dbconfig['catchment'],dbconfig['runframework']), shell=True)
            ##                                print("Finished the Model {}".format(a))
            ##                            except:
            ##                                print("Erroned : {}".format(a))
            ##                            print('sleeping ')
            ##                            time.sleep(10) #if you need proper memory usage, extend the sleep time between checks
            ##                    #finally execute the model
            else:
                # let's clean the config file
                for a in xrange(1, int(self.le_NSUBSTORUN.text()) + 1):
                    confpath = os.path.join(dbconfig['tmp'], str(a), dbconfig['catchment'], dbconfig['configuration'])
                    print(confpath)
                    f = open(confpath, "r")
                    strings = ''
                    # now we have a clean config, let's modify values
                    new_strings = ''
                    for x in f:
                        if not re.match(r'^\s*$', x):
                            if ("TIMESTEPS " in x) and not ("NRTIMESTEPS " in x):
                                egal_index = x.find("=")
                                new_x = x[:egal_index] + dic_old['TIMESTEPS']
                                new_x = """ TIMESTEPS  = {}\n""".format(dic_old['TIMESTEPS'])
                                new_strings += new_x

                            elif ("NRTIMESTEPS " in x):
                                egal_index = x.find("=")
                                new_x = x[:egal_index] + dic_old['NRTIMESTEPS']
                                new_x = """ NRTIMESTEPS  = {}\n""".format(dic_old['NRTIMESTEPS'])
                                new_strings += new_x

                            elif ("SIMULATION_START_DATE " in x):
                                egal_index = x.find("=")
                                new_x = x[:egal_index] + dic_old['SIMULATION_START_DATE']
                                new_x = """ SIMULATION_START_DATE  = {}\n""".format(dic_old['SIMULATION_START_DATE'])
                                new_strings += new_x

                            else:
                                new_strings += x
                                pass
                    f.close()

                    time.sleep(.5)
                    print("###########")
                    print(new_strings)
                    print("###########")

                    f = open(confpath, "w")
                    f.write(new_strings)
                    f.close()

                for a in xrange(1, int(self.le_NSUBSTORUN.text()) + 1):
                    b = ExecuteMod(a)
                    Threads.append(b)
                self.CheckThreads(Threads)
        pass

    def addLAImin(self):
        # add LAI_min to LAI.py files in catchment folders

        LAI_min = str(self.btn_LAImin.text())

        path_tmp = "C:\\tmp"
        list_subs = os.listdir(path_tmp)

        for sub in list_subs:
            path_to_LAI = os.path.join(path_tmp, sub, "Runner\Bin")
            files_in_LAI = os.listdir(path_to_LAI)
            for file_name in files_in_LAI:
                if "myWetSpaModel" in file_name:
                    LAI_path = os.listdir(path_to_LAI, file_name)
                    LAI_old = open(LAI_path, "r")
                    old = LAI_old.readlines()
                    LAI_old.close()
                    old[601] = "\t\tself.LAI = 	" + "'" + LAI_min + "'" + "\n"

                    LAI_new = open(LAI_path, "w")

                    for line in old:
                        LAI_new.write(line)

    def SetActions(self):
        self.btn_define.clicked.connect(self.definepara)
        self.btn_waterbalanec.clicked.connect(self.showbalance)
        self.btn_showseries.clicked.connect(self.lisseries)
        self.lv_showseries.doubleClicked.connect(self.showseries)

        self.btn_showmaps.clicked.connect(self.listmapss)
        self.lv_showmaps.doubleClicked.connect(self.showmaps)
        self.btn_run.clicked.connect(self.runpro)
        self.btn_LAImin.clicked.connect(self.addLAImin)

    def CheckThreads(self, Threads):
        freemom = psutil.virtual_memory()[-1] / 1024 / 1024 / 1024  # in GB
        print("Current Free Memory : {} Gb".format(freemom))
        if (freemom > int(dbconfig['memorythreads'])):
            for count, t in enumerate(Threads):
                freemom = psutil.virtual_memory()[-1] / 1024 / 1024 / 1024  # in GB
                print("Current Free Memory : {} Gb".format(freemom))
                if (freemom > int(dbconfig['memorythreads'])):
                    if t.finished == False and t.started == False:
                        print("{} will start now".format(t))
                        t.start()
                        time.sleep(
                            30)  # this time sleeping is to wait the preprocessing thing/ modeling buffering memory
                        if (t == Threads[-1]):
                            t.join()
                    if t.finished == True:
                        if t.erroned == True:
                            print("{} is erroned !".format(t.getName()))
                    else:
                        print("{} is running !".format(t.getName()))
                else:
                    print("no free memory, we'll sleep for 30 seconds before trying again")
                    time.sleep(30)
                    self.CheckThreads((Threads))

            _ALL = []

            for count, t in enumerate(Threads):
                if t.erroned or t.finished:
                    print("Checking  {}".format(t.sub))
                    _ALL.append(True)
                else:
                    _ALL.append(False)
            if False in (_ALL):
                self.CheckThreads(Threads)

        else:
            print("no free memory, we'll sleep for 30 seconds before trying again")
            time.sleep(30)
            self.CheckThreads((Threads))


class Basic_Dialog(object):
    def setupUi(self, Dialog, main):
        self.main = main
        Dialog.setObjectName(_fromUtf8("Dialog"))

        Dialog.resize(752, 212)
        self.groupBox_0 = QtGui.QGroupBox(Dialog)
        self.groupBox_0.setGeometry(QtCore.QRect(20, 20, 700, 100))
        self.groupBox_0.setObjectName(_fromUtf8("groupBox_0"))

        self.groupBox_1 = QtGui.QGroupBox(self.groupBox_0)
        self.groupBox_1.setGeometry(QtCore.QRect(340, 20, 350, 60))
        self.groupBox_1.setObjectName(_fromUtf8("groupBox_1"))

        self.label = QtGui.QLabel(self.groupBox_0)
        self.label.setGeometry(QtCore.QRect(20, 40, 150, 21))
        self.label.setObjectName(_fromUtf8("label"))

        self.le_NSubs = QtGui.QLineEdit(self.groupBox_0)
        self.le_NSubs.setGeometry(QtCore.QRect(180, 40, 51, 20))
        self.le_NSubs.setText(_fromUtf8(""))
        self.le_NSubs.setObjectName(_fromUtf8("le_NSubs"))
        self.le_NSubs.setValidator(QtGui.QIntValidator(0, 99999, self.le_NSubs))

        self.le_SRCC = QtGui.QLineEdit(self.groupBox_1)
        self.le_SRCC.setGeometry(QtCore.QRect(20, 20, 281, 20))
        self.le_SRCC.setObjectName(_fromUtf8("le_SRCC"))

        self.tb_SRCC = QtGui.QToolButton(self.groupBox_1)
        self.tb_SRCC.setGeometry(QtCore.QRect(310, 20, 25, 19))
        self.tb_SRCC.setObjectName(_fromUtf8("tb_SRCC"))

        self.btn_run = QtGui.QPushButton(Dialog)
        self.btn_run.setGeometry(QtCore.QRect(300, 150, 151, 41))
        self.btn_run.setObjectName(_fromUtf8("btn_run"))

        self.retranslateUi(Dialog)
        self.SetUpActions()
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.closeEvent = self.closeEvent

    def closeEvent(self, diag):
        self.main.show()

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Wetspa_Urban : Basic", None))
        self.groupBox_0.setTitle(_translate("Dialog", "Inputs ", None))
        self.groupBox_1.setTitle(_translate("Dialog", "Surface runoff core code ", None))
        self.label.setText(_translate("Dialog", "Number of subcatchements : ", None))
        self.btn_run.setText(_translate("Dialog", "Run", None))
        self.tb_SRCC.setText(_translate("Dialog", "...", None))

    def tb_SRCC_fun(self):
        fname = QFileDialog.getExistingDirectory(None, "Select Directory")
        self.le_SRCC.setText(fname)

    def btn_run_fun(self):

        dir_number = self.le_NSubs.text()
        src_dir = str(self.le_SRCC.text())  # +'\\'
        self.main.dir_numb = dir_number

        if ((dir_number.replace(" ", "") != '') and (src_dir.replace(" ", "") != '')):

            if not os.path.exists('C:/TMP'):
                os.makedirs('C:/TMP')
            for i in range(1, int(dir_number) + 1):
                if not os.path.exists('C:/TMP/' + str(i)):
                    os.makedirs('C:/TMP/' + str(i))
                dest = 'C:/TMP/' + str(i) + '/' + src_dir.split('\\')[-1]  # +'\\'
                # print dest

                if not os.path.exists(dest):
                    copytree(src_dir, dest)

            if not os.path.exists('output'):
                os.makedirs('output')
            for i in range(1, int(dir_number) + 1):
                if not os.path.exists('output/' + str(i)):
                    os.makedirs('output/' + str(i))

            print 'Finished with success'


        else:
            print 'Please fill all fields before run'

    def SetUpActions(self):
        self.tb_SRCC.clicked.connect(self.tb_SRCC_fun)
        self.btn_run.clicked.connect(self.btn_run_fun)


class Sewer_Dialog(object):
    def setupUi(self, Dialog, main):
        self.main = main
        Dialog.setObjectName(_fromUtf8("Dialog"))
        self.settings = read_settings()

        Dialog.resize(700, 550)
        self.groupBox_0 = QtGui.QGroupBox(Dialog)
        self.groupBox_0.setGeometry(QtCore.QRect(20, 20, 650, 75))
        self.groupBox_0.setObjectName(_fromUtf8("groupBox_0"))

        self.label = QtGui.QLabel(self.groupBox_0)
        self.label.setGeometry(QtCore.QRect(20, 30, 210, 21))
        self.label.setObjectName(_fromUtf8("label"))

        self.le_NSubs = QtGui.QLineEdit(self.groupBox_0)
        self.le_NSubs.setGeometry(QtCore.QRect(250, 30, 51, 20))
        self.le_NSubs.setText(_fromUtf8(""))
        self.le_NSubs.setObjectName(_fromUtf8("le_NSubs"))
        self.le_NSubs.setValidator(QtGui.QIntValidator(0, 99999, self.le_NSubs))

        self.btn_validate = QtGui.QPushButton(self.groupBox_0)
        self.btn_validate.setGeometry(QtCore.QRect(530, 25, 100, 30))
        self.btn_validate.setObjectName(_fromUtf8("btn_validate"))

        self.groupBox_1 = QtGui.QGroupBox(Dialog)
        self.groupBox_1.setGeometry(QtCore.QRect(20, 120, 500, 400))
        self.groupBox_1.setObjectName(_fromUtf8("groupBox_1"))

        self.label2 = QtGui.QLabel(self.groupBox_1)
        self.label2.setGeometry(QtCore.QRect(80, 30, 210, 21))
        self.label2.setObjectName(_fromUtf8("label2"))

        self.cb1 = QtGui.QComboBox(self.groupBox_1)
        self.cb1.setGeometry(QtCore.QRect(280, 30, 100, 25))
        self.cb1.setObjectName('cb1')

        self.groupBox_2 = QtGui.QGroupBox(self.groupBox_1)
        self.groupBox_2.setGeometry(QtCore.QRect(20, 90, 150, 250))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))

        self.list = QtGui.QListWidget(self.groupBox_2)
        self.list.setGeometry(QtCore.QRect(20, 20, 110, 180))
        self.list.setObjectName('list')
        self.list.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.list.setVerticalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        self.list.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)

        for i in range(len(os.listdir('C:/TMP'))):
            self.list.addItem(str(i + 1))

        self.btn_select = QtGui.QPushButton(self.groupBox_1)
        self.btn_select.setGeometry(QtCore.QRect(210, 145, 80, 25))
        self.btn_select.setObjectName(_fromUtf8("btn_select"))
        self.btn_select.setEnabled(False)

        self.btn_deselect = QtGui.QPushButton(self.groupBox_1)
        self.btn_deselect.setGeometry(QtCore.QRect(210, 195, 80, 25))
        self.btn_deselect.setObjectName(_fromUtf8("btn_deselect"))
        self.btn_deselect.setEnabled(False)

        self.groupBox_3 = QtGui.QGroupBox(self.groupBox_1)
        self.groupBox_3.setGeometry(QtCore.QRect(330, 90, 150, 250))
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))

        self.list2 = QtGui.QListWidget(self.groupBox_3)
        self.list2.setGeometry(QtCore.QRect(20, 20, 110, 180))
        self.list2.setObjectName('list2')
        self.list2.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.list2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.list2.setVerticalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)

        self.btn_save = QtGui.QPushButton(Dialog)
        self.btn_save.setGeometry(QtCore.QRect(550, 125, 100, 30))
        self.btn_save.setObjectName(_fromUtf8("btn_save"))

        self.btn_sum = QtGui.QPushButton(Dialog)
        self.btn_sum.setGeometry(QtCore.QRect(550, 400, 120, 41))
        self.btn_sum.setObjectName(_fromUtf8("btn_sum"))

        self.btn_run = QtGui.QPushButton(Dialog)
        self.btn_run.setGeometry(QtCore.QRect(550, 480, 120, 41))
        self.btn_run.setObjectName(_fromUtf8("btn_run"))

        self.retranslateUi(Dialog)
        self.SetUpActions()
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.closeEvent = self.closeEvent

    def closeEvent(self, diag):
        self.main.show()

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Wetspa_Urban : Aggregated Subcatchement", None))
        self.groupBox_0.setTitle(_translate("Dialog", "Inputs ", None))
        self.groupBox_1.setTitle(_translate("Dialog", "Subs Association ", None))
        self.groupBox_2.setTitle(_translate("Dialog :", "Available Subs:  ", None))
        self.groupBox_3.setTitle(_translate("Dialog :", "Selected Subs:  ", None))
        self.label.setText(_translate("Dialog", "Number of aggregated subcatchements : ", None))
        self.label2.setText(_translate("Dialog", "Aggregated subcatchement : ", None))
        self.btn_run.setText(_translate("Dialog", "Run Sewer Model", None))
        self.btn_sum.setText(_translate("Dialog", "Sum Subs", None))
        self.btn_save.setText(_translate("Dialog", "Save", None))
        self.btn_validate.setText(_translate("Dialog", "New ", None))
        self.btn_select.setText(_translate("Dialog", "Select  >>", None))
        self.btn_deselect.setText(_translate("Dialog", "<<  Unselect", None))

    def btn_validate_fun(self):
        self.settings = {'folder_number': len(os.listdir('C:/TMP')), 'available': [], 'associations': {}}
        for i in range(1, len(os.listdir('C:/TMP')) + 1):
            self.settings['available'].append(i)
        self.cb1.clear()
        for i in range(1, int(self.le_NSubs.text()) + 1):
            self.cb1.addItem(str(i))
            self.settings['associations'][str(i)] = []

        self.btn_select.setEnabled(True)
        self.btn_deselect.setEnabled(True)

    def btn_select_fun(self):

        for item in self.list.selectedItems():
            self.settings['associations'][str(self.cb1.currentText())].append(int(item.text()))
            self.settings['available'].remove(int(item.text()))
        self.list2.clear()

        self.settings['associations'][str(self.cb1.currentText())].sort()
        for item in self.settings['associations'][str(self.cb1.currentText())]:
            self.list2.addItem(str(item))

        for item in self.list.selectedItems():
            self.list.takeItem(self.list.row(item))

    def btn_deselect_fun(self):
        for item in self.list2.selectedItems():
            self.settings['associations'][str(self.cb1.currentText())].remove(int(item.text()))
            self.settings['available'].append(int(item.text()))
            self.list2.takeItem(self.list2.row(item))

        self.settings['available'].sort()
        self.list.clear()
        for item in self.settings['available']:
            self.list.addItem(str(item))

    def cb1_change_fun(self):
        self.list2.clear()
        self.settings['associations'][str(self.cb1.currentText())].sort()
        for item in self.settings['associations'][str(self.cb1.currentText())]:
            self.list2.addItem(str(item))

    def btn_save_fun(self):
        save_settings(self.settings)

    def btn_sum_fun(self):

        for aggre in self.settings['associations']:

            content = []
            if len(self.settings['associations'][aggre]) != 0:

                for subs in self.settings['associations'][aggre]:
                    with open('C:/TMP/' + str(subs) + '/Runner/catchment/OF.tss', 'r') as inputfile:
                        content.append(inputfile.readlines())

                with open('C:/TMP/' + aggre + '/Runner/catchment/diss.tss', 'w') as outputfile:

                    for line_num in range(len(content[0])):

                        if line_num < 4:
                            outputfile.write(content[0][line_num])
                        else:
                            res_line = 0
                            for file in content:
                                if len(file) != 0:
                                    # print line_num, file[line_num].split(str(line_num-3),1)[1].replace(' ','')
                                    res_line += float(file[line_num].split(str(line_num - 3), 1)[1].replace(' ',
                                                                                                            ''))  # .split('\t')#[1].rstrip('\n')
                            # print line_num, res_line
                            indent = len(str(line_num - 3)) - 1  # , str(line_num)
                            space = '        '[indent:]
                            outputfile.write(space + str(line_num - 3) + '        ' + str(res_line) + '\n')

    def SetUpActions(self):
        self.cb1.activated.connect(self.cb1_change_fun)
        self.btn_validate.clicked.connect(self.btn_validate_fun)
        self.btn_select.clicked.connect(self.btn_select_fun)
        self.btn_deselect.clicked.connect(self.btn_deselect_fun)
        self.btn_save.clicked.connect(self.btn_save_fun)
        self.btn_run.clicked.connect(self.old_sewer)
        self.btn_sum.clicked.connect(self.btn_sum_fun)

    def old_sewer(self):
        # print self.settings
        # read timestepsvariables
        _conf = os.path.join(dbconfig['tmp'], str(1), dbconfig['catchment'], dbconfig['configuration'])
        _f = open(_conf, 'r')
        _allconf = _f.read().split("\n")
        _f.close()
        _conf = {}
        for c in _allconf:
            if 'TIMESTEPS' in c:
                _conf[c.split()[0]] = c.split()[2]
            if 'SIMULATION_START_DATE' in c:
                _conf[c.split()[0]] = c.split()[2]
        # read values from tss file
        files = [f for f in os.listdir(dbconfig['tmp'])
                 if (os.path.isdir(os.path.join(dbconfig['tmp'], f)) and (f in self.settings['associations']))]
        # print files
        subs = []
        for f in files:
            number = True
            try:
                int(f)
            except:
                number = False
            if number:
                subs.append(os.path.join(dbconfig['tmp'], f, dbconfig['dis'].replace('dis.tss', 'diss.tss')))

        print '#######', subs

        for sub in subs:

            f = open(sub, 'r')
            _list = f.read().split("\n")[4:]
            f.close()
            _vals = []
            for _l in _list:
                aa = _l.split("\t")
                aa = aa[0].split()
                if len(aa) != 0:
                    _vals.append(aa)
            _dates = (str(datetime.timedelta(seconds=int(_conf['TIMESTEPS'])))).split(':')
            _start_date = datetime.datetime(int(_conf['SIMULATION_START_DATE'].split("/")[-1]),
                                            int(_conf['SIMULATION_START_DATE'].split("/")[-2])
                                            , int(_conf['SIMULATION_START_DATE'].split("/")[0])
                                            , 0, 0, 0)
            b = _start_date
            _st = _start_date
            # open a file and write data there
            _dir = "\\".join(sub.split("\\")[:-1])
            _datafile = os.path.join(_dir, "dis.dat")
            dt = open(_datafile, "w")
            dt.write(";Flow\n"
                     ";Date    Time    Flow [m3/s] \n")
            print(_vals)
            if _start_date.minute < 10:
                dt.write(str(_start_date.strftime("%m/%d/%Y")) + """\t{}:0{}""".format(str(_start_date.hour),
                                                                                       str(_start_date.minute)) + "\t" +
                         _vals[0][1] + "\n")
            else:
                dt.write(str(_start_date.strftime("%m/%d/%Y")) + """\t{}:{}""".format(str(_start_date.hour),
                                                                                      str(_start_date.minute)) + "\t" +
                         _vals[0][1] + "\n")
            for timestep in range(1, len(_vals)):
                if timestep > len(_vals) - 1:
                    break

                b = b + datetime.timedelta(0, int(_conf['TIMESTEPS']))  # days, seconds, then other fields.

                if b.date() > _st.date():
                    _st = b
                    if _start_date.minute < 10:
                        dt.write(str(_st.strftime("%m/%d/%Y")) + """\t{}:0{}""".format(str(_st.hour),
                                                                                       str(_st.minute)) + "\t" +
                                 _vals[timestep][1] + "\n")
                    else:
                        dt.write(str(_st.strftime("%m/%d/%Y")) + """\t{}:{}""".format(str(_st.hour),
                                                                                      str(_st.minute)) + "\t" +
                                 _vals[timestep][1] + "\n")
                else:
                    if b.minute < 10:
                        dt.write("\t" + str(b.hour) + ':0' + str(b.minute) + "\t" + _vals[timestep][1] + "\n")
                    else:
                        dt.write("\t" + str(b.hour) + ':' + str(b.minute) + "\t" + _vals[timestep][1] + "\n")

            dt.close()

        _INP = os.path.join(dbconfig['tmp'], 'Final.inp')

        timeseries = False
        files = [f for f in os.listdir(dbconfig['tmp'])
                 if ((os.path.isdir(os.path.join(dbconfig['tmp'], f)) and (f in self.settings['associations'])))]
        subs = []
        for f in files:
            number = True
            try:
                int(f)
            except:
                number = False
            if number:
                subs.append(os.path.join(dbconfig['tmp'], f, dbconfig['dat'].replace('dis.tss', 'diss.tss')))

        print(subs)
        f = open(_INP, 'r')
        _listsplitting = f.read().split("\n")
        f.close()
        _linenumber = 0
        # check whether timeseries and INLFOWS included
        for n, _line in enumerate(_listsplitting):
            if '[TIMESERIES]' in _line:
                timeseries = True
                _linenumber = n
                print("linenumber Timeseries {}".format(_linenumber))
                break

        # case included
        if timeseries:
            print ("I'm in timeseries")
            # we will extract the content of timeseries part
            _firsthalf = _listsplitting[_linenumber:]
            _end = 0
            found = False
            _tmp_num = 0
            for n, _line in enumerate(_firsthalf):
                if ('[' in _line) and ("TIMESERIES" not in _line):
                    found = True
                    _tmp_num = n
                    break
            _timeseries_list = _firsthalf[:_tmp_num]
            _toadd = []

            if _timeseries_list[-1] != ';':
                for n, sub in enumerate(subs):
                    _timeseries_list.append(';')
                    _timeseries_list.append("""{}      FILE "{}" """.format(n + 1, sub))
                _timeseries_list.append('')

            _newf = _listsplitting[:_linenumber] + _timeseries_list + _listsplitting[_linenumber + _tmp_num:]
            # same job for INFLOWS
            #########################################################################################
            for n, _line in enumerate(_newf):
                if '[INFLOWS]' in _line:
                    timeseries = True
                    _linenumber = n
                    print("linenumber of Inflows {}".format(_linenumber))

                    break

            _firsthalf = _newf[_linenumber:]
            _end = 0
            found = False
            _tmp_num = 0
            for n, _line in enumerate(_firsthalf):
                if ('[' in _line) and ("INFLOWS" not in _line):
                    found = True
                    _tmp_num = n
                    break
            _inflows_list = _firsthalf[:_tmp_num]
            _toadd = []
            if _inflows_list[-1] != ';':
                for n, sub in enumerate(subs):
                    _inflows_list.append(
                        """{}\t\t\t\t FLOW \t\t\t\t {}\t\t\t\tFLOW     1.0      1.0""".format(n + 1, n + 1))
                _inflows_list.append('')
            _newf = _newf[:_linenumber] + _inflows_list + _newf[_linenumber + _tmp_num:]
            try:
                a = open(os.path.join(dbconfig['tmp'], 'tmp.inp'), "w")
                a.write("\n".join(_newf))
                a.close()
            except Exception as e:
                print (e)
        else:

            # Manually inject
            _Manuallist = []
            _Manuallist.append('[TIMESERIES]')
            _Manuallist.append(";;Name           Date       Time       Value     ")
            _Manuallist.append(";;-------------- ---------- ---------- ----------")
            for n, sub in enumerate(subs):
                _Manuallist.append("""{}      FILE "{}" """.format(n + 1, sub))
                _Manuallist.append(';')

            _Manuallist.pop()
            _Manuallist.append('')
            _Manuallist.append(("[INFLOWS]"))

            for n, sub in enumerate(subs):
                _Manuallist.append("""{}\t\t\t\t FLOW \t\t\t\t {}\t\t\t\tFLOW     1.0      1.0""".format(n + 1, n + 1))
            _Manuallist.append('')

            for ele in _Manuallist:
                _listsplitting.append(ele)
            a = open(os.path.join(dbconfig['tmp'], 'tmp.inp'), "w")
            a.write("\n".join(_listsplitting))
            a.close()

        # now we run, run,run
        _QUERY = """{} {} {}""".format(os.path.join(dbconfig['tmp'], 'swmm5.exe'),
                                       os.path.join(dbconfig['tmp'], 'tmp.inp'),
                                       os.path.join(dbconfig['tmp'], 'tmp.rpt'))
        subprocess.Popen(_QUERY)


class LID_Loc_Dialog(object):
    def __init__(self):

        self.comb_algs = {}
        self.outputAll = maps.Map()
        self.outputPref = maps.Map()

    def setupUi(self, Dialog, main):
        self.main = main
        Dialog.setObjectName(_fromUtf8("Dialog"))

        Dialog.resize(1850, 780)

        # Input Maps
        self.groupBox_InputMaps = QtGui.QGroupBox(Dialog)
        self.groupBox_InputMaps.setGeometry(QtCore.QRect(10, 10, 361, 390))
        self.groupBox_InputMaps.setObjectName(_fromUtf8("groupBox_InputMaps"))

        # Ground Water
        self.groupBox_GW = QtGui.QGroupBox(self.groupBox_InputMaps)
        self.groupBox_GW.setGeometry(QtCore.QRect(10, 20, 341, 41))
        self.groupBox_GW.setObjectName(_fromUtf8("groupBox_GW"))
        self.tb_GW = QtGui.QToolButton(self.groupBox_GW)
        self.tb_GW.setGeometry(QtCore.QRect(310, 20, 25, 19))
        self.tb_GW.setObjectName(_fromUtf8("tb_GW"))
        self.le_GW = QtGui.QLineEdit(self.groupBox_GW)
        self.le_GW.setGeometry(QtCore.QRect(20, 20, 281, 20))
        self.le_GW.setObjectName(_fromUtf8("le_GW"))
        self.le_GW.setText("C:/Users/nrezazad/Desktop/watermaelbeek_38 - Copy/Runner/catchment/parammaps/gw.asc")


        # Parcel
        self.groupBox_Parcel = QtGui.QGroupBox(self.groupBox_InputMaps)
        self.groupBox_Parcel.setGeometry(QtCore.QRect(10, 60, 341, 41))
        self.groupBox_Parcel.setObjectName(_fromUtf8("groupBox_Parcel"))
        self.tb_Parcel = QtGui.QToolButton(self.groupBox_Parcel)
        self.tb_Parcel.setGeometry(QtCore.QRect(310, 20, 25, 19))
        self.tb_Parcel.setObjectName(_fromUtf8("tb_Parcel"))
        self.le_Parcel = QtGui.QLineEdit(self.groupBox_Parcel)
        self.le_Parcel.setGeometry(QtCore.QRect(20, 20, 281, 20))
        self.le_Parcel.setObjectName(_fromUtf8("le_Parcel"))
        self.le_Parcel.setText("C:/Users/nrezazad/Desktop/watermaelbeek_38 - Copy/Runner/catchment/parammaps/parcel.asc")

        # Detailed Land use
        self.groupBox_DlandUse = QtGui.QGroupBox(self.groupBox_InputMaps)
        self.groupBox_DlandUse.setGeometry(QtCore.QRect(10, 100, 341, 41))
        self.groupBox_DlandUse.setObjectName(_fromUtf8("groupBox_DlandUse"))
        self.tb_DlandUse = QtGui.QToolButton(self.groupBox_DlandUse)
        self.tb_DlandUse.setGeometry(QtCore.QRect(310, 20, 25, 19))
        self.tb_DlandUse.setObjectName(_fromUtf8("tb_DlandUse"))
        self.le_DlandUse = QtGui.QLineEdit(self.groupBox_DlandUse)
        self.le_DlandUse.setGeometry(QtCore.QRect(20, 20, 281, 20))
        self.le_DlandUse.setObjectName(_fromUtf8("le_DlandUse"))
        self.le_DlandUse.setText("C:/Users/nrezazad/Desktop/watermaelbeek_38 - Copy/Runner/catchment/parammaps/detailedlandusemap.asc")

        # Water Shed
        self.groupBox_Wshed = QtGui.QGroupBox(self.groupBox_InputMaps)
        self.groupBox_Wshed.setGeometry(QtCore.QRect(10, 140, 341, 41))
        self.groupBox_Wshed.setObjectName(_fromUtf8("groupBox_Wshed"))
        self.tb_Wshed = QtGui.QToolButton(self.groupBox_Wshed)
        self.tb_Wshed.setGeometry(QtCore.QRect(310, 20, 25, 19))
        self.tb_Wshed.setObjectName(_fromUtf8("tb_Wshed"))
        self.le_Wshed = QtGui.QLineEdit(self.groupBox_Wshed)
        self.le_Wshed.setGeometry(QtCore.QRect(20, 20, 281, 20))
        self.le_Wshed.setObjectName(_fromUtf8("le_Wshed"))
        self.le_Wshed.setText("C:/Users/nrezazad/Desktop/meteo/watershed.asc")

        # landuse for whole catchment
        self.groupBox_Landuse = QtGui.QGroupBox(self.groupBox_InputMaps)
        self.groupBox_Landuse.setGeometry(QtCore.QRect(10, 180, 341, 41))
        self.groupBox_Landuse.setObjectName(_fromUtf8("groupBox_Landuse"))
        self.tb_Landuse = QtGui.QToolButton(self.groupBox_Landuse)
        self.tb_Landuse.setGeometry(QtCore.QRect(310, 20, 25, 19))
        self.tb_Landuse.setObjectName(_fromUtf8("tb_Landuse"))
        self.le_Landuse = QtGui.QLineEdit(self.groupBox_Landuse)
        self.le_Landuse.setGeometry(QtCore.QRect(20, 20, 281, 20))
        self.le_Landuse.setObjectName(_fromUtf8("le_Landuse"))
        self.le_Landuse.setText("C:/Users/nrezazad/Desktop/watermaelbeek_38 - Copy/Runner/catchment/parammaps/landuse.asc")

        # soil for whole catchment
        self.groupBox_Soil = QtGui.QGroupBox(self.groupBox_InputMaps)
        self.groupBox_Soil.setGeometry(QtCore.QRect(10, 220, 341, 41))
        self.groupBox_Soil.setObjectName(_fromUtf8("groupBox_Soil"))
        self.tb_Soil = QtGui.QToolButton(self.groupBox_Soil)
        self.tb_Soil.setGeometry(QtCore.QRect(310, 20, 25, 19))
        self.tb_Soil.setObjectName(_fromUtf8("tb_Soil"))
        self.le_Soil = QtGui.QLineEdit(self.groupBox_Soil)
        self.le_Soil.setGeometry(QtCore.QRect(20, 20, 281, 20))
        self.le_Soil.setObjectName(_fromUtf8("le_Soil"))
        self.le_Soil.setText("C:/Users/nrezazad/Desktop/watermaelbeek_38 - Copy/Runner/catchment/parammaps/soil.asc")

        # elev for whole catchment
        self.groupBox_Elev = QtGui.QGroupBox(self.groupBox_InputMaps)
        self.groupBox_Elev.setGeometry(QtCore.QRect(10, 260, 341, 41))
        self.groupBox_Elev.setObjectName(_fromUtf8("groupBox_Elev"))
        self.tb_Elev = QtGui.QToolButton(self.groupBox_Elev)
        self.tb_Elev.setGeometry(QtCore.QRect(310, 20, 25, 19))
        self.tb_Elev.setObjectName(_fromUtf8("tb_Elev"))
        self.le_Elev = QtGui.QLineEdit(self.groupBox_Elev)
        self.le_Elev.setGeometry(QtCore.QRect(20, 20, 281, 20))
        self.le_Elev.setObjectName(_fromUtf8("le_Elev"))
        self.le_Elev.setText("C:/Users/nrezazad/Desktop/watermaelbeek_38 - Copy/Runner/catchment/parammaps/elevation.asc")

        # inp file
        self.groupBox_inp = QtGui.QGroupBox(self.groupBox_InputMaps)
        self.groupBox_inp.setGeometry(QtCore.QRect(10, 300, 341, 41))
        self.groupBox_inp.setObjectName(_fromUtf8("groupBox_inp"))
        self.tb_inp = QtGui.QToolButton(self.groupBox_inp)
        self.tb_inp.setGeometry(QtCore.QRect(310, 20, 25, 19))
        self.tb_inp.setObjectName(_fromUtf8("tb_inp"))
        self.le_inp = QtGui.QLineEdit(self.groupBox_inp)
        self.le_inp.setGeometry(QtCore.QRect(20, 20, 281, 20))
        self.le_inp.setObjectName(_fromUtf8("le_inp"))
        self.le_inp.setText("C:/TMP/tmp.inp")

        # rpt file

        self.groupBox_rpt = QtGui.QGroupBox(self.groupBox_InputMaps)
        self.groupBox_rpt.setGeometry(QtCore.QRect(10, 340, 341, 41))
        self.groupBox_rpt.setObjectName(_fromUtf8("groupBox_rpt"))
        self.tb_rpt = QtGui.QToolButton(self.groupBox_rpt)
        self.tb_rpt.setGeometry(QtCore.QRect(310, 20, 25, 19))
        self.tb_rpt.setObjectName(_fromUtf8("tb_inp"))
        self.le_rpt = QtGui.QLineEdit(self.groupBox_rpt)
        self.le_rpt.setGeometry(QtCore.QRect(20, 20, 281, 20))
        self.le_rpt.setObjectName(_fromUtf8("le_inp"))
        self.le_rpt.setText("")


        # Building Parammap for whole catchment
        self.groupBox_Building_Parammap = QtGui.QGroupBox(Dialog)
        self.groupBox_Building_Parammap.setGeometry(QtCore.QRect(10, 400, 361, 300))
        self.groupBox_Building_Parammap.setObjectName(_fromUtf8("groupBox_Building_Parammap"))

        self.btn_DefinePara = QtGui.QPushButton(self.groupBox_Building_Parammap)
        self.btn_DefinePara.setGeometry(QtCore.QRect(40, 22, 130, 40))
        self.btn_DefinePara.setObjectName(_fromUtf8("btn_DefinePara"))
        self.btn_RunPre = QtGui.QPushButton(self.groupBox_Building_Parammap)
        self.btn_RunPre.setGeometry(QtCore.QRect(190, 22, 130, 40))
        self.btn_RunPre.setObjectName(_fromUtf8("btn_RunPre"))

        self.groupBox_See_gen_maps = QtGui.QGroupBox(self.groupBox_Building_Parammap)
        self.groupBox_See_gen_maps.setGeometry(QtCore.QRect(20, 310, 360, 161))
        self.groupBox_See_gen_maps.setObjectName(_fromUtf8("groupBox_See_gen_maps"))
        self.lv_parammapWhole = QtGui.QListView(self.groupBox_See_gen_maps)
        self.lv_parammapWhole.setGeometry(QtCore.QRect(10, 20, 171, 91))
        self.lv_parammapWhole.setObjectName(_fromUtf8("lv_parammapWhole"))
        self.btn_show_maps_whole = QtGui.QPushButton(self.groupBox_See_gen_maps)
        self.btn_show_maps_whole.setGeometry(QtCore.QRect(100, 120, 91, 31))
        self.btn_show_maps_whole.setObjectName(_fromUtf8("btn_show_maps_whole"))

        self.le_SubNn = QtGui.QLineEdit(self.groupBox_See_gen_maps)
        self.le_SubNn.setGeometry(QtCore.QRect(200, 60, 51, 20))
        self.le_SubNn.setObjectName(_fromUtf8("le_SubN"))
        self.label_1n = QtGui.QLabel(self.groupBox_See_gen_maps)
        self.label_1n.setGeometry(QtCore.QRect(200, 20, 145, 16))
        self.label_1n.setObjectName(_fromUtf8("label_1"))




        # Search Algs
        self.groupBox_SearchAlgs = QtGui.QGroupBox(Dialog)
        self.groupBox_SearchAlgs.setGeometry(QtCore.QRect(380, 10, 361, 220))
        self.groupBox_SearchAlgs.setObjectName(_fromUtf8("groupBox_SearchAlgs"))

        self.cb_alg1 = QtGui.QCheckBox(self.groupBox_SearchAlgs)
        self.cb_alg1.setGeometry(QtCore.QRect(30, 30, 200, 17))
        self.cb_alg1.setObjectName(_fromUtf8("cb_alg1"))

        self.cb_alg2 = QtGui.QCheckBox(self.groupBox_SearchAlgs)
        self.cb_alg2.setGeometry(QtCore.QRect(30, 50, 200, 17))
        self.cb_alg2.setObjectName(_fromUtf8("cb_alg2"))

        self.cb_alg3 = QtGui.QCheckBox(self.groupBox_SearchAlgs)
        self.cb_alg3.setGeometry(QtCore.QRect(30, 70, 200, 17))
        self.cb_alg3.setObjectName(_fromUtf8("cb_alg3"))

        self.cb_alg4 = QtGui.QCheckBox(self.groupBox_SearchAlgs)
        self.cb_alg4.setGeometry(QtCore.QRect(30, 90, 200, 17))
        self.cb_alg4.setObjectName(_fromUtf8("cb_alg4"))

        self.cb_alg5 = QtGui.QCheckBox(self.groupBox_SearchAlgs)
        self.cb_alg5.setGeometry(QtCore.QRect(30, 110, 200, 17))
        self.cb_alg5.setObjectName(_fromUtf8("cb_alg5"))

        self.cb_alg6 = QtGui.QCheckBox(self.groupBox_SearchAlgs)
        self.cb_alg6.setGeometry(QtCore.QRect(30, 130, 200, 17))
        self.cb_alg6.setObjectName(_fromUtf8("cb_alg6"))

        self.cb_alg7 = QtGui.QCheckBox(self.groupBox_SearchAlgs)
        self.cb_alg7.setGeometry(QtCore.QRect(30, 150, 200, 17))
        self.cb_alg7.setObjectName(_fromUtf8("cb_alg7"))

        self.cb_alg8 = QtGui.QCheckBox(self.groupBox_SearchAlgs)
        self.cb_alg8.setGeometry(QtCore.QRect(30, 170, 200, 17))
        self.cb_alg8.setObjectName(_fromUtf8("cb_alg8"))

        self.cb_alg9 = QtGui.QCheckBox(self.groupBox_SearchAlgs)
        self.cb_alg9.setGeometry(QtCore.QRect(30, 190, 200, 17))
        self.cb_alg9.setObjectName(_fromUtf8("cb_alg9"))

        # High Potential
        self.groupBox_High_Potential = QtGui.QGroupBox(Dialog)
        self.groupBox_High_Potential.setGeometry(QtCore.QRect(380, 230, 361, 400))
        self.groupBox_High_Potential.setObjectName(_fromUtf8("groupBox_High_Potential"))

        self.label_Runoff = QtGui.QLabel(self.groupBox_High_Potential)
        self.label_Runoff.setGeometry(QtCore.QRect(20, 40, 230, 21))
        self.label_Runoff.setObjectName(_fromUtf8("label_Runoff"))

        self.le_Runoff = QtGui.QLineEdit(self.groupBox_High_Potential)
        self.le_Runoff.setGeometry(QtCore.QRect(190, 40, 51, 20))
        self.le_Runoff.setText(_fromUtf8(""))
        self.le_Runoff.setObjectName(_fromUtf8("le_Runoff"))
        self.le_Runoff.setText("X")

        self.label_Lambda = QtGui.QLabel(self.groupBox_High_Potential)
        self.label_Lambda.setGeometry(QtCore.QRect(20, 80, 230, 21))
        self.label_Lambda.setObjectName(_fromUtf8("label_Lambda"))

        self.le_Lambda = QtGui.QLineEdit(self.groupBox_High_Potential)
        self.le_Lambda.setGeometry(QtCore.QRect(190, 80, 51, 20))
        self.le_Lambda.setText(_fromUtf8(""))
        self.le_Lambda.setObjectName(_fromUtf8("le_Lambda"))
        self.le_Lambda.setText("X")

        self.label_Number_of_subc = QtGui.QLabel(self.groupBox_High_Potential)
        self.label_Number_of_subc.setGeometry(QtCore.QRect(20, 120, 160, 21))
        self.label_Number_of_subc.setObjectName(_fromUtf8("label_Number_of_subc"))

        self.le_Number_of_subc = QtGui.QLineEdit(self.groupBox_High_Potential)
        self.le_Number_of_subc.setGeometry(QtCore.QRect(190, 120, 51, 20))
        self.le_Number_of_subc.setText(_fromUtf8(""))
        self.le_Number_of_subc.setObjectName(_fromUtf8("le_Number_of_subc"))
        self.le_Number_of_subc.setText("X")

        self.label_Flow = QtGui.QLabel(self.groupBox_High_Potential)
        self.label_Flow.setGeometry(QtCore.QRect(20, 160, 160, 21))
        self.label_Flow.setObjectName(_fromUtf8("label_Flow"))

        self.le_Flow = QtGui.QLineEdit(self.groupBox_High_Potential)
        self.le_Flow.setGeometry(QtCore.QRect(190, 160, 51, 20))
        self.le_Flow.setText(_fromUtf8(""))
        self.le_Flow.setObjectName(_fromUtf8("le_Flow"))
        self.le_Flow.setText("X")

        self.label_Nodes = QtGui.QLabel(self.groupBox_High_Potential)
        self.label_Nodes.setGeometry(QtCore.QRect(20, 200, 200, 21))
        self.label_Nodes.setObjectName(_fromUtf8("le_Nodes"))

        self.le_Nodes = QtGui.QLineEdit(self.groupBox_High_Potential)
        self.le_Nodes.setGeometry(QtCore.QRect(40, 230, 300, 20))
        self.le_Nodes.setText(_fromUtf8(""))
        self.le_Nodes.setObjectName(_fromUtf8("le_Nodes"))
        self.le_Nodes.setText("X")

        # Result Highpot
        self.groupBox_Result = QtGui.QGroupBox(self.groupBox_High_Potential)
        self.groupBox_Result.setGeometry(QtCore.QRect(20, 260, 320, 130))
        self.groupBox_Result.setObjectName(_fromUtf8("groupBox_Result"))

        self.List_maps = QtGui.QListView(self.groupBox_Result)
        self.List_maps.setGeometry(QtCore.QRect(10, 20, 171, 91))
        self.List_maps.setObjectName(_fromUtf8("List_maps"))
        self.btn_List_maps = QtGui.QPushButton(self.groupBox_Result)
        self.btn_List_maps.setGeometry(QtCore.QRect(200, 25, 91, 80))
        self.btn_List_maps.setObjectName(_fromUtf8("btn_List_maps"))

        # Suitable Location
        self.groupBox_Suitable = QtGui.QGroupBox(Dialog)
        self.groupBox_Suitable.setGeometry(QtCore.QRect(750, 10, 361, 430))
        self.groupBox_Suitable.setObjectName(_fromUtf8("groupBox_Suitable"))

        self.label_Depth = QtGui.QLabel(self.groupBox_Suitable)
        self.label_Depth.setGeometry(QtCore.QRect(20, 40, 270, 21))
        self.label_Depth.setObjectName(_fromUtf8("label_Depth"))

        self.le_Depth = QtGui.QLineEdit(self.groupBox_Suitable)
        self.le_Depth.setGeometry(QtCore.QRect(300, 40, 51, 20))
        self.le_Depth.setText(_fromUtf8(""))
        self.le_Depth.setObjectName(_fromUtf8("le_Depth"))
        self.le_Depth.setValidator(QtGui.QIntValidator(0, 99999, self.le_Depth))
        self.le_Depth.setText("X")

        self.label_SuitableSoil = QtGui.QLabel(self.groupBox_Suitable)
        self.label_SuitableSoil.setGeometry(QtCore.QRect(20, 80, 270, 21))
        self.label_SuitableSoil.setObjectName(_fromUtf8("label_SuitableSoil"))

        self.le_SuitableSoil = QtGui.QLineEdit(self.groupBox_Suitable)
        self.le_SuitableSoil.setGeometry(QtCore.QRect(300, 80, 51, 20))
        self.le_SuitableSoil.setText(_fromUtf8(""))
        self.le_SuitableSoil.setObjectName(_fromUtf8("le_SuitableSoil"))
        self.le_SuitableSoil.setText("X")

        self.label_Width_rip = QtGui.QLabel(self.groupBox_Suitable)
        self.label_Width_rip.setGeometry(QtCore.QRect(20, 120, 270, 21))
        self.label_Width_rip.setObjectName(_fromUtf8("label_Width_rip"))

        self.le_Width_rip = QtGui.QLineEdit(self.groupBox_Suitable)
        self.le_Width_rip.setGeometry(QtCore.QRect(300, 120, 51, 20))
        self.le_Width_rip.setText(_fromUtf8(""))
        self.le_Width_rip.setObjectName(_fromUtf8("le_Width"))
        #self.le_Width_rip.setValidator(QtGui.QIntValidator(0, 99999, self.le_Width_rip))
        self.le_Width_rip.setText("X")

        self.label_min_roof = QtGui.QLabel(self.groupBox_Suitable)
        self.label_min_roof.setGeometry(QtCore.QRect(20, 160, 270, 21))
        self.label_min_roof.setObjectName(_fromUtf8("label_min_roof"))

        self.le_min_roof = QtGui.QLineEdit(self.groupBox_Suitable)
        self.le_min_roof.setGeometry(QtCore.QRect(300, 160, 51, 20))
        self.le_min_roof.setText(_fromUtf8(""))
        self.le_min_roof.setObjectName(_fromUtf8("le_min_roof"))
        #self.le_min_roof.setValidator(QtGui.QIntValidator(0, 99999, self.le_min_roof))
        self.le_min_roof.setText("X")

        self.label_max_roof = QtGui.QLabel(self.groupBox_Suitable)
        self.label_max_roof.setGeometry(QtCore.QRect(20, 200, 290, 21))
        self.label_max_roof.setObjectName(_fromUtf8("label_max_roof"))

        self.le_max_roof = QtGui.QLineEdit(self.groupBox_Suitable)
        self.le_max_roof.setGeometry(QtCore.QRect(310, 200, 40, 20))
        self.le_max_roof.setText(_fromUtf8(""))
        self.le_max_roof.setObjectName(_fromUtf8("le_max_roof"))
        self.le_max_roof.setText("X")

        self.label_min_rain = QtGui.QLabel(self.groupBox_Suitable)
        self.label_min_rain.setGeometry(QtCore.QRect(20, 240, 270, 21))
        self.label_min_rain.setObjectName(_fromUtf8("label_min_rain"))

        self.le_min_rain = QtGui.QLineEdit(self.groupBox_Suitable)
        self.le_min_rain.setGeometry(QtCore.QRect(300, 240, 51, 20))
        self.le_min_rain.setText(_fromUtf8(""))
        self.le_min_rain.setObjectName(_fromUtf8("le_min_rain"))
        self.le_min_rain.setValidator(QtGui.QIntValidator(0, 99999, self.le_min_rain))
        self.le_min_rain.setText("X")

        # Result
        self.groupBox_ResultS = QtGui.QGroupBox(self.groupBox_Suitable)
        self.groupBox_ResultS.setGeometry(QtCore.QRect(20, 280, 320, 130))
        self.groupBox_ResultS.setObjectName(_fromUtf8("groupBox_Result"))

        self.List_mapsS = QtGui.QListView(self.groupBox_ResultS)
        self.List_mapsS.setGeometry(QtCore.QRect(10, 20, 171, 91))
        self.List_mapsS.setObjectName(_fromUtf8("List_mapsS"))
        self.btn_List_mapsS = QtGui.QPushButton(self.groupBox_ResultS)
        self.btn_List_mapsS.setGeometry(QtCore.QRect(200, 25, 91, 80))
        self.btn_List_mapsS.setObjectName(_fromUtf8("btn_List_mapsS"))

        # Max Suitable Areas
        self.groupBox_Max = QtGui.QGroupBox(Dialog)
        self.groupBox_Max.setGeometry(QtCore.QRect(750, 450, 361, 250))
        self.groupBox_Max.setObjectName(_fromUtf8("groupBox_Max"))

        self.label_Prioritizing = QtGui.QLabel(self.groupBox_Max)
        self.label_Prioritizing.setGeometry(QtCore.QRect(80, 30, 200, 21))
        self.label_Prioritizing.setObjectName(_fromUtf8("label_Prioritizing"))

        self.le_Prioritizing = QtGui.QLineEdit(self.groupBox_Max)
        self.le_Prioritizing.setGeometry(QtCore.QRect(200, 25, 80, 30))
        self.le_Prioritizing.setText(_fromUtf8(""))
        self.le_Prioritizing.setObjectName(_fromUtf8("le_Prioritizing"))

        self.btn_Max_pref = QtGui.QPushButton(self.groupBox_Max)
        self.btn_Max_pref.setGeometry(QtCore.QRect(70, 60, 220, 40))
        self.btn_Max_pref.setObjectName(_fromUtf8("btn_Max_pref"))

        # Show Result Final
        self.groupBox_ResultFinal = QtGui.QGroupBox(self.groupBox_Max)
        self.groupBox_ResultFinal.setGeometry(QtCore.QRect(20, 110, 320, 130))
        self.groupBox_ResultFinal.setObjectName(_fromUtf8("groupBox_ResultFinal"))

        self.List_mapsFinal = QtGui.QListView(self.groupBox_ResultFinal)
        self.List_mapsFinal.setGeometry(QtCore.QRect(10, 20, 300, 91))
        self.List_mapsFinal.setObjectName(_fromUtf8("List_mapsFinal"))
        # self.btn_List_mapsFinal = QtGui.QPushButton(self.groupBox_ResultFinal)
        # self.btn_List_mapsFinal.setGeometry(QtCore.QRect(200, 25, 91, 80))
        # self.btn_List_mapsFinal.setObjectName(_fromUtf8("btn_List_mapsFinal"))

        # Cost opt

        self.groupBox_cost = QtGui.QGroupBox(Dialog)
        self.groupBox_cost.setGeometry(QtCore.QRect(1125, 10, 280, 350))
        self.groupBox_cost.setObjectName(_fromUtf8("groupBox_cost"))

        self.label_percentage_source = QtGui.QLabel(self.groupBox_cost)
        self.label_percentage_source.setGeometry(QtCore.QRect(20, 20, 270, 21))
        self.label_percentage_source.setObjectName(_fromUtf8("label_percentage_source"))

        self.le_percentage_source = QtGui.QLineEdit(self.groupBox_cost)
        self.le_percentage_source.setGeometry(QtCore.QRect(150, 20, 51, 20))
        self.le_percentage_source.setObjectName(_fromUtf8("le_percentage_source"))
        self.le_percentage_source.setText("X")

        self.cb_GenMap = QtGui.QCheckBox(self.groupBox_cost)
        self.cb_GenMap.setGeometry(QtCore.QRect(10, 50, 200, 17))
        self.cb_GenMap.setObjectName(_fromUtf8("cb_GenMap"))

        self.cb_opt1 = QtGui.QCheckBox(self.groupBox_cost)
        self.cb_opt1.setGeometry(QtCore.QRect(10, 70, 200, 17))
        self.cb_opt1.setObjectName(_fromUtf8("cb_opt1"))

        self.cb_opt2 = QtGui.QCheckBox(self.groupBox_cost)
        self.cb_opt2.setGeometry(QtCore.QRect(90, 70, 200, 17))
        self.cb_opt2.setObjectName(_fromUtf8("cb_opt2"))

        self.cb_opt3 = QtGui.QCheckBox(self.groupBox_cost)
        self.cb_opt3.setGeometry(QtCore.QRect(170, 70, 200, 17))
        self.cb_opt3.setObjectName(_fromUtf8("cb_opt3"))

        self.groupBox_ResultCost = QtGui.QGroupBox(self.groupBox_cost)
        self.groupBox_ResultCost.setGeometry(QtCore.QRect(20, 250, 250, 90))
        self.groupBox_ResultCost.setObjectName(_fromUtf8("groupBox_ResultCost"))

        self.List_mapsCost = QtGui.QListView(self.groupBox_ResultCost)
        #self.List_mapsCost.setGeometry(QtCore.QRect(10, 20, 200, 91))
        self.List_mapsCost.setGeometry(QtCore.QRect(5, 5, 50, 80))
        self.List_mapsCost.setObjectName(_fromUtf8("List_mapsFinal"))

        self.btn_Start_opt = QtGui.QPushButton(self.groupBox_ResultCost)
        #self.btn_Start_opt.setGeometry(QtCore.QRect(60, 220, 90, 70))
        self.btn_Start_opt.setGeometry(QtCore.QRect(60, 10, 90, 70))
        self.btn_Start_opt.setObjectName(_fromUtf8("btn_Start_opt"))

        # -------------------------------------------------

        self.groupBox_GenElev = QtGui.QGroupBox(Dialog)
        self.groupBox_GenElev.setGeometry(QtCore.QRect(1125, 360, 300, 170))
        self.groupBox_GenElev.setObjectName(_fromUtf8("groupBox_GenElev"))

        self.label_slopePercent = QtGui.QLabel(self.groupBox_GenElev)
        self.label_slopePercent.setGeometry(QtCore.QRect(20, 20, 270, 21))
        self.label_slopePercent.setObjectName(_fromUtf8("label_slopePercent"))
        self.le_slopePercent = QtGui.QLineEdit(self.groupBox_GenElev)
        self.le_slopePercent.setGeometry(QtCore.QRect(100, 20, 60, 20))
        self.le_slopePercent.setObjectName(_fromUtf8("le_slopePercent"))

        self.label_maxDepth = QtGui.QLabel(self.groupBox_GenElev)
        self.label_maxDepth.setGeometry(QtCore.QRect(20, 45, 270, 21))
        self.label_maxDepth.setObjectName(_fromUtf8("label_maxDepth"))
        self.le_maxDepth = QtGui.QLineEdit(self.groupBox_GenElev)
        self.le_maxDepth.setGeometry(QtCore.QRect(100, 45, 60, 20))
        self.le_maxDepth.setObjectName(_fromUtf8("le_maxDepth"))

        self.label_new_landuse_for_elev = QtGui.QLabel(self.groupBox_GenElev)
        self.label_new_landuse_for_elev.setGeometry(QtCore.QRect(20, 70, 270, 21))
        self.label_new_landuse_for_elev.setObjectName(_fromUtf8("label_new_landuse_for_elev"))
        self.le_new_landuse_for_elev = QtGui.QLineEdit(self.groupBox_GenElev)
        self.le_new_landuse_for_elev.setGeometry(QtCore.QRect(20, 90, 260, 20))
        self.le_new_landuse_for_elev.setObjectName(_fromUtf8("le_new_landuse_for_elev"))

        self.btn_GenElev = QtGui.QPushButton(self.groupBox_GenElev)
        self.btn_GenElev.setGeometry(QtCore.QRect(100, 120, 90, 40))
        self.btn_GenElev.setObjectName(_fromUtf8("btn_GenElev"))

        # ---------------------------------------------------------------------

        self.groupBox_GenSoil = QtGui.QGroupBox(Dialog)
        self.groupBox_GenSoil.setGeometry(QtCore.QRect(1125, 530, 300, 150))
        self.groupBox_GenSoil.setObjectName(_fromUtf8("groupBox_GenSoil"))

        self.label_soilType = QtGui.QLabel(self.groupBox_GenSoil)
        self.label_soilType.setGeometry(QtCore.QRect(20, 20, 270, 21))
        self.label_soilType.setObjectName(_fromUtf8("label_soilType"))
        # input format {20: 3, 40: 2, 30: 1}
        self.le_soilType = QtGui.QLineEdit(self.groupBox_GenSoil)
        self.le_soilType.setGeometry(QtCore.QRect(20, 40, 260, 20))
        self.le_soilType.setObjectName(_fromUtf8("le_soilType"))

        self.label_new_landuse = QtGui.QLabel(self.groupBox_GenSoil)
        self.label_new_landuse.setGeometry(QtCore.QRect(20, 60, 270, 21))
        self.label_new_landuse.setObjectName(_fromUtf8("label_new_landuse"))
        self.le_new_landuse = QtGui.QLineEdit(self.groupBox_GenSoil)
        self.le_new_landuse.setGeometry(QtCore.QRect(20, 80, 260, 20))
        self.le_new_landuse.setObjectName(_fromUtf8("le_new_landuse"))



        self.btn_soilType = QtGui.QPushButton(self.groupBox_GenSoil)
        self.btn_soilType.setGeometry(QtCore.QRect(100, 105, 90, 40))
        self.btn_soilType.setObjectName(_fromUtf8("btn_soilType"))


        # ---------------------------------------------------------------------

        self.checkbox_depthGW = self.cb_alg1.checkState()
        self.checkbox_SuitableSoil = self.cb_alg2.checkState()
        self.checkbox_width_rip = self.cb_alg3.checkState()
        self.checkbox_hydrolic = self.cb_alg4.checkState()
        self.checkbox_roof = self.cb_alg5.checkState()
        self.checkbox_road = self.cb_alg6.checkState()
        self.checkbox_runoff = self.cb_alg7.checkState()
        self.checkbox_rain = self.cb_alg8.checkState()
        self.checkbox_lambda = self.cb_alg9.checkState()

        self.groupBox_SearchAlgs.raise_()
        self.groupBox_InputMaps.raise_()
        self.groupBox_DlandUse.raise_()
        self.groupBox_GW.raise_()
        self.groupBox_Parcel.raise_()
        self.groupBox_High_Potential.raise_()
        self.groupBox_Wshed.raise_()
        self.groupBox_ResultFinal.raise_()
        self.groupBox_Elev.raise_()
        self.groupBox_Landuse.raise_()
        self.groupBox_Soil.raise_()
        self.groupBox_Building_Parammap.raise_()
        self.groupBox_cost.raise_()

        self.retranslateUi(Dialog)
        self.SetUpActions()

        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.closeEvent = self.closeEvent

    def closeEvent(self, diag):
        self.main.show()

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Wetspa_Urban", None))
        self.groupBox_InputMaps.setTitle(_translate("Dialog", "Input Maps", None))
        self.groupBox_GW.setTitle(_translate("Dialog", "Ground Water", None))
        self.groupBox_ResultFinal.setTitle(_translate("Dialog", "Final Results", None))
        self.groupBox_Parcel.setTitle(_translate("Dialog", "Parcel", None))
        self.groupBox_DlandUse.setTitle(_translate("Dialog", "Detailed Landuse", None))
        self.groupBox_SearchAlgs.setTitle(_translate("Dialog", "Search Algorithms", None))
        self.groupBox_High_Potential.setTitle(_translate("Dialog", "High Potential", None))
        self.groupBox_Result.setTitle(_translate("Dialog", "Results", None))
        self.groupBox_Suitable.setTitle(_translate("Dialog", "Suitable Location", None))
        self.groupBox_ResultS.setTitle(_translate("Dialog", "Results", None))
        self.groupBox_Max.setTitle(_translate("Dialog", "Max Suitable Areas for Prior LIDs", None))
        self.groupBox_Wshed.setTitle(_translate("Dialog", "Watershed", None))
        self.groupBox_Landuse.setTitle(_translate("Dialog", "Landuse for whole catchment", None))
        self.groupBox_Soil.setTitle(_translate("Dialog", "Soil for whole catchment", None))
        self.groupBox_Elev.setTitle(_translate("Dialog", "Elevation for whole catchment", None))
        self.groupBox_inp.setTitle(_translate("Dialog", "Inp file", None))
        self.groupBox_rpt.setTitle(_translate("Dialog", "Report file", None))
        self.groupBox_Building_Parammap.setTitle(
            _translate("Dialog", "Building parameter map for whole catchment", None))
        self.groupBox_cost.setTitle(_translate("Dialog", "Cost Optimization", None))
        self.groupBox_GenElev.setTitle(_translate("Dialog", "Generating Elevation", None))
        self.groupBox_GenSoil.setTitle(_translate("Dialog", "Generating Soil", None))


        self.label_Lambda.setText(_translate("Dialog", "Lambda :", None))
        self.label_Runoff.setText(_translate("Dialog", "Runoff Coefficient : [-]", None))
        self.label_Number_of_subc.setText(_translate("Dialog", "Number of Subcatchments :", None))
        self.label_Flow.setText(_translate("Dialog", "Max/Full Flow Limitation :", None))
        # self.label_Nodes.setText(_translate("Dialog", "Nodes Connected to Each Outloet :", None))
        self.label_Depth.setText(_translate("Dialog", "Depth of GW table to LID : [m]", None))
        self.label_SuitableSoil.setText(_translate("Dialog", "Suitable Soil class :", None))
        self.label_Width_rip.setText(_translate("Dialog", "Width of Riparian Zone : [m]", None))
        self.label_min_rain.setText(_translate("Dialog", "Min possible area of Raingardens : [m*m]", None))
        self.label_Prioritizing.setText(_translate("Dialog", "Prioritizing LIDs :", None))
        self.label_min_roof.setText(_translate("Dialog", "Min possible area of green roofs :", None))
        self.label_max_roof.setText(_translate("Dialog", "Max Possible elevation in pixels of Greenroof : [m]", None))
        self.label_percentage_source.setText(_translate("Dialog", "Percentage source : ", None))
        self.label_soilType.setText(_translate("Dialog", "Change Soil type input :", None))
        self.label_new_landuse.setText(_translate("Dialog", "New Landuse :", None))
        self.label_slopePercent.setText(_translate("Dialog", "slope (%) : ", None))
        self.label_maxDepth.setText(_translate("Dialog", "Max depth : ", None))
        self.label_new_landuse_for_elev.setText(_translate("Dialog", "New Landuse :", None))

        self.label_Nodes.setText(_translate("Dialog", "Merge nodes : ", None))


        self.btn_List_mapsS.setText(_translate("Dialog", "List\nmaps", None))
        self.btn_Max_pref.setText(_translate("Dialog", "Max Suitable area for prefered LIDs", None))
        self.btn_List_maps.setText(_translate("Dialog", "List\nmaps", None))
        self.btn_DefinePara.setText(_translate("Dialog", "Define parameters", None))
        self.btn_RunPre.setText(_translate("Dialog", "Run preprocessing", None))
        self.btn_Start_opt.setText(_translate("Dialog", "Start\nOptimization", None))
        self.btn_soilType.setText(_translate("Dialog", "Start", None))
        self.btn_GenElev.setText(_translate("Dialog", "Start", None))

        # self.btn_List_mapsFinal.setText(_translate("Dialog", "List\nmaps", None))

        self.tb_DlandUse.setText(_translate("Dialog", "...", None))
        self.tb_Parcel.setText(_translate("Dialog", "...", None))
        self.tb_GW.setText(_translate("Dialog", "...", None))
        self.tb_Wshed.setText(_translate("Dialog", "...", None))
        self.tb_Landuse.setText(_translate("Dialog", "...", None))
        self.tb_Soil.setText(_translate("Dialog", "...", None))
        self.tb_Elev.setText(_translate("Dialog", "...", None))
        self.tb_inp.setText(_translate("Dialog", "...", None))
        self.tb_rpt.setText(_translate("Dialog", "...", None))

        self.cb_alg1.setText(_translate("Dialog", "Suitable Area Based on GW", None))
        self.cb_alg2.setText(_translate("Dialog", "Suitable Soil Area", None))
        self.cb_alg3.setText(_translate("Dialog", "Finding Riparian Zone", None))
        self.cb_alg4.setText(_translate("Dialog", "Hydrolic", None))
        self.cb_alg5.setText(_translate("Dialog", "Flat Roof Finder", None))
        self.cb_alg6.setText(_translate("Dialog", "Road Finder", None))
        self.cb_alg7.setText(_translate("Dialog", "High Potential Runoff Area", None))
        self.cb_alg8.setText(_translate("Dialog", "Rain Garden Finder", None))
        self.cb_alg9.setText(_translate("Dialog", "Lambda Calculator", None))
        self.cb_opt1.setText(_translate("Dialog", "Option 1", None))
        self.cb_opt2.setText(_translate("Dialog", "Option 2", None))
        self.cb_opt3.setText(_translate("Dialog", "Option 3", None))
        self.cb_GenMap.setText(_translate("Dialog", "Generating Map", None))

    def setLEParcel(self):
        fname = QFileDialog.getOpenFileName(None, 'Open file',
                                            os.getcwd(), "ascii maps (*.asc)")
        self.le_Parcel.setText(fname)

    def setLEDlandUse(self):
        fname = QFileDialog.getOpenFileName(None, 'Open file',
                                            os.getcwd(), "ascii maps (*.asc)")
        self.le_DlandUse.setText(fname)

    def setLEGW(self):
        fname = QFileDialog.getOpenFileName(None, 'Open file',
                                            os.getcwd(), "")
        self.le_GW.setText(fname)

    def setLEWatershed(self):
        fname = QFileDialog.getOpenFileName(None, 'Open file',
                                            os.getcwd(), "ascii maps (*.asc)")
        self.le_Wshed.setText(fname)

    def setLELanduse(self):
        fname = QFileDialog.getOpenFileName(None, 'Open file',
                                            os.getcwd(), "ascii maps (*.asc)")
        self.le_Landuse.setText(fname)

    def setLESoil(self):
        fname = QFileDialog.getOpenFileName(None, 'Open file',
                                            os.getcwd(), "ascii maps (*.asc)")
        self.le_Soil.setText(fname)

    def setLEElev(self):
        fname = QFileDialog.getOpenFileName(None, 'Open file',
                                            os.getcwd(), "ascii maps (*.asc)")
        self.le_Elev.setText(fname)

    def setLEInp(self):
        fname = QFileDialog.getOpenFileName(None, 'Open file',
                                            os.getcwd(),"ascii maps (*.inp)")
        self.le_inp.setText(fname)

    def setLERpt(self):
        fname = QFileDialog.getOpenFileName(None, 'Open file',
                                            os.getcwd(),"(*.rpt)")
        self.le_rpt.setText(fname)


    def prior(self):

        list_show_final_results = []

        # input format for GUI : a:10;b:20;c:30

        input_prio = str(self.le_Prioritizing.text())

        # list_maps = ["FinalPavement.asc", "FinalRainGarden.asc", "FinalGreenRoof.asc", "FinalRiparian.asc"]
        # input format for func: [("a.asc", 10), ("b.asc", 20), ]

        input_prio = input_prio.split(";")
        for i in range(len(input_prio)):
            input_prio[i] = input_prio[i].split(":")
            input_prio[i][0] += ".asc"
            input_prio[i][0] = os.path.join("parammaps", input_prio[i][0])
            input_prio[i][1] = int(input_prio[i][1])

        Final_Prioritized = algorithms.Overlay()
        Final_Prioritized = Final_Prioritized.overlay_or_with_priority_3(input_prio)

        Final_Prioritized.to_file_parammaps("fpcl.asc")

        list_show_final_results.append("fpcl.asc")

        path_to_fpcl = os.path.join("parammaps","fpcl.asc")
        final_output = algorithms.Overlay()
        final_output = final_output.overlay_with_landuse(path_to_fpcl, str(self.le_Landuse.text()))
        final_output.to_file_parammaps("FinalOutput.asc")

        list_show_final_results.append("FinalOutput.asc")

        model = QStringListModel()
        model.setStringList(list_show_final_results)
        self.List_mapsFinal.setModel(model)

    def gen_Suitable_maps(self):

        comb_Rip_list = []
        comb_Roof_list = []
        comb_Rain_list = []
        comb_Road_list = []

        # check if Highpot.asc is in parammaps
        file_in_parammaps = os.listdir("parammaps")
        if "HighPot.asc" in file_in_parammaps :
            self.hasHighpot = True

        if self.hasHighpot:
            comb_Rip_list.append("HighPot.asc")
            comb_Roof_list.append("HighPot.asc")
            comb_Rain_list.append("HighPot.asc")
            comb_Road_list.append("HighPot.asc")

        list = []

        if self.checkbox_depthGW == 2:
            # list.append("GWFinal.asc")

            DepthGW = str(self.le_Depth.text())
            #print(str(self.le_GW.text()))
            GW = algorithms.SuitableAreaBasedOnGW()
            Map_GW = GW.get_suitable_areas(str(self.le_GW.text()), str(self.le_Elev.text()), float(DepthGW))

            Map_GW.to_file_parammaps("GWFinal.asc")

            comb_Rain_list.append("GWFinal.asc")
            comb_Rip_list.append("GWFinal.asc")
            comb_Road_list.append("GWFinal.asc")

            list.append("GWFinal.asc")

            print ("gw done !")

        if self.checkbox_SuitableSoil == 2:
            # list.append("SoilFinal.asc")
            # le_SuitableSoil input must be : 21,34,676,74,...

            SuitableSoilClass_numbers = str(self.le_SuitableSoil.text())
            SuitableSoilClass_numbers = SuitableSoilClass_numbers.split(",")

            for i in range(len(SuitableSoilClass_numbers)):
                SuitableSoilClass_numbers[i] = int(SuitableSoilClass_numbers[i])

            SoilArea = algorithms.SuitableSoilArea()

            Map_Soil = SoilArea.get_suitable_areas(str(self.le_Soil.text()), str(self.le_Landuse.text()), SuitableSoilClass_numbers)

            Map_Soil.to_file_parammaps("SoilFinal.asc")

            # b = pcraster.Map2Asc()
            # b.asc2map("SoilFinal.asc", "SoilFinal")

            comb_Rain_list.append("SoilFinal.asc")
            comb_Rip_list.append("SoilFinal.asc")

            list.append("SoilFinal.asc")

            print ("SuitableSoil done !")

        if self.checkbox_width_rip == 2:
            WidthRip = float(str(self.le_Width_rip.text()))

            Riparian = algorithms.FindingRiperianZone()
            Map_Riparian = Riparian.get_riperian_zone(str(self.le_Landuse.text()), WidthRip)

            Map_Riparian.to_file_parammaps("RiparianFinal.asc")

            list.append("RiparianFinal.asc")
            comb_Rip_list.append("RiparianFinal.asc")

            print("Rip Done!")

        if self.checkbox_roof == 2:
            # list.append("GreenRoofFinal.asc")
            Min_green = float(str(self.le_min_roof.text()))
            Max_slope = float(str(self.le_max_roof.text()))

            Flatroof = algorithms.FlatRoofFinder()
            Map_greenroof = Flatroof.get_flat_roofs_by_elevation_map(str(self.le_Landuse.text()), str(self.le_Parcel.text()),
                                                                     str(self.le_Elev.text()),
                                                                     Min_green, Max_slope)

            Map_greenroof.to_file_parammaps("GreenRoofFinal.asc")

            comb_Roof_list.append("GreenRoofFinal.asc")

            list.append("GreenRoofFinal.asc")

            print("roof done !")

        # RainGarden
        if self.checkbox_rain == 2:

            Min_rain = float(str(self.le_min_rain.text()))

            RainGarden = algorithms.RainGardenFinder()
            Map_RainGarden = RainGarden.get_rain_gardens(str(self.le_Landuse.text()), Min_rain)

            Map_RainGarden.to_file_parammaps("RainGardenFinal.asc")

            comb_Rain_list.append("RainGardenFinal.asc")
            list.append("RainGardenFinal.asc")

            print("RainGarden Done !")

        # Map road
        if self.checkbox_road == 2:
            road = algorithms.RoadFinder()
            Map_road = road.get_detailed_landuse_map(str(self.le_DlandUse.text()))

            Map_road.to_file_parammaps("PavementFinal.asc")

            comb_Road_list.append("PavementFinal.asc")
            list.append("PavementFinal.asc")

            print("Pavement done!")

        # New_Rain [GW & soil & Rain & HighPot]
        # comb_Rain_list = ["GWFinal.asc", "SoilFinal.asc", "RainGardenFinal.asc"]
        path_comb_Rain_list = "parammaps"
        for i in range(len(comb_Rain_list)):
            comb_Rain_list[i] = os.path.join(path_comb_Rain_list, comb_Rain_list[i])

        final_rain = algorithms.Overlay()
        final_rain = final_rain.overlay_and(comb_Rain_list)

        final_rain.to_file_parammaps("FinalRainGarden.asc")

        list.append("FinalRainGarden.asc")

        # New Road [GW & Road & HighPot]
        # comb_Road_list = ["GWFinal.asc", "PavementFinal.asc"]
        path_comb_Road_list = "parammaps"
        for i in range(len(comb_Road_list)):
            comb_Road_list[i] = os.path.join(path_comb_Road_list, comb_Road_list[i])

        final_road = algorithms.Overlay()
        final_road = final_road.overlay_and(comb_Road_list)
        final_road.to_file_parammaps("FinalPavement.asc")

        list.append("FinalPavement.asc")

        # New Rip [Rip & gw & soil & HighPot]
        # comb_Rip_list = ["GWFinal.asc","SoilFinal.asc", "RiparianFinal.asc"]
        path_comb_Rip_list = "parammaps"
        for i in range(len(comb_Rip_list)):
            comb_Rip_list[i] = os.path.join(path_comb_Rip_list, comb_Rip_list[i])

        final_rip = algorithms.Overlay()
        final_rip = final_rip.overlay_and(comb_Rip_list)
        final_rip.to_file_parammaps("FinalRiparian.asc")

        list.append("FinalRiparian.asc")

        # New Roof [Roof & HighPot]
        # comb_Roof_list = ["GreenRoofFinal.asc"]
        path_comb_Roof_list = "parammaps"
        for i in range(len(comb_Roof_list)):
            comb_Roof_list[i] = os.path.join(path_comb_Roof_list, comb_Roof_list[i])

        final_roof = algorithms.Overlay()
        final_roof = final_roof.overlay_and(comb_Roof_list)
        final_roof.to_file_parammaps("FinalGreenRoof.asc")

        list.append("FinalGreenRoof.asc")

        model = QStringListModel()
        model.setStringList(list)
        self.List_mapsS.setModel(model)

    def listMaps(self):

        runoff_limit = self.le_Runoff.text()
        landa = self.le_Lambda.text()
        NumOfSubc = self.le_Number_of_subc.text()
        Max_Full = self.le_Flow.text()
        Nodes = self.le_Nodes.text()

        f = []
        output_maps_highpot = []

        # runoff
        if self.checkbox_runoff == 2:
            f.append("runoffFinal.asc")
            path_dot_map = os.path.join("C:\\", "TMP", "whole_catchment", "Runner", "catchment", "parammaps", "runoff_co.map")
            #path_dot_map.replace("\\\\", "\\")
            #print path
            #runoffcoMap = map_loader.MapLoader()
            #runoffcoMap_obj = runoffcoMap.load_dot_map(maps.RunoffCoMap, path)

            outrunoff = algorithms.RunoffCoefficient()

            Map_runoff = outrunoff.get_runoff_coefficient_map(path_dot_map, runoff_limit)

            output_maps_highpot.append("runoffFinal.asc")

            Map_runoff.to_file_parammaps("runoffFinal.asc")

            print("hell!")
            #print(str(runoff_limit))

        # landa
        if self.checkbox_lambda == 2:
            f.append("landa.asc")
            slopeMap = map_loader.MapLoader()
            path = os.path.join("C:\\","TMP","whole_catchment","Runner","catchment","parammaps","slope.map")
            #path = path.replace("\\","\\")
            path.replace("\\\\","\\")
            print path
            slopeMap_obj = slopeMap.load_dot_map(maps.BasicMap, path)

            conductivityMap = map_loader.MapLoader()
            path = os.path.join("C:\\","TMP","whole_catchment","Runner","catchment","parammaps","conductivity.map")
            #path = path.replace("\\\\", "\\")
            path.replace("\\\\", "\\")
            print path
            conductivityMap_obj = conductivityMap.load_dot_map(maps.BasicMap, path)

            flowaccMap = map_loader.MapLoader()
            path = os.path.join("C:\\","TMP","whole_catchment","Runner","catchment","parammaps","flowacc.map")
            #path = path.replace("\\\\", "\\")
            path.replace("\\\\", "\\")
            print path
            flowaccMap_obj = flowaccMap.load_dot_map(maps.BasicMap, path)

            LandaOut = algorithms.LandaEq()

            path_flowaccCr = os.path.join("C:\\","TMP","whole_catchment","Runner","catchment","parammaps","flowaccCr.asc")
            path_slopeCr = os.path.join("C:\\", "TMP", "whole_catchment", "Runner", "catchment", "parammaps",
                                          "slopeCr.asc")
            conductivityCr = os.path.join("C:\\", "TMP", "whole_catchment", "Runner", "catchment", "parammaps",
                                          "conductivityCr.asc")

            MapLanda = LandaOut.get_output_with_user_limit(path_flowaccCr, path_slopeCr, conductivityCr, landa)
            #MapLanda = LandaOut.get_output_with_user_limit("flowaccCr.asc", "slopeCr.asc", "conductivityCr.asc", landa)

            output_maps_highpot.append("landa.asc")

            MapLanda.to_file_parammaps("landa.asc")

        # High pot

        # type of Nodes = "20:10,12,13;3:13,4"
        # if  LandaEq != 0 and RunoffCoefficient != 0 :
        if self.checkbox_hydrolic == 2:
            f.append("hydrolic.asc")
            Nodes = str(Nodes)[1:len(Nodes)-1]
            Nodes = Nodes.split(",")
            merge_nodes = []
            for i in Nodes:
                merge_nodes.append(int(i))
            print merge_nodes

            high = high_potential_area.HighPotentialArea()

            hydrolic_outp = high.build_output_based_on_hydrolic(str(self.le_Wshed.text()), "report.rpt", "MAX/FULL FLOW",NumOfSubc,str(self.le_inp.text()),Max_Full,merge_nodes)

            output_maps_highpot.append("hydrolic.asc")

            hydrolic_outp.to_file_parammaps("hydrolic.asc")


        if len(output_maps_highpot) == 0:
            print "Nothing to merge! plz give some maps!"
            self.hasHighpot = False

        else:
            f.append("Highpot.asc")
            self.HighPot = algorithms.Overlay()
            path_Cr = "parammaps"
            for i in range(len(output_maps_highpot)):
                output_maps_highpot[i] = os.path.join(path_Cr, output_maps_highpot[i])

            self.HighPot = self.HighPot.overlay_and(output_maps_highpot)

            self.HighPot.to_file_parammaps("HighPot.asc")
            self.hasHighpot = True


            print("overlay_and done!")

        model = QStringListModel()
        model.setStringList(f)
        self.List_maps.setModel(model)

        print("Highpot finish !")

    def showmaps(self, selected):
        print("Show maps")
        Sub_path = "parammaps"
        a = (str(self.List_maps.model().data(selected, 0).toString()))
        pathss = os.path.join(Sub_path, a)
        agrus = "aguila {}".format(pathss)
        subprocess.Popen(agrus)

    def showmapsS(self, selected):
        print("hello")
        # Sub_path = os.path.join("D:/Python_Proj/water-engineering/parammaps")
        Sub_path = "parammaps"
        a = (str(self.List_mapsS.model().data(selected, 0).toString()))
        pathss = os.path.join(Sub_path, a)
        agrus = "aguila {}".format(pathss)
        subprocess.Popen(agrus)

    def showmapsFinal(self, selected):
        print("hello")
        Sub_path = "parammaps"
        a = (str(self.List_mapsFinal.model().data(selected, 0).toString()))
        pathss = os.path.join(Sub_path, a)
        agrus = "aguila {}".format(pathss)
        subprocess.Popen(agrus)

    def MaxAll_LID(self):

        dic = self.comb_algs

        Road = dic["Road 20"]
        RainG = dic["RainGarden 30"]
        Riparian = dic["Riparian 40"]
        GreenRoof = dic["GreenRoof 50"]
        Landuse = dic["Landuse"]

        for i in range(len(Road.matrix)):
            self.outputAll.matrix.append([])
            for j in range(len(Road.matrix[i])):
                temp = ""

                if Landuse.map.matrix[i][j] > 0:
                    if int(Road.matrix[i][j]) == 1:
                        temp += "20"
                    if int(RainG.matrix[i][j]) == 1:
                        temp += "30"
                    if int(Riparian.matrix[i][j]) == 1:
                        temp += "40"
                    if int(GreenRoof.matrix[i][j]) == 1:
                        temp += "50"
                    temp += Landuse.map.matrix[i][j]
                else:
                    temp = Landuse.map.matrix[i][j]

                self.outputAll.matrix[i].append(temp)

        return self.outputAll

    def Max_Pref(self):

        prior = str(self.le_Prioritizing.text())

        ls_prior = prior.split(",")

        for i in range(len(self.outputAll.matrix)):
            self.outputPref.matrix.append([])
            for j in range(len(self.outputPref.matrix[i])):
                temp = ""
                if len(int(self.outputAll.matrix[i][j]) >= 20):
                    first = self.outputPref.matrix[i][j][0] + self.outputPref.matrix[i][j][1]

                    counter = 0
                    while counter < ls_prior:

                        if first == ls_prior[counter]:
                            self.outputPref.matrix[i].append(first)
                            counter = ls_prior
                        counter += 1

                else:
                    self.outputPref.matrix[i].append(self.outputAll.matrix[i][j])

        return self.outputPref

    def checkbox1(self):
        self.checkbox_depthGW = self.cb_alg1.checkState()

        if self.checkbox_depthGW != 2:
            self.le_Depth.setText("X")
        if self.checkbox_depthGW == 2:
            self.le_Depth.setText("")
            self.le_Depth.setText("0")

        print self.checkbox_depthGW



    def checkbox2(self):
        self.checkbox_SuitableSoil = self.cb_alg2.checkState()

        if self.checkbox_SuitableSoil != 2:
            self.le_SuitableSoil.setText("X")
        if self.checkbox_SuitableSoil == 2:
            self.le_SuitableSoil.setText("")
            self.le_SuitableSoil.setText("3,11")

        print self.checkbox_SuitableSoil

    def checkbox3(self):
        self.checkbox_width_rip = self.cb_alg3.checkState()

        if self.checkbox_width_rip != 2:
            self.le_Width_rip.setText("X")
        if self.checkbox_width_rip == 2:
            self.le_Width_rip.setText("")
            self.le_Width_rip.setText("30")

        print self.checkbox_width_rip

    def checkbox4(self):
        self.checkbox_hydrolic = self.cb_alg4.checkState()

        if self.checkbox_hydrolic != 2:
            self.le_Number_of_subc.setText("X")
            self.le_Flow.setText("X")
            self.le_Nodes.setText("X")

        if self.checkbox_hydrolic == 2:
            self.le_Number_of_subc.setText("")
            self.le_Flow.setText("")
            self.le_Nodes.setText("")

            self.le_Number_of_subc.setText("31")
            self.le_Flow.setText("0.8")
            self.le_Nodes.setText("[1,2,3,2,4,5,6,7,8,9,6,1,10,11,12,13,13,14,15,16,17,18,19,15,20,21,22,23,24,25,26,27,28,29,26,30,31,26]")

        print self.checkbox_hydrolic

    def checkbox5(self):
        self.checkbox_roof = self.cb_alg5.checkState()

        if self.checkbox_roof != 2:
            self.le_min_roof.setText("X")
            self.le_max_roof.setText("X")
        if self.checkbox_roof == 2:
            self.le_min_roof.setText("")
            self.le_max_roof.setText("")
            self.le_min_roof.setText("10")
            self.le_max_roof.setText("0.1")

        print self.checkbox_roof

    def checkbox6(self):
        self.checkbox_road = self.cb_alg6.checkState()
        print self.checkbox_road

    def checkbox7(self):
        self.checkbox_runoff = self.cb_alg7.checkState()

        if self.checkbox_runoff != 2:
            self.le_Runoff.setText("X")
        if self.checkbox_runoff == 2:
            self.le_Runoff.setText("")
            self.le_Runoff.setText("0.8")

        print self.checkbox_runoff

    def checkbox8(self):
        self.checkbox_rain = self.cb_alg8.checkState()

        if self.checkbox_rain != 2:
            self.le_min_rain.setText("X")
        if self.checkbox_rain == 2:
            self.le_min_rain.setText("")
            self.le_min_rain.setText("30")
        print self.checkbox_rain

    def checkbox9(self):
        self.checkbox_lambda = self.cb_alg9.checkState()
        if self.checkbox_lambda != 2:
            self.le_Lambda.setText("X")
        if self.checkbox_lambda == 2:
            self.le_Lambda.setText("")
            self.le_Lambda.setText("3")

        print self.checkbox_lambda

    def OpenUserinput(self):
        os.chdir(_Current)
        subprocess.Popen("notepad userinput.ini")

    def runpre_LID(self):

        # todo create colone with code , in static

        lnd = pcraster.Map2Asc()  # clone nominal
        lnd.asc2map_forNuminal(str(self.le_Landuse.text()), os.path.join("C:\TMP\whole_catchment\Runner\catchment\staticmaps","landuse_start.map"))

        sl = pcraster.Map2Asc()  # clone nominal
        sl.asc2map_forNuminal(str(self.le_Soil.text()), os.path.join("C:\TMP\whole_catchment\Runner\catchment\staticmaps","soil_start.map"))

        elv = pcraster.Map2Asc()  # clonescalar
        elv.asc2map_forScalar(str(self.le_Elev.text()), os.path.join("C:\TMP\whole_catchment\Runner\catchment\staticmaps","elevation_start.map"))

        print "3 done "
        subprocess.Popen(os.path.join("C:\TMP\whole_catchment\Runner\catchment","runWetSpaPreprocess.bat"))
        #subprocess.Popen("pause")

        #subprocess.Popen("runWetSpaPreprocess.bat")

    def cost_opt(self):
        alg_to_use = []
        prcnt_src = str(self.le_percentage_source.text())

        gen_map = self.cb_GenMap.checkState()
        if gen_map != 0 :
            gen_map = True
        else :
            gen_map = False

        print "gen_map", gen_map

        opt1 = self.cb_opt1.checkState()
        opt2 = self.cb_opt2.checkState()
        opt3 = self.cb_opt3.checkState()

        if opt1 == 2 :
            alg_to_use.append(1)
        if opt1 != 2 and (1 in alg_to_use):
            alg_to_use.remove(1)

        if opt2 == 2 :
            alg_to_use.append(2)
        if opt2 != 2 and (2 in alg_to_use):
            alg_to_use.remove(2)

        if opt3 == 2 :
            alg_to_use.append(3)
        if opt3 != 2 and (3 in alg_to_use):
            alg_to_use.remove(3)

        # print gen_map,opt1,opt2,opt3

        adv_land_use = "FanialOutput.asc"
        num_subc = "31"  # todo get from UI

        cur = os.getcwd()
        print cur
        os.chdir("map")
        maps_dir = os.path.join(cur, "map")

        # copy inputs to map folder

        copy2dir.copy2dir(str(self.le_Wshed.text()), os.path.join(maps_dir,"wateshed.asc"))
        copy2dir.copy2dir(str(self.le_Landuse.text()), os.path.join(maps_dir, "landuse.asc"))
        copy2dir.copy2dir(str(self.le_Parcel.text()), os.path.join(maps_dir, "parcel.asc"))
        copy2dir.copy2dir(str(self.le_Elev.text()), os.path.join(maps_dir, "elevation.asc"))
        copy2dir.copy2dir(str(self.le_rpt.text()), os.path.join(maps_dir, "report.rpt"))
        copy2dir.copy2dir(str(self.le_inp.text()), os.path.join(maps_dir, "tmp.inp"))

        # -----------------------

        cost = map_merge.Main()
        cost.run_with_init("wateshed.asc", "landuse.asc", "FanialOutput.asc", "parcel.asc", "elevation.asc", "report.rpt",int(num_subc),float(prcnt_src),int(str(self.le_min_rain.text())),int(str(self.le_min_roof.text())),str(self.le_max_roof),"tmp.inp",cost_optimization.basic_priorities,gen_map,alg_to_use)

        os.chdir(cur)
        print os.getcwd()

        pass

    def gen_soil(self): # soil for whole !
        # landuse_to_soil_type format func: {20: 3, 40: 2, 30: 1}
        # format input 20:3;40:2;30:1
        landuse_to_soil_type = {}

        str_type = str(self.le_soilType.text())
        a = str_type.split(";")
        for elm in a:
            tmp = elm.split(":")
            landuse_to_soil_type[int(tmp[0])] = int(tmp[1])

        # landuse_to_soil_type format ready !

        soil_path = str(self.le_Soil.text())
        advance_land_use = str(self.le_new_landuse.text())

        if advance_land_use == "FinalOutput":
            advance_land_use = os.path.join("parammaps",advance_land_use)
            advance_land_use += ".asc"
            new_soil = algorithms.change_soil_type_by_advanced_landuse_map(soil_path, advance_land_use, landuse_to_soil_type)
            new_soil.to_file_parammaps("NewSoil.asc")
        else :
            print "enter right filename!"

    def gen_elev(self):

        slope_percent = str(self.le_slopePercent.text())
        max_depth = int(str(self.le_maxDepth.text()))
        advance_land_use = str(self.le_new_landuse_for_elev.text())

        if advance_land_use == "FinalOutput":
            advance_land_use = os.path.join("parammaps", advance_land_use)
            advance_land_use += ".asc"

            new_elev = algorithms.RainGardenBuilder()
            new_elev = new_elev.build_rain_garden_with_slope_and_max_depth(advance_land_use, slope_percent, max_depth, str(self.le_Elev.text()))
            new_elev.to_file_parammaps("NewElevation.asc")

        else :
            print "enter right filename!"

    def SetUpActions(self):
        self.tb_Parcel.clicked.connect(self.setLEParcel)
        self.tb_GW.clicked.connect(self.setLEGW)
        self.tb_DlandUse.clicked.connect(self.setLEDlandUse)
        self.tb_Wshed.clicked.connect(self.setLEWatershed)
        self.tb_Landuse.clicked.connect(self.setLELanduse)
        self.tb_Soil.clicked.connect(self.setLESoil)
        self.tb_Elev.clicked.connect(self.setLEElev)
        self.tb_inp.clicked.connect(self.setLEInp)
        self.tb_rpt.clicked.connect(self.setLERpt)

        self.btn_List_maps.clicked.connect(self.listMaps)
        self.btn_List_mapsS.clicked.connect(self.gen_Suitable_maps)
        self.btn_Max_pref.clicked.connect(self.prior)
        self.btn_DefinePara.clicked.connect(self.OpenUserinput)
        self.btn_RunPre.clicked.connect(self.runpre_LID)
        self.btn_soilType.clicked.connect(self.gen_soil)
        self.btn_GenElev.clicked.connect(self.gen_elev)
        self.btn_Start_opt.clicked.connect(self.cost_opt)

        self.cb_alg1.clicked.connect(self.checkbox1)
        self.cb_alg2.clicked.connect(self.checkbox2)
        self.cb_alg3.clicked.connect(self.checkbox3)
        self.cb_alg4.clicked.connect(self.checkbox4)
        self.cb_alg5.clicked.connect(self.checkbox5)
        self.cb_alg6.clicked.connect(self.checkbox6)
        self.cb_alg7.clicked.connect(self.checkbox7)
        self.cb_alg8.clicked.connect(self.checkbox8)
        self.cb_alg9.clicked.connect(self.checkbox9)

        self.List_maps.doubleClicked.connect(self.showmaps)
        self.List_mapsS.doubleClicked.connect(self.showmapsS)
        self.List_mapsFinal.doubleClicked.connect(self.showmapsFinal)

        # self.btn_Max_all.clicked.connect(self.MaxAll_LID)
        # self.btn_Max_pref.clicked.connect(self.Max_Pref)


class Ui_Home(object):
    def setupUi(self, Dialog):
        self.openedlist = []
        Dialog.setObjectName(_fromUtf8("Dialog"))
        self.dialog = Dialog
        self.dialog.setWindowIcon(QtGui.QIcon('ico.png'))
        Dialog.resize(635, 342)

        self.btn_basic = QtGui.QPushButton(Dialog)
        self.btn_basic.setGeometry(QtCore.QRect(40, 90, 131, 61))
        self.btn_basic.setObjectName(_fromUtf8("btn_basic"))

        self.btn_Preprocessing = QtGui.QPushButton(Dialog)
        self.btn_Preprocessing.setGeometry(QtCore.QRect(180, 90, 131, 61))
        self.btn_Preprocessing.setObjectName(_fromUtf8("btn_Preprocessing"))

        self.btn_model = QtGui.QPushButton(Dialog)
        self.btn_model.setGeometry(QtCore.QRect(320, 90, 131, 61))
        self.btn_model.setObjectName(_fromUtf8("btn_model"))

        self.btn_LID = QtGui.QPushButton(Dialog)
        self.btn_LID.setGeometry(QtCore.QRect(250, 160, 131, 61))
        self.btn_LID.setObjectName(_fromUtf8("btn_LID"))

        self.btn_minimize = QtGui.QPushButton(Dialog)
        self.btn_minimize.setGeometry(QtCore.QRect(460, 90, 131, 61))
        self.btn_minimize.setObjectName(_fromUtf8("btn_minimize"))

        self.label_logo = QtGui.QLabel(Dialog)
        self.label_logo.setGeometry(QtCore.QRect(250, 280, 161, 51))
        self.label_logo.setText(_fromUtf8(""))
        self.label_logo.setPixmap(QtGui.QPixmap(_fromUtf8("log.png")))
        self.label_logo.setObjectName(_fromUtf8("label_logo"))
        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(120, 250, 261, 50))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setTextFormat(QtCore.Qt.RichText)
        self.label.setObjectName(_fromUtf8("label"))
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        self.btn_minimize.clicked.connect(self.minimize)
        self.btn_model.clicked.connect(self.model)
        self.btn_Preprocessing.clicked.connect(self.preprocess)
        self.btn_basic.clicked.connect(self.basic)
        self.btn_LID.clicked.connect(self.LID)
        self.label.setText(_translate("Dialog", "Developed by Vrije Universiteit Brussel", None))
        self.label.setStyleSheet("QLabel#label {color: gray}")
        self.label.setGeometry(QtCore.QRect(190, 250, 261, 16))
        myappid = 'mycompany.myproduct.subproduct.version'  # arbitrary string
        import ctypes
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    def basic(self):
        self.dialog.hide()
        Dialog = QtGui.QDialog()
        ui = Basic_Dialog()
        ui.setupUi(Dialog, self.dialog)
        Dialog.setWindowIcon(QtGui.QIcon('ico.png'))
        Dialog.show()
        self.openedlist.append(Dialog)

    def minimize(self):
        self.dialog.hide()
        Dialog = QtGui.QDialog()
        ui = Sewer_Dialog()
        ui.setupUi(Dialog, self.dialog)
        Dialog.setWindowIcon(QtGui.QIcon('ico.png'))
        Dialog.show()
        self.openedlist.append(Dialog)

    def model(self):
        self.dialog.hide()
        Dialog = QtGui.QDialog()
        ui = Ui_Dialogone()
        ui.setupUi(Dialog, self.dialog)
        Dialog.setWindowIcon(QtGui.QIcon('ico.png'))
        Dialog.show()
        self.openedlist.append(Dialog)

    def preprocess(self):
        self.dialog.hide()
        Dialog = QtGui.QDialog()
        ui = Ui_Dialog()
        ui.setupUi(Dialog, self.dialog)
        self.openedlist.append(Dialog)
        Dialog.setWindowIcon(QtGui.QIcon('ico.png'))
        Dialog.show()

        # sys.exit(app.exec_())

    def LID(self):
        self.dialog.hide()
        Dialog = QtGui.QDialog()
        ui = LID_Loc_Dialog()
        ui.setupUi(Dialog, self.dialog)
        self.openedlist.append(Dialog)
        Dialog.setWindowIcon(QtGui.QIcon('ico.png'))
        Dialog.show()

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Wetspa_Urban", None))
        self.btn_basic.setText(_translate("Dialog", "Basic", None))
        self.btn_Preprocessing.setText(_translate("Dialog", "Preprocessing", None))
        self.btn_model.setText(_translate("Dialog", "Model", None))
        self.btn_minimize.setText(_translate("Dialog", "Sewer Model", None))
        self.btn_LID.setText(_translate("Dialog", "LID Locator", None))


def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise


def main():
    sys.setrecursionlimit(10 ** 6)

    print('hi')
    ##########################################################################"
    # arcpy.env.workspace = os.getcwd()
    # Dir = arcpy.env.workspace
    # arcpy.CheckOutExtension("Spatial")
    ##########################################################################"
    make_sure_path_exists(_OUTPUT_DIR)
    Dic = {}
    ################################################################################"


    app = QtGui.QApplication(sys.argv)
    Dialog = QtGui.QDialog()
    ui = Ui_Home()
    ui.setupUi(Dialog)
    Dialog.show()
    (app.exec_())


if __name__ == "__main__":
    main()
