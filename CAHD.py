import numpy


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
        # print(band_matrix)
        self.sensitive_items = sensitive_items
        self.sensitive_items.index = self.band_matrix.index

    def clean_sensitive_item(self):
        a_series = (self.sensitive_items != 0).any(axis=1)
        print(a_series)
        new_df = self.sensitive_items.loc[a_series]
        # print(new_df)
        return new_df

    ###
    # istogramma -> dentro ci vanno tutte le occorrenze per sensitive item
    # https: // pandas.pydata.org / pandas - docs / stable / reference / api / pandas.DataFrame.hist.html
    # per farlo con i dataframe da pandas
    # pero non riesco ad accedere all'istogramma.
    # meglio contare le occorrenze tipo -\|-.-|/-
    ###
    def create_histogram(self):
        # hist = self.clean_sensitive_item().hist(bins=2)
        # Get ndArray of all column names
        sensitive_histogram = dict()  # SI -> quanti sono
        sensitive_row = dict()  # riga -> quali SI per riga
        # csl sta per clean sensitive list
        self.csi = self.clean_sensitive_item()
        non_zero_index = self.csi.to_numpy().nonzero()
        nzi_row = non_zero_index[0]
        nzi_col = non_zero_index[1]
        for i in range(0, len(nzi_row)):
            # print("riga", baba_row[i], "colonna", baba_col[i], "ovvero", bibi.columns.values[baba_col[i]])
            active_sensitive_column = self.csi.columns.values[nzi_col[i]]
            active_sensitive_row = self.csi.index.values[nzi_row[i]]
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

    def qid_similarity(self, cl, t):
        abc = dict()
        count = 0
        for i in cl:
            abc[count] = len(t.compare(i))
            count += 1
        xyz = sorted(abc.items(), key=lambda kv: (kv[1], kv[0]))
        result = list()
        result.append(t)
        for i in range(0, self.p - 1):
            result.append(cl[xyz[i][0]])
        return result

    def create_groups(self):
        # compute histogram
        self.create_histogram()
        cl = dict()
        list_rows = self.band_matrix.index.values
        remaining = len(list_rows)
        # print(list_rows)
        for j in self.csi.index.values:
            # mi da una series che ci sta
            # riga sensitive
            t = self.band_matrix.loc[j, :]
            temp_histogram = self.sensitive_histogram.copy()
            for si in self.sensitive_row[j]:
                temp_histogram[si] -= 1
            cl[j] = list()
            pos_idx = j + 1
            neg_idx = j - 1
            counter = 0
            stop = self.alpha * self.p
            while counter < 2 * stop:
                if neg_idx > 0:
                    counter += self.populate_cl(cl, j, neg_idx, temp_histogram)
                    neg_idx -= 1
                if pos_idx < remaining:
                    counter += self.populate_cl(cl, j, pos_idx, temp_histogram)
                    pos_idx += 1
            list_similar = self.qid_similarity(cl[j], t)
            # print(list_similar[0], "is named ", list_similar[0].name) <- ottengo nome della riga inserita :)
            # print(len(list_similar))
            if self.privacy_requisite_chek(remaining, temp_histogram):
                #   allora tolgo le righe dal dataframe tipo
                #   aggiorno i remaining
                #   inserisco il gruppo nella mia struttura a dict
                self.sensitive_histogram = temp_histogram
                pass
            else:
                # se esiste vado avanti -> (continue?) o nulla...
                continue
            break
        # esco dal loop e quello che rimane lo metto nella struttura a senza SI :)
        # rimuovere dalla band matrix in qualche modo o trovare un modo per non guardare più quelle righe
        # poi va beh salvi ultimo e fine

    def populate_cl(self, cl, main_idx, idx, sensitive_histogram):
        if idx in self.sensitive_row:
            for main_si in self.sensitive_row[main_idx]:
                for other_si in self.sensitive_row[idx]:
                    if main_si == other_si:
                        return 0
            # aggiorno histogram
            for si in self.sensitive_row[idx]:
                sensitive_histogram[si] -= 1
        cl[main_idx].append(self.band_matrix.loc[idx, :])
        return 1

    def privacy_requisite_chek(self, remaining, sensitive_histogram):
        for elem in sensitive_histogram.values():
            # print(elem, "*", self.p, ">?", remaining)
            if elem * self.p > remaining:
                return False
        return True
