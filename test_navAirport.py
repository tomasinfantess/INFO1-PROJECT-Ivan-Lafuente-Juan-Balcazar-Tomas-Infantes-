from navAirport import NavAirport
from navPoint import NavPoint


def test_nav_airport():
    airport = NavAirport("LEBL")
    point1 = NavPoint(6063, "IZA.D", 38.8731546833, 1.37242975)
    point2 = NavPoint(6062, "IZA.A", 38.8772804833, 1.36930455)

    airport.add_sid(point1)
    airport.add_star(point2)

    print("Testing NavAirport:")
    print(airport)
    print("\nSIDs:")
    for sid in airport.sids:
        print(sid)
    print("\nSTARs:")
    for star in airport.stars:
        print(star)


if __name__ == "__main__":
    test_nav_airport()