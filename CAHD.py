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
    histogram_for_KL = None

    def __init__(self, alpha, p, band_matrix, sensitive_items):
        """
        Costruttore della classe CAHD
        :param alpha: parametro per la ricerca di QID simili
        :param p: grado di privacy
        :param band_matrix: dataframe di una matrice a bande
        :param sensitive_items: dataframe di sensitive item
        """
        self.alpha = alpha
        self.p = p
        self.band_matrix = band_matrix
        self.band_matrix.index = range(0, len(self.band_matrix.index))
        self.sensitive_items = sensitive_items
        self.sensitive_items.index = self.band_matrix.index

    def clean_sensitive_item(self):
        """
        Funzione per selezionare le sensitive transaction dal dataframe di sensitive item
        :return: dataframe contenente solo le sensitive transaction
        """
        new_df = self.sensitive_items[(self.sensitive_items != 0).any(1)]
        return new_df

    def create_histogram(self):
        """
        La funzione crea 2 dizionari, dei quali uno associa ai sensitive item quante occorrenze ci sono nella matrice 
        mentre l'altro associa alla riga contenente sensitive item una lista dei sensitive item contenuti. 
        """
        # Get ndArray of all column names
        sensitive_histogram = dict()
        sensitive_row = dict()

        # csi sta per clean sensitive item
        self.csi = self.clean_sensitive_item()
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

        self.sensitive_row = sensitive_row
        self.sensitive_histogram = sensitive_histogram
        self.histogram_for_KL = sensitive_histogram.copy()

    def qid_similarity(self, cl, t):
        """
        Data la candidate list, seleziona le righe che andranno a fare parte del gruppo
        in base alla similarità dei QID
        :param cl: candidate list
        :param t: riga sensitive su cui viene creato il gruppo
        :return: lista con i nomi delle righe che fanno parte del gruppo
        """
        row_len_dict = dict()
        count = 0

        for row in cl:
            row_len_dict[count] = len(t.compare(row))
            count += 1
        ordered_dict = sorted(row_len_dict.items(), key=lambda kv: (kv[1], kv[0]))
        result = list()
        result.append(t.name)

        for i in range(0, self.p - 1):
            result.append(cl[ordered_dict[i][0]].name)

        return result

    def check_if_already_in(self, index, list_sensitive_added):
        """
        Controlla che il sensitive item non sia già stato inserito in un gruppo
        :param index: sensitive transaction da inserire
        :param list_sensitive_added: lista dei sensitive item già aggiunti in gruppi
        :return: True se index è già in un gruppo
        """
        for sensitive_added in list_sensitive_added:
            if index == sensitive_added:
                return True

        return False

    def create_groups(self):
        """
        Funzione per la computazione dei gruppi
        :return: dizionario che associa riga sensitive al dataframe
        """
        # compute histogram
        self.create_histogram()
        cl = dict()
        list_rows = self.band_matrix.index.values
        remaining = len(list_rows)

        list_sensitive_added = list()
        group_dict = dict()

        value = 1
        old_value = 0

        while value > 0:
            for j in self.csi.index.values:

                if self.check_if_already_in(j, list_sensitive_added):
                    continue

                t = self.band_matrix.loc[j, :]

                cl[j] = list()

                index = numpy.where(list_rows == j)[0][0]

                pos_idx = index + 1
                neg_idx = index - 1
                counter = 0
                stop = 2 * self.alpha * self.p

                not_groupable = False

                while counter < stop:

                    if neg_idx >= 0:
                        counter += self.populate_cl(cl, j, list_rows[neg_idx])
                        neg_idx -= 1

                    if pos_idx < remaining:
                        counter += self.populate_cl(cl, j, list_rows[pos_idx])
                        pos_idx += 1

                    if pos_idx == remaining and neg_idx == -1:

                        if len(cl[j]) < self.p - 1:
                            not_groupable = True

                        break

                if not_groupable:
                    continue

                list_similar = self.qid_similarity(cl[j], t)

                for idx in list_similar:
                    if idx in self.sensitive_row:
                        list_sensitive_added.append(idx)
                        for si in self.sensitive_row[idx]:
                            self.sensitive_histogram[si] -= 1

                if self.privacy_requisite_chek(remaining):

                    for elem in list_similar:
                        list_rows = list_rows[list_rows != elem]

                    remaining = len(list_rows)
                    # inserisco il gruppo nella struttura a dict
                    group_dict[t.name] = list_similar
                    pass

                else:
                    for idx in list_similar:
                        # print(list_sensitive_added, idx)
                        if idx in self.sensitive_row:
                            list_sensitive_added.remove(idx)
                            for si in self.sensitive_row[idx]:
                                self.sensitive_histogram[si] += 1
                    continue

            value = 0

            for histogram_value in self.sensitive_histogram.items():
                value += histogram_value[1]

            if value > 0 and old_value == value:
                # l'istogramma non è cambiato quindi non posso migliorare nulla
                print(f"Grado di privacy {self.p} non soddisfacibile")
                return -1

            elif value > 0:
                old_value = value

        print("Grado di privacy soddisfacibile.")

        counter = 0

        result = dict()

        for group in group_dict:
            counter += 1
            final_anonymized = pandas.DataFrame()
            # print("GRUPPO", counter, "con Sensitive Item", self.sensitive_row[group])

            for row in group_dict[group]:
                new_row = self.band_matrix.iloc[lambda x: x.index == row]
                final_anonymized = final_anonymized.append(other=new_row)

            result[group] = final_anonymized
            # print(final_anonymized)

        final_anonymized = pandas.DataFrame()
        for non_sensitive_row_index in list_rows:
            new_row = self.band_matrix.iloc[lambda x: x.index == non_sensitive_row_index]
            final_anonymized = final_anonymized.append(other=new_row)

        # print("GRUPPO", (counter + 1), "non sensitive")
        # print(final_anonymized)
        result[-1] = final_anonymized

        return result

    def populate_cl(self, cl, main_idx, idx):
        """
        Funzione che decreta se aggiungere la riga idx alla candidate list.
        :param cl: candidate list
        :param main_idx: indice della riga sensitive che sto analizzando
        :param idx: candidata ad entrare nella candidate list
        :return: 1 se aggiunge, 0 se non aggiunge
        """
        if idx in self.sensitive_row:
            for main_si in self.sensitive_row[main_idx]:
                for other_si in self.sensitive_row[idx]:
                    if main_si == other_si:
                        return 0

        cl[main_idx].append(self.band_matrix.loc[idx, :])
        return 1

    def privacy_requisite_chek(self, remaining):
        """
        Funzione che il gruppo formato non porti ad un errore di anonimizzazione
        :param remaining: righe rimanenti nella list rows
        :return: True se va bene
        """
        for elem in self.sensitive_histogram.values():
            if elem * self.p > remaining:
                return False
        return True
