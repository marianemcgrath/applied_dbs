# Data Access Object - Database query functions
# Author: Mariane McGrath
#
# NOTE: This file contains the INNOVATION FEATURE - Networking (Suggested Connections)
# The 'networking()' function implements a friend-of-a-friend recommendation engine
# using Neo4j graph traversal up to 4 degrees of separation.


# INNOVATION FEATURE - Networking (Suggested Connections)

# Uses Neo4j shortestPath to find attendees within N degrees of separation
# who are not already directly connected to the given attendee.
# The user can filter results by choosing how many degrees away to search (2-4).
# Names are looked up from MySQL to enrich the Neo4j results.
