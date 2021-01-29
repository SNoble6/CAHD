import itertools
import operator
import random
from math import log10 as log

import pandas


class KL_Divergence:
    p = None
    r = None
    band_matrix = None
    groups = None
    sensitive_rows = None
    sensitive_histogram = None

    def __init__(self, p, r, band_matrix, groups, sensitive_rows, sensitive_histogram):
        self.p = p
        self.r = r
        self.band_matrix = band_matrix
        self.groups = groups
        self.sensitive_rows = sensitive_rows
        self.sensitive_rows[-1] = []
        self.sensitive_histogram = sensitive_histogram

    def compute_Act(self, selected_QID, my_row, si):
        """
        :param s: è il sensitive item che sto analizzando
        :param c: c è la combinazione di 1 e 0 che sto analizzando
        :return: il risultato della divisione
        """
        # numero occorrenze di s nel dataset
        # print("occorrenze di si in T", self.sensitive_histogram[si])
        denominator = self.sensitive_histogram[si]
        # numero occorrenze di s in C
        # dobbiamo fare for su sensitive rows
        # print(self.sensitive_rows)
        # my_row = pandas.Series(combination, index=selected_QID)

        occurrences = 0

        for row, items in self.sensitive_rows.items():
            if si in items:
                # print(si, "è in", row)
                matching_row = self.band_matrix.loc[row, selected_QID]
                if len(my_row.compare(matching_row)) == 0:
                    occurrences += 1
                # poi vedere quali tra queste righe rispettano il pattern

        result = float(occurrences) / float(denominator)
        # print(result)
        return result

    def compute_Est(self, selected_QID, my_row, si):

        # numero occorrenze di s nel dataset
        # print("occorrenze di si in T", self.sensitive_histogram[si])
        denominator = float(self.sensitive_histogram[si])

        # my_row = pandas.Series(combination, index=selected_QID)

        a = 1
        dim_G = self.p
        b = 0

        for row, group_df in self.groups.items():

            if si not in self.sensitive_rows[row]:
                continue

            temp_df = group_df.loc[:, selected_QID]
            for group_row in temp_df.iterrows():
                # print(group_row[1])
                # print(len(my_row.compare(group_row[1])))
                if len(my_row.compare(group_row[1])) == 0:
                    b += 1

        numerator = float(a * b) / float(dim_G)

        return numerator / denominator

    # devo farla per ogni s, occhio che in un gruppo posso avere piu di una s
    def compute_kl_divergence(self):
        # devo estrarre a caso r QID, come label
        # devo ottenere tutte le combinazioni di 1 e 0 di r elementi => 2^r
        # print(self.sensitive_histogram)
        # fai la prova con histogram con tutti value uguali
        si = max(self.sensitive_histogram.items(), key=operator.itemgetter(1))[0]
        # print("SI", si)
        new_list = list(self.band_matrix.columns.values)[:]
        random.shuffle(new_list)
        selected_QID = new_list[-self.r:]
        # print(selected_QID)
        lst = [list(i) for i in itertools.product([0, 1], repeat=self.r)]

        final_result = 0.0

        for combination in lst:
            # idea è di usare compare tra series
            my_row = pandas.Series(combination, index=selected_QID)
            act = self.compute_Act(selected_QID, my_row, si)
            est = self.compute_Est(selected_QID, my_row, si)

            if est != 0 and act != 0:
                final_result += act * log(act / est)
            final_result += 0.0
        # TODO: REMOVE COMMENT
        # print(final_result)
        return final_result
