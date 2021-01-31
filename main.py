from Dataset import Dataset
from CAHD import CAHD
from matplotlib.pylab import show
import time

from KL_Divergence import KL_Divergence

if __name__ == '__main__':
    # fattore moltiplicativo per candidate list
    alfa = 3
    # dimensione del dataset da analizzare
    dim_dataset = 1000
    # grado di privacy
    p = 10
    # numero sensitive item da estrarre randomicamente
    num_sensitive_items = 10
    # dim pattern
    r = 4
    # nome dataset
    dataset_name = 'BMS1'

    list_item_path = 'Dataset/' + dataset_name + '_list_item.txt'
    transaction_item = 'Dataset/' + dataset_name + '_transaction_matrix.csv'
    # costruzione Dataset
    dataset = Dataset(list_item_path=list_item_path, dataset_path=transaction_item)
    # calcolo band matrix
    print("Computing band matrix...")
    print("")
    start_time = time.time()
    band_matrix = dataset.compute_band_matrix(num_sens_items=num_sensitive_items, dim_dataset=dim_dataset)

    end_time = time.time() - start_time
    print("")
    print(f"Band matrix computed in {end_time} seconds.")
    print("")

    # generazione gruppi
    print("Executing CAHD...")
    print("")

    groups = CAHD(alfa, p, band_matrix, dataset.sensitive_items)
    group_dict = groups.create_groups()

    end_time_2 = time.time() - start_time
    end_time = end_time_2 - end_time
    print(f"CAHD executed in {end_time} seconds.")
    print("")

    print(f"Total time: {end_time_2} seconds")
    print("")

    if group_dict != -1:
        print("Printing groups...")
        print("")

        counter = 0
        for row in group_dict:
            counter += 1
            if row == -1:
                print(f"Group {counter} without sensitive item:")
            else:
                print(f"Group {counter} with sensitive item {groups.sensitive_row[row]}:")
            print(group_dict[row])

        print("")

        # computazione kl-divergence se grado di privacy è rispettabile

        xxx = KL_Divergence(p=p, band_matrix=band_matrix, groups=group_dict, r=r, sensitive_rows=groups.sensitive_row,
                            sensitive_histogram=groups.histogram_for_KL)
        xxx.compute_kl_divergence()

    show()
