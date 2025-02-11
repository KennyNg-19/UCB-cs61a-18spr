"""A Yelp-powered Restaurant Recommendation Program"""

from abstractions import *
from data import ALL_RESTAURANTS, CATEGORIES, USER_FILES, load_user_file
from ucb import main, trace, interact
from utils import distance, mean, zip, enumerate, sample
from visualize import draw_map

##################################
# Phase 2: Unsupervised Learning #
##################################


def find_closest(location, centroids):
    """Return the centroid in centroids that is closest to location.
    If multiple centroids are equally close, return the first one.

    >>> find_closest([3.0, 4.0], [[0.0, 0.0], [2.0, 3.0], [4.0, 3.0], [5.0, 5.0]])
    [2.0, 3.0]
    """
    # BEGIN Question 3
    "*** YOUR CODE HERE ***"
    
    # return min([distance(location, centroid) for centroid in centroids])
    # 问题：how to get index of min in list?

    # 正解：min + built-in key=lambda, 对于多参数的func，只要在lambda那里定义好iterate的参数即可！!
    return min(centroids, key=lambda centroid: distance(location, centroid))
    # END Question 3


def group_by_first(pairs):
    """Return a list of pairs that relates each unique key in the [key, value]
    pairs to a list of all values that appear paired with that key.

    Arguments:
    pairs -- a sequence of pairs

    >>> example = [ [1, 2], [3, 2], [2, 4], [1, 3], [3, 1], [1, 2] ]
    >>> group_by_first(example)
    [[2, 3, 2], [2, 1], [4]]
    """
    keys = []
    for key, _ in pairs:
        if key not in keys:
            keys.append(key)
    return [[y for x, y in pairs if x == key] for key in keys]


def group_by_centroid(restaurants, centroids):
    """Return a list of clusters, where each cluster contains all restaurants
    nearest to a corresponding centroid in centroids. 
    Each item in restaurants should appear once in the result, along with the other
    restaurants closest to the same centroid.

    Argument:
    centroids----a list of centroids[location]
    restaurant----a list of restaurants[name, location, categories, price, reviews]

    Return:
    [restaurants1, restaurants2, restaurants3 ....]
    """
    # BEGIN Question 4

    "*** YOUR CODE HERE ***"
    # pair of [centroid, restaurant] in list form
    centroid_rst_pairs = [[find_closest(restaurant_location(rst), centroids), rst] for rst in restaurants] 
    return group_by_first(centroid_rst_pairs)
    # END Question 4


def find_centroid(cluster):
    """Return the centroid of the locations of the restaurants in cluster.
    
    Argument: 
    cluster----list of restaurants
    """
    # BEGIN Question 5
    "*** YOUR CODE HERE ***"
    locations = []
    longtitudes = [restaurant_location(rst)[0] for rst in cluster]
    langtitudes = [restaurant_location(rst)[1] for rst in cluster]
    return [mean(longtitudes), mean(langtitudes)]
    # END Question 5


def k_means(restaurants, k, max_updates=100):
    """Use k-means to group restaurants by location into k clusters."""
    assert len(restaurants) >= k, 'Not enough restaurants to cluster'
    old_centroids, n = [], 0
    # Select initial centroids randomly by choosing k different restaurants
    centroids = [restaurant_location(r) for r in sample(restaurants, k)]

    while old_centroids != centroids and n < max_updates:
        old_centroids = centroids
        # BEGIN Question 6
        "*** YOUR CODE HERE ***"
        clusters = group_by_centroid(restaurants, centroids)

        # update the centroids
        centroids = [find_centroid(cluster) for cluster in clusters]
        # END Question 6
        n += 1
    return centroids


################################
# Phase 3: Supervised Learning #
################################


def find_predictor(user, restaurants, feature_fn):
    """Return a rating predictor (a function from restaurants to ratings),
    for a user by performing least-squares linear regression using feature_fn
    on the items in restaurants. Also, return the R^2 value of this model.

    Arguments:
    user -- A user
    restaurants -- A sequence of restaurants
    feature_fn -- A function that takes a restaurant and returns a number
    """
    reviews_by_user = {review_restaurant_name(review): review_rating(review)
                       for review in user_reviews(user).values()}

    xs = [feature_fn(r) for r in restaurants]
    ys = [reviews_by_user[restaurant_name(r)] for r in restaurants]

    # BEGIN Question 7
    x_mean = mean(xs)
    y_mean = mean(ys)
    S_xx = sum([(x - x_mean) ** 2 for x in xs])
    S_yy = sum([(y - y_mean) ** 2 for y in ys])

    # 使用zip
    # sxy = sum([x*y for x, y in zip([x - mean(xs) for x in xs], [y - mean(ys) for y in ys])])
    # 简化：expr部分提出来，而不是在in后面的iterable那
    S_xy = sum([(x - x_mean) * (y - y_mean) for x, y in zip(xs, ys)])
    
    b = S_xy / S_xx  # REPLACE THIS LINE WITH YOUR SOLUTION
    a = y_mean - b * x_mean
    r_squared = S_xy ** 2 / (S_xx * S_yy)

    # END Question 7

    def predictor(restaurant):
        return b * feature_fn(restaurant) + a

    return predictor, r_squared


