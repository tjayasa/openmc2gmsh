// -----------------------------------------------------------------------------
//
//  Gmsh C++ extended tutorial 1
//
//  Geometry and mesh data
//
// -----------------------------------------------------------------------------

// The C++ API allows to do much more than what can be done in .geo files. These
// additional features are introduced gradually in the extended tutorials,
// starting with `x1.cpp'.

// In this first extended tutorial, we start by using the API to access basic
// geometrical and mesh data.

#include <iostream>
#include <fstream>
#include <vector>
#include <gmsh.h>
#include <cstdio>
#include <string>

double meshSize = 0.1;

std::vector<int> getNumEnt(std::string filename, int xdim){

	std::vector<int> entvec;

	gmsh::initialize();
	gmsh::open(filename);

	std::vector<std::pair<int, int> > entities;
  	gmsh::model::getEntities(entities);

	for(auto e : entities) {
    		// Dimension and tag of the entity:
    		int dim = e.first, tag = e.second;

    		if(dim == xdim){

    			entvec.push_back(tag);
    			//outputReport << tag << std::endl;


    		}


  	}
	//BooleanIntersection(k+1) = { Volume{1}; Delete; }{ Volume{1}; Delete; };

	gmsh::clear();
  	gmsh::finalize();

	return entvec;

}

void viewGeo(std::string filename){

	gmsh::initialize();
        gmsh::open(filename);

	gmsh::fltk::run();

	gmsh::clear();
        gmsh::finalize();
}

std::pair<int,int> getMinMax(std::vector<int> entvec){

	int vmin = -1;
	int vmax = -1;

	if(entvec.size() > 0){

		for(auto t : entvec) {

        		if(vmin < 0 || t < vmin){

				vmin = t;

			}

			if(vmax < 0 || t > vmax){
                                
                                vmax = t;

                        }

 		}

	}


	std::pair<int,int> minmax;
	minmax.first = vmin;
	minmax.second = vmax;
	return minmax;

}

bool isOverlap(std::vector<int> vec1, std::vector<int> vec2){

	for(auto v1 : vec1) {
                

		for(auto v2: vec2){

			if(v1==v2){

				return true;

			}

		}

        }


	return false;


}


std::string fnameMod(std::string filename){

	std::string mod = "_mod";
        std::string geo = ".geo";
        std::string filenameMod;

	filenameMod.append(filename.begin(),filename.end()-4);
        filenameMod.append(mod);
        filenameMod.append(geo);

	return filenameMod;
}


std::string fnameMerge(std::string filename1, std::string filename2, bool isInv){

        std::string merge;
	if(isInv == false){
       		merge = "_merge";
	}
	else{
		merge = "mergeInv";
	}
        std::string geo = ".geo";
        std::string filenameMerge;

        filenameMerge.append(filename1.begin(),filename1.end()-4);
	filenameMerge.append("_");
	filenameMerge.append(filename2.begin(),filename2.end()-4);
        filenameMerge.append(merge);
        filenameMerge.append(geo);

        return filenameMerge;
}


void printModStart(std::string filename, int k){

	std::ofstream outputMod(fnameMod(filename));


	outputMod << "SetFactory(\"OpenCASCADE\");" << std::endl;
	outputMod << "Mesh.CharacteristicLengthMax = " << meshSize << ";" << std::endl;
	outputMod << "Mesh.CharacteristicLengthMin = " << meshSize << ";" << std::endl;
	outputMod << "k = " << k << ";" << std::endl;
	outputMod << "Include \"" << filename << "\";" << std::endl;


	outputMod.close();

}


