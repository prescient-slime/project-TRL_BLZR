import matplotlib.pyplot as plt


# Function to read polygons from a text file
def read_polygons(filename):
    polygons = []
    with open(filename, "r") as file:
        polygon = []
        for line in file:
            if "shape" in line:
                if polygon:
                    polygons.append(polygon)
                    polygon = []
            else:
                lat, lon = map(float, line.split(","))
                polygon.append((lat, lon))
        if polygon:
            polygons.append(polygon)
    return polygons


# Function to plot polygons using matplotlib
def plot_polygons(polygons):
    plt.figure()
    for polygon in polygons:
        latitudes, longitudes = zip(*polygon)
        plt.plot(longitudes, latitudes)
    plt.savefig("polygons.png")


# Read polygons from a text file
polygons = read_polygons("boundary_vertices.txt")

# Plot the polygons
plot_polygons(polygons)
