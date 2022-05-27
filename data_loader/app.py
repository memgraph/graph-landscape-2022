from ast import literal_eval
from csv import reader
from gqlalchemy import Memgraph, match
from pathlib import Path
import models
import time


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
                name=row[0],
                website=row[3],
                img="".join(row[0].split()).lower(),
            ).save(memgraph)

            models.Category(name=row[1]).save(memgraph)
            models.Subcategory(name=row[2]).save(memgraph)

            (
                match()
                .node(labels="Company", variable="company")
                .where(item="company.name", operator="=", literal=row[0])
                .with_(results={"company": "company"})
                .match()
                .node(labels="Subcategory", variable="subcategory")
                .where(item="subcategory.name", operator="=", literal=row[2])
                .merge()
                .node(variable="company")
                .to(edge_label="IS_PART_OF")
                .node(variable="subcategory")
                .execute()
            )

            (
                match()
                .node(labels="Subcategory", variable="subcategory")
                .where(item="subcategory.name", operator="=", literal=row[2])
                .with_(results={"subcategory": "subcategory"})
                .match()
                .node(labels="Category", variable="category")
                .where(item="category.name", operator="=", literal=row[1])
                .merge()
                .node(variable="subcategory")
                .to(edge_label="BELONGS_TO")
                .node(variable="category")
                .execute()
            )

    print("Data has been loaded into Memgraph. Open Memgraph Lab to query it.")


def connect_to_memgraph():
    """Establish a connection to the database."""
    memgraph = Memgraph()
    connection_established = False

    while not connection_established:
        try:
            if memgraph._get_cached_connection().is_active():
                connection_established = True
                return memgraph
        except:
            print("Memgraph probably isn't running.")
            time.sleep(4)


memgraph = connect_to_memgraph()


def main():
    load_data()


if __name__ == "__main__":
    main()
