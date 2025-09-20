  include <modules/module_gridfinity.scad>
  $fn=64;
//  difference() {
//    grid_block(5,2,8,lip_settings=LipSettings(lipStyle="none"));
//    #translate([2.900,2.900,8.000])cube([204.200,78.200,56.000]);
//  }

difference() {
    grid_block(4,3,8,lip_settings=LipSettings(lipStyle="none"));
    translate([2.900,2.900,8.000])cube([162.200,120.200,56.000]);
   #translate([126.000,-1.000,-1.000])cube([43,128,60.000]);
}

//union() {
//cube([60,42,7],center=true);
//difference() {
//translate([0,0,3.5])linear_extrude(30,convexity=0.5,scale=0.9)square([58,37],center=true);
//translate([0,0,3.5])linear_extrude(31,convexity=0.5,scale=0.9)square([53,32],center=true);
//};
//}
