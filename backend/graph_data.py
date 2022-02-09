from pathlib import Path
from csv import reader
import models
from app import memgraph


def load():
    path = Path("import-data/graphlandscapenew1.csv")

    with open(path) as read_obj:
        csv_reader = reader(read_obj)
        header = next(csv_reader)
        if header is None:
            return
        for row in csv_reader:
            company = models.Company(
                name=row[0],
                website=row[3],
                img="".join(row[0].split()).lower(),
            ).save(memgraph)
            category = models.Category(name=row[1]).save(memgraph)
            subcategory = models.Subcategory(name=row[2]).save(memgraph)
            is_part_of = models.IsPartOf(
                _start_node_id=company._id, _end_node_id=subcategory._id
            ).save(memgraph)

            belongs_to = models.BelongsTo(
                _start_node_id=subcategory._id, _end_node_id=category._id
            ).save(memgraph)
