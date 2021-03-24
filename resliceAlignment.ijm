#@ String(label="Time-point to use as template, e.g. 01,02, etc") slide

run("Stack to Images");
run("Tile");
list = getList("image.titles");

nROI = roiManager("count"); 
for (i = 0; i <list.length; i++){
	y=list[i];
	selectWindow(y);
	roiManager("select",i);
}
list = getList("image.titles");

template="ReslMax_3WJ_T"+slide;

for (i=0; i<list.length; i++){
	x=list[i];
	run("Align Image by line ROI", "source=&x target=&template rotate");
}

for (i=0; i<list.length;i++){
	y=list[i];
	selectWindow(y);
	close();
}
