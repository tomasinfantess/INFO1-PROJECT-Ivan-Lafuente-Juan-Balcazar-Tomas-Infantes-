from airSpace import AirSpace


def test_air_space():
    airspace = AirSpace()

    # Test loading (you'll need to create small test files or mock data)
    print("Testing AirSpace loading...")

    # For actual testing, you should create small test files
    # airspace.load_nav_points("test_nav.txt")
    # airspace.load_nav_segments("test_seg.txt")
    # airspace.load_nav_airports("test_ger.txt")
    # airspace.build_neighbors()

    print("\nAirSpace created successfully")


if __name__ == "__main__":
    test_air_space()