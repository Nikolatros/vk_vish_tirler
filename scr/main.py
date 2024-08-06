# GOT ENV VARIABLES
# GOT CONNETCTION
from database import DBWriter
from parser import Parser


def main():
    parser = Parser()
    writer = DBWriter()

    writer.db_connect()

    parsing = True
    offset = 0
    while parsing:
        try:
            posts = parser.parse_posts(conut=100, offset=offset)
            writer.insert_data(posts=posts)
            offset += 101
        except:
            parsing = False
    else:
        writer.db_disconnect()


if __name__ == "__main__":
    main()
