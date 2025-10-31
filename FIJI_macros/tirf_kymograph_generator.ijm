base_path = "/Volumes/data_ssd1/Rojas_Lab/data";
// Note: Include only conditions and scenes for which you want to generate kymographs.
//
expt_id="/240730_bFB83_10mMMgCl2_Tun_TIRF";
conds=newArray("55min");
scene_nums=newArray(1,1); // Note that the length of this vector needs to be greater than 1 for it to work

//
//expt_id="/240122_bFB12_TIRF_Xylose_depletion";
//conds=newArray("LB", "20min", "40min", "60min");
//scene_nums=newArray(2,2,2,2); // Note that the length of this vector needs to be greater than 1 for it to work

//
//expt_id="/240223_bFB2_Tun_TIRF";
////conds=newArray("LB", "0min", "5min","10min", "15min","20min", "25min", "30min", "35min","40min", "50min", "60min");
////scene_nums=newArray(2,2,2,2,2,2,2,2,2,2,2,2,2); // Note that the length of this vector needs to be greater than 1 for it to work
//conds=newArray("LB", "30min", "60min");
//scene_nums=newArray(2,2,2,2); // Note that the length of this vector needs to be greater than 1 for it to work

//conds=newArray("60min");
//scene_nums=newArray(2,2); // Note that the length of this vector needs to be greater than 1 for it to work
//
//expt_id="/240729_bFB2_25uM_GlpQ_recovery_TIRF";
//base_path = "/Volumes/data_ssd2/Rojas_Lab/data";
////conds=newArray("40min", "50min");
////scene_nums=newArray(2,2); // Note that the length of this vector needs to be greater than 1 for it to work
//conds=newArray("40min");
//scene_nums=newArray(2,2); // Note that the length of this vector needs to be greater than 1 for it to work


// Assumes no other image windows are open
numconds=lengthOf(conds);
for (i0=1; i0<numconds+1;i0++){
	print(i0);
	print(scene_nums[i0]);
	for (i1=1; i1<scene_nums[i0-1]+1;i1++){
		print(i1);
		cond=conds[i0-1];
		temp_path=base_path+expt_id+"/"+cond;
		temp_path1=base_path+expt_id;
		out_name=expt_id+"_"+cond+"_s"+IJ.pad(i1,3)+"_kymo.tif";
		out_name1=expt_id+"_"+cond+"_s"+IJ.pad(i1,3)+"_kymo_sample.tif";
		open(temp_path+expt_id+"_"+cond+"_s"+IJ.pad(i1,3)+"_crop.tif"); // opening the actual tirf file
		myImageID = getImageID();  
		// selecting an ROI
		setTool("line");
		beep();                                              //alert the user
		selectImage(myImageID);                              //make sure we have the same foreground image again
		waitForUser("Line Selection", "Select line to generate kymograph. Typical length: 1.25um");
		run("Duplicate...", "use");
		run("Grays");
		run("Restore Selection");
		run("Flatten");
		run("RGB Color");
		myImageID1 = getImageID();  
		// selecting an ROI
		setTool(0);                                          //Rectangle tool 
		beep();                                              //alert the user
		selectImage(myImageID1);                              //make sure we have the same foreground image again
		waitForUser("Area Selection", "Select Rectangular Area to process");
		if (selectionType() != 0){                            //make sure we have got a rectangular selection
			exit("Sorry, no rectangle");
		}
		run("Crop");
		run("Set Scale...", "distance=1 known=0.0929 unit=micron global");
//		run("Scale Bar...", "width=5 height=7 thickness=4 font=16 color=White background=None location=[Lower Right] horizontal bold hide overlay");
		run("Scale Bar...", "width=5 height=7 thickness=4 font=16 color=White background=None location=[Lower Right] horizontal bold hide");
		saveAs("TIFF", temp_path1+out_name1);
//		if (selectionType() != 0)                            //make sure we have got a rectangular selection
//		exit("Sorry, no line");
		selectImage(myImageID);    
		run("KymographBuilder", "input="+substring(expt_id,1)+"_"+cond+"_s"+IJ.pad(i1,3)+"_crop.tif");
		run("Set Scale...", "distance=1 known=0.0929 unit=micron global");
		run("Scale Bar...", "width=0.5 height=2 thickness=2 font=16 color=White background=None location=[Lower Right] horizontal bold hide");
		run("RGB Color");
		saveAs("TIFF", temp_path1+out_name);	
		close();
		close();
		close();
	}
}
while (nImages>0) { 
        	selectImage(nImages); 
        	close(); 
      	}

