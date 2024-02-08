import numpy as np
import pandas as pd
import shapely
#import matplotlib.pyplot as plt


def air_spaces():
    points = pd.read_csv("new_data.csv")
    points = points.drop_duplicates(subset = ["LATITUDE", "LONGITUDE"])
    points = points.groupby("APT1_NAME")
    return {name: data for name, data in points}


def boundary_input():
    boundary = np.zeros([4, 2])
    count = 0
    while count < 4:
        point = str(input("Enter Lat, Long for boundary points. Must be 4 points: "))
        point = point.split(", ")
        lat = float(point[0])
        long = float(point[1])
        point = [lat, long]
        boundary[count] = point
        count += 1
    return boundary


def poly_gen(points):
    polygon = shapely.Polygon(points)
    return polygon


def sort_points(points):
    centroid = np.mean(points, axis=0)

    angles = np.arctan2(points[:, 1] - centroid[1], points[:, 0] - centroid[0])

    sorted_points = points[np.argsort(angles)]

    return sorted_points


def plot_boundary(polygon, color="red"):
    x, y = polygon.exterior.coords.xy
    plt.fill(x, y, color, alpha=0.5)
    plt.plot(x, y, color="black")
    plt.xlabel("X Coords")
    plt.ylabel("Y Coords")
    plt.title("Polygon Plot")
    plt.grid(True)
    plt.axis("equal")


def main():
    air_spaces_list = air_spaces()
    flight_boundary = poly_gen(
        [
            [-101.9137372711676, 34.9799071416371],
            [-101.91374530871289, 34.98069082284931],
            [-101.91527244230875, 34.98077643462814],
            [-101.91520814194682, 34.979940069570056],
        ]
        #boundary_input()
    )
    print(flight_boundary)
    for space_name, space_data in air_spaces_list.items():
        space_points = np.array(
            [
                [long, lat]
                for long, lat in zip(space_data["LONGITUDE"], space_data["LATITUDE"])
            ]
        )
        space_points = sort_points(space_points)
        space_polygon = shapely.Polygon(space_points)
        if flight_boundary.overlaps(space_polygon):
            print(f"Overlap detected for air space: {space_name}. Aborting...")
            #flight_boundary = flight_boundary.difference(space_polygon)
            exit()
        with open('boundary_vertices.txt', 'w') as file:
            try:
                for coord in list(flight_boundary.exterior.coords):
                    file.write(f"{coord[1]}, {coord[0]}\n")
            except AttributeError as e:
                count = 1
                for geom in flight_boundary.geoms:
                    file.write(f"shape no. {count}:\n")
                    for coord in list(geom.exterior.coords):
                        file.write(f"{coord[1]}, {coord[0]}\n")
                    count += 1
            file.close() 

if __name__ == "__main__":
    main()
