from Dataset import Dataset
from CAHD import CAHD
from matplotlib.pylab import show

if __name__ == '__main__':
    alfa = 3
    dim_dataset = 1000
    p = 10
    num_sensitive_items = 10
    # dim pattern
    r = 4
    dataset_name = 'BMS1'

    list_item_path = 'Dataset/' + dataset_name + '_list_item.txt'
    transaction_item = 'Dataset/' + dataset_name + '_transaction_matrix.csv'
    # costruzione Dataset
    dataset = Dataset(list_item_path=list_item_path, dataset_path=transaction_item)
    # calcolo band matrix
    band_matrix = dataset.compute_band_matrix(num_sens_items=num_sensitive_items, dim_dataset=dim_dataset)

    # generazione gruppi
    groups = CAHD(alfa, p, band_matrix, dataset.sensitive_items)
    group_dict = groups.create_groups()

    group_dict[list(groups.sensitive_row.keys())[0]].to_csv("gruppo0.csv")
    group_dict[list(groups.sensitive_row.keys())[1]].to_csv("gruppo1.csv")
    show()
