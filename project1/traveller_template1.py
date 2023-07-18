"""

Name:       Minh Vu
Email:      2004minhvu@gmail.com

Project: Road Trip Optimizer

This program examines and manipulates the distance between a departure city and a destination city.It can add a
connection between a departure and a destination city, and it can remove a connection between a departure and
a destination city. Moreover, it can find all the neighbouring cities of a city, and it can print a route to go
from a city to another city.
"""


def find_route(data, departure, destination):
    """
    This function, an already provided function, tries to find
    a route between <departure> and <destination> cities. It assumes
    the existence of the two functions fetch_neighbours and distance_to_neighbour
    (see the assignment and the function templates below).
    They are used to get the relevant information from the data
    structure <data> for find_route to be able to do the search.

    The return value is a list of cities one must travel through
    to get from <departure> to <destination>. If for any
    reason the route does not exist, the return value is
    an empty list [].

    :param data: dict, A data structure which contains the distance information between the cities.
    :param departure: str, the name of the departure city.
    :param destination: str, the name of the destination city.
    :return: list[str], a list of cities the route travels through, or
           an empty list if the route can not be found. If the departure
           and the destination cities are the same, the function returns
           a two element list where the departure city is stored twice.
    """

    if departure not in data:
        return []

    elif departure == destination:
        return [departure, destination]

    greens = {departure}
    deltas = {departure: 0}
    came_from = {departure: None}

    while True:
        if destination in greens:
            break

        red_neighbours = []
        for city in greens:
            for neighbour in fetch_neighbours(data, city):
                if neighbour not in greens:
                    delta = deltas[city] + distance_to_neighbour(data, city, neighbour)
                    red_neighbours.append((city, neighbour, delta))

        if not red_neighbours:
            return []

        current_city, next_city, delta = min(red_neighbours, key=lambda x: x[2])

        greens.add(next_city)
        deltas[next_city] = delta
        came_from[next_city] = current_city

    route = []
    while True:
        route.append(destination)
        if destination == departure:
            break
        destination = came_from.get(destination)

    return list(reversed(route))


def read_distance_file(file_name):
    """
    Reads the distance information from <file_name> and stores it
    in a suitable data structure (you decide what kind of data
    structure to use). This data structure is also the return value,
    unless an error happens during the file reading operation.

    :param file_name: str, The name of the file to be read.
    :return: dict | None: A data structure containing the information
             read from the <file_name> or None if any kind of error happens.
             The data structure to be chosen is completely up to you as long
             as all the required operations can be implemented using it.
    """

    try:
        distance_file = open(file_name, mode="r")
        # distance information in the file is store as dictionaries in an outer dictionary
        # each key of the big dictionary is a departure city, payload of that key is an inner dictionary
        # keys of the small dict are destination, payloads of those keys are distance between the destination and
        # the departure
        data = {}
        # iterate through every line of the file
        for line in distance_file:
            line = line.rstrip()
            departure, destination, distance = line.split(";")
            # check if a departure city is stored as the key of the outer dictionary or not
            if departure not in data:
                # if not, create a new inner dictionary for it
                data[departure] = {}
            # if the departure city is already stored, add more destination and distance into its inner dictionary
            data[departure][destination] = distance
            # connect departure and destination + distance through the big dictionary

    except OSError:
        data = None

    return data


def fetch_neighbours(data, city):
    """
    Returns a list of all the cities that are directly
    connected to parameter <city>. In other words, a list
    of cities where there exist an arrow from <city> to
    each element of the returned list. Return value is
    an empty list [], if <city> is unknown or if there are no
    arrows leaving from <city>.

    :param data: dict, A data structure containing the distance
           information between the known cities.
    :param city: str, the name of the city whose neighbours we
           are interested in.
    :return: list[str], the neighbouring city names in a list.
             Returns [], if <city> is unknown (i.e. not stored as
             a departure city in <data>) or if there are no
             arrows leaving from the <city>.
    """

    # create an empty list which is meant for containing the neighbouring city of the parameter city
    neighbours_list = []
    if city in data:
        # this city is not a city that can be departure from, then return the empty list
        if not data[city]:
            return neighbours_list
        else:
            # this city is a city that can be departure from, then add all the neighbouring city into the list
            # and return that list
            for neighbours in data[city]:
                neighbours_list.append(neighbours)
            return neighbours_list
    # this city is not stored in the <data> parameter, then return the empty list
    else:
        return neighbours_list


def distance_to_neighbour(data, departure, destination):
    """
    Returns the distance between two neighbouring cities.
    Returns None if there is no direct connection from
    <departure> city to <destination> city. In other words
    if there is no arrow leading from <departure> city to
    <destination> city.

    :param data: dict, A data structure containing the distance
           information between the known cities.
    :param departure: str, the name of the departure city.
    :param destination: str, the name of the destination city.
    :return: int | None, The distance between <departure> and
           <destination>. None if there is no direct connection
           between the two cities.
    """

    neighbour = fetch_neighbours(data, departure)
    # utilizing the function fetch_neighbours to check if the destination city is a neighbour of the departure
    # city or not
    if destination not in neighbour:
        return None
    # If yes, return the distance between two neighbouring cities
    else:
        return int(data[departure][destination])