void printBolIntVol(std::string filename, std::vector<int> entvecVol, int numk){

        //std::string mod = "_mod";
        //std::string geo = ".geo";
        //std::string filenameMod;

        std::string blint1 = "BooleanIntersection(";
        std::string blint2v = ") = { Volume{";
        std::string blint3v = "}; Delete; }{ Volume{";
        std::string blint4 = "}; Delete; };";

        std::string kp = "k+";

        //filenameMod.append(filename.begin(),filename.end()-4);
        //filenameMod.append(mod);
        //filenameMod.append(geo);

        //std::cout << filenameMod << std::endl;

        std::ofstream outputMod;
       	outputMod.open(fnameMod(filename), std::ios_base::app);

        for(auto t : entvecVol) {

                outputMod << blint1;
                for(int i=0; i<numk; i++){
                        outputMod << kp;
                }
                outputMod << t << blint2v;

                for(int j1=1; j1<numk; j1++){
                        outputMod << kp;
                }
                outputMod << t << blint3v;
                for(int j2=1; j2<numk; j2++){
                        outputMod << kp;
		}
                outputMod << t << blint4 << std::endl;

        }


        outputMod.close();

}


void printBolIntSurf(std::string filename, std::vector<int> entvecSurf, int numk){

	//std::string mod = "_mod";
	//std::string geo = ".geo";
	//std::string filenameMod;

	std::string blint1 = "BooleanIntersection(";
	std::string blint2s = ") = { Surface{";
	std::string blint3s = "}; Delete; }{ Surface{";
	std::string blint4 = "}; Delete; };";

	std::string kp = "k+";

	//filenameMod.append(filename.begin(),filename.end()-4);
	//filenameMod.append(mod);
	//filenameMod.append(geo);

	//std::cout << filenameMod << std::endl;

	std::ofstream outputMod;
	outputMod.open(fnameMod(filename), std::ios_base::app);

	for(auto t : entvecSurf) {

        	outputMod << blint1;
		for(int i=0; i<numk; i++){
			outputMod << kp;
		}
		outputMod << t << blint2s;

		for(int j1=1; j1<numk; j1++){
			outputMod << kp;
		}
		outputMod << t << blint3s;
		for(int j2=1; j2<numk; j2++){
                        outputMod << kp;
                }
		outputMod << t << blint4 << std::endl;

  	}

	outputMod.close();

}

void printTranDup(std::string filename, std::vector<int> entvecVol){

	std::string trdu1 = "Translate {0, 0, 0} { Duplicata{ Volume{";
	std::string trdu2 = "}; } }";
	std::string del1 = "Delete{ Volume{";
	std::string del2 = "};}";


	std::ofstream outputMod;
        outputMod.open(fnameMod(filename), std::ios_base::app);

	for(auto t : entvecVol) {

                        
                outputMod << trdu1 << t << trdu2 << std::endl;
		outputMod << del1 << t << del2 << std::endl;


        }


        outputMod.close();

}




std::vector<int> addNonDup(std::vector<int> vecall, std::vector<int> vecexc){

	std::vector<int> vecunq;
	int countnoteq;

	std::cout << "vecall vals:" << std::endl;
	for(auto tall1 : vecall){

		std::cout << tall1 << std::endl;

	}

	std::cout << "vecexc vals:" << std::endl;
	for(auto texc1 : vecexc){

		std::cout << texc1 << std::endl;

	}

	std::cout << "vecunq fill fcn:" << std::endl;
	for(auto tall : vecall){

		countnoteq = 0;

                for(auto texc : vecexc){

               		std::cout << tall << "," << texc << std::endl;
			if(tall != texc){
				countnoteq = countnoteq + 1;
			}

        	}

		std::cout << "countnoteq:" << countnoteq << std::endl;
		std::cout << "vecexc size:" << vecexc.size() << std::endl;
		if(countnoteq == vecexc.size()){
			vecunq.push_back(tall);
		}

        }

	std::cout << "vecunq vals:" << std::endl;
        for(auto tunq1 : vecunq){

                std::cout << tunq1 << std::endl;

        }


	return vecunq;

}


