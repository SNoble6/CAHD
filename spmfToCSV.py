import csv
import numpy as np

if __name__ == "__main__":
    delimiter = 10000
    delimiter += 1
    items = list()
    item_set = set()
    # definisco i nomi dei file
    dataset = 'BMS2'
    main_csv = 'Dataset/' + dataset + '.csv'
    transaction_csv = 'Dataset/' + dataset + '_transaction_matrix.csv'
    list_item_txt = 'Dataset/' + dataset + '_list_item.txt'

    with open(main_csv) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            for col in row:
                item_set.add(col)
                # if col not in items:
                # items.append(col)
                # item_set.add(col)
            line_count += 1
            ###
            # prova con delimiter item
            if line_count == delimiter:
                break
            ###
        csv_file.close()

    for elem in item_set:
        items.append(elem)

    num_items = len(items)
    print(num_items, "items")

    transaction_matrix = np.zeros((line_count, num_items))

    with open(main_csv) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            for col in row:
                transaction_matrix[line_count][items.index(col)] = 1
            line_count += 1
            ###
            # prova con delimiter item
            if line_count == delimiter:
                break
            ###
        csv_file.close()

    with open(transaction_csv, 'w') as f:
        for row in range(0, line_count - 1):
            for col in range(0, num_items - 1):
                f.write("%s," % int(transaction_matrix[row][col]))
            f.write("%s\n" % int(transaction_matrix[row][num_items - 1]))
        for col in range(0, num_items - 1):
            f.write("%s," % int(transaction_matrix[line_count - 1][col]))
        f.write("%s" % int(transaction_matrix[line_count - 1][num_items - 1]))
        # f.write("SECONDA RIGA\n")
        f.close()

    with open(list_item_txt, 'w') as f:
        for i in range(0, num_items - 1):
            f.write("%s\n" % items[i])
        f.write("%s" % items[num_items - 1])
        '''for item in items:
            f.write("%s\n" % item)'''
        f.close()
