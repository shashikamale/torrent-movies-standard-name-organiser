import PTN
import re
import datetime
import os
from os import listdir,rename, path
from os.path import isfile, join, splitext,dirname


############## INPUTS ############################################


#mypath="Y:/Movies/zMovieDumps"
mypath = input("Path to Movies Folder : ").strip()
print ("Your Input Path is ==> " + mypath+"\n======================================================")

###################### VARIABLES ####################################
oldnamelist=[]
newnamelist=[]
i=0
buildjsonString=""

###################### FUNCTIONS ####################################

def getexcess(excess):
    if(isinstance(excess, list)):
        nw=""
        for word in excess:
            nw = nw+" "+re.sub('[^A-Za-z0-9.]+', '', word)

        nw=(nw.replace("  "," ",-1)).strip()
        nw="["+nw+"]"
       # print(nw)
        return (nw)
    else:
       return (str(excess))


def getNewNameofMovieFile(info):

    info2= info
    newname=""
    
    if(info.get('title')):
        newname=info['title'].title()
        info2.pop('title') 
    if(info.get('year')):
        newname=newname+ " ("+str(info.get('year')) +")" 
        info2.pop('year')
    if(info.get('quality')):
        newname=newname+" - "+info.get('quality')
        info2.pop('quality') 
    if(info.get('resolution')):
        newname=newname+" - "+info.get('resolution')
        info2.pop('resolution')
    if(info.get('codec')):
        newname=newname+" - "+info.get('codec')
        info2.pop('codec')
    if(info.get('audio')):
        newname=newname+" - "+info.get('audio')
        info2.pop('audio')
    if(info.get('excess')):
        excessinfo=getexcess(info.get('excess'))
        newname=newname+" - "+excessinfo
        info2.pop('excess')

    if(info.get('group')):
        info2.pop('group')
   
    if(info.get('container')):
        info2.pop('container')

    return (newname)

def extensionHandling(ext, newname, newnamelist):

    if(ext.lower().endswith("srt")):
        ext=".en.srt"
    
    if(ext.lower().endswith("jpg")):
        if (newname+ext) in newnamelist:
            ext=".front.jpg"
            if((newname+ext) in newnamelist):
                ext=".1"+ext
    
    return ext

def writeTheDatatoAFile(buildjsonString):
    
    onelevelUP=(os.path.dirname(mypath))
    now = datetime.datetime.now()
    dt_string = now.strftime("%Y-%m-%d_%H_%M")
    f= open(onelevelUP+"/Results_"+dt_string+".txt","w+")
    f.write("[\n")  
    buildjsonString=buildjsonString[:-2]+ " \n"
    f.write(buildjsonString)
    f.write("]\n")
    f.close() 
    print("Changes are stored in file at => "+onelevelUP+"/Results_"+dt_string+".txt")

###################### PROGRAM #####################################



onlyfiles = [
    f for f in listdir(mypath) 
        if isfile(join(mypath, f))]

print (onlyfiles)

for file in onlyfiles:
    name, ext = splitext(file)
    info =PTN.parse(file)
    #print(info)
    #info2= info
    
    newname=getNewNameofMovieFile(info)
    ext=extensionHandling(ext, newname, newnamelist)

    i=i+1

    oldnamelist.append(file)
    newfileName=newname+ext
    newnamelist.append(newfileName)
    
    if(not path.exists(mypath+"/"+newfileName)):
        rename(mypath+"/"+file , mypath+"/"+newfileName)
        buildjsonString=buildjsonString+"\t{\"count\" : "+str(i)+", \"oldfile\" : \""+file +"\" , \"newfile\" : \""+newfileName +"\" },\n"
        print(str(i) +") RENAMING : " +"\"" +file+"\" \t==>\t \"" + newfileName +"\"" )


print("==================================================")
print("\nProcessed [" + str(len(newnamelist))+ "] files")
writeTheDatatoAFile(buildjsonString)
print("==================================================")

