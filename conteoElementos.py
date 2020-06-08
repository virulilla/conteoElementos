import arcpy, os
from datetime import datetime, timedelta


print "Inicio " + str(datetime.now().time())

f = open("C://CYII//conteoElementos//data//conteo.txt",'w')
mdbRecibido = "C://CYII//conteoElementos//data//recibido//RA_58270//replica.mdb"
mdbEnviado = "C://CYII//conteoElementos//data//enviado//RA_58270//replica.mdb"

replicaRecibido = os.path.join("C://CYII//conteoElementos//data//recibido//RA_58270", "replicaREC.gdb")
replicaEnviado = os.path.join("C://CYII//conteoElementos//data//enviado//RA_58270", "replicaENV.gdb")
if arcpy.Exists(replicaRecibido):
    arcpy.Delete_management(replicaRecibido)
if arcpy.Exists(replicaEnviado):
    arcpy.Delete_management(replicaEnviado)
arcpy.CreateFileGDB_management("C://CYII//conteoElementos//data//recibido//RA_58270", "replicaREC")
arcpy.CreateFileGDB_management("C://CYII//conteoElementos//data//enviado//RA_58270", "replicaENV")

arcpy.env.workspace = mdbRecibido
dicRecibido = {}
listaDS = arcpy.ListDatasets()
for ds in listaDS:
    arcpy.env.workspace = os.path.join(mdbRecibido, ds)
    listaFC = arcpy.ListFeatureClasses()
    for fc in listaFC:
        arcpy.CopyFeatures_management(fc, os.path.join("C://CYII//conteoElementos//data//recibido//RA_58270//replicaREC.gdb", fc))
        arcpy.MakeTableView_management(os.path.join("C://CYII//conteoElementos//data//recibido//RA_58270//replicaREC.gdb", fc), fc + "ViewREC")
        key = arcpy.Describe(fc).name
        value = str(arcpy.GetCount_management(fc + "ViewREC"))
        dicRecibido[key] = value

arcpy.env.workspace = mdbEnviado
dicEnviado = {}
listaDS = arcpy.ListDatasets()
for ds in listaDS:
    arcpy.env.workspace = os.path.join(mdbEnviado, ds)
    listaFC = arcpy.ListFeatureClasses()
    for fc in listaFC:
        arcpy.CopyFeatures_management(fc, os.path.join(
            "C://CYII//conteoElementos//data//enviado//RA_58270//replicaENV.gdb", fc))
        arcpy.MakeTableView_management(
            os.path.join("C://CYII//conteoElementos//data//enviado//RA_58270//replicaENV.gdb", fc), fc + "ViewENV")
        key = arcpy.Describe(fc).name
        value = str(arcpy.GetCount_management(fc + "ViewENV"))
        dicEnviado[key] = value

f.writelines("FC    ENVIADO    RECIBIDO" + "\n")
f.writelines("--------------------------" + "\n")
for env, rec in zip(dicEnviado.items(), dicRecibido.items()):
    if env > rec:
        line = env[0] + ": " + env[1] + ">" + rec[1] + "\n"
        f.writelines(line)

f.close()

print "Fin " + str(datetime.now().time())