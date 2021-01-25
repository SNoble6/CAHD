import numpy
import pandas


class CAHD:
    alpha = None
    p = None
    band_matrix = None
    sensitive_items = None
    sensitive_histogram = None
    sensitive_row = None
    csi = None

    def __init__(self, alpha, p, band_matrix, sensitive_items):
        self.alpha = alpha
        self.p = p
        self.band_matrix = band_matrix
        self.band_matrix.index = range(0, len(self.band_matrix.index))
        self.sensitive_items = sensitive_items
        self.sensitive_items.index = self.band_matrix.index

    def clean_sensitive_item(self):
        new_df = self.sensitive_items[(self.sensitive_items != 0).any(1)]
        #print("OéPIKACHU\r\n", new_df)
        return new_df

    ###
    # istogramma -> dentro ci vanno tutte le occorrenze per sensitive item
    # https: // pandas.pydata.org / pandas - docs / stable / reference / api / pandas.DataFrame.hist.html
    # per farlo con i dataframe da pandas
    # pero non riesco ad accedere all'istogramma.
    # meglio contare le occorrenze tipo -\|-.-|/-
    ###
    def create_histogram(self):
        # Get ndArray of all column names
        sensitive_histogram = dict()  # SI -> quanti sono
        sensitive_row = dict()  # riga -> quali SI per riga
        # csl sta per clean sensitive list
        self.csi = self.clean_sensitive_item()
        print(self.csi)
        nzi_row, nzi_col = self.csi.to_numpy().nonzero()
        for value in self.clean_sensitive_item().columns.values:
            sensitive_histogram[value] = 0
        for i in range(0, len(nzi_row)):
            active_sensitive_column = self.csi.columns.values[nzi_col[i]]
            active_sensitive_row = self.csi.index.values[nzi_row[i]]
            sensitive_histogram[active_sensitive_column] += 1
            if active_sensitive_row not in sensitive_row:
                sensitive_row[active_sensitive_row] = list()
            sensitive_row[active_sensitive_row].append(active_sensitive_column)
        print(sensitive_row)
        print(sensitive_histogram)
        self.sensitive_row = sensitive_row
        self.sensitive_histogram = sensitive_histogram

    def qid_similarity(self, cl, t):
        abc = dict()
        count = 0
        for i in cl:
            abc[count] = len(t.compare(i))
            count += 1
        xyz = sorted(abc.items(), key=lambda kv: (kv[1], kv[0]))
        result = list()
        result.append(t.name)
        for i in range(0, self.p - 1):
            result.append(cl[xyz[i][0]].name)
        return result

    def check_if_already_in(self, index, list_sensitive_added):
        for sensitive_added in list_sensitive_added:
            if index == sensitive_added:
                return True
        else:
            return False

    def create_groups(self):
        # compute histogram
        self.create_histogram()
        cl = dict()
        list_rows = self.band_matrix.index.values
        remaining = len(list_rows)

        list_sensitive_added = list()
        group_dict = dict()
        for j in self.csi.index.values:
            list_sensitive_added_temp = list_sensitive_added.copy()
            if self.check_if_already_in(j, list_sensitive_added):
                continue
            t = self.band_matrix.loc[j, :]
            temp_histogram = self.sensitive_histogram.copy()
            for si in self.sensitive_row[j]:
                temp_histogram[si] -= 1
            cl[j] = list()

            index = numpy.where(list_rows == j)[0][0]

            pos_idx = index + 1
            neg_idx = index - 1
            counter = 0
            stop = self.alpha * self.p
            while counter < 2 * stop:
                if neg_idx > 0:
                    counter += self.populate_cl(cl, j, list_rows[neg_idx], temp_histogram, list_sensitive_added_temp)
                    neg_idx -= 1
                if pos_idx < remaining:
                    counter += self.populate_cl(cl, j, list_rows[pos_idx], temp_histogram, list_sensitive_added_temp)
                    pos_idx += 1
            list_similar = self.qid_similarity(cl[j], t)
            if self.privacy_requisite_chek(remaining, temp_histogram):
                for elem in list_similar:
                    list_rows = list_rows[list_rows != elem]
                remaining = len(list_rows)
                # inserisco il gruppo nella mia struttura a dict
                group_dict[t.name] = list_similar
                list_sensitive_added = list_sensitive_added_temp
                self.sensitive_histogram = temp_histogram
                pass
            else:
                continue

        # final_anonymized = pandas.DataFrame()
        # n_rows = len(self.band_matrix.index.values)

        counter = 0
        for group in group_dict:
            counter += 1
            final_anonymized = pandas.DataFrame()
            print("GRUPPO con Sensitive Item", self.sensitive_row[group], "numero", counter)
            for row in group_dict[group]:
                new_row = self.band_matrix.iloc[lambda x: x.index == row]
                """
                counter = n_rows
                for si in self.sensitive_histogram:
                    if si in self.sensitive_row[group]:
                        new_row.insert(counter, si, 1, True)
                        counter += 1
                    else:
                        new_row.insert(counter, si, 0, True)
                        counter += 1
                """
                final_anonymized = final_anonymized.append(other=new_row)
            print(final_anonymized)
        #final_anonymized.to_csv("zia_Marta.csv")

        final_anonymized = pandas.DataFrame()
        for non_sensitive_row_index in list_rows:
            new_row = self.band_matrix.iloc[lambda x: x.index == non_sensitive_row_index]
            final_anonymized = final_anonymized.append(other=new_row)
            '''
            counter = n_rows
            for si in self.sensitive_histogram:
                new_row.insert(counter, si, 0, True)
                counter += 1
            '''
        print("GRUPPO non sensitive")
        print(final_anonymized)
        #final_anonymized.to_csv("zia_Marta.csv")

    def populate_cl(self, cl, main_idx, idx, sensitive_histogram, list_sensitive_added_temp):
        if idx in self.sensitive_row:
            for main_si in self.sensitive_row[main_idx]:
                for other_si in self.sensitive_row[idx]:
                    if main_si == other_si:
                        return 0
            # aggiorno histogram
            list_sensitive_added_temp.append(idx)
            for si in self.sensitive_row[idx]:
                sensitive_histogram[si] -= 1
        cl[main_idx].append(self.band_matrix.loc[idx, :])
        return 1

    def privacy_requisite_chek(self, remaining, sensitive_histogram):
        for elem in sensitive_histogram.values():
            if elem * self.p > remaining:
                return False
        return True
