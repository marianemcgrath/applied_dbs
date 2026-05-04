#!/usr/bin/env python3
"""
Quick test script for Conference Management System
Run this to verify all functionality before submission
"""

import subprocess
import sys

def run_test(test_name, inputs, expected_strings):
    """Run a single test and report result"""
    print(f"\n{'='*60}")
    print(f"TEST: {test_name}")
    print(f"{'='*60}")
    
    try:
        # Run main.py with inputs
        result = subprocess.run(
            [sys.executable, "main.py"],
            input=inputs,
            text=True,
            capture_output=True,
            timeout=10
        )
        
        output = result.stdout
        
        # Check for expected strings
        all_found = True
        for expected in expected_strings:
            if expected in output:
                print(f"✅ Found: {expected}")
            else:
                print(f"❌ MISSING: {expected}")
                all_found = False
        
        if all_found:
            print(f"\n✅ TEST PASSED")
        else:
            print(f"\n❌ TEST FAILED")
            
        return all_found
        
    except subprocess.TimeoutExpired:
        print("❌ TEST TIMEOUT - application hung")
        return False
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False


def main():
    print("\n" + "="*60)
    print(" CONFERENCE MANAGEMENT SYSTEM - TEST SUITE")
    print("="*60)
    
    tests = [
        # Test 1: View Speakers
        (
            "Option 1 - View Speakers (partial search)",
            "1\nAlan\nx\n",
            ["Session Details For : Alan", "Prof. Alan Shaw", "Scaling Neo4j", "Graph Modelling"]
        ),
        
        # Test 2: View Speakers (no results)
        (
            "Option 1 - No results",
            "1\nXYZ123\nx\n",
            ["No speakers found"]
        ),
        
        # Test 3: View Attendees by Company (valid)
        (
            "Option 2 - Valid company",
            "2\n1\nx\n",
            ["DataNova Attendees", "Ava Murphy", "Ella Finn"]
        ),
        
        # Test 4: View Attendees by Company (non-existent)
        (
            "Option 2 - Non-existent company",
            "2\n99\nx\n",
            ["Company with ID 99 doesn't exist"]
        ),
        
        # Test 5: Add New Attendee (valid)
        (
            "Option 3 - Add valid attendee",
            "3\n999\nTest User\n1990-01-01\nM\n5\nx\n",
            ["Attendee successfully added"]
        ),
        
        # Test 6: Add New Attendee (duplicate ID)
        (
            "Option 3 - Duplicate ID",
            "3\n101\nTest\n1990-01-01\nM\n1\nx\n",
            ["already exists"]
        ),
        
        # Test 7: Add New Attendee (invalid gender)
        (
            "Option 3 - Invalid gender",
            "3\n998\nTest\n1990-01-01\nX\n1\nx\n",
            ["Gender must be M/F"]
        ),
        
        # Test 8: View Connected Attendees (has connections)
        (
            "Option 4 - Attendee with connections",
            "4\n101\nx\n",
            ["Ava Murphy", "107", "109", "111"]
        ),
        
        # Test 9: View Connected Attendees (no connections in Neo4j)
        (
            "Option 4 - MySQL only (no Neo4j node)",
            "4\n112\nx\n",
            ["Daniel Quinn", "No connections"]
        ),
        
        # Test 10: Add Attendee Connection (valid)
        (
            "Option 5 - Add new connection",
            "5\n101\n102\nx\n",
            ["now connected"]
        ),
        
        # Test 11: Add Attendee Connection (self-connection)
        (
            "Option 5 - Self connection",
            "5\n101\n101\nx\n",
            ["cannot connect to him/herself"]
        ),
        
        # Test 12: View Rooms
        (
            "Option 6 - View rooms",
            "6\nx\n",
            ["Main Hall", "Graph Lab", "Cloud Suite"]
        ),
        
        # Test 13: Innovation - Recommendations
        (
            "Option 7 - Networking suggestions",
            "7\n101\nx\n",
            ["Suggested connections", "Key Connectors", "mutual connections"]
        ),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, inputs, expected in tests:
        if run_test(test_name, inputs, expected):
            passed += 1
        else:
            failed += 1
    
    print("\n" + "="*60)
    print(" TEST SUMMARY")
    print("="*60)
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"📊 Total:  {passed + failed}")
    
    if failed == 0:
        print("\n🎉 ALL TESTS PASSED! Ready for submission!")
    else:
        print(f"\n⚠️  {failed} test(s) failed. Please fix before submitting.")
    
    print("\n" + "="*60)


if __name__ == "__main__":
    main()