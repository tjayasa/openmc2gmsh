SetFactory("OpenCASCADE");
R = 5.0; // Major radius
r = 2.0; // Minor radius
Torus(1) = {0.0, 0.0, 0.0, R, r};
Mesh.CharacteristicLengthMin = 0.1;
Mesh.CharacteristicLengthMax = 0.1;
Mesh 3;
