from random import randint as rnd

from flask import Flask, render_template
from werkzeug.exceptions import abort

from data import title, subtitle, description, departures, tours

app = Flask(__name__)

###############################################################################
#                              static templates                               #
###############################################################################


@app.route('/')
def main_page():

    rand_tours = {}
    while len(rand_tours) != 6:
        index = rnd(1, len(tours))
        if index not in rand_tours:
            rand_tours[index] = tours[index]

    context = {
        'title': title,
        'subtitle': subtitle,
        'description': description,
        'departures': departures,
        'tours': rand_tours
    }

    return render_template('index.html', **context)


@app.route('/departures/<departure>/')
def departures_list(departure):

    departure_tours = {key: value for key, value in tours.items() if value['departure'] == departure}
    list_tour = departure_tours.values()
    price_min = min(list_tour, key=lambda x: x['price'])
    price_max = max(list_tour, key=lambda x: x['price'])
    nights_min = min(list_tour, key=lambda x: x['nights'])
    nights_max = max(list_tour, key=lambda x: x['nights'])

    context = {
        'title': title,
        'page_title': title,
        'departures': departures,
        'departure': departures[departure],
        'tours': departure_tours,
        'price_min': price_min['price'],
        'price_max': price_max['price'],
        'nights_min': nights_min['nights'],
        'nights_max': nights_max['nights'],
    }

    return render_template('departure.html', **context)


@app.route('/tours/<int:tour_id>/')
def tours_element(tour_id):

    if tour_id not in tours:
        abort(404)

    tour = tours[tour_id]
    stars = '★' * int(tour.get('stars'))

    context = {
        'page_title': tour.get('title'),
        'title': title,
        'departures': departures,
        'tour_departure': departures.get(tour.get('departure')),
        'tour': tour,
        'stars': stars,
    }

    return render_template('tour.html', **context)


@app.errorhandler(404)
def page_not_found(error):

    return '<h1>404 error</h1><p>There is no such page.<p>', 404


###############################################################################
#                               jinja templates                               #
###############################################################################


@app.route('/data')
def data():

    return render_template('data.html', tours=tours)


@app.route('/data/departures/<departure>')
def data_departures(departure):

    if departure not in departures:
        return 'Такого направления не существует.'

    departure_title = departures[departure]
    departure_tours = {key: value for key, value in tours.items() if value['departure'] == departure}

    return render_template('data-departure.html', departure=departure_title, tours=departure_tours)


@app.route('/data/tours/<tour_id>')
def data_tour(tour_id):

    tour_id = int(tour_id)  # предпочёл бы реализовать в декораторе, но не рискну нарушить тз.

    if tour_id not in tours:
        return 'Такого тура не существует.'

    tour_data = tours[tour_id]

    return render_template('data-tour.html', tour=tour_data)


if __name__ == '__main__':
    app.run('0.0.0.0', 8000, debug=True)
