// Note: can remove a point with alt+click
// Note: You should restart imageJ prior to running this code! For some reason, "Fresh Start" doesn't do it.
run("Fresh Start");

base_path="/Users/felixbarber/Documents/Rojas_lab/data";

expt_id="/250626_bFB66_tun_lysis";
len_time = 31;
scene_nums = 3;
starting_point = newArray(6,10,6,6); // This should be the timepoint at which you first observe cell lysis by eye for each scene
base_path = "/Volumes/data_ssd1/Rojas_Lab/data";

//expt_id="/240729_bFB69_Tun_lysis";
//len_time = 26;
//scene_nums = 4;
//starting_point = newArray(1,1,1,12,1); // This should be the timepoint at which you first observe cell lysis by eye for each scene
//base_path = "/Volumes/data_ssd1/Rojas_Lab/data";

//expt_id="/230317_bFB69_Tun_Lysis";
//scene_nums = 6;
//len_time = 19;
//starting_point = newArray(2,6,1,7,1,2); // This should be the timepoint at which you first observe cell lysis by eye for each scene
//base_path="/Volumes/data_ssd1/Rojas_Lab/data"";

//expt_id="/230314_bFB169_Mecillinam_Tun";
//scene_nums = 5;

//
//expt_id="/230321_bFB7_Tun_lysis";
//scene_nums = 7;
//len_time = 28;
//starting_point = newArray(14,13,12,1,8,4,16); // This should be the timepoint at which you first observe cell lysis


//expt_id="/230327_bFB8_Tun_lysis";
//scene_nums = 6;
//len_time = 38;
//starting_point = newArray(11,11,9,13,13,13); // This should be the timepoint at which you first observe cell lysis

//expt_id="/230322_bFB69_Tun_lysis";
//scene_nums = 6;
//len_time = 26;
//starting_point = newArray(6,3,2,1,1,1); // This should be the timepoint at which you first observe cell lysis by eye for each scene


temp_path=base_path+expt_id;  // This part will need to change
temp_path1=base_path+expt_id+"/annotated_images";

if (File.isDirectory(temp_path1)==0){
	File.makeDirectory(temp_path1) 
}

