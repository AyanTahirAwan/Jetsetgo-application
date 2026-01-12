from CRUD_dic import crud
from create_func import create, read, update, delete
import mysql.connector
from mysql.connector import Error

def main():
    
    while True:
        for i, table_name in enumerate(crud.keys(), start =1):
            print(f"{i}.{table_name}")
    
        table_choice= input("Select table number or q to  quit:")
        if table_choice == 'q':
            break

        try:
            table_name= list(crud.keys())[int(table_choice)-1]
        except(ValueError,IndexError):
            print(f"Invalid Choice. {Error.msg}")
            continue
    
        print("\nCRUD Operations:")
        print("1. Create")
        print("2. Read")
        print("3. Update")
        print("4. Delete")

        op_choice= input("Select Operation:")

        if op_choice == '1':
            data={}
            for field in crud[table_name]["fields"]:
                if field != crud[table_name]["primary_key"]:
                    data[field]= input(f"Enter value for {field}:")
            create(table_name,data)
        
        elif op_choice == '2':

            read(table_name)
        
        elif op_choice == '3':

            pk = crud[table_name]["primary_key"]
            pk_value = input(f"Enter {pk} of record you want to update: ")
            updated_data={}
            
            for field in crud[table_name]["fields"]:
                if field != pk:
                    temp = input(f"Enter new value for {field}: ")
                    if temp is not None:
                        updated_data[field] = temp
            update(table_name,pk_value,updated_data)

        elif op_choice == '4':

            pk= crud[table_name]["primary_key"]
            pk_value= input("Enter {pk} of record you want to delete : ")
            delete(table_name, pk_value)

        else:
            print("Invalid operation.")


if __name__ == "__main__":
    main()





















