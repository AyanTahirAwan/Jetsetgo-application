from CRUD_dic import crud
from database import db, cursor

def fetch_records(table_name):
    cursor.execute(f"SELECT FROM {table_name}")
    rows= cursor.fetchall()
    return rows

def print_records(table_name):
    rows= fetch_records(table_name)
    if not rows:
        print("No records found. ")
        return
    print("\n --- Records in ", table_name, "---")

    col_names=[desc[0] for desc in cursor.description]
    print("\t".join(col_names))
    for row in rows:
        print("\t".join(str(val) if val is not None else "" for val in row))
        

def create(table_name, data):
    pk= crud[table_name]["primary_key"][0]
    
    # insert_data = ", ".join(value for value in data.values())
    placeholders=", ".join(["%s"] * len(data))
    insert_fields=", ".join(field for field in data) 
    query=f"INSERT INTO {table_name} ({insert_fields}) VALUES ({placeholders})"
    print(query)
    cursor.execute(query, tuple(value for value in data.values()))
    db.commit()
    print("Record created.")

def read(table_name):
    cursor.execute(f"SELECT * FROM {table_name}")
    for row in cursor.fetchall():
        print(row)

def update(table_name, pk_value, updated_data):
    
    pk = crud[table_name]["primary_key"]
    fields= [field for field in crud[table_name]["fields"] if field != pk]
    set_clause= ", ".join(f"{field}=%s" for field in fields)
    query= f"UPDATE {table_name} SET {set_clause} WHERE {pk}=%s"
    print(f"table:{table_name}, PK: {pk}")
    print(query)
    cursor.execute(query, tuple(updated_data[field] for field in fields) + (pk_value,))
    db.commit()
    print("Record Updated.")


def delete(table_name,pk_value):
    pk=crud[table_name]["primary_key"]
    query=f"DELETE FROM {table_name} WHERE {pk}=%s"
    cursor.execute(query,(pk_value,))
    db.commit()
    print("Record Deleted.")
    