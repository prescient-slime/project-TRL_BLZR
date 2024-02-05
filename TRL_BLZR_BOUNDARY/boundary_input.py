import numpy as np
import pandas as pd
import shapely


def air_spaces():
    points = pd.read_csv("new_data.csv")
    points = points.groupby("APT1_NAME")
    return points

def boundary_input():
    boundary = np.zeros([4, 2])
    count = 0
    while count < 4:
        point = str(input("Enter Lat, Long for boundary points. Must be 4 points"))
        point = point.split(",")
        lat = float(point[0])
        long = float(point[1])
        point = [lat, long]
        boundary[count] = point
        count += 1
    return boundary

def poly_gen(points):
    polygon = shapely.Polygon(points)
    return polygon

def main():
    # boundary_input()
    #air_spaces()
    shape = poly_gen(boundary_input())
    print(shape)

if __name__ == "__main__":
    main()
