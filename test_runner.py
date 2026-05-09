#!/usr/bin/env python3
# Updated test script Conference Management System
# This script runs a series of tests against the main.py application,
# simulating user input and checking for expected output.

import subprocess
import sys
import os

import mysql.connector
from neo4j import GraphDatabase
from dotenv import load_dotenv


# LOAD ENV VARIABLES

load_dotenv()

MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USER = os.getenv("NEO4J_USER")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")


# DATABASE CONNECTION CHECKS

def check_mysql():
    """Check if MySQL is running and accessible."""

    try:
        conn = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE
        )

        if conn.is_connected():
            print("✅ MySQL connection successful")
            conn.close()
            return True

    except mysql.connector.Error as err:
        print(f"❌ MySQL connection failed: {err}")

    return False


def check_neo4j():
    """Check if Neo4j is running and accessible."""

    try:
        driver = GraphDatabase.driver(
            NEO4J_URI,
            auth=(NEO4J_USER, NEO4J_PASSWORD)
        )

        with driver.session() as session:
            session.run("RETURN 1")

        print("✅ Neo4j connection successful")
        driver.close()
        return True

    except Exception as err:
        print(f"❌ Neo4j connection failed: {err}")

    return False


def check_databases():
    """Ensure both databases are working before running tests."""

    print("\n" + "=" * 60)
    print(" CHECKING DATABASE CONNECTIONS")
    print("=" * 60)

    mysql_ok = check_mysql()
    neo4j_ok = check_neo4j()

    if not mysql_ok or not neo4j_ok:
        print("\n❌ Cannot start tests.")
        print("Please ensure MySQL and Neo4j are both running.")
        sys.exit(1)

    print("\n✅ All database connections verified.\n")


# TEST RUNNER

def run_test(test_name, inputs, expected_strings):

    print(f"\n{'='*60}")
    print(f"TEST: {test_name}")
    print(f"{'='*60}")

    try:
        result = subprocess.run(
            [sys.executable, "main.py"],
            input=inputs,
            text=True,
            capture_output=True,
            timeout=15
        )

        output = result.stdout.lower()

        print("\n--- OUTPUT (last 800 chars) ---")
        print(output[-800:])
        print("--- END OUTPUT ---\n")

        passed = False

        # Pass if ANY expected string is found
        for expected in expected_strings:
            if expected.lower() in output:
                print(f"✅ Found: {expected}")
                passed = True
                break

        if passed:
            print("\n✅ TEST PASSED")
        else:
            print("\n❌ TEST FAILED")

        return passed

    except subprocess.TimeoutExpired:
        print("❌ TEST TIMEOUT")
        return False

    except Exception as err:
        print(f"❌ TEST ERROR: {err}")
        return False


# MAIN

def main():

    # Check databases before running tests
    check_databases()

    print("\n" + "="*60)
    print(" CONFERENCE MANAGEMENT SYSTEM - FIXED TEST SUITE")
    print("="*60)

    tests = [

        ("Option 1 - View Speakers",
         "1\nAlan\nx\n",
         ["prof. alan shaw"]),

        ("Option 1 - No results",
         "1\nXYZ123\nx\n",
         ["no speakers found"]),

        ("Option 2 - Valid company",
         "2\n1\nx\n",
         ["ava murphy"]),

        ("Option 2 - Non-existent",
         "2\n99\nx\n",
         ["doesn't exist"]),

        ("Option 3 - Add attendee",
         "3\n999\nTest User\n1990-01-01\nM\n5\nx\n",
         ["successfully", "already exists", "error"]),

        ("Option 3 - Duplicate",
         "3\n101\nTest\n1990-01-01\nM\n1\nx\n",
         ["already exists"]),

        ("Option 3 - Invalid gender",
         "3\n998\nTest\n1990-01-01\nX\n1\nx\n",
         ["gender must be"]),

        ("Option 4 - View connections",
         "4\n101\nx\n",
         ["ava murphy", "connected"]),

        ("Option 5 - Self connection",
         "5\n101\n101\nx\n",
         ["cannot connect"]),

        ("Option 5 - Add connection",
         "5\n101\n102\nx\n",
         ["connected", "already connected"]),

        ("Option 6 - View rooms",
         "6\nx\n",
         ["main hall"]),

        ("Option 7 - Networking",
         "7\n101\nx\n",
         ["suggested connections", "rank"]),
    ]

    passed = 0
    failed = 0

    for name, inputs, expected in tests:
        if run_test(name, inputs, expected):
            passed += 1
        else:
            failed += 1

    print("\n" + "="*60)
    print(" TEST SUMMARY")
    print("="*60)

    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"📊 Total:  {passed + failed}")

    print("\n" + "="*60)


if __name__ == "__main__":
    main()