import os
import csv
from tqdm import tqdm


def listdir_nohidden(dir):
    return sorted([a for a in os.listdir(dir) if not a.startswith('.')])


def aggregate(path, headers):

    with open('output.csv', 'w', newline='') as fp:
        f = csv.writer(fp)
        #print(headers)
        f.writerow(headers)

        for feeder_folder in tqdm(listdir_nohidden(path)):
            line = []
            total_obs = 0
            zero_obs_l1 = 0
            zero_obs_l2 = 0
            zero_obs_l3 = 0

            for date_folder in listdir_nohidden(os.path.join(path, feeder_folder)):
                for csv_file in listdir_nohidden(os.path.join(path, feeder_folder, date_folder)):
                    total_obs += 1

                    with open(os.path.join(path, feeder_folder, date_folder, csv_file)) as file:

                        # only read second row of each file
                        row = list(csv.reader(file, delimiter=','))[1]

                        if int(row[1]) == 0:
                            zero_obs_l1 += 1

                        if int(row[2]) == 0:
                            zero_obs_l2 += 1

                        if int(row[3]) == 0:
                            zero_obs_l3 += 1

                        file.close()

            line.append(feeder_folder)
            line.append(total_obs)
            line.append(zero_obs_l1)
            line.append(zero_obs_l2)
            line.append(zero_obs_l3)
            #print(line)
            f.writerow(line)

        fp.close()

if __name__ == "__main__":
    path = 'lv_cable'
    headers = ['LV_Feeder', 'Total_Observations', 'Zero_Obs_L1', 'Zero_Obs_L2', 'Zero_Obs_L3']
    aggregate(path, headers)
