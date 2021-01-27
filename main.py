from Dataset import Dataset
from CAHD import CAHD
from matplotlib.pylab import show

from KL_Divergence import KL_Divergence

if __name__ == '__main__':
    alfa = 3
    dim_dataset = 1000
    p = 20
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
    #show()

    # generazione gruppi
    groups = CAHD(alfa, p, band_matrix, dataset.sensitive_items)
    group_dict = groups.create_groups()

    # print(list(groups.sensitive_row.keys()), len(list(groups.sensitive_row.keys())))
    # print(group_dict.keys().__dict__, len(group_dict.keys()))

    # Per farlo andare non usare sensitive row!
    # group_dict[list(groups.sensitive_row.keys())[0]].to_csv("gruppo0.csv")
    # group_dict[list(groups.sensitive_row.keys())[1]].to_csv("gruppo1.csv")

    xxx = KL_Divergence(band_matrix=band_matrix, groups=group_dict, r=r, sensitive_rows=groups.sensitive_row, sensitive_histogram=groups.histogram_for_KL)
    xxx.compute_kl_divergence()

