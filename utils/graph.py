import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import utils.data_db as data_db


def setup(path):
    data_db.setup(path)


def get_confirmed(country):
    data = data_db.get_daily_info(country)
    y_confirmed = []
    for timestamp in data.values():
        info = data_db.get_db_info(country, timestamp)
        y_confirmed.append(info[1])
    return y_confirmed


def get_deaths(country):
    data = data_db.get_daily_info(country)
    y_deaths = []
    for timestamp in data.values():
        info = data_db.get_db_info(country, timestamp)
        y_deaths.append(info[2])
    return y_deaths


def get_reco(country):
    data = data_db.get_daily_info(country)
    y_reco = []
    for timestamp in data.values():
        info = data_db.get_db_info(country, timestamp)
        y_reco.append(info[3])
    return y_reco


def get_x(country):
    data = data_db.get_daily_info(country)
    x = []
    for key in data.keys():
        year, month, day = key.split(sep="-")
        x.append("-".join([month, day]))
    return x


def get_graph(country):
    instance = plt
    instance.bar(get_x(country), get_confirmed(country), label="Confiremd cases")
    if get_reco(country) > get_deaths(country):
        instance.bar(get_x(country), get_reco(country), color="green", label="Recovered")
        instance.bar(get_x(country), get_deaths(country), color="red", label="Deaths")
    else:
        instance.bar(get_x(country), get_deaths(country), color="red", label="Deaths")
        instance.bar(get_x(country), get_reco(country), color="green", label="Recovered")

    instance.xlabel("Date")
    instance.ylabel("People")
    instance.title(f"{country.capitalize()} stats (2020)")
    instance.legend()
    return instance


def draw_graph(country):
    graph = get_graph(country)
    graph.show()
    graph.close()


def save_graph(country, path="graph.png"):
    graph = get_graph(country)
    graph.savefig(path)
    graph.close()


if __name__ == '__main__':
    save_graph("china", "china.png")
    # save_graph("us", "us.png")
    # draw_graph("us")
    # draw_graph("italy")
