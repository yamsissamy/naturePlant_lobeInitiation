#@ File(label="Select max projected PM directory", style = "directory") regStackDir
#@ File(label="Output", style = "directory") outputDir
#@ File(label="ROI zip file to be used as alignment") roi
#@ String (label="Image naming format sans the timepoint. e.g T26 = T") imgForm
#@ Integer (label="Timepoint to align to") source
#@ String (label="Save registerd name") saveName

setBatchMode(true);
roiManager("reset");
run("Image Sequence...", "open=&regStackDir sort");
id1=getImageID();
roiManager("open", roi);
nROI = roiManager("count");
maxZ = 1;
minZ = 100;

for (i = 0; i < nROI; i++){
	roiName=call("ij.plugin.frame.RoiManager.getName",i);
	tmpTime = substring(roiName, 1,3);
	time = parseInt(tmpTime);
	if (time < minZ){
		minZ = time;
	}
	if (time > maxZ){
		maxZ = time;
	}
}
run("Duplicate...", "duplicate range=&minZ-&maxZ");
id2=getImageID();
selectImage(id1);
close();
selectImage(id2);
run("Stack to Images");
run("Tile");
list = getList("image.titles");
for (i = 0; i < nROI; i++){
	y=list[i];
	selectWindow(y);
	roiManager("select",i);
}
list = getList("image.titles");
slide = IJ.pad(minZ,2);
template= imgForm+slide;
for (i=0; i<list.length; i++){
	x=list[i];
	run("Align Image by line ROI", "source=&x target=&template rotate");
}
for (i=0; i<list.length;i++){
	y=list[i];
	selectWindow(y);
	close();
}
tmpSegName = File.getName(roi);
segName = substring(tmpSegName, 0, 5);
tmpC1 = File.getName(regStackDir);
tmpC2 = lengthOf(tmpC1);
channel = substring(tmpC1,tmpC2-3,tmpC2);
stackName = "reg"+channel+segName;
run("Images to Stack", "name=&stackName title=[] use");
savePath = outputDir + File.separator + saveName + ".tif";
saveAs("tiff", savePath);
close();
roiManager("reset");