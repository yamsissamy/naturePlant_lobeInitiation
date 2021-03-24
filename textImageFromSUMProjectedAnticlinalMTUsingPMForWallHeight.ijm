#@ File (label = "Input directory", style = "directory") input
#@ File (label = "Output directory", style = "directory") output
#@ File (label = "Select ROI Zip File", style = "file") roiFile
#@ String (label = "File suffix", value = ".tif") suffix
#@ Float (label = "XY Pixel size (µm)") xy
#@ Float (label = "Z-step") zStep
#@ boolean (label = "Save all intermediate step outputs?") saveAll
MTDir = input+File.separator+"488";
PMDir = input+File.separator+"561";
if (saveAll == true){
	intDir = output+File.separator+"Intermediates";
	File.makeDirectory(intDir);
	if (!File.exists(intDir)) exit("Unable to create directory");
}
run("Set Measurements...", "mean modal min bounding median display redirect=None decimal=3");
run("Input/Output...", "jpeg=100 gif=-1 file=.csv save_column");
list= getFileList(input);
run("Clear Results");
roiManager("reset"); 
run("Close All");
roiManager("open",roiFile);
n = roiManager("count"); 
newImage("M", "16-bit white", 512, 512, 1);
run("Properties...", "channels=1 slices=1 frames=1 unit=µm pixel_width=&xy pixel_height=&xy voxel_depth=zStep global");
selectWindow("M");close();
setBatchMode(false);
cropROIs = newArray(n);
for (i=0; i<n; i++){
	newImage("M", "16-bit white", 512, 512, 1);
	roiManager("select",i);
	r = getInfo("roi.name");
	rL = lengthOf(r);
	t=substring(r,rL-3,rL);
	selectWindow("M");close();
	rawImg = t+".tif";
	open(PMDir + File.separator + rawImg);
	ID1=getImageID();
	original=getTitle();
	fileName=File.nameWithoutExtension();

	imageProc(ID1,original,false, false);
	selectWindow("SUM_Reslice of Straight");
	ID = getImageID();
	funCropROI(ID);
	cropROIs[i] = n+i;
	open(MTDir + File.separator + rawImg);
	ID2=getImageID();
	imageProc(ID2,original,saveAll,true);
	selectWindow("SUM_Resl_ST_RB15_"+t+".tif");
	ID5 = getImageID();
	roiManager("select", n+i);
 	run("Crop");
 	run("Select All");
	run("Measure");
 	saveAs("Text Image",output+ File.separator + "AW_"+original);
 	selectImage(ID1); close();
 	selectImage(ID2); close();
 	selectImage(ID5);close();
 }
 saveAs("Results",  output + File.separator+ "AW_details" + ".csv");
 roiManager("select", cropROIs);
 roiManager("save selected", output+File.separator+"ROISet.zip");
 selectWindow("ROI Manager");run("Close");


function imageProc(ID,original,saveAll,MT) {
	run("Smooth", "stack");
	run("Subtract Background...", "rolling=15 stack");
	run("Sharpen", "stack");

	roiManager("select",i);
	run("Straighten...", "title=Straight line=40 process");
	ID3=getImageID();
	if (saveAll == true){
	newName = "ST_RB15_"+original;run("16-bit");
	saveAs("tiff", intDir+File.separator+newName);
	}
	selectImage(ID3);
	setVoxelSize(xy, xy, zStep, "µm");
	run("Select All");
	run("Reslice [/]...", "output=&xy start=Top flip");
	ID4=getImageID();
	if (saveAll == true){
	newName = "Resl_ST_RB15_"+original;run("16-bit");
	saveAs("tiff", intDir+File.separator+newName);
	}
	selectImage(ID3);close();
	selectImage(ID4);
	if (MT == true) {
		oPeri(ID4,original,xy);
	}
	selectImage(ID4);
	run("Z Project...", "start=17 stop=23 projection=[Sum Slices]");
	if (MT == false) {
		run("16-bit");
	}
	ID5=getImageID();
	if (saveAll == true){
	newName = "SUM_Resl_ST_RB15_"+original;
	saveAs("tiff", intDir+File.separator+newName);
	}
 	selectImage(ID4);close();
}
function funCropROI(ID) {
	selectImage(ID);
	getDimensions(width, height, channels, slices, frames);
 	run("Specify...", "width=&width height=&height x=0 y=0");
 	waitForUser("Crop", "Adjust Box to fit only anticlinal signal");
 	roiManager("add");
 	roiManager("select", n+i);
 	cropName = "crop_" + t;
 	roiManager("rename", cropName);
 	close();
}
function oPeri(ID, original,xy) {
	selectImage(ID);
	getDimensions(width, height, channels, slices, frames);
	run("Properties...", "channels=1 slices=&slices frames=&frames unit=µm pixel_width=&xy pixel_height=&xy voxel_depth=&xy");
	roiManager("select", n+i);
	run("Make Inverse");
	run("Reslice [/]...", "output=&xy start=Top");
	oPID1 = getImageID();
	run("Z Project...", "projection=[Max Intensity]");
	oPID2 = getImageID();
	selectImage(oPID1);
	selectImage(oPID2);
	getDimensions(width, height, channels, slices, frames);
	run("Specify...", "width=&width height=19 x=0 y=0");
	cell1 = "C1_"+original;
	run("Duplicate...", "title=&cell1");
	oPID3 = getImageID();
	saveAs("Text Image",output+ File.separator + cell1);
	selectImage(oPID2);
	run("Specify...", "width=&width height=19 x=0 y=20");
	cell2 = "C2_"+original;
	run("Duplicate...", "title=&cell2");
	oPID4 = getImageID();
	run("Flip Vertically");
	saveAs("Text Image",output+ File.separator + cell2);
	selectImage(oPID1);close;
	selectImage(oPID2);close;
 	selectImage(oPID3);close;
	selectImage(oPID4);close;
}