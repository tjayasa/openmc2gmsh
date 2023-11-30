// Define Points
Point(1) = {-10, -10, 0, 1.0};
Point(2) = {10, -10, 0, 1.0};
Point(3) = {10, 10, 0, 1.0};
Point(4) = {-10, 10, 0, 1.0};

// Define Lines
Line(1) = {1, 2};
Line(2) = {2, 3};
Line(3) = {3, 4};
Line(4) = {4, 1};

// Define Line Loop and Surface
Line Loop(1) = {1, 2, 3, 4};
Plane Surface(1) = {1};
