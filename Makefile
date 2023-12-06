spmvmake: convTool.cpp
	g++ convTool.cpp -o convTool.exe -I${PWD}/gmsh-4.11.1-Linux64-sdk/include -L${PWD}/gmsh-4.11.1-Linux64-sdk/lib -lgmsh
