import numpy


class CAHD:
    alpha = None
    p = None
    band_matrix = None
    sensitive_items = None
    sensitive_histogram = None
    sensitive_row = None
    def __init__(self, alpha, p, band_matrix, sensitive_items):
        self.alpha = alpha
        self.p = p
        self.band_matrix = band_matrix
        self.sensitive_items = sensitive_items

    def clean_sensitive_item(self):
        a_series = (self.sensitive_items != 0).any(axis=1)
        print(a_series)
        new_df = self.sensitive_items.loc[a_series]
        #print(new_df)
        return new_df

    ###
    # istogramma -> dentro ci vanno tutte le occorrenze per sensitive item
    # https: // pandas.pydata.org / pandas - docs / stable / reference / api / pandas.DataFrame.hist.html
    # per farlo con i dataframe da pandas
    # pero non riesco ad accedere all'istogramma.
    # meglio contare le occorrenze tipo -\|-.-|/-
    ###
    def create_histogram(self):
        #hist = self.clean_sensitive_item().hist(bins=2)
        # Get ndArray of all column names
        sensitive_histogram = dict()  # SI -> quanti sono
        sensitive_row = dict()  # riga -> quali SI per riga
        # csl sta per clean sensitive list
        csi = self.clean_sensitive_item()
        non_zero_index = csi.to_numpy().nonzero()
        nzi_row = non_zero_index[0]
        nzi_col = non_zero_index[1]
        for i in range(0, len(nzi_row)):
            # print("riga", baba_row[i], "colonna", baba_col[i], "ovvero", bibi.columns.values[baba_col[i]])
            active_sensitive_column = csi.columns.values[nzi_col[i]]
            active_sensitive_row = csi.index.values[nzi_row[i]]
            if active_sensitive_column not in sensitive_histogram:
                sensitive_histogram[active_sensitive_column] = 0
            sensitive_histogram[active_sensitive_column] += 1
            if active_sensitive_row not in sensitive_row:
                sensitive_row[active_sensitive_row] = list()
            sensitive_row[active_sensitive_row].append(active_sensitive_column)
        print(sensitive_row)
        print(sensitive_histogram)
        self.sensitive_row = sensitive_row
        self.sensitive_histogram = sensitive_histogram

    def qid_similiarity(self, cl, t, stop):
        abc = dict()
        count = 0
        for i in cl:
            abc[count] = len(t.compare(i))
            count += 1
        # print(abc)
        xyz = sorted(abc.items(), key=lambda kv: (kv[1], kv[0]))
        # print(xyz)
        result = list()
        for i in range(0, stop):
            result.append(cl[xyz[i][0]])
        return result

    #    d = {​​​​'col1': [0, 1, 0, 1], 'col2': [1, 0, 0, 0], 'col3': [0, 1, 0, 0], 'col4': [0, 0, 1, 0]}​​​​
    #    df = pandas.DataFrame(data=d)
    #    print(df)
    #    print(df.iloc[0])
    #    for i in range(1, 4):
    #       print(df.iloc[0].compare(df.iloc[i]))
    # questa sotto dice il numero di differenze :)
    #        print(len(df.iloc[0].compare(df.iloc[i])))
    def create_groups(self):
        # compute histogram
        self.create_histogram()
        cl = dict()
        list_rows = self.band_matrix.index.values
        remaining = len(list_rows)
        # print(list_rows)
        for j in self.sensitive_items.index.values:
            # mi da una series che ci sta
            # riga sensitive
            t = self.band_matrix.loc[j, :]
            cl[j] = list()

            idx = numpy.where(list_rows == int(j))[0]
            counter = 0
            counter_neg = 0
            counter_pos = 0
            stop = self.alpha * self.p
            while counter < 2 * stop:
                pos_idx = idx + counter_pos + 1
                neg_idx = idx - counter_neg - 1
                neg_row = list_rows[neg_idx][0]
                pos_row = list_rows[pos_idx][0]
                if neg_idx > 0:
                    if neg_row in self.sensitive_row:
                        #non devi guardare j, ma il sensitive item in questione...
                        if j in self.sensitive_row[neg_row]:
                            continue
                        for v in self.sensitive_row[neg_row]:
                            self.sensitive_histogram[v] -= 1
                    cl[j].append(self.band_matrix.loc[neg_row, :])
                    counter_neg += 1
                if pos_idx < remaining:
                    if pos_row in self.sensitive_row:
                        if j in self.sensitive_row[pos_row]:
                            continue
                        for v in self.sensitive_row[neg_row]:
                            self.sensitive_histogram[v] -= 1
                    cl[j].append(self.band_matrix.loc[pos_row, :])
                    counter_pos += 1
                counter = counter_pos + counter_neg
            #print(cl)
            list_similiar = self.qid_similiarity(cl[j], t, stop)
            break