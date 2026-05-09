#!/usr/bin/env python3
# Conference Management System - Test Suite
# Runs automated integration tests against main.py

import subprocess
import sys


def run_test(test_name, inputs, expected_strings):

    print(f"\n{'=' * 60}")
    print(f"TEST: {test_name}")
    print(f"{'=' * 60}")

    try:
        result = subprocess.run(
            [sys.executable, "main.py"],
            input=inputs,
            text=True,
            capture_output=True,
            timeout=15
        )

        output = result.stdout.lower()
        errors = result.stderr.lower()

        print("\n--- OUTPUT (last 800 chars) ---")
        print(output[-800:])
        print("--- END OUTPUT ---\n")

        print("\n--- STDERR ---")
        print(errors[-800:])
        print("--- END STDERR ---\n")

        # Require ALL expected strings to exist
        passed = all(
            expected.lower() in output
            for expected in expected_strings
        )

        if passed:
            for expected in expected_strings:
                print(f"✅ Found: {expected}")

            print("\n✅ TEST PASSED")

        else:
            print("\n❌ TEST FAILED")
            print("Missing expected output(s):")

            for expected in expected_strings:
                if expected.lower() not in output:
                    print(f"   - {expected}")

        return passed

    except subprocess.TimeoutExpired:
        print("❌ TEST TIMEOUT")
        return False

    except Exception as err:
        print(f"❌ TEST ERROR: {err}")
        return False


def main():

    print("\n" + "=" * 60)
    print(" CONFERENCE MANAGEMENT SYSTEM - TEST SUITE")
    print("=" * 60)

    tests = [

        
        # OPTION 1
        
        (
            "Option 1 - View Speakers",
            "1\nAlan\nx\n",
            ["prof. alan shaw"]
        ),

        (
            "Option 1 - No results",
            "1\nXYZ123\nx\n",
            ["no speakers match search string"]
        ),

        # OPTION 2
        
        (
            "Option 2 - Valid company",
            "2\n1\nx\n",
            ["ava murphy"]
        ),

        (
            "Option 2 - Non-existent company",
            "2\n99\nx\n",
            ["doesn't exist"]
        ),

        # OPTION 3

        (
            "Option 3 - Add attendee",
            "3\n999\nTest User\n1990-01-01\nM\n5\nx\n",
            ["already exists"]
        ),

        (
            "Option 3 - Duplicate attendee",
            "3\n101\nTest\n1990-01-01\nM\n1\nx\n",
            ["already exists"]
        ),

        (
            "Option 3 - Invalid gender",
            "3\n998\nTest\n1990-01-01\nX\n1\nx\n",
            ["gender must be"]
        ),

        # OPTION 4

        (
            "Option 4 - View connections",
            "4\n101\nx\n",
            ["ava murphy"]
        ),

        # OPTION 5

        (
            "Option 5 - Self connection",
            "5\n101\n101\nx\n",
            ["cannot connect"]
        ),

        (
            "Option 5 - Add connection",
            "5\n101\n102\nx\n",
            ["connected"]
        ),

        # OPTION 6

        (
            "Option 6 - View rooms",
            "6\nx\n",
            ["main hall"]
        ),

        # OPTION 7
        
        (
            "Option 7 - Networking insights",
            "7\n101\nx\n",
            ["suggested connections"]
        ),
    ]

    passed = 0
    failed = 0

    for name, inputs, expected in tests:

        if run_test(name, inputs, expected):
            passed += 1
        else:
            failed += 1

    print("\n" + "=" * 60)
    print(" TEST SUMMARY")
    print("=" * 60)

    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"📊 Total:  {passed + failed}")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()