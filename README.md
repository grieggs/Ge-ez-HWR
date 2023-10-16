# Ge-ez-HWR
## Quick Start
1. Install [Conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html)
2. Open a terminal (conda terminal in windows), navigate to the Ge-ez-HWR directory, and then run the following depending on your operating system:  
   Linux: ```conda env create -f environment.yml``` (Recomended)  
   Windows: ```conda env create -f environment-win.yml```  
   OSX: ```conda env create -f environment-OSX.yml```  
If you have issues using one of the default environments, or would like to use GPU acceleration, go to section 2 to see detailed instructions for creating your own.
3. activate the conda environment ```conda activate geezHWR``` or ```conda activate geezHWR-GPU```
4. Make an image directory.  This is specified in the ```config_transcribe.json``` file. By default the program expects  it to be```./images```, but it can be changed to any directory on you computer by editing the ```"image_root_directory"``` in the .json file.
5. Run ```python transcribe.py``` It wil transcribe all the line images in the folder, and save the results in a .csv file.

## Troubleshooting the Environment

If the default environment.yml files don't work for you, enter the following commands:

1. ```conda create -n geezHWRc python=3.9```
2. ```conda activate geezHWRc```
3. If you are using Windows or Linux: ```conda install pytorch torchvision torchaudio cpuonly -c pytorch```  
 If you are using OSX: ```conda install pytorch torchvision torchaudio -c pytorch```  
 If you want to use a GPU go to the [PyTorch](https://pytorch.org/) website, and genrate the appropriate conda install command
4. ```pip install editdistance```
5. ```conda install tqdm```
6. From here  you should be able to return to step 4 of the quick start guide.

If you have any trouble with this software, feel free to reach out to me at sgrieggs@iup.edu
