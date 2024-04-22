def change_date(date1):
    year1 = int(date1[:4])
    month1 = int(date1[5:7])
    day1 = int(date1[-2:])
    
    day1 -= 5
    
    if day1 <= 0:
        day1 += 30
        month1 -= 1
        
        if month1 <= 0:
            month1 = 12
            year1 -= 1
        
    if len(str(month1)) == 2 and len(str(day1)) == 2:
        new_date = str(year1) + "." + str(month1) + "." + str(day1)
        
    elif len(str(month1)) == 1 and len(str(day1)) == 1:
        month1 = "0" + str(month1)
        day1 = "0" + str(day1)
        new_date = str(year1) + "." + str(month1) + "." + str(day1)
    
    elif len(str(month1)) == 1:
        month1 = "0" + str(month1)
        new_date = str(year1) + "." + str(month1) + "." + str(day1)
        
    elif len(str(day1)) == 1:
        day1 = "0" + str(day1)
        new_date = str(year1) + "." + str(month1) + "." + str(day1)
    # cnt += 1
    # print(new_date)
    return new_date 

end_date = "2024.04.16"
start_date = "2024.04.12"

for i in range(10):
    print(start_date, end_date)
    start_date = change_date(start_date)
    end_date = change_date(end_date)
    
    