
# year=int(input("Enter a 4 digit year "))
# if year%4 ==0 and (year%100!=0)or year%400 == 0:
#     print("The year is leap year ")
    
# else:
#     print("The year is not a leap year")



pattern_height=5
for i in range(1,pattern_height+1):
    for i in range(pattern_height-1,i-1,-1):
        print(" ",end="")
        
    for j in range(1,i+1):
        print("*",end="")
        
    print()