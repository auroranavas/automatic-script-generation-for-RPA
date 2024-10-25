# Automatic Script Generation for RPA
This is the repository for the University of Seville's Software Engineering bachelor degree dissertation "Automatic Script Generation for RPA" made by Aurora Navas Jiménez. 

The increasing demand for process automation and standardization across various industries has developed the need for a tool to tackle this problem. Since then, a wide range of companies have taken care of this matter, and a novel business paradigm, Robotic Process Automation (RPA), has been born.

The process of taming these tools can be tedious. Each tool comes with its unique user interface and functionalities, which translates into spending hours and hours trying to learn them all while deciding which one works best for you and your needs.

To overcome this problem, this project proposes a tool that eliminates the need to construct automations within specific RPA tools. For this, the [ES3](https://www.linkedin.com/company/grupoes3/?originalSubdomain=es) research group, leader in the generation of RPA process models, has put part of their knowledge at my disposal. My goal will be the **generation of an executable software robot from an intermediate and vendor-agnostic process language**. In addition, the results obtained will benefit ES3’s ongoing research.

Currently, the solution is implemented for **OpenRPA** and **UiPath**.

## Repository file structure
### additional_material folder
Contains files useful to better understand the project report. Does not hold any of the final implementation.

### solution folder
- main.py: file containing the Tkinter desktop application.
- openrpa/uipath: both of these folders have the same structure.
	- conversion.py: these files hold all the functions necessary to convert the input file into an executable OpenRPA/UiPath automation.
	- monitoring_results.bpmn: input file sample.
	- openrpa/uipath_template.xaml: these files are used for the executable script generation.
	- tests_openrpa/uipath.py: several unit tests that verify the conversion process.
	- output folders: they contain examples of the output file when the *monitoring_results.bpmn* is used.

## How to use
### Installation
The system can be used in two ways: through the executable file or by running the scripts manually.

To use the executable file, simply download it from the latest release of this repository, and run the executable. In this way, you do not need to install any additional artifacts.

If you choose to use the application by downloading the code and running it, you will need to follow the following steps so everything functions as intended:

1. Download the source code from the repository.
2. The only dependency on the project is Tkinter, however, it comes pre-installed with Python in the majority of installations. In case it is not installed with your Python version, be sure to install it. 
3. From the *solution* directory, run the command: `python main.py`
### Usage
1. **Input file and RPA platform selection**: Once the application is running, click the "Browse" button to select an input file. A file explorer window will pop up. With the input file selected, you need to choose one of the two RPA target platforms. When the input file and the RPA target platform have been selected, you can click the "Generate" button.
2. **Output file generation**: After having clicked the "Generate" button, wait for the generation to finish.
3. **Output file download**: When the progress bar is completed, a "Download Executable Process'' will appear. Click it and choose a name and directory for it. When the file has been downloaded, close the window or click the "Back to Start'' button to convert more files.
