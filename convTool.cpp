#include <iostream>
#include <fstream>
#include <vector>
#include <gmsh.h>
#include <cstdio>
#include <string>

//Global variable for mesh size (needs to be set for OpenCascade)
double meshSize = 0.1;

//Function to get the entity tags from file filename of dimension xdim
std::vector<int> getNumEnt(std::string filename, int xdim){

	std::vector<int> entvec;

	//Opening file in gmsh
	gmsh::initialize();
	gmsh::open(filename);

	//Get entity vector
	std::vector<std::pair<int, int> > entities;
  	gmsh::model::getEntities(entities);

	//Looping over entities
	for(auto e : entities) {

    		int dim = e.first, tag = e.second;

		//If entity is specificed dimension, adds the tag to return vector
    		if(dim == xdim){

    			entvec.push_back(tag);


    		}


  	}

	//Closing gmsh
	gmsh::clear();
  	gmsh::finalize();

	return entvec;

}

//File to open filename in gmsh and run the CAD geometry viewer
void viewGeo(std::string filename){

	gmsh::initialize();
        gmsh::open(filename);

	gmsh::fltk::run();

	gmsh::clear();
        gmsh::finalize();
}

//Gets the minimum and maximum values from a vector of positive integers
std::pair<int,int> getMinMax(std::vector<int> entvec){

	//Intializing min and max value variables
	int vmin = -1;
	int vmax = -1;

	//Checking if input vector is empty
	if(entvec.size() > 0){

		//Looping over input vector values
		for(auto t : entvec) {

			//Setting minimum value
        		if(vmin < 0 || t < vmin){

				vmin = t;

			}

			//Seeting macimum value
			if(vmax < 0 || t > vmax){
                                
                                vmax = t;

                        }

 		}

	}


	//Creation and setting of output pair
	std::pair<int,int> minmax;
	minmax.first = vmin;
	minmax.second = vmax;
	return minmax;

}

//Function checks if there are any overlapping values between two vectors
bool isOverlap(std::vector<int> vec1, std::vector<int> vec2){

	//Loop over vector 1
	for(auto v1 : vec1) {
                
		//Loop over vector 2
		for(auto v2: vec2){

			if(v1==v2){

				return true;

			}

		}

        }


	return false;


}

//Function that creates the mod file name for input filename
std::string fnameMod(std::string filename){

	std::string mod = "_mod";
        std::string geo = ".geo";
        std::string filenameMod;

	filenameMod.append(filename.begin(),filename.end()-4);
        filenameMod.append(mod);
        filenameMod.append(geo);

	return filenameMod;
}

//Function that creates the merge file name for two input files
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

//Prints the header strings of the mod file with tag shift k
void printModStart(std::string filename, int k){

	std::ofstream outputMod(fnameMod(filename));


	outputMod << "SetFactory(\"OpenCASCADE\");" << std::endl;
	outputMod << "Mesh.CharacteristicLengthMax = " << meshSize << ";" << std::endl;
	outputMod << "Mesh.CharacteristicLengthMin = " << meshSize << ";" << std::endl;
	outputMod << "k = " << k << ";" << std::endl;
	outputMod << "Include \"" << filename << "\";" << std::endl;


	outputMod.close();

}

