#!/usr/bin/env python3
"""
Simple test to trace backend errors
"""
import sys
import os
import traceback

# Add the backend directory to Python path
backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_dir)

print("🔍 Testing backend imports...")

try:
    print("1️⃣ Testing core imports...")
    from app.schemas.bazi import BaziCalculateRequest, BaziCalculateResponse
    print("✅ Schemas imported successfully")
    
    print("2️⃣ Testing main module...")
    from app.services.main import calculate_bazi_data
    print("✅ Main module imported successfully")
    
    print("3️⃣ Testing calculation with real data...")
    from datetime import datetime
    
    # Create test request
    test_request = BaziCalculateRequest(
        gender="男",
        birth_datetime=datetime.fromisoformat("1990-04-29T12:00:00+08:00"),
        birth_place="北京"
    )
    
    print("✅ Test request created successfully")
    print(f"Request: {test_request}")
    
    # Try to calculate (this is async, so we need to handle it properly)
    import asyncio
    
    async def test_calc():
        try:
            result = await calculate_bazi_data(test_request, quick_mode=True)
            print("✅ Calculation successful!")
            print(f"Result type: {type(result)}")
            print(f"Basic fields: {list(result.__dict__.keys())}")
            return result
        except Exception as e:
            print(f"❌ Calculation failed: {e}")
            traceback.print_exc()
            return None
    
    # Run the async test
    print("4️⃣ Running async calculation test...")
    result = asyncio.run(test_calc())
    
    if result:
        print("🎉 Test completed successfully!")
    else:
        print("💥 Test failed!")

except Exception as e:
    print(f"❌ Import or setup failed: {e}")
    traceback.print_exc()
