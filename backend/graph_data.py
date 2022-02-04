from pathlib import Path
from csv import reader
import models
from app import memgraph


def load():
    path = Path("import-data/graphlandscape.csv")

    with open(path) as read_obj:
        csv_reader = reader(read_obj)
        header = next(csv_reader)
        if header != None:
            for row in csv_reader:
                technology = models.Technology(
                    name=row[1],
                    description=row[3],
                    website=row[4],
                    img_url="".join(row[1].split()).lower(),
                ).save(memgraph)
                organization = models.Organization(name=row[0]).save(memgraph)
                category = models.Category(name=row[2]).save(memgraph)

                is_part_of = models.IsPartOf(
                    _start_node_id=technology._id, _end_node_id=organization._id
                ).save(memgraph)

                belongs_to = models.BelongsTo(
                    _start_node_id=technology._id, _end_node_id=category._id
                ).save(memgraph)
