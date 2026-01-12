def statuses():
    try:
        x=input()
        if x == '0':
            status= False
            print(status)
        elif x == '1':
            status= True
            print(status)
    except:
            print("Invalid input.")
                    

statuses()