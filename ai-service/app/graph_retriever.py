from neo4j import GraphDatabase

URI = "neo4j://127.0.0.1:7687"
USERNAME = "neo4j"
PASSWORD = "12345678"

driver = GraphDatabase.driver(
    URI,
    auth=(USERNAME, PASSWORD)
)


def retrieve_graph(question):

    with driver.session(database="neo4j") as session:

        result = session.run(
            """
            MATCH (a)-[r]->(b)
            RETURN
                a.name AS source,
                type(r) AS relation,
                b.name AS target
            LIMIT 100
            """
        )

        graph_context = []

        for record in result:

            graph_context.append(
                f"{record['source']} {record['relation']} {record['target']}"
            )

        return "\n".join(graph_context)