# This is a sample Python script.

# Press Maiusc+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from Dataset import Dataset
from CAHD import CAHD
from matplotlib.pyplot import show


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    alfa = 3
    dim_dataset = 1000
    p = 10
    num_sensitive_items = 10

    list_item_path = 'Dataset/BMS2_list_item.txt'
    transaction_item = 'Dataset/BMS2_transaction_matrix.csv'
    dataset = Dataset(list_item_path=list_item_path, dataset_path=transaction_item)
    band_matrix = dataset.compute_band_matrix(num_sens_items=num_sensitive_items, dim_dataset=dim_dataset)
    #print("BAND", band_matrix)
    #dataset.sensitive_items.to_csv("zio_gino.csv")
    lol = CAHD(alfa, p, band_matrix, dataset.sensitive_items)
    # lol.clean_sensitive_item()
    # lol.create_histogram()
    # lol.qid_similiarity()
    lol.create_groups()

    show()
