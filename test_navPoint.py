from navPoint import NavPoint, AddNavNeighbor


def test_nav_point():
    n1 = NavPoint(1, "GIR", 41.9313888889, 2.7716666667)
    n2 = NavPoint(2, "GODOX", 39.3725, 1.4108333333)

    print("Testing NavPoint:")
    print(n1)
    print(n2)

    print("\nTesting AddNavNeighbor:")
    print(AddNavNeighbor(n1, n2))  # Should return True
    print(AddNavNeighbor(n1, n2))  # Should return False

    print("\nNeighbors of n1:")
    for neighbor in n1.neighbors:
        print(neighbor)


if __name__ == "__main__":
    test_nav_point()