from neo4j import GraphDatabase
from dotenv import load_dotenv
import os

load_dotenv()

def get_neo4j_driver():
    return GraphDatabase.driver(
        os.getenv("NEO4J_URI"),
        auth=("neo4j", os.getenv("NEO4J_PASSWORD"))
    )