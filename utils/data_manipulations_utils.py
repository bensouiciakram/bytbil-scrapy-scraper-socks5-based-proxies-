from re import sub,search 


# helper functions : 
def format_number(number:str,key:str,response) -> float: 
    if not number:
        return number 
    else :
        if 'price' in key :
            price = sub('\s+|_','',number.split('kr')[0])
            if not price :
                return price 
            else: 
                return float(price)
        elif key in ('Mileage','engine_size') :
            if number == 'Uppgift saknas':
                return 0
            return float(sub('\s+','',search('\d+\s+\d+|\d+',number)[0]))
        elif key in ('vehicle_year','model_year') :
            return float(number)
        