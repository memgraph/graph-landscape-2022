from csv import reader
from gqlalchemy import Memgraph
from pathlib import Path
import models
import time


memgraph = Memgraph()


def load_data():
    """Load data into the database."""

    memgraph.drop_database()
    path = Path("graphlandscape.csv")

    with open(path) as read_obj:
        csv_reader = reader(read_obj)
        header = next(csv_reader)
        if header is None:
            return
        for row in csv_reader:
            # Create nodes and save them into Memgraph
            company = models.Company(
                name=row[0], website=row[3], img="".join(row[0].split()).lower(),
            ).save(memgraph)
            category = models.Category(name=row[1]).save(memgraph)
            subcategory = models.Subcategory(name=row[2]).save(memgraph)

            # Create relationships and save them into Memgraph
            models.IsPartOf(
                _start_node_id=company._id, _end_node_id=subcategory._id
            ).save(memgraph)
            models.BelongsTo(
                _start_node_id=subcategory._id, _end_node_id=category._id
            ).save(memgraph)
    print("Data has been loaded into Memgraph. Open Memgraph Lab to query it.")


def connect_to_memgraph():
    """Establish a connection to the database."""

    connection_established = False
    while not connection_established:
        try:
            if memgraph._get_cached_connection().is_active():
                connection_established = True
        except:
            print("Memgraph probably isn't running.")
            time.sleep(4)


def main():
    connect_to_memgraph()
    load_data()


if __name__ == "__main__":
    main()