//Writes strings for volume duplication + replacement for the mod file
void printBolIntVol(std::string filename, std::vector<int> entvecVol, int numk){

	//Setting string segments
        std::string blint1 = "BooleanIntersection(";
        std::string blint2v = ") = { Volume{";
        std::string blint3v = "}; Delete; }{ Volume{";
        std::string blint4 = "}; Delete; };";

        std::string kp = "k+";

	//Open ofstream for mod file appending
        std::ofstream outputMod;
       	outputMod.open(fnameMod(filename), std::ios_base::app);

	//Loop over volume entity vector
        for(auto t : entvecVol) {

		//Writing process for volume entity duplication + replacement
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


	//Close ofstream
        outputMod.close();

}


//Writes strings for surface duplication + replacement for the mod file
void printBolIntSurf(std::string filename, std::vector<int> entvecSurf, int numk){

	//Setting string segments
	std::string blint1 = "BooleanIntersection(";
	std::string blint2s = ") = { Surface{";
	std::string blint3s = "}; Delete; }{ Surface{";
	std::string blint4 = "}; Delete; };";

	std::string kp = "k+";

	//Open ofstream for mod file appending
	std::ofstream outputMod;
	outputMod.open(fnameMod(filename), std::ios_base::app);

	//Loop over surface entity vector
	for(auto t : entvecSurf) {

		//Writing process for surface entity duplication + replacement
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

	//Close ofstream
	outputMod.close();

}

//Prints alternate method for volume duplication+replacement (obsolete)
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



//For two input vector, adds vector elements in vecall that are NOT also in vecexc to an output vector
//Used for addressing bug of File 1 entity tags changing in the merge file
std::vector<int> addNonDup(std::vector<int> vecall, std::vector<int> vecexc){

	std::vector<int> vecunq;
	int countnoteq;

	//std::cout << "vecall vals:" << std::endl;
	//for(auto tall1 : vecall){

	//	std::cout << tall1 << std::endl;

	//}

	//std::cout << "vecexc vals:" << std::endl;
	//for(auto texc1 : vecexc){

	//	std::cout << texc1 << std::endl;

	//}

	//std::cout << "vecunq fill fcn:" << std::endl;
	for(auto tall : vecall){

		countnoteq = 0;

                for(auto texc : vecexc){

               		//std::cout << tall << "," << texc << std::endl;
			if(tall != texc){
				countnoteq = countnoteq + 1;
			}

        	}

		//std::cout << "countnoteq:" << countnoteq << std::endl;
		//std::cout << "vecexc size:" << vecexc.size() << std::endl;
		if(countnoteq == vecexc.size()){
			vecunq.push_back(tall);
		}

        }

	//std::cout << "vecunq vals:" << std::endl;
        //for(auto tunq1 : vecunq){

                //std::cout << tunq1 << std::endl;

        //}


	return vecunq;

}

//Creates and prints the merge file content with Boolean Difference
void printMerge(std::string filename1, std::string filename2, std::vector<int> ev3_1, std::vector<int> ev3_2, bool isInv){

	//Open ofstream for merge file
        std::ofstream outputMod(fnameMerge(filename1,filename2, isInv));

	//Setting merge file header strings
        outputMod << "SetFactory(\"OpenCASCADE\");" << std::endl;
        outputMod << "Mesh.CharacteristicLengthMax = " << meshSize << ";" << std::endl;
        outputMod << "Mesh.CharacteristicLengthMin = " << meshSize << ";" << std::endl;
        outputMod << "Merge \"" << fnameMod(filename2) << "\";" << std::endl;
	outputMod << "Merge \"" << filename1 << "\";" << std::endl;

	//Temporarily close the merge file (to run the merge file to get merge file entity tags)
	outputMod.close();

	//Getting entity tag from Boolean Difference function that won't cause a final entity tag conflict
	int max1 = getMinMax(ev3_1).second;
	int max2 = getMinMax(ev3_2).second;
	int tag_diff = max1 + max2 + 1;

	//Addressing issue of File 1 entity tags changing after merge
	std::vector<int> ev3_Merge = getNumEnt(fnameMerge(filename1,filename2, isInv),3);
	std::vector<int> ev3_1M = addNonDup(ev3_Merge,ev3_2);
	
	//Reopen merge file and appending
	outputMod.open(fnameMerge(filename1,filename2, isInv), std::ios_base::app);

	//Setting string segments for Boolean Difference function
	std::string bldif1 = "BooleanDifference(";
	std::string bldif2 = ") = { Volume{";
	std::string bldif3 = "}; Delete; }{ Volume{";
	std::string bldif4 = "}; Delete; };";

	outputMod << bldif1 << tag_diff << bldif2;

	int i1 = 1;
	int i2 = 1;

	//Writing file volume entities into Boolean Difference function
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

	//Closing merge file
        outputMod.close();

}


//Main function
int main(int argc, char **argv)
{

  //Checking if correct number of command line arguments are given
  if(argc < 2){
	std::cout << "Need to specify two files" << std::endl;
   	return 1;
  }
  else if(argc > 2){
	std::cout << "Too many arguments supplied" << std::endl;
	return 1;
  }


  //Retreiving input file names
  std::string filename1 = argv[1];
  std::string filename2 = argv[2];

  //Getting all entity tags for file 1
  std::vector<int> ev0_1 = getNumEnt(filename1,0);
  std::vector<int> ev1_1 = getNumEnt(filename1,1);
  std::vector<int> ev2_1 = getNumEnt(filename1,2);
  std::vector<int> ev3_1 = getNumEnt(filename1,3);

  //Getting surface and volume entity tags for file 2
  std::vector<int> ev2_2 = getNumEnt(filename2,2);
  std::vector<int> ev3_2 = getNumEnt(filename2,3);

  //Getting minimum and maximum surface and volume tags from file 2
  std::pair<int,int> ev2R = getMinMax(ev2_2);
  std::pair<int,int> ev3R = getMinMax(ev3_2);

  int k;

  //Determining tag shift from file 2 maximum surface and volume tags
  if(ev2R.second > ev3R.second){
	k = ev2R.second;
  }
  else{
	k = ev3R.second;
  }

  //Writing header for mod file
  printModStart(filename2,k+1);

  //std::cout << ev3_2.size() << std::endl;

  //Determining if volume entity tags conflict between file 1 and 2
  if(ev3_2.size() > 0 && isOverlap(ev3_1,ev3_2)){

	//Writing boolean intersection duplication + replacement volume strings to mod file
	std::cout << "Volume overlap found" << std::endl;
	printBolIntVol(filename2,ev3_2,1);

  }

  //Getting new entity tags from mod file
  std::vector<int> ev0_2mod = getNumEnt(fnameMod(filename2),0);
  std::vector<int> ev1_2mod = getNumEnt(fnameMod(filename2),1);
  std::vector<int> ev2_2mod = getNumEnt(fnameMod(filename2),2);
  std::vector<int> ev3_2mod = getNumEnt(fnameMod(filename2),3);

  std::vector<int> ev2_2mod_hold = ev2_2mod;

  //Setting variables for surface duplication + replacement loop
  int loopBreak = 0;
  int kint = 1;

  //Checking for surface, line, and point entity tag conflicts
  while((isOverlap(ev2_1,ev2_2mod) || isOverlap(ev1_1,ev1_2mod) || isOverlap(ev0_1,ev0_2mod)) && loopBreak == 0){


	//Writing boolean intersection duplication + replacement surface strings to mod file
	std::cout << "P,L,S overlap found, iteration = "<< kint << std::endl;
	printBolIntSurf(filename2,ev2_2mod_hold,kint);

	//Getting new surface, line, and point entity tags
	ev0_2mod = getNumEnt(fnameMod(filename2),0);
  	ev1_2mod = getNumEnt(fnameMod(filename2),1);
  	ev2_2mod = getNumEnt(fnameMod(filename2),2);

	kint=kint+1;

	//Loop break functionality
	if(kint > 25){
		loopBreak = 1;
	}

	//Print debugging information
	//std::cout << "P Range: 1: (" << getMinMax(ev0_1).first << "," << getMinMax(ev0_1).second << ") 2: (" << getMinMax(ev0_2mod).first << "," << getMinMax(ev0_2mod).second << ")" << std::endl;
	//std::cout << "L Range: 1: (" << getMinMax(ev1_1).first << "," << getMinMax(ev1_1).second << ") 2: (" << getMinMax(ev1_2mod).first << "," << getMinMax(ev1_2mod).second << ")" << std::endl;
	//std::cout << "S Range: 1: (" << getMinMax(ev2_1).first << "," << getMinMax(ev2_1).second << ") 2: (" << getMinMax(ev2_2mod).first << "," << getMinMax(ev2_2mod).second << ")" << std::endl << std::endl;

  }

  //std::cout << fnameMerge(filename1,filename2,false) << std::endl;

  //Writing the merge file
  printMerge(filename1,filename2,ev3_1,ev3_2mod,false);

  //Running CAD geometry viewer for merge file
  viewGeo(fnameMerge(filename1,filename2,false));

  return 0;
}