def best_predictor(user, restaurants, feature_fns):
    """Find the feature within feature_fns that gives the highest R^2 value
    for predicting ratings by the user; return a predic tor using that feature.

    Arguments:
    user -- A user
    restaurants -- A list of restaurants
    feature_fns -- A sequence of functions that each takes a restaurant
    """
    reviewed = user_reviewed_restaurants(user, restaurants)
    # BEGIN Question 8
    "*** YOUR CODE HERE ***"
    fn = max(feature_fns, key = lambda feature_fn: find_predictor(user, reviewed, feature_fn)[1])
    
    # return a predictor
    return find_predictor(user, reviewed, fn)[0]
    # END Question 8


def rate_all(user, restaurants, feature_fns):
    """Return the predicted ratings of restaurants by user using the best
    predictor based on a function from feature_fns.

    Arguments:
    user -- A user
    restaurants -- A list of restaurants
    feature_fns -- A sequence of feature functions
    """
    predictor = best_predictor(user, ALL_RESTAURANTS, feature_fns)
    reviewed = user_reviewed_restaurants(user, restaurants)
    # BEGIN Question 9
    "*** YOUR CODE HERE ***"
    # trick: 为了避免通过difference of lists来获取unreviewed rst，
    # 1、先用predictor算一遍
    # predictor is a func(rst) with params a & b:  return b * feature_fn(restaurant) + a
    ratings = {restaurant_name(rst): predictor(rst) for rst in restaurants}

    # 2. 再用可以已有的reviewed重新算部分
    # reviewed is a list of rst, but user_rating needs rst_name: needs restaurant_name(rst)
    for rst in reviewed:
        # update dict
        ratings[restaurant_name(rst)] = user_rating(user, restaurant_name(rst))

    '''
    BETTER solution： dict 自带update func，就不用管先后顺序了
    ratings = {restaurant_name(rst): user_rating(user, restaurant_name(rst)) for rst in reviewed}
    ratings_predicted = {restaurant_name(rst): predictor(rst) for rst in restaurants if restaurant_name(rst) not in ratings}
    ratings.update(ratings_predicted)
    '''
    return ratings
    # END Question 9


def search(query, restaurants):
    """Return each restaurant in restaurants that has query as a category.

    Arguments:
    query -- A string
    restaurants -- A sequence of restaurants
    """
    # BEGIN Question 10
    "*** YOUR CODE HERE ***"
    # 使用 restaurant_categories(restaurant), 
    # 注意query是single str, 允许多类别，restaurant_categories(rst)是list of str----所以用in
    return [ rst for rst in restaurants if query in restaurant_categories(rst)]
    # END Question 10


def feature_set():
    """Return a sequence of feature functions."""
    return [lambda r: mean(restaurant_ratings(r)),
            restaurant_price,
            lambda r: len(restaurant_ratings(r)),
            lambda r: restaurant_location(r)[0],
            lambda r: restaurant_location(r)[1]]


@main
def main(*args):
    import argparse
    parser = argparse.ArgumentParser(
        description='Run Recommendations',
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument('-u', '--user', type=str, choices=USER_FILES,
                        default='test_user',
                        metavar='USER',
                        help='user file, e.g.\n' +
                        '{{{}}}'.format(','.join(sample(USER_FILES, 3))))
    parser.add_argument('-k', '--k', type=int, help='for k-means')
    parser.add_argument('-q', '--query', choices=CATEGORIES,
                        metavar='QUERY',
                        help='search for restaurants by category e.g.\n'
                        '{{{}}}'.format(','.join(sample(CATEGORIES, 3))))
    parser.add_argument('-p', '--predict', action='store_true',
                        help='predict ratings for all restaurants')
    parser.add_argument('-r', '--restaurants', action='store_true',
                        help='outputs a list of restaurant names')
    args = parser.parse_args()

    # Output a list of restaurant names
    if args.restaurants:
        print('Restaurant names:')
        for restaurant in sorted(ALL_RESTAURANTS, key=restaurant_name):
            print(repr(restaurant_name(restaurant)))
        exit(0)

    # Select restaurants using a category query
    if args.query:
        restaurants = search(args.query, ALL_RESTAURANTS)
    else:
        restaurants = ALL_RESTAURANTS

    # Load a user
    assert args.user, 'A --user is required to draw a map'
    user = load_user_file('{}.dat'.format(args.user))

    # Collect ratings
    if args.predict:
        ratings = rate_all(user, restaurants, feature_set())
    else:
        restaurants = user_reviewed_restaurants(user, restaurants)
        names = [restaurant_name(r) for r in restaurants]
        ratings = {name: user_rating(user, name) for name in names}

    # Draw the visualization
    if args.k:
        centroids = k_means(restaurants, min(args.k, len(restaurants)))
    else:
        centroids = [restaurant_location(r) for r in restaurants]
    draw_map(centroids, restaurants, ratings)