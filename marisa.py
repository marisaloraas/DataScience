# Author: Marisa Loraas
#2/3/2021
#CSE489 Data Science
#HW 1


def attributes(alien_list):
    for i in alien_list[1:]:
        x = i.split(',')
        flag = 0
        p = 0
        n = 0
        if float(x[1]) <= 3.5:
            x.append('small')
        else:
            x.append('large')
        for j in x[2]:
            if j == 'G':
                n += 1
                if flag == 0:
                    flag = 1
            elif j == 'C':
                n += 1
                if flag == 1:
                    p += 1
                flag = 0
            else:
                flag = 0
        x.remove(x[2])
        x.remove(x[1])
        x.append(p)
        x.append(n)
        x.append((2 * p) / n)
        #print(x)
        alien_list[alien_list.index(i)] = x
    alien_list.remove(alien_list[0])
    #print(alien_list)
    return alien_list


def table_print(alien_list):
    print("ID\t Small\t Large\t Number of Patterns  Number of C\G  Patter Frequency\n")
    for i in alien_list:
        print(i[0], "\t", end ="")
        for j in i[1:]:
            if j == 'small':
                print("  1\t   0\t\t", end = "")
            elif j == 'large':
                print("  0\t   1\t\t", end = "")
            else:
                print(round(j, 2), "\t\t", end = "")
        print("\n")


def sm_lg_table(alien_list):
    sm_count = 0
    sm_p = 0
    sm_n = 0
    lg_count = 0
    lg_p = 0
    lg_n = 0
    for i in alien_list:
        if i[1] == 'small':
            sm_count += 1
            sm_p += i[2]
            sm_n += i[3]
        else:
            lg_count += 1
            lg_p += i[2]
            lg_n += i[3]

    print("Forehead Size Category \t Count \t Total number of Patterns \t Total number of C/G \t Aggregate Pattern Frequency \n")
    print("S \t\t\t", sm_count, "\t", sm_p , "\t\t\t\t", sm_n, "\t\t\t", round((2 *sm_p / sm_n)*100, 2), "%\n")
    print("L \t\t\t", lg_count, "\t", lg_p , "\t\t\t\t", lg_n, "\t\t\t", round((2 *lg_p / lg_n)*100, 2), "%\n")

    f = open('marisa-result.csv', 'w')
    print("ForeheadCategory,Count,TotalNumPattern,TotalNumC/G,AggPatFreq", file = f)
    print("S," + str(sm_count) + "," + str(sm_p) + "," + str(sm_n) + "," + str(round((2 *sm_p / sm_n), 2)), file = f)
    print("L," + str(lg_count) + "," + str(lg_p) + "," + str(lg_n) + "," + str(round((2 *lg_p / lg_n), 2)), file = f)
    f.close()


def main():
    file = open('data-aliens.txt', 'r')
    aliens = file.readlines()
    #print(aliens)
    alien_attributes = attributes(aliens)
    #print(alien_attributes)
    table_print(alien_attributes)
    sm_lg_table(alien_attributes)
    file.close()

if __name__ == '__main__':
    main()
