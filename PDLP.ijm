macro "PDLP" {
	Dialog.create("Save All?");
	Dialog.addChoice("Save all intermediate step outputs?", newArray("Yes","No"));
	Dialog.show();
	saveAll = Dialog.getChoice();
	
	// Selects directory where the microtubule z-stacks are located. Source images
	myDir = getDirectory("Choose a directory");
	// Selects directory where the output text image files (.txt) and segment xy coordinates (.csv) will be outputted 
	outDir = getDirectory("Output");

	if (saveAll == "Yes"){
		intDir = outDir+"Intermediates"+File.separator;
		File.makeDirectory(intDir);
		if (!File.exists(intDir)) exit("Unable to create directory");
	}
	
	/* 
	 *  Selects ROI zip file which were manually traced and are in the following format ##-##-##
	 *  First set of #'s are Time-point e.g. 05
	 *  Second set of #'s are z-slide from which that segment starts, e.g. 01
	 *  Third set of #'s are z-slide from which the segment ends, e.g. 18
	 *  e.g. 05-01-18 is time-point 5 from which a duplicate z-stack will be created from z-slide 1 to 18 
	 *  which encompases the whole traced segment 
	 */ 
	roiFile = File.openDialog("Select ROI zip file");
	setBatchMode(true);
	list= getFileList(myDir);
	m = lengthOf(list);
	roiManager("reset");
	roiManager("open",roiFile);
	n = roiManager("count"); // Counts number of ROIs

	/*
	 * Next block of code will check that the number of ROIs match the number of images in the source file
	 * if not a error message will appear and the macro will be exited
	 */
	
	run("Bridge (174K)");
	for (i=0; i<n; i++){
		roiManager("select",i);
		r = getInfo("roi.name");
 		time = substring(r,0,2);
 		zmin = substring(r,3,5);
 		zmax = substring(r,6,8);
		file = "T"+time+".tiff";
		open(myDir + file);
		ID1=getImageID();
 		original=getTitle();
 		fileName=File.nameWithoutExtension();
		roiManager("select",i);
		
		/*
		 * Next bloxk of code will extract information from the ROI names for stack duplication 
		 * only having the slides that contain the segment of interest as defined by the user
		 */
 		
 		
  		run("Duplicate...", "duplicate range=&zmin-&zmax");
 		ID2=getImageID();
 		selectImage(ID2);

 		/*
 		 * Next block will first smooth the images, subtrack background using the rolling ball method 
 		 * using a bal radius of 15 pixels then sharpen the image
 		 */
 		run("Smooth", "stack");
		run("Subtract Background...", "rolling=15 stack");
		run("Sharpen", "stack");

 		if (saveAll == "Yes"){
		newName = "RB15_"+original;
		saveAs("tiff", intDir+newName);
		}
 		/*
 		 * Next block will straighten the segment
 		 * set the correct resoulution for x,y,and z
 		 * Reslice the image with .212 output 
 		 * Project the reslice using SUM slice projection method and
 		 * output the image as a text image in the output folder 
 		 * as a .txt file
 		 */
 		roiManager("select",i);
 		run("Straighten...", "title=Straight line=20 process");
 		ID3=getImageID();
		if (saveAll == "Yes"){
		newName = "ST_RB15_"+original;
		saveAs("tiff", intDir+newName);
		}
 		
 		selectImage(ID2);close();
 		selectImage(ID3);
 		setVoxelSize(0.212, 0.212, 0.5, "um");
 		run("Select All");
 		run("Reslice [/]...", "output=.212 start=Top flip");
 		ID4=getImageID();
 		if (saveAll == "Yes"){
		newName = "Resl_ST_RB15_"+original;
		saveAs("tiff", intDir+newName);
		}
		
 		selectImage(ID3);close();
 		selectImage(ID4);
 		run("Z Project...", "projection=[Max Intensity]");
 		ID5=getImageID();
 		if (saveAll == "Yes"){
		newName = "MAX_Resl_ST_RB15_"+original;
		run("16-bit");
		saveAs("tiff", intDir+newName);
		}
		
 		selectImage(ID4);close();
 		selectImage(ID5);

		
		
		getDimensions(width,height,channels,slices,frames);
		w=width+4;
		h=height;
		run("Canvas Size...","width=&w height=&h position=Center zero");
		/*
		y=(height)/2;
		x=width-1;
		setColor("white");
		setLineWidth(1);
		drawOval(0,y,4,4);
		fillOval(0,y,4,4);
		drawOval(x,y,4,4);
		fillOval(x,y,4,4);
		*/
		newName="3WJ_MAX_Resl_ST_RB15_"+original;
		saveAs("tiff",outDir+newName);
 		selectImage(ID1);
		
 		/*
 		 * Next block will extract the xy-coordinates of the ROI and save them as a .csv file
 		 */
 		roiManager("select",i);
 		Roi.getCoordinates(x, y);
		run("Clear Results");
		for (j=0; j<x.length; j++){
			setResult("X",j,x[j]);
			setResult("Y",j,y[j]);
			}
		setOption("ShowRowNumbers",false);
		updateResults;
		csvName=fileName+".csv";
		saveAs("Results",outDir+csvName);
 		selectImage(ID1);close();
 		selectImage(ID5);close();
 		}
 		selectWindow("bridge.gif");close();
 		//selectWindow("ROI Manager");run("Close");
 		selectWindow("Results");run("Close");
}
