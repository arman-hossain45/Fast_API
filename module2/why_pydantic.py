def insert_student(name:str,math:int,eng:int):
 if type(math) == int and type(eng)==int:
    print("Name : ",name)

    totall = math+ eng

    print('Totall marks :',totall)
 else:
    print('Wrong data type')
    


insert_student('rakin','34','45')
# here we see that here we input the data in a 
# string format thats rong input that user give for that reason we need validation of this data


# but this fpormmula is not well design when our code is so big then it increase error
#so for that reason we need pydantic formula 
# we check many things using pydantic formula 

