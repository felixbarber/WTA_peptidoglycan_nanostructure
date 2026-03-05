// Note: please split your .nd2 file into scene and channel .TIF image stacks first!
// Populate the values below with your experimental values (expt_id, num_channels, scene_nums and base_path. 
// When prompted, select a unique feature within this image that can be used to align separate timepoints throughout the timecourse.

expt_id="/250626_bFB66_tun_lysis";
num_channels = 2;
scene_nums =3;
base_path = "/Volumes/data_ssd2/Rojas_Lab/data";



for (alignment_scene=1; alignment_scene<scene_nums+1;alignment_scene++){
	temp_im_path=base_path+expt_id+expt_id+"_s"+IJ.pad(alignment_scene,3)+"_C1.tif";
	temp_val=alignment_scene-1;
	temp_im_path_original=base_path+expt_id+expt_id+".nd2 - Z="+temp_val+" C=0.tif";
	alt_temp_im_path_original=base_path+expt_id+expt_id+".nd2 - "+substring(expt_id, 1)+".nd2 (series "+alignment_scene+") - Z=0 C=0.tif";
	if( File.exists(temp_im_path)){
	    open(temp_im_path);	
	} else if(File.exists(temp_im_path_original)) {
		open(temp_im_path_original);	
	} else{
		open(alt_temp_im_path_original);	
	}
//	open(base_path+expt_id+expt_id+"_s"+IJ.pad(alignment_scene,3)+"_C1.tif");	
	myImageID = getImageID();  
	setTool(0);                                          //Rectangle tool 
	beep();                                              //alert the user
	waitForUser("Area Selection", "Select a unique rectangular Area to align relative to");
	selectImage(myImageID);                              //make sure we have the same foreground image again
	if (selectionType() != 0)                            //make sure we have got a rectangular selection
	exit("Sorry, no rectangle");
	run("Crop");
	if (File.isDirectory(base_path+expt_id+expt_id+"_reg_s"+IJ.pad(alignment_scene,3))==0){
		File.makeDirectory(base_path+expt_id+expt_id+"_reg_s"+IJ.pad(alignment_scene,3)) 
	}
	run("Image Sequence... ", "dir="+base_path+expt_id+expt_id+"_reg_s"+IJ.pad(alignment_scene,3)+"/ format=TIFF name="+substring(expt_id,1)+"_s"+IJ.pad(alignment_scene,3)+"_t"+" start=1");
	while (nImages>0) { 
  		selectImage(nImages); 
  		close(); 
	}
}