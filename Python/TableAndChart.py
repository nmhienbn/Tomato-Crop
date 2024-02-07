# # Open the saved PNG image
import os
import StatisticsPNG as SPNG
import matplotlib.pyplot as plt
import numpy as np


fig1Dir = "outputs/Figure1_Weather_Data.png"
table1Dir = "outputs/Table1_Plant_structure_and_Fruit_set.png"
tableDir = "outputs/Table_tmp_Yield_Component.png"
table2Dir = "outputs/Table2_Spacing.png"
table3Dir = "outputs/Table3_Truss.png"
table4Dir = "outputs/Table4_Treatment.png"
table5Dir = "outputs/Table5_TreatmentTruss.png"
table6Dir = "outputs/Table6_TrussSpacingMarketableYield2Ws.png"
fig2Dir = "outputs/Fig2_Yield.png"
Table7Dir = "outputs/Table7_FruitMorphology.png"


def open(path):
    os.system("start " + path)


def Weather():
    import Weather

    SPNG.weatherChart(Weather.res_after_transplanting)
    plt.savefig(fig1Dir, dpi=300)
    open(fig1Dir)


def PlantStructure():
    import PlantStructure as PS

    SPNG.configTable(PS.res, table1Dir)
    os.system("start " + table1Dir)


def YieldComponent():
    import YieldComponent as YC

    # SPNG.configTable(YC.tmp, tableDir)
    # open(tableDir)

    SPNG.configTable(YC.Table2, table2Dir)
    open(table2Dir)

    SPNG.configTable(YC.Table3, table3Dir)
    open(table3Dir)

    SPNG.configTable(YC.Table4, table4Dir)
    open(table4Dir)

    SPNG.configTable(YC.Table5, table5Dir)
    open(table5Dir)

    SPNG.configTable(YC.Table6, table6Dir, showIndex=True)
    open(table6Dir)

    SPNG.colChart(YC.Fig2Table, fig2Dir)
    open(fig2Dir)


def FruitMorphology():
    import FruitMorphology as FM

    SPNG.configTable(FM.res, Table7Dir)
    open(Table7Dir)


Weather()
PlantStructure()
YieldComponent()
FruitMorphology()
