# @Author Marisa Loraas
# CSE 489 Data Science
# Home Work #4
# 3/3/2021

import numpy as np


def standard_deviation(mpg, hp):
    mgp_std = np.std(mpg)
    hp_std = np.std(hp)
    cov = np.cov(mpg, hp)
    return cov / (hp_std * mgp_std)
    # This does not return the same values previously in mpg vs HP,

# prints out name of column, covariance matrix, and the correlation value
def print_values(column, mpg):
    print("Covariance Matrix w/ MPG:\n", np.cov(column, mpg))
    print("Correlation Value:\n", mpg_cyl_cov(mpg, column))


# returns matrix from equation
def mpg_cyl_cov(mpg, cyl):
    cov_xy = np.cov(mpg, cyl)
    cov_xx = np.cov(mpg, mpg)
    cov_xx = np.sqrt(cov_xx)
    cov_yy = np.cov(mpg, mpg)
    cov_yy = np.sqrt(cov_yy)
    return np.array(cov_xy / (cov_xx * cov_yy))


# removes duplicate
def remove_duplicates(array):
    new_array, indexes = np.unique(array, axis=0, return_index=True)
    removed_cars = []
    for item in range(len(array)):
        if item not in indexes:
            removed_cars.append(array[item])
    print("Duplicate Items Removed:")
    print(removed_cars)
    return new_array


# removes items where the HP entry is nan
def missing_hp(array):
    new_array = [item for item in array if not np.isnan(item['HP'])]
    removed_nans = [item for item in array if np.isnan(item['HP'])]
    print("Records Deleted because of HP = nan:")
    print(np.array(removed_nans))
    return np.array(new_array)


def main():
    try:
        csv = np.genfromtxt('auto-mpg.csv', delimiter=',', encoding=None, dtype=None,
                            names=('MPG', 'Cyl', 'Displacement', 'HP', 'Wt', 'Accel', 'ModelYr', 'Origin', 'Name'))
    except FileNotFoundError:
        print("Error: File was not found")
    else:
        # print(csv)
        no_hp = missing_hp(csv)
        # print(no_hp)
        new_array = remove_duplicates(no_hp)
        # print(new_array)
        mpg_cyl = mpg_cyl_cov(new_array['MPG'], new_array['Cyl'])
        print("Correlation Matrix of MPG against Cyl:")
        print(mpg_cyl)
        print('HP')
        print_values(new_array['HP'], new_array['MPG'])
        print("Cyl")
        print_values(new_array['Cyl'], new_array['MPG'])
        print("Wt")
        print_values(new_array['Wt'], new_array['MPG'])
        print('Accel')
        print_values(new_array['Accel'], new_array['MPG'])
        print('ModelYr')
        print_values(new_array['ModelYr'], new_array['MPG'])
        print('Origin')
        print_values(new_array['Origin'], new_array['MPG'])
        mpg_hp = standard_deviation(new_array['MPG'], new_array['HP'])
        print("MPG vs HP Correlation Matrix:")
        print(mpg_hp)


if __name__ == '__main__':
    main()