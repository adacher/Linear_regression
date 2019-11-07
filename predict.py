import re
import sys
import csv


def get_csv_km():
    km = []
    try:
        with open('data.csv', 'rt') as csv_content:
            data = csv.reader(csv_content, delimiter=',')
            for row in data:
                km.append(row[0])
        km.pop(0)
        km = list(map(float, km))
    except:
        print("Error: something went wrong.")
        exit(1)
    return km


def find_price_estimation(theta, km):
    csv_km = get_csv_km()
    min_km = min(csv_km)
    max_km = max(csv_km)
    scaled_km = (km - min_km) / (max_km - min_km)
    price = theta[0] + (theta[1] * scaled_km)
    if price < 0:
        print("Not enough data to provide a good estimation.")
    else:
        print("The estimated price for " + str(km) +
              " miles is " + str(price) + " euros.")


def check_user_input(user_input):
    check_input = re.match(r'^[-+]?[0-9]+$', user_input)
    if check_input:
        if int(user_input) < 0:
            print("Error: km can't be lower than 0.")
            exit(1)
    else:
        print("Error: km must be a number.")
        exit(1)


def get_user_input():
    user_input = input("Enter a mileage:\n")
    check_user_input(user_input)
    km = int(user_input)
    return km


def get_theta_file_values():
    tmp = []
    theta = [0, 0]
    with open('theta.csv', 'rt') as csv_content:
        data = csv.reader(csv_content, delimiter=',')
        for row in data:
            tmp.append(row[0])
            tmp.append(row[1])
    theta[0] = float(tmp[2])
    theta[1] = float(tmp[3])
    tmp.clear()
    return theta


def create_theta_csv():
    with open('theta.csv', 'w') as csv_file:
        filewriter = csv.writer(csv_file, delimiter=',',
                                quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(['theta0', 'theta1'])
        filewriter.writerow(['0', '0'])


def check_theta_file_exists():
    try:
        with open('theta.csv', 'r') as f:
            return 0
    except FileNotFoundError:
        return 1


def check_args():
    nb_args = len(sys.argv)
    if nb_args != 1:
        print("Error: no arguments needed.")
        exit(1)


def main():
    check_args()
    if check_theta_file_exists() == 1:
        create_theta_csv()
    theta = get_theta_file_values()
    km = get_user_input()
    find_price_estimation(theta, km)
    exit(0)


if __name__ == "__main__":
    main()
