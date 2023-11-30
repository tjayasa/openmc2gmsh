lc = 0.3;
Point(1) = {0.0,0.0,0.0,lc};
Point(2) = {1,0.0,0.0,lc};
Point(3) = {1,1,0.0,lc};
Point(4) = {0,1,0.0,lc};
Point(5) = {0.0,0.0,1,lc};
Point(6) = {1,0.0,1,lc};
Point(7) = {1,1,1,lc};
Point(8) = {0,1,1,lc};
//
Line(43) = {4,3};
Line(32) = {3,2};
Line(21) = {2,1};
Line(14) = {1,4};
//
Line(78) = {7,8};
Line(67) = {6,7};
Line(56) = {5,6};
Line(85) = {8,5};
//
Line(51) = {5,1};
Line(15) = {1,5};
Line(26) = {2,6};
Line(62) = {6,2};
Line(73) = {7,3};
Line(37) = {3,7};
Line(48) = {4,8};
Line(84) = {8,4};
//
Line Loop(1234) = {43,32,21,14};
Plane Surface(1) = {1234};
Line Loop(5678) = {85,56,67,78};
Plane Surface(2) = {5678};
Line Loop(1458) = {14,48,85,51};
Plane Surface(3) = {1458};
Line Loop(1256) = {21,15,56,62};
Plane Surface(4) = {1256};
Line Loop(2367) = {32,26,67,73};
Plane Surface(5) = {2367};
Line Loop(3478) = {43,37,78,84};
Plane Surface(6) = {3478};

Surface Loop(7) = {1,2,3,4,5,6};

Volume(8) = {7};