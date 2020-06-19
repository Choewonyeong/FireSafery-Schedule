from os import listdir
import setting


def returnMainList():
    fileNames = []
    for fileName in listdir(setting.databaseMain):
        fileNames.append(fileName.replace('.db', ''))
    return fileNames
