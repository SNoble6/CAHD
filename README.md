# CAHD
Anonymization of transactional data by using CAHD(Correlation aware Anonymization of High_dimendional Data) on dataset reordered by using RCM (ReverseCuthill-McKee).

### Prerequisite
- Data in transactional form (see [transaction matrix](https://github.com/SNoble6/CAHD/blob/main/Dataset/BMS1_transaction_matrix.csv) and [list_item](https://github.com/SNoble6/CAHD/blob/main/Dataset/BMS1_list_item.txt))
- Python 3.x (we used 3.9)
- Pandas, Numpy, Scipy

### Install requirements 
```
    pip3 install -r requirements.txt
```

### Run
To run the script, just launch [Main.py](https://github.com/SNoble6/CAHD/blob/main/main.py)
```
python Main.py
```
Parameters can be modified in [Main.py](https://github.com/SNoble6/CAHD/blob/main/main.py) if needed.
