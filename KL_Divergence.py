import itertools
import random
from math import log10 as log

import pandas


class KL_Divergence:
    r = None
    band_matrix = None
    groups = None
    sensitive_rows = None
    sensitive_histogram = None

    def __init__(self, r, band_matrix, groups, sensitive_rows, sensitive_histogram):
        self.r = r
        self.band_matrix = band_matrix
        self.groups = groups
        self.sensitive_rows = sensitive_rows
        self.sensitive_histogram = sensitive_histogram

    def compute_Act(self, s, c, ):
        """
        :param s: è il sensitive item che sto analizzando
        :param c: c è la combinazione di 1 e 0 che sto analizzando
        :return: il risultato della divisione
        """
        # numero occorrenze di s in C
        # numero occorrenze di s nel dataset (copi histogram prima di modificarlo?)

        pass

    def compute_Est(self, s, c):
        pass

    #devo farla per ogni s, occhio che in un gruppo posso avere piu di una s
    def compute_kl_divergence(self):
        # devo estrarre a caso r QID, come label
        # devo ottenere tutte le combinazioni di 1 e 0 di r elementi => 2^r
        new_list = list(self.band_matrix.columns.values)[:]
        random.shuffle(new_list)
        selected_QID = new_list[-self.r:]
        lst = [list(i) for i in itertools.product([0, 1], repeat=self.r)]
        for combination in lst:
            #idea è di usare compare tra series
            print(pandas.Series(combination, index=selected_QID))
        '''
        result = 0
        s = 0
        for c in r_QID:
            act = self.compute_Act(c, s)
            est = self.compute_Est(c, s)
            if act != 0 and est != 0:
                result += act * log(act / est)
        pass
        '''
