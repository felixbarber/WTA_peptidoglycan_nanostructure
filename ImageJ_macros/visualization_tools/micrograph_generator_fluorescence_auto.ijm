expt_id="/250616_bFB66_EDADA";
conds=newArray("/LB", "/Tun", "/fos"); // note the brightest condition should go first
scene_nums = 3; // number of scenes to analyze per condition

//expt_id="/241121_bFB69_GlpQ_antibody_staining";
//conds=newArray("/GlpQ", "/Buffer"); // note the brightest condition should go first
//scene_nums = 3; // number of scenes to analyze per condition


//expt_id="/221212_bFB69_Bocillin_Tun";
//conds=newArray("/LB", "/0min", "/5min", "/10min"); // note the brightest condition should go first
//scene_nums = 3; // number of scenes to analyze per condition

//expt_id="/220104_bFB66_Tun_HADA";
//conds=newArray("/LB", "/0min", "/5min", "/10min"); // note the brightest condition should go first
//scene_nums = 3; // number of scenes to analyze per condition


//expt_id="/240126_bFB66_Tun_HADA";
//conds=newArray("/LB", "/0min", "/5min", "/10min"); // note the brightest condition should go first
//scene_nums = 3; // number of scenes to analyze per condition


//expt_id="/240131_bFB205_Tun_HADA";
//conds=newArray("/LB", "/0min", "/5min", "/10min"); // note the brightest condition should go first
//scene_nums = 3; // number of scenes to analyze per condition


//expt_id="/210416_FB2_HADA_Staining";
//conds=newArray("/LB", "/5min", "/10min", "/15min", "/25min"); // note the brightest condition should go first
//scene_nums = 3; // number of scenes to analyze per condition


//expt_id="/220104_bFB66_Tun_HADA";
//conds=newArray("/LB", "/0min", "/5min", "/10min"); // note the brightest condition should go first
//scene_nums = 2; // number of scenes to analyze per condition

//expt_id="/210506_FB6_inducer_loss";
//conds=newArray("/Xylose_induced", "/10min", "/25min", "/60min"); // note the brightest condition should go first
//scene_nums = 2; // number of scenes to analyze per condition


//base_path="/Volumes/easystore_hdd/Rojas_Lab/data";
//base_path="/Volumes/data_ssd1/Rojas_Lab/data";
base_path="/Volumes/data_ssd2/Rojas_Lab/data";
out_path=base_path+expt_id
num_conds=lengthOf(conds);
nums=1
for (i0=1; i0<num_conds+1;i0++){
	cond=conds[i0-1];
	temp_path=base_path+expt_id+cond+"/C2";
	for(i1=1; i1<scene_nums+1;i1++){
		imname=expt_id+"_"+substring(cond,1)+"_s"+IJ.pad(i1,3)+"_C2.tif";
		outname=expt_id+"_"+substring(cond,1)+"_s"+IJ.pad(i1,3)+"_C2_crop.tif";
		open(temp_path+imname);
		if (nums==1){
			oriImageID = getImageID();  // This will be our reference image
			run("Brightness/Contrast..."); // now the user must select the right B&C range
			waitForUser("Title", "Select B&C.");
		}
		myImageID = getImageID();  

		if (nums>1){ // Now we adjust and crop accordingly
			selectImage(oriImageID);
			run("Brightness/Contrast..."); // now the user must select the right B&C range
			waitForUser("Title", "Apply B&C to all images. Do this with B&C>set>propagate.");
			getMinAndMax(min2, max2);
			selectImage(myImageID);                              //make sure we have the same foreground image again
			setMinAndMax(min2, max2);
			setTool(0);                                          //Rectangle tool 
			beep();                                              //alert the user
			selectImage(myImageID);                              //make sure we have the same foreground image again
			makeRectangle(500, 500, 100, 100);
			waitForUser("Area Selection", "Select rectangular area to generate micrograph. Standard size=100 pixels.");
			selectImage(myImageID);                              //make sure we have the same foreground image again
			if (selectionType() != 0)                            //make sure we have got a rectangular selection
				exit("Sorry, no rectangle");
			run("Crop");
			run("RGB Color");
			run("Set Scale...", "distance=1 known=0.0929 unit=micron global");
			run("Scale Bar...", "width=5 height=7 thickness=4 font=16 color=White background=None location=[Lower Right] horizontal bold hide overlay");
//			run("RGB Color");
			run("16-bit");
			saveAs("PNG", out_path+outname);	
			close();	
		}
		nums=nums+1;
		
	}
}
setTool(0);                                          //Rectangle tool 
beep();                                              //alert the user
selectImage(oriImageID);                              //make sure we have the same foreground image again
makeRectangle(500, 500, 100, 100);
waitForUser("Area Selection", "Select rectangular area to generate micrograph. Standard size=200 pixels.");
selectImage(oriImageID);                              //make sure we have the same foreground image again
if (selectionType() != 0)                            //make sure we have got a rectangular selection
	exit("Sorry, no rectangle");
run("Crop");
//run("RGB Color");
run("16-bit");
run("Set Scale...", "distance=1 known=0.0929 unit=micron global");
//run("Scale Bar...", "width=5 height=7 thickness=4 font=16 color=White background=None location=[Lower Right] horizontal bold hide overlay");
run("Scale Bar...", "width=1 height=7 thickness=4 font=16 color=White background=None location=[Lower Right] horizontal bold hide overlay");
run("RGB Color");
outname=expt_id+"_"+substring(conds[0],1)+"_s"+IJ.pad(1,3)+"_C2_crop.tif";
saveAs("PNG", out_path+outname);	
close();	
