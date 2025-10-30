//base_path = "D:/Documents_D/Rojas_lab/data";
//base_path = "/Users/felixbarber/Documents/Rojas_lab/data";
//base_path = "/Volumes/easystore_hdd/Rojas_Lab/data";
//base_path = "/Volumes/data_ssd1/Rojas_Lab/data";
base_path = "/Volumes/data_ssd2/Rojas_Lab/data";
// Assumes no other image windows are open
//

//expt_id="/250606_bFB323_10uM_IPTG_tun";
//conds=newArray("10uM_IPTG", "0min","10min","20min","30min","50min","70min","90min");
//scene_nums=newArray(5,2,2,2,2,3,2,2,2); // Note that the length of this vector needs to be greater than 1 for it to work
//// note 20min scene 1 bf is wrong.

//expt_id="/250609_bFB323_10uM_IPTG_tun_TIRF";
////conds=newArray("10uM_IPTG", "0min","10min","20min","30min","40min","50min","70min","90min");
////scene_nums=newArray(3,2,2,2,2,2,2,2,2,2); // Note that the length of this vector needs to be greater than 1 for it to work
//// note 50min scene 2 bf is wrong.

expt_id="/250609_bFB323_10uM_IPTG_Tun_TIRF_v2";
conds=newArray("10uM_IPTG", "0min","10min","20min","30min","50min","70min","90min");
scene_nums=newArray(3,2,2,2,2,2,2,2,2); // Note that the length of this vector needs to be greater than 1 for it to work



// Assumes no other image windows are open
numconds=lengthOf(conds);
for (i0=1; i0<numconds+1;i0++){
	print(i0);
	print(scene_nums[i0]);
	for (i1=1; i1<scene_nums[i0-1]+1;i1++){
		print(i1);
		cond=conds[i0-1];
		temp_path=base_path+expt_id+"/"+cond;
		open(temp_path+"/s"+IJ.pad(i1,3)+".nd2"); // opening the brightfield image
		myImageID = getImageID();  
		saveAs("Tiff", temp_path+"/s"+IJ.pad(i1,3));
		// selecting an ROI
		setTool(0);                                          //Rectangle tool 
		beep();                                              //alert the user
		selectImage(myImageID);                              //make sure we have the same foreground image again
		waitForUser("Area Selection", "Select Rectangular Area to process");
		if (selectionType() != 0)                            //make sure we have got a rectangular selection
		exit("Sorry, no rectangle");
		open(temp_path+expt_id+"_"+cond+"_s"+IJ.pad(i1,3)+".nd2"); // opening the actual tirf file
		myImageID1 = getImageID();  
		saveAs("Tiff", temp_path+expt_id+"_"+cond+"_s"+IJ.pad(i1,3));
		run("Restore Selection");
		run("Crop");
		saveAs("Tiff", temp_path+expt_id+"_"+cond+"_s"+IJ.pad(i1,3)+"_crop");
		close();
		selectImage(myImageID);                              //make sure we have the same foreground image again
		close();
		print('here');
	}
}
while (nImages>0) { 
        	selectImage(nImages); 
        	close(); 
      	}

//lengthOf(conds)
//Array.print(scene_nums)
////conds[0]=
//temp=conds[1]
//temp1=newArray(temp);
//Array.print(temp1)