void printMerge(std::string filename1, std::string filename2, std::vector<int> ev3_1, std::vector<int> ev3_2, bool isInv){

        std::ofstream outputMod(fnameMerge(filename1,filename2, isInv));

        outputMod << "SetFactory(\"OpenCASCADE\");" << std::endl;
        outputMod << "Mesh.CharacteristicLengthMax = " << meshSize << ";" << std::endl;
        outputMod << "Mesh.CharacteristicLengthMin = " << meshSize << ";" << std::endl;
        outputMod << "Merge \"" << fnameMod(filename2) << "\";" << std::endl;
	outputMod << "Merge \"" << filename1 << "\";" << std::endl;

	outputMod.close();

	int max1 = getMinMax(ev3_1).second;
	int max2 = getMinMax(ev3_2).second;

	int tag_diff = max1 + max2 + 1;

	std::vector<int> ev3_Merge = getNumEnt(fnameMerge(filename1,filename2, isInv),3);
	std::vector<int> ev3_1M = addNonDup(ev3_Merge,ev3_2);

	//for(auto t3: ev3_Merge){

	//	std::cout << t3 << std::endl;

	//}

	//int idk = 1;

	//for(auto t3 : ev3_Merge){


		//for(auto t2M : ev3_2){

			//std::cout << t3 << " , " << t2M << std::endl;

			//if(t3 == t2M){

			  // std::cout << "hit" << std::endl;			   
			   //idk == 0;

			   //std::cout << "in if,idk=" << idk << std::endl;	   

			//}

			//std::cout << "out if,idk=" << idk << std::endl;

		//}
                
		//if(idk == 1){

			//ev3_1M.push_back(t3);


		//}

        //}
	
	outputMod.open(fnameMerge(filename1,filename2, isInv), std::ios_base::app);

	std::string bldif1 = "BooleanDifference(";
	std::string bldif2 = ") = { Volume{";
	std::string bldif3 = "}; Delete; }{ Volume{";
	std::string bldif4 = "}; Delete; };";

	outputMod << bldif1 << tag_diff << bldif2;

	int i1 = 1;
	int i2 = 1;

	for(auto t1 : ev3_1M){

		if(i1 > 1){
			outputMod << ",";
		}

		outputMod << t1;

		i1 = i1+1;

	}

	outputMod << bldif3;

	for(auto t2 : ev3_2){

                if(i2 > 1){
                        outputMod << ",";
                }

                outputMod << t2;

                i2 = i2+1;

        }

	outputMod << bldif4 << std::endl;

        outputMod.close();

}



