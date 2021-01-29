from Dataset import Dataset
from CAHD import CAHD
from matplotlib.pylab import show
import time

from KL_Divergence import KL_Divergence

if __name__ == '__main__':
    alfa_array = [1, 2, 3, 4, 5]
    dim_dataset = 1000
    p_array = [4, 6, 8, 10, 15, 20]
    num_sensitive_items_array = [5, 10, 15, 20]
    # dim pattern
    r_array = [2, 4, 6, 8]
    dataset_name = 'BMS1'

    list_item_path = 'Dataset/' + dataset_name + '_list_item.txt'
    transaction_item = 'Dataset/' + dataset_name + '_transaction_matrix.csv'
    # costruzione Dataset
    for alfa in alfa_array:
        for p in p_array:
            for num_sensitive_items in num_sensitive_items_array:
                for r in r_array:
                    dataset = Dataset(list_item_path=list_item_path, dataset_path=transaction_item)
                    # calcolo band matrix
                    start_time = time.time()
                    band_matrix = dataset.compute_band_matrix(num_sens_items=num_sensitive_items, dim_dataset=dim_dataset)

                    # generazione gruppi
                    groups = CAHD(alfa, p, band_matrix, dataset.sensitive_items)
                    group_dict = groups.create_groups()

                    end_time = time.time() - start_time
                    # TODO: REMOVE COMMENT
                    # print("CAHD executed in", end_time, "seconds.")



    # print(list(groups.sensitive_row.keys()), len(list(groups.sensitive_row.keys())))
    # print(group_dict.keys().__dict__, len(group_dict.keys()))

    # Per farlo andare non usare sensitive row!
    # group_dict[list(groups.sensitive_row.keys())[0]].to_csv("gruppo0.csv")
    # group_dict[list(groups.sensitive_row.keys())[1]].to_csv("gruppo1.csv")

                    if group_dict != -1:
                        xxx = KL_Divergence(p=p, band_matrix=band_matrix, groups=group_dict, r=r, sensitive_rows=groups.sensitive_row,
                                            sensitive_histogram=groups.histogram_for_KL)
                        temp = xxx.compute_kl_divergence()
                        with open("kl_divergence_value.txt", "a") as klfile:
                            klfile.write(str(temp) + "\n")
                            klfile.close()

                    with open("time_value.txt", "a") as timefile:
                        timefile.write(str(end_time) + "\n")
                        timefile.close()
                    with open("parameters_value.txt", "a") as params:
                        params.write(str(alfa) + " " + str(p) + " " + str(num_sensitive_items) + " " + str(r) + "\n")
                        params.close()

                    print("Giro: ", alfa, p, num_sensitive_items, r)



    show()