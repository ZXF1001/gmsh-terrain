// Gmsh project created on Thu Dec 14 10:48:53 2023
//+
Point(1) = {0, 0, 0, 1.0};
//+
Point(2) = {0, 1, 0.5, 1.0};
//+
Point(3) = {1, 1, 0, 1.0};
//+
Point(4) = {1, 0, 0, 1.0};
//+
Line(1) = {2, 1};
//+
Line(2) = {1, 1};
//+
Line(3) = {1, 4};
//+
Line(4) = {4, 3};
//+
Line(5) = {3, 2};
//+
Curve Loop(1) = {5, 1, 3, 4};
//+
Surface(1) = {1};
//+
Extrude {0, 0, 1.5} {
  Surface{1}; Layers {2}; Recombine;
}//+
Physical Surface("top", 28) = {27};
//+
Physical Surface("top", 28) += {27};
