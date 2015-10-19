def getQuadname(fname):
            
    #Extract quadname from USGS geopdf file name
    
    # i = look through the name, if you see a "_" grab the character after that
    i = fname.find("_") + 1
    
    # j = look through the name, if you see a "_" grab the character after i
    j = fname.find("_",i+1)
    
    # if it didnt find shit, prints error
    if j < 0:
        print "Couldn't find '_' brackets around quad name"
        quadname = ""
    
    # quadname = the characters between i and j, with all the spaces replaced with _
    else: quadname = (fname[:j]).replace(' ','_')
    return quadname
    
f1 = 'NV_Silverado Mountain_320068_1990_24000_geo.pdf'
f2 = 'WI_Not a valid nameGeo.pdf'
f3 = 'Another invalid_nameGeo.pdf'
print getQuadname(f1)
print getQuadname(f2)
print getQuadname(f3)