import arcpy, os
from datetime import datetime, timedelta

mdb = ""
flag = False
while not flag:
    path = input("Ubicacion de " + mdb + ": ")
    arcpy.env.workspace = path
    if arcpy.Exists(mdb):
        flag = True
    else:
        print("Este directorio no contiene el mdb")

f = open(os.path.join(path, "conteo.txt"), 'w')
replica = os.path.join(path, "replica.gdb")
if arcpy.Exists(replica):
    arcpy.Delete_management(replica)
arcpy.CreateFileGDB_management(path, "replica")
arcpy.TableToTable_conversion(os.path.join(mdb, ""), replica, "")
table = arcpy.env.workspace = os.path.join(path, replica, "")



diccionario = {}
listaDS = arcpy.ListDatasets(gdb)
for ds in listaDS:
    listaFC = arcpy.ListFeatureClasses(listaDS)
    for fc in listaFC:
        diccionario = {
            arcpy.Describe(fc).name + ": " + arcpy.GetCount(fc)
        }
        f.writelines(lineaFichero)