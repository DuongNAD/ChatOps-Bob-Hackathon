"""
Script to export OpenAPI schema from FastAPI application
Usage: python export_openapi.py
"""
import json
from pathlib import Path
from main import app


def export_openapi_schema():
    """
    Export OpenAPI schema from FastAPI app to openapi.json file
    """
    print("=" * 60)
    print("  Exporting OpenAPI Schema")
    print("=" * 60)
    print()
    
    # Get OpenAPI schema from FastAPI app
    print("Generating OpenAPI schema from FastAPI app...")
    openapi_schema = app.openapi()
    
    # Define output file path
    output_file = Path(__file__).parent / "openapi.json"
    
    # Write schema to JSON file with pretty formatting
    print(f"Writing schema to: {output_file}")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(openapi_schema, f, indent=2, ensure_ascii=False)
    
    # Print summary
    print()
    print("=" * 60)
    print("  Export Complete!")
    print("=" * 60)
    print()
    print(f"File: {output_file}")
    print(f"Size: {output_file.stat().st_size:,} bytes")
    print()
    
    # Print schema info
    print("Schema Information:")
    print(f"   - Title: {openapi_schema.get('info', {}).get('title', 'N/A')}")
    print(f"   - Version: {openapi_schema.get('info', {}).get('version', 'N/A')}")
    print(f"   - OpenAPI Version: {openapi_schema.get('openapi', 'N/A')}")
    
    # Count endpoints
    paths = openapi_schema.get('paths', {})
    endpoint_count = sum(len(methods) for methods in paths.values())
    print(f"   - Total Endpoints: {endpoint_count}")
    print(f"   - Total Paths: {len(paths)}")
    
    # List all endpoints
    if paths:
        print()
        print("Available Endpoints:")
        for path, methods in paths.items():
            for method, details in methods.items():
                summary = details.get('summary', 'No summary')
                print(f"   - {method.upper():6} {path:30} - {summary}")
    
    print()
    print("You can now use openapi.json for:")
    print("   - API documentation")
    print("   - Client code generation")
    print("   - API testing tools")
    print("   - Integration with other services")
    print()


if __name__ == "__main__":
    try:
        export_openapi_schema()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        exit(1)

# Made with Bob
