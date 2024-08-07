from database import DBWriter
from parser import Parser


def main():
    parser = Parser()
    writer = DBWriter()

    writer.db_connect()

    data = parser.parse_all()

    writer.insert_data(data)

    writer.db_disconnect()


if __name__ == "__main__":
    main()
