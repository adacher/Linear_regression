import csv
import plotly.graph_objects as go
from plotly.subplots import make_subplots

g_accuracy = []


def append_estimation_coordinates(scaled_km, thetas):
    estimated_price = []
    for i in range(0, len(scaled_km)):
        estimated_price.append(thetas[0] + (thetas[1] * scaled_km[i]))
    return estimated_price


def append_rmse_coordinates():
    x = []
    y = []
    for i in range(0, len(g_accuracy)):
        x.append(i)
        y.append(g_accuracy[i])
    return [x, y]


def price_estimation(fig, km, scaled_km, price, thetas):
    y_rmse = append_rmse_coordinates()
    y_esti = append_estimation_coordinates(scaled_km, thetas)
    fig.add_trace(go.Scatter(x=km, y=price, mode='markers', name='Raw',
                             marker=dict(size=10, color='blue')), row=2, col=1)
    fig.add_trace(go.Scatter(x=km, y=y_esti, mode='lines',
                             name='Estimation', line=dict(color='red')), row=2, col=1)
    fig.add_trace(go.Scatter(x=y_rmse[0], y=y_rmse[1], mode='lines',
                             name='Accuracy', line=dict(color='limegreen')), row=2, col=2)
    fig.update_xaxes(title_text="Km", row=2, col=1)
    fig.update_yaxes(title_text="Euros", row=2, col=1)
    fig.update_xaxes(title_text="Iterations", row=2, col=2)
    fig.update_yaxes(title_text="Rmse", row=2, col=2)


def scaling_difference(fig, km, scaled_km, price):
    fig.add_trace(go.Bar(x=price, y=km, name='Non scaled',
                         width=60), row=1, col=1)
    fig.add_trace(go.Bar(x=price, y=scaled_km, name='Scaled',
                         width=60), row=1, col=2)
    fig.update_xaxes(title_text="Euros", row=1, col=1)
    fig.update_yaxes(title_text="Km", row=1, col=1)
    fig.update_xaxes(title_text="Euros", row=1, col=2)
    fig.update_yaxes(title_text="Scaled km", row=1, col=2)
    fig.update_traces(marker_color='blue',
                      marker_line_width=1.5, opacity=0.8, row=1, col=1)
    fig.update_traces(marker_color='red',
                      marker_line_width=1.5, opacity=0.8, row=1, col=2)


def display(km, scaled_km, price, thetas):
    fig = make_subplots(rows=2, cols=2, subplot_titles=(
        'Feature Scaling(1)', 'Feature scaling(2)', 'Price estimation', 'Accuracy'))
    scaling_difference(fig, km, scaled_km, price)
    price_estimation(fig, km, scaled_km, price, thetas)
    fig.update_layout(template="seaborn",
                      title_text="Linear Regression", title_font_size=30)
    fig.show()


def update_theta_csv(thetas):
    with open('theta.csv', 'w') as csv_file:
        filewriter = csv.writer(csv_file, delimiter=',')
        filewriter.writerow(['theta0', 'theta1'])
        filewriter.writerow([thetas[0], thetas[1]])


def find_rmse(price, estimation):
    diff_squared = 0
    for i in range(len(price)):
        diff = estimation[i] - price[i]
        diff_squared += (diff ** 2)
    mean_of_diff = diff_squared / float(len(price))
    return mean_of_diff ** 0.5


def find_accuracy(theta_a, theta_b, km, price):
    estimation = []
    for i in range(0, len(km)):
        estimation.append(theta_a + (theta_b * km[i]))
    rmse = find_rmse(price, estimation)
    return rmse


def find_derivates(theta_a, theta_b, km, price):
    derivate_a = 0
    derivate_b = 0
    estimation = 0
    learning_rate = 0.1
    nb_items = len(km)
    derivates = [0, 0]
    for i in range(0, nb_items):
        estimation = (theta_a + theta_b * km[i]) - price[i]
        derivate_a += estimation
        derivate_b += estimation * km[i]
    derivates[0] = derivate_a / nb_items * learning_rate
    derivates[1] = derivate_b / nb_items * learning_rate
    return derivates


def apply_gradient_descent(km, price, boo):
    theta_a = 0
    theta_b = 0
    thetas = [0, 0]
    iterations = 6500
    for i in range(0, iterations):
        thetas = find_derivates(theta_a, theta_b, km, price)
        theta_a -= thetas[0]
        theta_b -= thetas[1]
        g_accuracy.append(find_accuracy(theta_a, theta_b, km, price))
    thetas[0] = theta_a
    thetas[1] = theta_b
    return thetas


def apply_feature_scaling(km):
    min_km = min(km)
    max_km = max(km)
    scaled_km = []
    for i in range(0, len(km)):
        scaled_value = float((km[i] - min_km) / (max_km - min_km))
        scaled_km.append(scaled_value)
    return scaled_km


def get_csv_km():
    km = []
    with open('data.csv', 'rt') as csv_file:
        data = csv.reader(csv_file, delimiter=',')
        for row in data:
            km.append(row[0])
    km.pop(0)
    km = list(map(float, km))
    return km


def get_csv_price():
    price = []
    with open('data.csv', 'rt') as csv_file:
        data = csv.reader(csv_file, delimiter=',')
        for row in data:
            price.append(row[1])
    price.pop(0)
    price = list(map(float, price))
    return price


def main():
    price = get_csv_price()
    km = get_csv_km()
    scaled_km = apply_feature_scaling(km)
    thetas = apply_gradient_descent(scaled_km, price, 1)
    update_theta_csv(thetas)
    display(km, scaled_km, price, thetas)
    exit(0)


if __name__ == "__main__":
    main()
