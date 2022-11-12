"""
Script adds HSG and Soil_Type attribute fields to SSURGO Soil Shapefiles
Run as tool in Arcmap.
Made by Nathan R
"""

import arcpy
import os

#Initial variable declaration
mxd = arcpy.mapping.MapDocument("CURRENT")
df = arcpy.mapping.ListDataFrames(mxd)[0]
soils_shp = str((arcpy.GetParameterAsText(0)))
muaggatt_txt_original = (soils_shp[:-27])+"\\tabular\\muaggatt.txt"
muaggatt_txt_processed = (soils_shp[:-27])+"\\tabular\\muaggatt_N.txt"
muaggatt_dbf_processed = (soils_shp[:-27])+"\\tabular\\muaggatt_N.dbf"

#Process muaggatt.txt table
f = open(muaggatt_txt_original,'r+')
nf = open(muaggatt_txt_processed,'a')
lines = f.readlines()
nf.write("FID,musym,muname,mustatus,slopegraddcp,slopegradwta,brockdepmin,wtdepannmin,wtdepaprjunmin,flodfreqdcd,flodfreqmax,pondfreqprs,aws025wta,aws050wta,aws0100wta,aws0150wta,drclassdcd,drclasswettest,hydgrpdcd,iccdcd,iccdcdpct,niccdcd,niccdcdpct,engdwobdcd,engdwbdcd,engdwbll,engdwbml,engstafdcd,engstafll,engstafml,engsldcd,engsldcp,englrsdcd,engcmssdcd,engcmssmp,urbrecptdcd,urbrecptwta,forpehrtdcp,hydclprs,awmmfpwwta,mukey\n")
for i in range(len(lines)):
    nline = (lines[i].replace("|",",")).replace('"None"', "")
    nf.write(str(i) + "," + nline)
f.close()
nf.close()

#create dbf from muaggatt_N
time.sleep(2)
arcpy.AddMessage(muaggatt_txt_processed)
arcpy.TableToTable_conversion(muaggatt_txt_processed, (soils_shp[:-27])+"\\tabular", "muaggatt_N.dbf")

#Add temp field in dbf. Must be string, as will join with string.
arcpy.AddField_management(muaggatt_dbf_processed, "TEMP", "TEXT", "", "", "16")
arcpy.CalculateField_management(muaggatt_dbf_processed, "TEMP", "!mukey!", "PYTHON_9.3")
fieldnames = [field.name for field in arcpy.ListFields(soils_shp)]
if "Soil_Type" in fieldnames:
    time.sleep(.01)
else:
    arcpy.AddField_management(soils_shp, "Soil_Type", "TEXT", "", "", "128")

if "HSG" in fieldnames:
    time.sleep(.01)
else:
    arcpy.AddField_management(soils_shp, "HSG", "TEXT", "", "", "8")

#join muaggatt_N.txt to SHP
addLayer = arcpy.mapping.Layer(soils_shp)
arcpy.mapping.AddLayer(df, addLayer, "BOTTOM")
addLayer = arcpy.mapping.TableView(muaggatt_dbf_processed)
arcpy.mapping.AddTableView(df, addLayer)
arcpy.RefreshTOC()
soils_layer = (arcpy.mapping.ListLayers(mxd))[0]
arcpy.AddJoin_management(soils_layer, "MUKEY", muaggatt_dbf_processed, "TEMP")

#Calculate Soil_Type
arcpy.CalculateField_management(soils_layer, "Soil_Type", "!muname!", "PYTHON_9.3")
arcpy.CalculateField_management(soils_layer, "HSG", "!hydgrpdcd!", "PYTHON_9.3")

#Remove join
arcpy.RemoveJoin_management(soils_layer, "muaggatt_N")

#Remove all layers from TOC
for lyr in arcpy.mapping.ListLayers(mxd, "", df):
    arcpy.mapping.RemoveLayer(df, lyr)
for tbl in arcpy.mapping.ListTableViews(mxd, "", df):
    arcpy.mapping.RemoveTableView(df, tbl)

#Delete files
os.remove((soils_shp[:-27])+"\\tabular\\muaggatt_N.cpg")
os.remove((soils_shp[:-27])+"\\tabular\\muaggatt_N.dbf")
os.remove((soils_shp[:-27])+"\\tabular\\muaggatt_N.dbf.xml")
os.remove((soils_shp[:-27])+"\\tabular\\muaggatt_N.txt")
