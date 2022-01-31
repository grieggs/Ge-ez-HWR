# Ge-ez-HWR

1. Install [Conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html)
2. Open a terminal (conda terminal in windows), navigate to the Ge-ez-HWR directory, and then run: ```conda env create -f environment.yml``` for no gpu, or ```conda env create -f environment_gpu.yml``` if you have a CUDA capable GPU.
3. activate the conda environment ```conda activate geezHWR```
4. Make an image directory.  This is specified in the ```config_transcribe.json``` file. By default the program expects  it to be```./images```, but it can be changed to any directory on you computer by editing the ```"image_root_directory"``` in the .json file.
5. Run ```python transcribe.py``` It wil transcribe all the line images in the folder, and save the results in a .csv file.