if __name__ == "__main__":
    d = {
        "f1": 4,
        "f2": 5,
    }
    print("d1:",d)
    d2 = d
    d2["f2"] = 6
    print("d1:", d)
    print("d2:", d2)