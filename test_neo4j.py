from neo4j import GraphDatabase

# Hardcode the credentials temporarily to test
URI = "neo4j+s://80769af1.databases.neo4j.io"
USERNAME = "80769af1"
PASSWORD = "gQSo1EwvFN4oVC45Jag3Yj69FLrHjYixUiqdqOCMx5Y"

print("Testing Neo4j connection...")
print(f"URI: {URI}")
print(f"Username: {USERNAME}")

try:
    driver = GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))
    with driver.session() as session:
        result = session.run("RETURN 'Connection successful!' as message")
        print(f"✅ SUCCESS: {result.single()['message']}")
    driver.close()
except Exception as e:
    print(f"❌ ERROR: {e}")