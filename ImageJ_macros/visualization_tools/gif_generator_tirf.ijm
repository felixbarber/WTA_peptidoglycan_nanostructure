base_path = "/Volumes/data_ssd1/Rojas_Lab/data";
//base_path = "/Volumes/data_ssd2/Rojas_Lab/data";
//timepoints = 31;

expt_id="/240730_bFB83_10mMMgCl2_Tun_TIRF";
//cond="/LB";
cond="/30min";
scene=1;
timepoints = 31;

//expt_id="/241130_bFB95_Tun_TIRF";
//timepoints = 31;
////cond="/LB";
////cond="/0min";
////cond="/10min";
////cond="/25min";
////cond="/30min";
////cond="/40min";
////cond="/50min";
//cond="/60min";
//scene = 2;

//expt_id="/220222_bFB83_Tun_TIRF_Mg";
//expt_id="/230221_bFB83_Tun_TIRF";
//timepoints = 46;
//expt_id="/240730_bFB83_10mMMgCl2_Tun_TIRF";
//cond="/LB";
//cond="/0min";
//cond="/10min";
//cond="/20min";
//cond="/30min";
//cond="/40min";
//cond="/50min";
//cond="/60min";
//scene = 2;

//expt_id="/241204_bFB12_Xylose_depletion_TIRF";
//expt_id="/210719_FB12_xylose_depletion_TIRF";
//expt_id="/240111_bFB12_TIRF_Xylose_depletion";
//expt_id="/231120_bFB12_Xylose_depletion_TIRF";
//expt_id="/240122_bFB12_TIRF_Xylose_depletion";
//cond="/LB";
//cond="/0min";
//cond="/20min";
//cond="/40min";
//cond="/60min";
//cond="/80min";
//cond="/100min";
//cond="/110min";
//scene = 1;

//
//expt_id="/221103_bFB72_TIRF";
//scene = 1;
//timepoints = 46;
//
//expt_id="/240122_bFB12_TIRF_Xylose_depletion";
////cond="/LB";
////scene=1;
//cond="/110min";
//scene=1;



//expt_id="/220211_bFB10_Tun_TIRF";
//cond="/LB";
//scene=1;

//expt_id="/240126_bFB10_Tun_TIRF";
//cond="/LB";
//scene=1;

//expt_id="/240124_bFB2_Tun_TIRF";
////cond="/LB";
////cond="/30min";
//cond="/60min";
//scene = 1;
//
//expt_id="/240410_bFB2_Tun_TIRF";
////cond="/LB";
////cond="/30min";
//cond="/60min";
//scene = 1;

//
//expt_id="/240729_bFB2_25uM_GlpQ_recovery_TIRF";
////cond="/LB";
////cond="/30min";
////cond="/50min";
//cond="/40min";
//scene = 2;
////scene = 1;
//base_path = "/Volumes/data_ssd2/Rojas_Lab/data";


//expt_id="/240122_bFB12_TIRF_Xylose_depletion";
////cond="/LB";
//cond="/110min";
//scene = 2;

//expt_id="/231120_bFB12_Xylose_depletion_TIRF";
//cond="/LB";
//scene = 2;
//expt_id="/220309_bFB2_Tun_TIRF";
//cond="/LB";
//scene = 1;
//cond="/30min";
//scene = 1;
//cond="/30min";
//scene = 1;

//expt_id="/240730_bFB83_10mMMgCl2_Tun_TIRF";
//cond="/LB";
//scene = 1;

//expt_id="/220215_bFB83_Tun_TIRF";
//cond="/LB";
//scene = 2;

//expt_id="/220222_bFB83_Tun_TIRF_Mg";
//cond="/LB";
//scene = 2;




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
run("Label...", "format=00:00 starting=0 interval=2 x=5 y=20 font=18 text=[] range=1-"+IJ.pad(timepoints,1));
run("Scale Bar...", "width=5 height=6 thickness=4 font=14 color=White background=None location=[Lower Right] horizontal bold label");

saveAs("Tiff", base_path+expt_id+cond+expt_id+"_"+substring(cond,1)+"_s"+IJ.pad(scene,3)+"_crop_gif_image"+".tif");
run("Animated Gif ... ", "name=["+substring(expt_id,1)+"_"+substring(cond,1)+"_s"+IJ.pad(scene,3)+"_crop_gif"+"] set_global_lookup_table_options=[Do not use] optional=[] image=[No Disposal] set=50 number=0 transparency=[No Transparency] red=0 green=0 blue=0 index=0 filename=["+base_path+expt_id+expt_id+"_"+substring(cond,1)+"_s"+IJ.pad(scene,3)+"_crop_gif.gif]");
close();
// Note that you should set the delay to 20ms for a long timelapse (parameter "set" above"), and around 150 for a ~45 min timelapse