import os
import shutil

basepath = "//home//kevin//workspace//SourceForge//with_rfc"
validfile = []
totalFile = 0
for filename in os.listdir(basepath):
	totalFile += 1
	if len(os.listdir( basepath + "//" + filename )) > 2:
		shutil.copytree(basepath + "//" + filename, "//home//kevin//workspace//SourceForge//final//"+ filename)
		validfile.append(filename)
print "Total file %d" %(totalFile)
print len(validfile)
