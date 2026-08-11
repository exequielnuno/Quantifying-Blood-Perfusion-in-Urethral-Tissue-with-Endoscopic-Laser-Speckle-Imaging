# Quantifying-Blood-Perfusion-in-Urethral-Tissue-with-Endoscopic-Laser-Speckle-Imaging
This repo contains the data from the article of the same name 

The code written to analyze the data contained in this repository was written in Python. Therefore, if you haven't yet, you must download it here: https://www.python.org/downloads/


Creating a virtual environment is recommended because it lets you use project-specific dependencies, keeping them isolated from other projects you work on. This helps avoid conflicts and maintains a clean, manageable setup for each project. To create and activate a virtual environment, you can use the venv module, which is available in Python 3.3 or newer. Steps are detailed here: https://docs.python.org/3/library/venv.html


Once you have Python on your machine, download the files and folder from this repository. Note that all the files and folders in this repository must be downloaded to the same parent folder. Then you can use Python's package installer (pip) to install the specific dependencies needed for this project by using the following command in the terminal.
To do this, open the terminal (whichever you used to create/activate your virtual environment in the previous step) and change your working directory to the folder containing all the files from this repository. Then run the following command:

```markdown 
pip install -r requirements.txt
```

Note that the requirements.txt file is also located in this repository. 

If you want to install the dependencies without the use of the requirements.txt file, use the following command 

```markdown 
pip install pandas==2.2.3 numpy==1.26.4 matplotlib==3.9.4 scipy==1.13.1 statsmodels==0.14.6
```
