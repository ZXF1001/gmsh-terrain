
SetFactory("OpenCASCADE");

lc = 0.5;
// 定义顶部高度
zMax = 2;
Point(1) = {0, 0, 0.7, lc};
Point(2) = {1, 0, 1.1, lc};
Point(3) = {0, 1, 1.1, lc};
Point(4) = {1, 1, 0.7, lc};
Point(4+1) = {0, 0, zMax, 0.2};
Point(4+2) = {1, 0, zMax, 0.2};
Point(4+3) = {0, 1, zMax, 0.2};
Point(4+4) = {1, 1, zMax, 0.2};

Line(1) = {1, 3};
Line(2) = {2, 4};
Line(3) = {1, 2};
Line(4) = {3, 4};

Line(4+1) = {1, 5};
Line(4+2) = {2, 6};
Line(4+3) = {3, 7};
Line(4+4) = {4, 8};

Line(8+1) = {5, 7};
Line(8+2) = {6, 8};
Line(8+3) = {5, 6};
Line(8+4) = {7, 8};

Line Loop(1) = {1, 4, -2, -3};
Line Loop(2) = {5,9,-7,-1};
Line Loop(3) = {6,10,-8,-2};
Line Loop(4) = {5,11,-6,-3};
Line Loop(5) = {7,12,-8,-4};
Line Loop(6) = {9,12,-10,-11};
Surface(1) = {1};
Plane Surface(2) = {2};
Plane Surface(3) = {3};
Plane Surface(4) = {4};
Plane Surface(5) = {5};
Plane Surface(6) = {6};
Surface Loop(1) = {1, 2, 3, 4, 5, 6};
Volume(1) = {1};

Extrude {0, 0, 0.1} {
  Surface{1}; Layers {5}; Recombine;
}

BooleanDifference{ Volume{1}; Delete; }{ Volume{2}; }

// Mesh.CharacteristicLengthMax = 1.0;
// // 画网格
//+
Physical Surface("front", 29) = {16, 9};
//+
Physical Surface("back", 30) = {12, 7};
//+
Physical Surface("inlet", 31) = {15, 10};
//+
Physical Surface("outlet", 32) = {13, 8};
//+
Physical Surface("terrain", 33) = {1};
//+
Physical Surface("upperWall", 34) = {14};
//+
Physical Volume("interfield", 35) = {1, 2};
