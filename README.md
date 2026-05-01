# 🧹 Clean-Log-Test
This repo harbors a data cleaning notebook together with data, src, log and test files within a regular file management.

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style="for-the-badge&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style="for-the-badge&logo=numpy&logoColor=white)
![Pytest](https://img.shields.io/badge/pytest-%230A9EDC.svg?style="for-the-badge&logo=pytest&logoColor=white)
![Logging](https://img.shields.io/badge/logging-informational?style="for-the-badge&logo=python&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-orange)

An end-to-end data cleaning and transformation structure designed to automate such processes, maintain detailed execution logs, and ensure code reliability through automated testing.

Please click to open it in binder:

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/ali-can-turan/clean-log-test/HEAD)
---
## 📂 Project Structure
```text
.
└── clean-log-test/
    ├── data/                  # Raw and processed datasets
    │   ├── clean.csv
    │   └── unclean.csv
    ├── logs/                  # Automated execution logs (logs.txt)
    │   └── logs.txt
    ├── notebooks/             # Data cleaning
    │   └── cleaning.ipynb
    ├── src/                   # Source codes
    │   ├── cleaning.py        # Data transformation automation codes
    │   └── logger.py          # Logging utility
    ├── tests/                 # Pytest suites
    │   └── test_cleaning.py
    ├── environment.yml        # Project dependencies
    ├── pytest.ini             # Pytest configuration
    └── requirements.txt       # Project dependencies
```
---
⚙️ Workflow & Architecture
This project is designed with a modular architecture that decouples the data processing logic from the logging and testing utilities.

🚀 Getting Started!
1. Installation:
- Clone the repository and install the dependencies:
``` shell
git clone https://github.com/ali-can-turan/clean-log-test
cd clean-log-test

pip install -r requirements.txt                           # or with conda

conda env create -f environment.yml
conda activate clean-log-test
```
2. Execution:
- You can execute and visualize the entire cleaning process via notebooks/cleaning.ipynb.
- The notebook processes the raw data located in data/uncleaned.csv: an AI generated, low-volume, sample data to simulate utmost dirtiness and noiseness at some columns.
- It leverages the DataCleaner class from src/cleaning.py to run automated cleaning scripts.
- You might intentionally play with the notebook parameters to evoke embedded errors in the python scripts.
    - Modular Architecture: Cleaning logic and logs is separated from the logging utility for better maintainability.
 
3. Log utility:
- Every transformation step is timestamped and recorded using a custom utility.
- A logger object from src/logger.py tracks the execution flow.
- Logs are simultaneously displayed in the notebook output and appended to logs/logs.txt for auditability.
    - Automated Logging: Every data transformation step is timestamped and recorded in logs/logs.txt.

4. Running Tests:
- Critical functions are covered by pytest to ensure stability and reliability.
- You are encouraged to initiate a pytest from the terminal to find out the reliability of src/cleaning.py test suite.
- So run from the terminal while you are either in the tests file or root directory:
``` shell
pytest
```
---
