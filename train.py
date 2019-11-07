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
    rmse = append_rmse_coordinates()
    y_esti = append_estimation_coordinates(scaled_km, thetas)
    fig.add_trace(go.Scatter(x=km, y=price, mode='markers', name='Raw',
                             marker=dict(size=10, color='blue')), row=2, col=1)
    fig.add_trace(go.Scatter(x=km, y=y_esti, mode='lines',
                             name='Estimation', line=dict(color='red')), row=2, col=1)
    fig.add_trace(go.Scatter(x=rmse[0], y=rmse[1], mode='lines',
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


def apply_gradient_descent(km, price):
    theta_a = 0
    theta_b = 0
    hypothesis = 0
    iterations = 10000
    learning_rate = 0.1
    for i in range(0, iterations):
        sum_rmse = 0
        sum_derivate_a = 0
        sum_derivate_b = 0
        for x in range(0, len(km)):
            hypothesis = theta_a + theta_b * km[x]
            sum_rmse += (hypothesis - price[x]) ** 2
            sum_derivate_a += hypothesis - price[x]
            sum_derivate_b += (hypothesis - price[x]) * km[x]
        theta_a -= learning_rate * sum_derivate_a / len(km)
        theta_b -= learning_rate * sum_derivate_b / len(km)
        g_accuracy.append((sum_rmse / len(km)) ** 0.5)
    return [theta_a, theta_b]


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
    try:
        with open('data.csv', 'rt') as csv_file:
            data = csv.reader(csv_file, delimiter=',')
            for row in data:
                km.append(row[0])
        km.pop(0)
        km = list(map(float, km))
    except:
        print("Error: something went wrong.")
        exit(1)
    return km


def get_csv_price():
    price = []
    try:
        with open('data.csv', 'rt') as csv_file:
            data = csv.reader(csv_file, delimiter=',')
            for row in data:
                price.append(row[1])
        price.pop(0)
        price = list(map(float, price))
    except:
        print("Error: something went wrong.")
        exit(1)
    return price


def main():
    price = get_csv_price()
    km = get_csv_km()
    scaled_km = apply_feature_scaling(km)
    thetas = apply_gradient_descent(scaled_km, price)
    update_theta_csv(thetas)
    display(km, scaled_km, price, thetas)
    return 0


if __name__ == "__main__":
    main()
