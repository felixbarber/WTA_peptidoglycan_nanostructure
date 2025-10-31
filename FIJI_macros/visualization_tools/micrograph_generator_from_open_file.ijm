expt_id="/250613_bFB66_EDADA_tun_full_rep2";
label=expt_id+"_LB_s001_C2";
//label=expt_id+"_LB_s002_C2";
//label=expt_id+"_LB_s003_C2";
//label=expt_id+"_tun_s003_C2";
//label=expt_id+"_tun_s001_C2";
//label=expt_id+"_tun_s002_C2";

//expt_id="/250616_FB6_xylose_depletion";
////label=expt_id+"_60min_s001_C2";
//label=expt_id+"_0min_s001_C2";

//expt_id="/210506_FB6_inducer_loss";
////label=expt_id+"_60min_s001_C2";
//label=expt_id+"_induced_s001_C2";

//expt_id="/220204_bFB69_Tun_gr_HADA";
//label=expt_id+"_45_s001_C2";

//expt_id="/220121_bFB66_Tun_gr";
//label=expt_id+"_45_s001_C2";

//expt_id="/240202_bFB69_Tun_HADA";
//label=expt_id+"_LB_s001_C2";
////label=expt_id+"_25min_s001_C2";

//expt_id="/210416_FB2_HADA_staining";
////label=expt_id+"_LB_s001_C2";
//label=expt_id+"_25min_s001_C2";

//expt_id="/250325_bFB293_IPTG_induction";
//label=expt_id+"_s001_t033";

//expt_id="/220309_bFB2_Tun_TIRF";
//expt_id="/210416_FB2_HADA_Staining";
//expt_id="/220207_bFB69_Tun_HADA";
//expt_id="/231012_bFB69_PBS_GlpQ_recovery_15min";
//label=expt_id+"_s001";
//expt_id="/231012_bFB69_PBS_GlpQ_recovery_15min";
//label=expt_id+"_s001";
//expt_id="/231030_bFB69_BuufferA_recovery_15min";
//label=expt_id+"_s003";
//expt_id="/230322_bFB69_Tun_lysis";
//label=expt_id+"_s001_t26_v2";
//expt_id="/230322_bFB69_Tun_lysis";
//label=expt_id+"_s001_t1_v1";
//label=expt_id+"_LB_s001_micrograph";
//label=expt_id+"_LB_s001_micrograph";
//label=expt_id+"_30min_s001_micrograph";
//expt_id="/211216_bFB66_Tun_gr";
//label=expt_id+"_s001_t151";
//expt_id="/221012_bFB69_Tun_gr";
//label=expt_id+"_s003_t001";
//label=expt_id+"_s003_t376";
//expt_id="/231004_bFB66_PBS_GlpQ_recovery_15min";
//label=expt_id+"_s001_t226_non_growing";
//expt_id="/231110_bFB66_PBS_GlpQ_500mMSorbitol_recovery_15min_ZPBS";
//label=expt_id+"_s002_t226_nongrowing";
//expt_id="/221004_bFB145_Tun_gr";
////label=expt_id+"_s001_a0376";
//label=expt_id+"_s002_a0376";
//expt_id="/221005_bFB149_Tun_gr";
////label=expt_id+"_s001_a0376";
//label=expt_id+"_s001_a0376";
//expt_id="/221012_bFB69_Tun_gr";
////label=expt_id+"_s001_a0376";
////label=expt_id+"_s001_a0376";
//label=expt_id+"_s002_a0376";



//expt_id="/221021_bFB66_Tun_gr";
//label=expt_id+"_s003_hada";
//expt_id="/220204_bFB69_Tun_gr";
//label=expt_id+"_s003_hada";


//num_channels=3;
num_channels=1;
out_path="/Users/barber.527/Documents/Rojas_lab/data/micrographs";
//out_path="/Users/felixbarber/Documents/Rojas_lab/data/micrographs";
//	imname=expt_id+"_"+substring(mutant,1)+"_"+substring(cond,1)+"_s"+IJ.pad(i0,3)+".nd2";
//	outname=expt_id+"_"+substring(mutant,1)+"_"+substring(cond,1)+"_s"+IJ.pad(i0,3)+"_crop.png";
myImageID = getImageID();
selectImage(myImageID);                              //make sure we have the same foreground image again  
setTool(0);                                          //Rectangle tool 
beep();                                              //alert the user
waitForUser("Area Selection", "Select rectangular area to generate micrograph. Standard size=100 pixels.");
selectImage(myImageID);                              //make sure we have the same foreground image again
if (selectionType() != 0)                            //make sure we have got a rectangular selection
	exit("Sorry, no rectangle");
run("Crop");
run("Set Scale...", "distance=1 known=0.0929 unit=micron global");
run("Scale Bar...", "width=5 height=7 thickness=4 font=14 color=White background=None location=[Lower Right] horizontal bold hide overlay label");
if (num_channels>1){
	run("Split Channels");
}
if (num_channels==1){
	run("Grays");
	run("RGB Color");
	saveAs("PNG", out_path+label+"_C1");	
	close();
}
if (num_channels==2){
	run("Grays");
	run("RGB Color");
	saveAs("PNG", out_path+label+"_C2");	
	close();
}
if (num_channels==3){
	run("Grays");
	run("RGB Color");
	saveAs("PNG", out_path+label+"_C3");	
	close();
	run("Grays");
	run("RGB Color");
	saveAs("PNG", out_path+label+"_C2");	
	close();
	run("Grays");
	run("RGB Color");
	saveAs("PNG", out_path+label+"_C1");	
	close();
}