labeling_types=newArray("Total","PI_stain");
//imname=expt_id+"_PI.nd2";
for (i0=1; i0<scene_nums+1;i0++){
	temp_path2=base_path+expt_id+"/annotated_images/s"+IJ.pad(i0,3);
	if (File.isDirectory(temp_path2)==0){
		File.makeDirectory(temp_path2) 
	}
//	for (i1=starting_point[i0-1]; i1<len_time+1;i1++){
	for (i1=starting_point[i0-1]; i1<len_time+1;i1++){
//		imname=expt_id+"_PI.nd2";
		if ((i1==starting_point[i0-1]) & File.exists(temp_path2+expt_id+"_s"+IJ.pad(i0,3)+"_t"+IJ.pad(i1,4)+"_lysed_cells.tif")){  // if there is a pre-annotated version of the first image, open that. I.e. if we have run the script before,
			// we use the previous version. However, this version won't use subsequent pre-annotated images since we carry over data from the first image.
			open(temp_path2+expt_id+"_s"+IJ.pad(i0,3)+"_t"+IJ.pad(i1,4)+"_lysed_cells.tif");
			myImageID1 = getImageID();
		}
		else {	
	//		imname=expt_id+"_PI.nd2";
			imname=expt_id+"_s"+IJ.pad(i0,3)+"_a"+IJ.pad(i1,4)+".tif";
			out_name=expt_id+"_s"+IJ.pad(i0,3)+"_t"+IJ.pad(i1,4);		
			open(temp_path+expt_id+"_s"+IJ.pad(i0,3)+"_1_a"+imname);		
			open(temp_path+expt_id+"_s"+IJ.pad(i0,3)+"_2_a"+imname);		
	//		run("Merge Channels...", "c4=["+substring(expt_id,1)+"_PI"+".nd2 - "+substring(expt_id,1)+"_PI"+".nd2 (series "+i0+") - Z=0 C=0] c7=["+substring(expt_id,1)+"_PI"+".nd2 - "+substring(expt_id,1)+"_PI"+".nd2 (series "+i0+") - Z=0 C=1] create");
			temp_imname=expt_id+"_s"+IJ.pad(i0,3)+"_a"+IJ.pad(i1,4)+"-1.tif";
			run("Merge Channels...", "c4="+substring(imname,1)+" c7="+substring(temp_imname,1)+" create");
			oldImageID = getImageID();
			run("RGB Color");
			myImageID = getImageID();
			selectImage(oldImageID);
			close();
			
			selectImage(myImageID);
			run("Duplicate...", "duplicate");
			myImageID1 = getImageID();
			// Now we track the total cell number
			if (i1>starting_point[i0-1]){
				temp_imname1="insert label here";
				open(temp_path2+expt_id+"_s"+IJ.pad(i0,3)+"_t"+IJ.pad(i1-1,4)+"_lysed_cells.tif");  // This image should have the previous annotations present
				tempImageID = getImageID();
				selectImage(myImageID1);
				run("Restore Selection");
				selectImage(tempImageID);
				close();
				selectImage(myImageID1);
			}
		}
		setTool("multipoint"); 								// Multipoint tool
		beep();                                              //alert the user
		waitForUser("Select lysed cells.");
		selectImage(myImageID1);                              //make sure we have the same foreground image again
		saveAs("Tiff", temp_path2+expt_id+"_s"+IJ.pad(i0,3)+"_t"+IJ.pad(i1,4)+"_lysed_cells.tif");	
		run("Measure");
		saveAs("Results", temp_path2+expt_id+"_s"+IJ.pad(i0,3)+"_t"+IJ.pad(i1,4)+"_lysed_cells.csv");
		run("Clear Results");
		close();
	    while (nImages>0) { 
	    	selectImage(nImages); 
	    	close(); 
	    } 
	}
}
////setTool("multipoint");
//run("Merge Channels...", "c4=[230314_bFB169_Mecillinam_Tun_PI.nd2 - 230314_bFB169_Mecillinam_Tun_PI.nd2 (series 5) - Z=0 C=0] c7=[230314_bFB169_Mecillinam_Tun_PI.nd2 - 230314_bFB169_Mecillinam_Tun_PI.nd2 (series 5) - Z=0 C=1] create keep");
////run("Brightness/Contrast...");
//run("Enhance Contrast", "saturated=0.35");
//makePoint(76, 454, "small yellow hybrid");
////setTool("multipoint");
//run("Point Tool...");
//selectWindow("230314_bFB169_Mecillinam_Tun_PI.nd2 - 230314_bFB169_Mecillinam_Tun_PI.nd2 (series 5) - Z=0 C=1");
//close();
//run("Tiff...");
//selectWindow("230314_bFB169_Mecillinam_Tun_PI.nd2 - 230314_bFB169_Mecillinam_Tun_PI.nd2 (series 5) - Z=0 C=0");
//makePoint(38, 435, "small yellow hybrid");
//selectWindow("Composite");
//selectWindow("230314_bFB169_Mecillinam_Tun_PI.nd2 - 230314_bFB169_Mecillinam_Tun_PI.nd2 (series 5) - Z=0 C=0");
//selectWindow("Composite");
//saveAs("Tiff", "/Users/felixbarber/Documents/Rojas_Lab/data/230314_bFB169_Mecillinam_Tun/annotated_images/230314_bFB169_Mecillinam_Tun_PI_composite_s005_PI_labeled.tif");
//run("In [+]");
//run("In [+]");
//run("In [+]");
//run("In [+]");
//run("Out [-]");
//saveAs("Tiff", "/Users/felixbarber/Documents/Rojas_Lab/data/230314_bFB169_Mecillinam_Tun/annotated_images/230314_bFB169_Mecillinam_Tun_PI_composite_s005_allcells_labeled.tif");
//close();
