from neo4j import GraphDatabase

URI = "bolt://127.0.0.1:7687"
USERNAME = "neo4j"
PASSWORD = "12345678"

driver = GraphDatabase.driver(
    URI,
    auth=(USERNAME, PASSWORD)
)


def create_entity(tx, entity_name, label):
    tx.run(
        """
        MERGE (e:Entity {
            name:$name,
            label:$label
        })
        """,
        name=entity_name,
        label=label
    )


def create_relationship(tx, source, relation, target):
    tx.run(
        f"""
        MERGE (a:Entity {{name:$source}})
        MERGE (b:Entity {{name:$target}})
        MERGE (a)-[:{relation}]->(b)
        """,
        source=source,
        target=target
    )


def save_entity(entity_name, label):
    with driver.session(database="neo4j") as session:
        session.execute_write(
            create_entity,
            entity_name,
            label
        )


def save_relationship(source, relation, target):
    with driver.session(database="neo4j") as session:
        session.execute_write(
            create_relationship,
            source,
            relation,
            target
        )