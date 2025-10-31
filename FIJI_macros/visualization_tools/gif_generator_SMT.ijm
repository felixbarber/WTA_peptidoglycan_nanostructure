//base_path = "/Volumes/data_ssd1/Rojas_Lab/data";
base_path = "/Volumes/data_ssd2/Rojas_Lab/data";
//timepoints = 31;

expt_id="/250527_bFB323_10uMIPTG_TIRF";
timepoints = 31;
cond="/10uM_IPTG";
//cond="/90min";
scene = 4;
int=0.5;


//expt_id="/250606_bFB323_10uM_IPTG_tun";
//timepoints = 45;
//cond="/10uM_IPTG";
////cond="/90min";
//scene = 1;
//int=0.09;

//base_path = "D:/Documents_D/Rojas_lab/data";
//base_path = "/Users/felixbarber/Documents/Rojas_lab/data";

//base_path = "/Volumes/easystore_hdd/Rojas_Lab/data";
//temp_path=base_path+expt_id;
temp_path=base_path+expt_id+cond;
//print(temp_path)
file=temp_path+expt_id+"_"+substring(cond,1)+"_s"+IJ.pad(scene,3)+".nd2";
//file=temp_path+expt_id+"_"+substring(cond,1)+"_"+IJ.pad(scene,3)+".nd2";
//print(file)
open(file);
myImageID = getImageID();  
run("Grays");
setTool(0);                                          //Rectangle tool 
beep();                                              //alert the user
waitForUser("Area Selection", "Select rectangular area to generate gif");
selectImage(myImageID);                              //make sure we have the same foreground image again
if (selectionType() != 0)                            //make sure we have got a rectangular selection
	exit("Sorry, no rectangle");
run("Crop");
run("RGB Color");
run("Set Scale...", "distance=1 known=0.0929 unit=micron global");
run("Series Labeler", "stack_type=[time series or movie] label_format=Decimal custom_suffix=sec custom_format=[] label_unit=s decimal_places=2 startup=0.000000000 interval=int every_n-th=1 first=0 last=45 location_presets=Custom x_=2 y_=30");

run("Scale Bar...", "width=5 height=6 thickness=4 font=14 color=White background=None location=[Lower Right] horizontal bold label");

saveAs("Tiff", base_path+expt_id+cond+expt_id+"_"+substring(cond,1)+"_s"+IJ.pad(scene,3)+"_crop_gif_image"+".tif");
run("Animated Gif ... ", "name=["+substring(expt_id,1)+"_"+substring(cond,1)+"_s"+IJ.pad(scene,3)+"_crop_gif"+"] set_global_lookup_table_options=[Do not use] optional=[] image=[No Disposal] set=50 number=0 transparency=[No Transparency] red=0 green=0 blue=0 index=0 filename=["+base_path+expt_id+expt_id+"_"+substring(cond,1)+"_s"+IJ.pad(scene,3)+"_crop_gif.gif]");
close();
// Note that you should set the delay to 20ms for a long timelapse (parameter "set" above"), and around 150 for a ~45 min timelapse