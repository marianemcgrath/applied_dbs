from neo4j import GraphDatabase

def get_neo4j_driver():
    return GraphDatabase.driver(
        "neo4j+s://383560de.databases.neo4j.io",
        auth=("neo4j", "ZL6ni5VbmTG0HQyhpms24uCiyXluMn4eve8569GD2o4")
    )