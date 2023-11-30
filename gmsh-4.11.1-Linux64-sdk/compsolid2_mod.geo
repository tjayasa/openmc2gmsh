SetFactory("OpenCASCADE");
Mesh.CharacteristicLengthMax = 0.1;
Mesh.CharacteristicLengthMin = 0.1;
k = 15;
Include "compsolid2.geo";
BooleanIntersection(k+1) = { Volume{1}; Delete; }{ Volume{1}; Delete; };
BooleanIntersection(k+2) = { Volume{2}; Delete; }{ Volume{2}; Delete; };
BooleanIntersection(k+3) = { Volume{3}; Delete; }{ Volume{3}; Delete; };
BooleanIntersection(k+4) = { Volume{4}; Delete; }{ Volume{4}; Delete; };
