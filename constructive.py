from classes.model.Depot import *


def constructive_heuristic(dataset):
    """
    This constructive heuristic uses the greedy algotithm to traces routes for the depot vehicles
    """
    max_cap = dataset.pop(0)
    vehicles = dataset.pop(0)
    depot_pos = dataset[0]

    depot = Depot(
        Point2D(depot_pos[0], depot_pos[1]),
        vehicles[0],
        max_cap[0]
    )

    depot.bulk_add_customer(dataset)

    return depot.trace_routes(1)
