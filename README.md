# MCAS Processor
> Tools for processing SIS MCAS data into Ellevation canonical format

<br>

## Table of Contents
- [MCAS Processor](#mcas-processor)
  - [Table of Contents](#table-of-contents)
  - [## How to Install and Use this Project](#-how-to-install-and-use-this-project)
  - [## `process_mcas_workflow.ipynb`](#-process_mcas_workflowipynb)
  - [## `mcasprocessor.py`](#-mcasprocessorpy)
  - [## `batch_process.py`](#-batch_processpy)
  - [## Notes](#-notes)

<br>

## How to Install and Use this Project
---
1) Create virtual environment
   ```bash
   python -m venv data_challenge
   ```
2) Activate the environment
   ```bash
   source data_challenge/bin/activate
   ```
3) Install requirements (Only pandas and jupyter)
   ```bash
   pip install -r requirements.txt
   ```
4) Run a script listed below

<br>

## `process_mcas_workflow.ipynb`
---

Jupyter notebook where I initially developed and tested the functions before moving them into a class and separate `.py` file.

This notebook can be run top to bottom, and will output a CSV with the same filename as the input file, with `_processorized.csv` appended.

<br>

## `mcasprocessor.py`
---

File for processing a single MCAS CSV file.  
There are three options for specifying the file to process:
1. As a command line flag:  
   ```bash
   python mcasprocessor.py --filename sample-mcas.csv
   ```  
2. Hard coded at the top of `mcasprocessor.py` as the *`filename_to_process`* variable  
   
3. CLI will prompt for a filename if previous two were not found:  
   ```bash
   python mcasprocessor.py  
   >> Please enter the filename to process:  
   ```  

The program will output a file with the same name as the input filename, with the suffix `_pyprocessed.csv` appended.

<br>

## `batch_process.py`
---

This file allows the user to specify an input and output folder to batch process multiple MCAS files.  
File pattern can be specified using the *glob* method in the `files` variable

 !!! note Note:
    These commands will create almost 5GB of testing and processed files, but will take less than 5 minutes to run start to finish.



Run the following command to create 1000 copies of the sample csv.
``` bash
 for i in {0001..1000}; do cp sample-mcas.csv "dummy_data/dummy$i.csv"; done
 ```

 Run the `batch_process.py` file to process all of the files created in `dummy_data` directory and output them into the `processed_data` directory.

 ```bash
 python batch_process.py
 ```

Files will be named with the original filename + `_batchprocessed.csv` appended.

Clean out the `dummy_data` and `processed_data` directories.
```bash
rm  dummy_data/* processed_data/*
```

<br>

## Notes
---
- What if MCASProcessor didn't return any data and the methods just transformed the data internally?  As in model.fit() etc.  Harder to inpsect the df.
- There is no input validation since I assume these files are coming from the same program that always outputs them in the same format. I feel uneasy about this.
- Should missing values have a blank space placeholder?
- Is there a better name for `subject_df` in the `create_subject_df()` function?