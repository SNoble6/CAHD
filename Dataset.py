import pandas as pd
import numpy as np
from scipy.sparse.csgraph import reverse_cuthill_mckee
from scipy.sparse import csr_matrix
import matplotlib.pyplot as plt


class Dataset:
    dataset = None
    list_item = None
    num_item = None
    sensitive_items = None
    list_sensitive_items = None
    num_sensitive_items = None
    dim_dataset = None
    band_matrix = None
    sensitive_label = None

    def __init__(self, dataset_path, list_item_path):
        self.dataset = pd.read_csv(dataset_path)
        self.list_item = np.genfromtxt(list_item_path, dtype=np.int)
        self.num_item = len(self.list_item)
        self.dataset.columns = range(0, self.num_item)
        # self.dataset.columns = self.list_item
        self.dataset.to_csv('test_transaction.csv')
        # print(self.list_item)
        # np.savetxt('test_item.txt', self.list_item, delimiter='\n')

    def random_sensitive_items(self):
        # result = np.random.choice(self.list_item, size=self.num_sensitive_items)
        self.list_sensitive_items = np.random.permutation(range(0, self.num_item))[:self.num_sensitive_items]

    def save_sensitive_items(self):
        self.sensitive_items = pd.DataFrame()
        label_list = list()
        # temp_list_item = self.list_item
        # print("lista prima", len(self.list_item))
        for item in self.list_sensitive_items:
            # print("ITEM", item)
            # print(self.dataset[item])
            self.sensitive_items[item] = self.dataset[item].copy()
            self.dataset.drop(columns=item, axis=1, inplace=True)
            label_list.append(self.list_item[item])
            # temp_list_item = np.delete(temp_list_item, item)
        self.sensitive_label = np.array(label_list)
        self.list_item = np.delete(self.list_item, self.list_sensitive_items)
        # print("lista dopo", len(self.list_item))

    def add_sensitive_items(self):
        # print("ADD SENSITIVE", self.sensitive_items)
        for item in self.list_sensitive_items:
            self.band_matrix[item] = self.sensitive_items[item].copy()
        self.list_item = np.concatenate((self.list_item, self.sensitive_label))

    def compute_band_matrix(self, dim_dataset=1000, num_sens_items=10):
        """
        Dobbiamo estrarre a sorte dei sensitive items Per analizzare casi diversi, permutiamo righe e, se necessario,
        colonne e limitiamo il dataset alla dimensione massima (default = 1000) Dobbiamo riordinare il list item. Se
        necessario, prima aggiungere fake items (item = 0) usiamo il reverse cuthcill mcdonald patatine fritte method
        :param num_sens_items:
        :param dim_dataset: :param num_sens_items: :return:
        """
        self.num_sensitive_items = num_sens_items
        # self.list_sensitive_items = self.random_sensitive_items()
        self.random_sensitive_items()
        print("SENSITIVE index", self.list_sensitive_items)
        self.save_sensitive_items()

        k = len(self.list_item) + num_sens_items
        for i in range(k, dim_dataset + num_sens_items):
            self.list_item = np.append(self.list_item, values=-i)
            self.dataset[i] = 0

        # print(self.list_item)
        # print(len(self.list_item), "lunghezza. ITEM", self.list_item)

        random_row = np.random.permutation(self.dataset.shape[0])[:dim_dataset]
        # random_col = np.random.permutation(self.list_item)[:dim_dataset]
        random_col = np.random.permutation(self.dataset.columns)[:dim_dataset]

        permutation_list_item_index = list()

        for i in random_col:
            if i >= k:
                permutation_list_item_index.append(i - num_sens_items)
            else:
                permutation_list_item_index.append(i)
        permutation_list_item_index = np.array(permutation_list_item_index)
        self.list_item = self.list_item[permutation_list_item_index]

        # print("col", len(random_col))
        # print("row", len(random_row))
        square_matrix = self.dataset.iloc[random_row][random_col]
        self.sensitive_items = self.sensitive_items.iloc[random_row][:dim_dataset]
        # print("SQUARE")
        # print(square_matrix)

        graph = csr_matrix(square_matrix)
        new_order = reverse_cuthill_mckee(graph)
        self.list_item = self.list_item[new_order]
        # bandizza = graph[np.ix_(new_order, new_order)].toarray()
        # items_final = [random_col[i] for i in new_order]
        column_reordered = [square_matrix.columns[i] for i in new_order]
        # creo gl item indicizzati con la colonna
        # items_final = dict(zip(column_reordered, items_final))

        # calcolo band matrix
        self.band_matrix = square_matrix.iloc[new_order][column_reordered]
        # ordinamento righe dei sensitive items
        self.sensitive_items = self.sensitive_items.iloc[new_order][:dim_dataset]

        # print(self.sensitive_items)
        # print(self.band_matrix)

        # plottiamo le figure
        plt.figure(1)
        plt.imshow(square_matrix, cmap='jet')
        plt.colorbar()
        plt.figure(2)
        plt.imshow(self.band_matrix, cmap='jet')
        plt.colorbar()
        # plt.draw()

        i, j = graph.nonzero()
        default_bandwidth = (i - j).max() + (j - i).max() + 1
        i, j = self.band_matrix.to_numpy().nonzero()
        band_bandwidth = (i - j).max() + (j - i).max() + 1
        print("default", default_bandwidth, "band", band_bandwidth)
        self.add_sensitive_items()
        return self.band_matrix
