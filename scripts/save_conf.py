from libraries.Environment import Environment

if __name__ == "__main__":
    table = Environment()
    table.startInit()
    table.save("./parser_data/conf.pkl")