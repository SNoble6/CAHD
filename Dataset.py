import pandas as pd
import numpy as np
from scipy.sparse.csgraph import reverse_cuthill_mckee
from scipy.sparse import csr_matrix
import matplotlib.pylab as plt


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
        """
        Costruttore del dataset
        :param dataset_path: percorso del file csv delle transazioni
        :param list_item_path: percorso del file txt della lista degli elementi
        """
        self.dataset = pd.read_csv(dataset_path)
        self.list_item = np.genfromtxt(list_item_path, dtype=np.int)
        self.num_item = len(self.list_item)
        self.dataset.columns = range(0, self.num_item)
        self.dataset.to_csv('test_transaction.csv')

    def random_sensitive_items(self, columns):
        """
        Funzione per estrarre a caso i sensitive items dal dataset prima delle permutazioni
        :param columns: colonne del dataset
        """
        # result = np.random.choice(self.list_item, size=self.num_sensitive_items)
        self.list_sensitive_items = np.random.permutation(columns)[:self.num_sensitive_items]

    def save_sensitive_items(self):
        """
        Funzione per salvare in un dataframe i sensitive items con le rispettive righe.
        I label dei sensitive item vengono memorizzati in una lista dedicata.
        La funzione rimuove tali elementi dal dataset iniziale e anche dalla list item.
        """
        self.sensitive_items = pd.DataFrame()
        label_list = list()

        for item in self.list_sensitive_items:
            self.sensitive_items[item] = self.dataset[item].copy()
            self.dataset.drop(columns=item, axis=1, inplace=True)
            label_list.append(self.list_item[item])

        self.sensitive_label = np.array(label_list)
        self.list_item = np.delete(self.list_item, self.list_sensitive_items)

    def add_sensitive_items(self):
        """
        Funzione per accodare i sensitive Item alla band matrix e per accodare i sensitive label
        alla list item
        """

        # for item in self.list_sensitive_items:
        #     self.band_matrix[item] = self.sensitive_items[item].copy()
        self.list_item = np.concatenate((self.list_item, self.sensitive_label))

    def compute_band_matrix(self, dim_dataset=1000, num_sens_items=10):
        """
        Funzione per il calcolo di una band matrix dim_dataset x dim_dataset
        Vengono estratti e salvati i sensitive item.
        Vengono permutate le righe e le colonne per analizzare casi diversi.
        Limitiamo il dataset alla dimensione massima (default = 1000)
        Dobbiamo riordinare il list item. Se necessario, prima aggiungere fake items (item = 0).
        Usiamo il reverse cuthcill mcdonald patatine fritte method
        :param num_sens_items: numero di sensitive items
        :param dim_dataset: dimensione finale del dataset da analizzare
        :return: la band matrix
        """
        self.num_sensitive_items = num_sens_items

        if len(self.list_item) > dim_dataset + num_sens_items:
            random_row = np.random.permutation(self.dataset.shape[0])[:dim_dataset]
            random_col = np.random.permutation(self.dataset.shape[1])[:dim_dataset + num_sens_items]

            temp_list_item = self.list_item

            square_matrix = self.dataset.iloc[random_row][random_col]
            self.random_sensitive_items(square_matrix.columns)

            self.save_sensitive_items()

            for i in self.list_sensitive_items:
                random_col = random_col[random_col != i]

            self.list_item = temp_list_item[random_col]
            square_matrix = self.dataset.iloc[random_row][random_col]
            self.num_item = dim_dataset

        else:
            self.random_sensitive_items(self.dataset.columns)
            # print("SENSITIVE index", self.list_sensitive_items)
            self.save_sensitive_items()

            k = len(self.list_item) + num_sens_items
            for i in range(k, dim_dataset + num_sens_items):
                self.list_item = np.append(self.list_item, values=-i)
                self.dataset[i] = 0

            random_row = np.random.permutation(self.dataset.shape[0])[:dim_dataset]
            random_col = np.random.permutation(self.dataset.columns)[:dim_dataset]

            permutation_list_item_index = list()

            for i in random_col:
                if i >= k:
                    permutation_list_item_index.append(i - num_sens_items)
                else:
                    permutation_list_item_index.append(i)
            permutation_list_item_index = np.array(permutation_list_item_index)
            self.list_item = self.list_item[permutation_list_item_index]

            square_matrix = self.dataset.iloc[random_row][random_col]
            self.sensitive_items = self.sensitive_items.iloc[random_row][:dim_dataset]

        graph = csr_matrix(square_matrix)
        new_order = reverse_cuthill_mckee(graph)
        self.list_item = self.list_item[new_order]
        column_reordered = [square_matrix.columns[i] for i in new_order]

        # calcolo band matrix
        self.band_matrix = square_matrix.iloc[new_order][column_reordered]
        # ordinamento righe dei sensitive items
        self.sensitive_items = self.sensitive_items.iloc[new_order][:dim_dataset]

        # plottiamo le figure
        # plt.figure(1)
        # plt.imshow(square_matrix, cmap='jet')
        # plt.colorbar()
        # plt.figure(2)
        # plt.imshow(self.band_matrix, cmap='jet')
        # plt.colorbar()
        # plt.draw()
        f, (ax1, ax2) = plt.subplots(1, 2, sharey=True)
        ax1.spy(square_matrix, marker='.', markersize='1')
        ax2.spy(self.band_matrix, marker='.', markersize='1')

        # banda prima di RCM
        i, j = graph.nonzero()
        default_bandwidth = (i - j).max() + 1

        # banda dopo RCM
        i, j = self.band_matrix.to_numpy().nonzero()
        band_bandwidth = (i - j).max() + 1

        print(f"Bandwidth before RCM: {default_bandwidth}")
        print(f"Bandwidth after RCM: {band_bandwidth}")
        print(f"Bandwidth reduction: {default_bandwidth - band_bandwidth}")

        self.add_sensitive_items()
        return self.band_matrix