def add(distance_dict):
    """"
    This function add a new connection from either a known or unknown city to a new destination
    
    :param distance_dict: the data structure containing the information read from the input file
    """""

    departure_city = input("Enter departure city: ")
    destination_city = input("Enter destination city: ")
    distance = input("Distance: ")
    # checking if the input distance is an integer or not
    if not distance.isdigit():
        print(f"Error: '{distance}' is not an integer.")
    else:
        # If there has been a connection between the departure city and destination city before, the distance
        # will be updated
        if departure_city in distance_dict:
            distance_dict[departure_city][destination_city] = distance
        # if not, a new connection will be created
        else:
            distance_dict[departure_city] = {}
            distance_dict[departure_city][destination_city] = distance


def remove(distance_dict):
    """"
    This function remove a connection from a known city to one of its destination

    :param distance_dict: the data structure containing the information read from the input file
    """

    departure_city = input("Enter departure city: ")
    # checking if this city can be departure from or not.
    if departure_city not in distance_dict:
        print(f"Error: '{departure_city}' is unknown.")

    else:
        destination_city = input("Enter destination city: ")
        # checking if there's any connection between the departure and destination city or not
        if destination_city not in distance_dict[departure_city]:
            print(f"Error: missing road segment between '{departure_city}' and '{destination_city}'.")
        else:
            distance_dict[departure_city].pop(destination_city)


def neighbouring(distance_dict):
    """"
    This function prints all the connection from a departure city to any of its destination

    :param distance_dict: the data structure containing the information read from the input file
    """

    departure_city = input("Enter departure city: ")
    # check if this city is a known city or not by checking if it can be departure from,
    # and it could be a destination or not
    if departure_city not in distance_dict:
        if departure_city not in checking_city(distance_dict, departure_city):
            print(f"Error: '{departure_city}' is unknown.")
        else:
            return
    # it the departure city is known, then print all the connections if possible
    else:
        sorted_destination = sorted(distance_dict[departure_city])
        for destination in sorted_destination:
            print(f"{departure_city:<14}{destination:<14}{distance_dict[departure_city][destination]:>5}")


def checking_city(data, city):
    """"
    This function test if a city that can't be departure from is known or not (can be a destination to go to from
    other cities or not)

    :param data: the data structure containing the information read from the input file
    :param city: the city which will be tested
    :return list: a list containing known city
    """

    known_city = []
    unknown_city = []
    for departure_city in data:
        if city not in data[departure_city]:
            unknown_city.append(city)
        else:
            known_city.append(city)
    return known_city


def print_route(data):
    """"
    This function utilizes the function find_route to print a route from one city to another
    together with the total distance

    :param data: the data structure containing the information read from the input file
    """

    departure = input("Enter departure city: ")
    # check if the departure city is unknown or not
    if departure not in data:
        # if this city is not a city that can be departure from, check if that city could be a destination or not
        if departure not in checking_city(data, departure):
            print(f"Error: '{departure}' is unknown.")
        else:
            # this departure city is a known city, but there is no way to go out of that city
            # Hence, there is no connection from that city to any other city
            des = input("Enter destination city: ")
            print(f"No route found between '{departure}' and '{des}'.")
    else:
        # the departure city is a known city and can be departure from
        destination = input("Enter destination city: ")
        # create a list that contain the route to go from the departure city to the destination city
        list_of_route = find_route(data, departure, destination)
        if not list_of_route:
            print(f"No route found between '{departure}' and '{destination}'.")
        else:
            # if the departure and destination city is 1 city
            if len(list_of_route) == 2 and list_of_route[0] == list_of_route[1]:
                print(f"{list_of_route[0]}-{list_of_route[1]} (0 km)")
            else:
                list_of_distance = []
                # this list contains the distance between every two cities
                for i in range(len(list_of_route)-1):
                    list_of_distance.append(int(data[list_of_route[i]][list_of_route[i+1]]))
                # add up every distance inside that list_of_distance and obtain the
                # total distance to travel
                total_distance = sum(list_of_distance)
                # print out the route and the total distance
                for idx in range(len(list_of_route)):
                    print(list_of_route[idx], end="")
                    if idx == len(list_of_route) - 1:
                        print(f" ({total_distance} km)\n")
                    else:
                        print("-", end="")


def main():
    input_file = input("Enter input file name: ")

    distance_data = read_distance_file(input_file)

    if distance_data is None:
        print(f"Error: '{input_file}' can not be read.")
        return

    while True:
        action = input("Enter action> ")

        if action == "":
            print("Done and done!")
            return

        elif "display".startswith(action):
            sorted_departure = sorted(distance_data)

            for departure in sorted_departure:
                sorted_destination = sorted(distance_data[departure])
                for destination in sorted_destination:
                    print(f"{departure:<14}{destination:<14}{distance_data[departure][destination]:>5}")

        elif "add".startswith(action):

            add(distance_data)
        elif "remove".startswith(action):

            remove(distance_data)
        elif "neighbours".startswith(action):

            neighbouring(distance_data)
        elif "route".startswith(action):
            print_route(distance_data)

        else:
            print(f"Error: unknown action '{action}'.")


if __name__ == "__main__":
    main()
