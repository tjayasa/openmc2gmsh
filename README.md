# OPENMC2GMSH

Currently Open Monte Carlo (OMC) is the standard for most nuclear reactor simulations. However, research in deterministic simulations does not currently have a convinient way to evaluate their results as OMC defines geometry very differntly from mesh geometry like Gmsh. This CLI tool allows users to convert from OMC files to Gmsh to make comparisons easier for researchers

## Getting Started

These instructions will help you get the CLI tool working on your machine.

### Prerequisites

Install GMsh via pip with the following command:

```
pip install gmsh
```

### Installing

First clone this repository into some location of your choosing.

```
cd DIR1
git clone git@github.com:tjayasa/openmc2gmsh.git
```

Then install this cli tool into a location of your choosing

```
cd DIR2
pip3 install -e DIR1
```

### Using the CLI
To make a run the conversion using the following format:
```
OMC2Gmsh cell_geo_file.xml cell_mat_file.xml
```

In this repo you can try to following command:
```
OMC2Gmsh OpenMC_Examples/complex_cell_geo.xml OpenMC_Examples/complex_cell_mat.xml   
```

which should generate the following gmsh view:
![example.png](https://github.com/tjayasa/openmc2gmsh/example.png?raw=true)

## Work to be done
Currently, this library cannot handle the following
* Filling universes with other universes
* Rendering any Assembly 
* Rendering any Lattice

## Notes about the code
* The Prims class is effectively a wrapper for some of the Gmsh geometry that can make it useful
* The Entity class makes it easy to create groups of Prims (Primitive) geometries
* Both of these functions will initialize a gmsh context if not already initialized. This helps abstract away any gmsh handling by higher level classes
* The OMCParser.py parses the OMC files and makes calls to the Prims and Entity classes. Ideally similar parsing files can be made to convert other file types to Gmsh as well.


## Authors

* **Swesik Ramineni**
* **Thomas Jayasankar**

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
