from app.neo4j_service import driver


def search_graph(entity_name):

    with driver.session(database="neo4j") as session:

        result = session.run(
         """
         MATCH (a:Entity)-[r]->(b)
         WHERE toLower(a.name) CONTAINS toLower($name)
         RETURN a.name AS source,
           type(r) AS relation,
           b.name AS target
            """,
            name=entity_name
        )

        return result.data()