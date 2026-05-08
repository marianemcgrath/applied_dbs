# Neo4j connection module for conference management system
# Author: Mariane McGrath

import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

def get_neo4j_driver():
    return GraphDatabase.driver(
        os.getenv("NEO4J_URI"),
        auth=(
            os.getenv("NEO4J_USER"),
            os.getenv("NEO4J_PASSWORD")
        )
    )

    # Source: [https://neo4j.com/docs/python-manual/current/connect-advanced/](Advanced Connection)
    # Source: [https://neo4j.com/docs/python-manual/current/](Neo4j Python Driver Manual)
    # Source: [https://docs.python.org/3/library/os.html#os.getenv](Python 3 Docs: os.getenv)