int main(int argc, char **argv)
{
  if(argc < 2) {
    std::cout << "Usage: " << argv[0] << " file" << std::endl;
    return 0;
  }

  //gmsh::initialize();

  // You can run this tutorial on any file that Gmsh can read, e.g. a mesh file
  // in the MSH format: `t1.exe file.msh'
  //gmsh::open(argv[1]);

  std::string filename1 = argv[1];
  std::string filename2 = argv[2];

  //viewGeo(filename1);

  //std::cout << filename << std::endl;

  //gmsh::open(filename);

  // Print the model name and dimension:
  //std::string name;
  //gmsh::model::getCurrent(name);
  //std::cout << "Model " << name << " (" << gmsh::model::getDimension()
  //          << "D)\n";

  // Get all the elementary entities in the model, as a vector of (dimension,
  // tag) pairs:
  //std::vector<std::pair<int, int> > entities;
  //gmsh::model::getEntities(entities);

  //std::vector<int> entvec = getNumEnt(filename,2);

  //std::ofstream outputReport("enttags.txt");

  //for(auto e : entities) {
    // Dimension and tag of the entity:
    //int dim = e.first, tag = e.second;
    
    //if(dim == 3){

    //entvec.push_back(tag);
    //outputReport << tag << std::endl;


    //}
    

  //}

  //for(auto t : entvec) {

  //	printf("%d\n",t);

  //}

  //std::pair<int,int> entvecRange = getMinMax(entvec);
  //printf("vec range:\n");
  //printf("%d\n",entvecRange.first);
  //printf("%d\n",entvecRange.second);

  std::vector<int> ev0_1 = getNumEnt(filename1,0);
  std::vector<int> ev1_1 = getNumEnt(filename1,1);
  std::vector<int> ev2_1 = getNumEnt(filename1,2);
  std::vector<int> ev3_1 = getNumEnt(filename1,3);

  //std::vector<int> ev0_2 = getNumEnt(filename2,0);
  //std::vector<int> ev1_2 = getNumEnt(filename2,1);
  std::vector<int> ev2_2 = getNumEnt(filename2,2);
  std::vector<int> ev3_2 = getNumEnt(filename2,3);

  //std::pair<int,int> ev0R = getMinMax(ev0_2);
  //std::pair<int,int> ev1R = getMinMax(ev1_2);
  std::pair<int,int> ev2R = getMinMax(ev2_2);
  std::pair<int,int> ev3R = getMinMax(ev3_2);

  int k;

  if(ev2R.second > ev3R.second){
	k = ev2R.second;
  }
  else{
	k = ev3R.second;
  }

  printModStart(filename2,k+1);

  std::cout << ev3_2.size() << std::endl;

  if(ev3_2.size() > 0 && isOverlap(ev3_1,ev3_2)){

	std::cout << "Volume overlap found" << std::endl;
	printBolIntVol(filename2,ev3_2,1);
	//printTranDup(filename2,ev3_2);

  }

  std::vector<int> ev0_2mod = getNumEnt(fnameMod(filename2),0);
  std::vector<int> ev1_2mod = getNumEnt(fnameMod(filename2),1);
  std::vector<int> ev2_2mod = getNumEnt(fnameMod(filename2),2);
  std::vector<int> ev3_2mod = getNumEnt(fnameMod(filename2),3);

  std::vector<int> ev2_2mod_hold = ev2_2mod;

  int loopBreak = 0;
  int kint = 1;

  while((isOverlap(ev2_1,ev2_2mod) || isOverlap(ev1_1,ev1_2mod) || isOverlap(ev0_1,ev0_2mod)) && loopBreak == 0){

	std::cout << "P,L,S overlap found, iteration = "<< kint << std::endl;
	printBolIntSurf(filename2,ev2_2mod_hold,kint);

	ev0_2mod = getNumEnt(fnameMod(filename2),0);
  	ev1_2mod = getNumEnt(fnameMod(filename2),1);
  	ev2_2mod = getNumEnt(fnameMod(filename2),2);

	kint=kint+1;

	if(kint > 25){
		loopBreak = 1;
	}

	std::cout << "P Range: 1: (" << getMinMax(ev0_1).first << "," << getMinMax(ev0_1).second << ") 2: (" << getMinMax(ev0_2mod).first << "," << getMinMax(ev0_2mod).second << ")" << std::endl;
	std::cout << "L Range: 1: (" << getMinMax(ev1_1).first << "," << getMinMax(ev1_1).second << ") 2: (" << getMinMax(ev1_2mod).first << "," << getMinMax(ev1_2mod).second << ")" << std::endl;
	std::cout << "S Range: 1: (" << getMinMax(ev2_1).first << "," << getMinMax(ev2_1).second << ") 2: (" << getMinMax(ev2_2mod).first << "," << getMinMax(ev2_2mod).second << ")" << std::endl << std::endl;

  }

  std::cout << fnameMerge(filename1,filename2,false) << std::endl;

  printMerge(filename1,filename2,ev3_1,ev3_2mod,false);

  viewGeo(fnameMerge(filename1,filename2,false));

  //const char * cmerge = fnameMerge(filename1,filename2,false).c_str();

  //std::remove(cmerge);

  //printBolIntSurf(filename,getNumEnt(filename,2),1);

  //outputReport.close();

  // We can use this to clear all the model data:
  //gmsh::clear();

  //gmsh::finalize();
  return 0;
}
