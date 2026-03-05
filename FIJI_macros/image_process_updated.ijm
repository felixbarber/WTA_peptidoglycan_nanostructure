// Note: please split your .nd2 file into scene and channel .TIF image stacks first!
// Populate the values below with your experimental values (expt_id, num_channels, scene_nums and base_path. 
// This will split timecourse stacks, generating individual folders folders for each of your channels and scenes, with individual images for each folder.

expt_id="/250626_bFB66_tun_lysis";
num_channels = 2;
scene_nums =3;
base_path = "/Volumes/data_ssd2/Rojas_Lab/data";


//

for (i0=1; i0<scene_nums+1;i0++){
	for (i2=1;i2<num_channels+1;i2++){
		temp_im_path=base_path+expt_id+expt_id+"_s"+IJ.pad(i0,3)+"_C"+IJ.pad(i2,1)+".tif";
		temp_val=i0-1;
		temp_val1=i2-1;
		temp_im_path_original=base_path+expt_id+expt_id+".nd2 - Z="+temp_val+" C="+temp_val1+".tif";
		alt_temp_im_path_original=base_path+expt_id+expt_id+".nd2 - "+substring(expt_id, 1)+".nd2 (series "+i0+") - Z=0 C="+temp_val1+".tif";
//		231018_bFB69_PBS_GlpQ_recovery_15min.nd2 - 231018_bFB69_PBS_GlpQ_recovery_15min.nd2 (series 1) - Z=0 C=0 Sample of alt im path
		if( File.exists(temp_im_path)){
		    open(temp_im_path);	
		} else if(File.exists(temp_im_path_original)) {
			open(temp_im_path_original);	
		} else{
			open(alt_temp_im_path_original);	
		}

		temp_path = base_path+expt_id+expt_id+"_s"+IJ.pad(i0,3)+"_C"+IJ.pad(i2,1);
		if (File.isDirectory(temp_path)==0){
			File.makeDirectory(temp_path) 
		}
		run("Image Sequence... ", "dir="+temp_path+"/ format=TIFF name="+substring(expt_id,1)+"_s"+IJ.pad(i0,3)+"_C"+IJ.pad(i2,1)+"_t"+" start=2");
		
//		for (i1=1; i1<num_timesteps+1;i1++1){
//			selectWindow(substring(expt_id,1)+"_s"+IJ.pad(i0,3)+"_C"+IJ.pad(i2,1)+"-"+IJ.pad(i1,4));
//			saveAs("Tiff", temp_path+expt_id+"_s"+IJ.pad(i0,3)+"_C"+IJ.pad(i2,1)+"_t"+IJ.pad(i1,4));
//		}
		while (nImages>0) { 
        	selectImage(nImages); 
        	close(); 
      	}
	}

}
