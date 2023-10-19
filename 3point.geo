SetFactory("OpenCASCADE");
// 定义底面和顶面分辨率
lc1 = 0.05;
lc2 = 0.1;
// 定义顶部高度
zMax = 2;
// 底面的点
Point(1) = {0, 0, 0.7, lc1}; Point(2) = {1, 0, 1.1, lc1}; Point(3) = {2, 0, 1.2, lc1};
Point(4) = {0, 1, 1.1, lc1}; Point(5) = {1, 1, 0.7, lc1}; Point(6) = {2, 1, 0.8, lc1};
Point(7) = {0, 2, 1.2, lc1}; Point(8) = {1, 2, 0.9, lc1}; Point(9) = {2, 2, 0.7, lc1};
// 顶面的点
Point(10) = {0, 0, zMax, lc2}; Point(11) = {1, 0, zMax, lc2}; Point(12) = {2, 0, zMax, lc2};
Point(13) = {0, 1, zMax, lc2}; Point(14) = {1, 1, zMax, lc2}; Point(15) = {2, 1, zMax, lc2};
Point(16) = {0, 2, zMax, lc2}; Point(17) = {1, 2, zMax, lc2}; Point(18) = {2, 2, zMax, lc2};

// 底面平行于x方向的线
Line(1) = {1, 2}; Line(2) = {2, 3};
Line(3) = {4, 5}; Line(4) = {5, 6};
Line(5) = {7, 8}; Line(6) = {8, 9};
// 底面平行于y方向的线
Line(7) = {1, 4}; Line(8) = {2, 5}; Line(9) = {3, 6};
Line(10) = {4, 7}; Line(11) = {5, 8}; Line(12) = {6, 9};
// 侧面的线
Line(13) = {1, 10}; Line(14) = {2, 11}; Line(15) = {3, 12};
Line(16) = {4, 13}; Line(17) = {5, 14}; Line(18) = {6, 15};
Line(19) = {7, 16}; Line(20) = {8, 17}; Line(21) = {9, 18};
// 顶面平行于x方向的线
Line(22) = {10, 11}; Line(23) = {11, 12};
Line(24) = {13, 14}; Line(25) = {14, 15};
Line(26) = {16, 17}; Line(27) = {17, 18};
// 顶面平行于y方向的线
Line(28) = {10, 13}; Line(29) = {11, 14}; Line(30) = {12, 15};
Line(31) = {13, 16}; Line(32) = {14, 17}; Line(33) = {15, 18};

// 底面
Curve Loop(1) = {1, 8, -3, -7}; Surface(1) = {1};
Curve Loop(3) = {2, 9, -4, -8}; Surface(2) = {3};
Curve Loop(5) = {3, 11, -5, -10}; Surface(3) = {5};
Curve Loop(7) = {4, 12, -6, -11}; Surface(4) = {7};

// y=0侧面
Curve Loop(9) = {1, 2, 15, -23, -22, -13};
Plane Surface(5) = {9};
// x=1侧面
Curve Loop(10) = {9, 12, 21, -33, -30, -15};
Plane Surface(6) = {10};
// y=1侧面
Curve Loop(11) = {-6, -5, 19, 26, 27, -21};
Plane Surface(7) = {11};
// x=0侧面
Curve Loop(13) = {10, 19, -31, -28, -13, 7};
Plane Surface(8) = {13};

// 顶面
Curve Loop(14) = {22, 23, 30, 33, -27, -26, -31, -28};
Plane Surface(9) = {14};

// 整体
Surface Loop(1) = {5, 1, 2, 4, 6, 7, 9, 8, 3};
Volume(1) = {1};

Extrude {0, 0, 0.05} {
  Surface{1}; Surface{2}; Surface{3}; Surface{4};  Layers{ {1,1,1,1,1}, {0.1343797033,0.2956353472,0.4891421200,0.7213502473,1} }; Recombine;
}
BooleanDifference{ Volume{1}; Delete; }{ Volume{2}; Volume{3}; Volume{4}; Volume{5}; }
//+
Physical Surface("front", 67) = {26, 10, 17};
//+
Physical Surface("back", 68) = {30, 20, 24};
//+
Physical Surface("inlet", 69) = {27, 21, 13};
//+
Physical Surface("outlet", 70) = {29, 16, 23};
//+
Physical Surface("upperWall", 71) = {28};
//+
Physical Surface("terrain", 72) = {3, 4, 2, 1};

Physical Volume("interfluid", 73) = {1, 4, 2, 5, 3};

// // 设置8核并行
// General.NumThreads = 8;
Mesh.MshFileVersion = 2.2;
Mesh 3;
Save "mesh.msh";

// 执行命令：gmsh .\3point.geo -nt 8 -