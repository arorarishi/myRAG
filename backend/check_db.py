"""
Quick script to check database state
"""
import sys
sys.path.insert(0, 'D:/Work/ML/Projects/myRAG/backend')

from app.database.database import engine
from sqlalchemy import inspect, text

# Check what tables exist
inspector = inspect(engine)
tables = inspector.get_table_names()
print("Tables in database:")
for table in tables:
    print(f"  - {table}")

# Check if documents table exists
if 'documents' in tables:
    print("\n✓ 'documents' table exists")
    
    # Get column info
    columns = inspector.get_columns('documents')
    print("\nColumns:")
    for col in columns:
        print(f"  - {col['name']} ({col['type']})")
    
    # Try to query documents
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT COUNT(*) FROM documents"))
            count = result.scalar()
            print(f"\nDocument count: {count}")
            
            if count > 0:
                result =conn.execute(text("SELECT id, filename, status FROM documents LIMIT 5"))
                print("\nRecent documents:")
                for row in result:
                    print(f"  - ID {row[0]}: {row[1]} ({row[2]})")
    except Exception as e:
        print(f"\n✗ Error querying documents: {e}")
else:
    print("\n✗ 'documents' table does NOT exist!")
    print("This is the problem - the table needs to be created!")
