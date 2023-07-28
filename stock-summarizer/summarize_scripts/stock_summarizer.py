import csv
import retrieve_stock_data as rsd

# returns true if str1 has a date occuring earlier than str2 and false otherwise
def date_order(str1, str2):
    if int(str1[:4]) < int(str2[:4]):
        return True
    elif int(str1[:4]) > int(str2[:4]):
        return False
    else:
        if int(str1[5:7]) < int(str2[5:7]):
            return True
        elif int(str1[5:7]) > int(str2[5:7]):
            return False
        else:
            if int(str1[8:10]) < int(str2[8:10]):
                return True
            elif int(str1[8:10]) > int(str2[8:10]):
                return False

def stock_analysis2(name):
    reader = rsd.stock_data(name)
    
    gains = [["AVG AT MIN", "MIN DATE", "MIN", "AVG AT MAX", "MAX DATE", "MAX", "CHANGE"]]
    drops = [["AVG AT MAX", "MAX DATE", "MAX", "AVG AT MIN", "MIN DATE", "MIN", "CHANGE"]]
        
    row_counter = 0
    
    max_price = 0
    max_date = ""
    avg_at_max = 0
    
    min_price = 100000
    min_date = ""
    avg_at_min = 0
    
    price_sum = 0
    avg_price = 0
    
    prev_price = 0
    
    day_average = 300
    
    prices = []
    
    for row in reader:
        if row["Adj Close"] != "null":
            curr_price = float(row["Adj Close"])
            
            if row_counter <= day_average - 1:
                price_sum += float(row["Adj Close"])
                prices.append(float(row["Adj Close"]))
            else:
                avg_price = price_sum/day_average
                
                price_sum -= prices.pop(0)
                price_sum += curr_price
                prices.append(curr_price)
                
                # looking for peak
                if curr_price > avg_price:
                    if prev_price < avg_price and min_price < 100000 and max_price > 0:
                        change = 0
                        if date_order(min_date, max_date): # gain
                            change = (max_price - min_price)
                            change /= min_price 
                            change *= 100
                        else: # loss
                            change = (min_price - max_price)
                            change /= max_price
                            change *= 100
                        
                        if change >= 20:
                            gains.append([str(avg_at_min)[:6], min_date, str(min_price)[:6], str(avg_at_max)[:6], max_date, str(max_price)[:6], str(change)[:8]])
                            # print("AVG AT MIN: {}, MIN DATE: {}, MIN: {}, AVG AT MAX: {}, MAX DATE: {}, MAX: {} CHANGE: {}".format(avg_at_min, min_date, min_price, avg_at_max, max_date, max_price, change))
                        elif change < -20:
                            drops.append([str(avg_at_max)[:6], max_date, str(max_price)[:6], str(avg_at_min)[:6], min_date, str(min_price)[:6], str(change)[:8]])
                            # print("AVG AT MAX: {}, MAX DATE: {}, MAX: {}, AVG AT MIN: {}, MIN DATE: {}, MIN: {}, CHANGE: {}".format(avg_at_max, max_date, max_price, avg_at_min, min_date, min_price, change))
                        
                        if date_order(min_date, max_date):
                            min_price = 100000
                            min_date = ""
                        else:
                            max_price = 0
                            max_date = ""
                            
                    if curr_price > max_price:
                        max_price = curr_price
                        max_date = row["Date"]
                        avg_at_max = avg_price
                            
                elif curr_price < avg_price:
                    if prev_price > avg_price and min_price < 100000 and max_price > 0:
                        change = 0
                        if date_order(min_date, max_date): # gain
                            change = (max_price - min_price)
                            change /= min_price 
                            change *= 100
                        else: # loss
                            change = (min_price - max_price)
                            change /= max_price
                            change *= 100
                            
                        if change >= 20:
                            gains.append([str(avg_at_min)[:6], min_date, str(min_price)[:6], str(avg_at_max)[:6], max_date, str(max_price)[:6], str(change)[:8]])
                            # print("AVG AT MIN: {}, MIN DATE: {}, MIN: {}, AVG AT MAX: {}, MAX DATE: {}, MAX: {} CHANGE: {}".format(avg_at_min, min_date, min_price, avg_at_max, max_date, max_price, change))
                        elif change < -20:
                            drops.append([str(avg_at_max)[:6], max_date, str(max_price)[:6], str(avg_at_min)[:6], min_date, str(min_price)[:6], str(change)[:8]])
                            # print("AVG AT MAX: {}, MAX DATE: {}, MAX: {}, AVG AT MIN: {}, MIN DATE: {}, MIN: {}, CHANGE: {}".format(avg_at_max, max_date, max_price, avg_at_min, min_date, min_price, change))
                        
                        if date_order(min_date, max_date):
                            min_price = 100000
                            min_date = ""
                        else:
                            max_price = 0
                            max_date = ""
                        
                    if curr_price < min_price:
                        min_price = curr_price
                        min_date = row["Date"]
                        avg_at_min = avg_price
                
            prev_price = curr_price
                
            row_counter += 1
    
    return gains, drops

def stock_analysis(name):
    # reader = rsd.stock_data(name)
    
    gains = [["AVG AT MIN", "MIN DATE", "MIN", "AVG AT MAX", "MAX DATE", "MAX", "CHANGE"]]
    drops = [["AVG AT MAX", "MAX DATE", "MAX", "AVG AT MIN", "MIN DATE", "MIN", "CHANGE"]]
        
    row_counter = 0
    
    max_price = 0
    max_date = ""
    avg_at_max = 0
    
    min_price = 100000
    min_date = ""
    avg_at_min = 0
    
    price_sum = 0
    avg_price = 0
    
    prev_price = 0
    
    day_average = 300
    
    prices = []
    
    date_active = False
    
    with open("summarize_scripts/BNS.TO.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["Close"] != "null":
                curr_price = float(row["Close"])
                if row_counter <= day_average - 1:
                    price_sum += float(row["Close"])
                    prices.append(float(row["Close"]))
                else:
                    avg_price = price_sum/day_average
                    
                    price_sum -= prices.pop(0)
                    price_sum += curr_price
                    prices.append(curr_price)
                    
                    if row["Date"] == '1999-01-04':
                        date_active = True
                    
                    if row["Date"] == '2000-03-09':
                        date_active = False
                    
                    if date_active:
                        print("date {}, curr price {}, max {}, date {}, min {}, date {}, avg {}".format(row["Date"], curr_price, max_price, max_date, min_price, min_date, avg_price))
                    
                    # looking for peak
                    if curr_price > avg_price:
                        if prev_price < avg_price and min_price < 100000 and max_price > 0:
                            change = 0
                            if date_order(min_date, max_date): # gain
                                change = max_price - min_price
                                change /= min_price 
                                change *= 100
                            else: # loss
                                change = min_price - max_price
                                change /= max_price
                                change *= 100
                            
                            if change >= 10:
                                gains.append([str(avg_at_min)[:6], min_date, str(min_price)[:6], str(avg_at_max)[:6], max_date, str(max_price)[:6], str(change)[:8]])
                                # print("AVG AT MIN: {}, MIN DATE: {}, MIN: {}, AVG AT MAX: {}, MAX DATE: {}, MAX: {} CHANGE: {}".format(avg_at_min, min_date, min_price, avg_at_max, max_date, max_price, change))
                            elif change < -10:
                                drops.append([str(avg_at_max)[:6], max_date, str(max_price)[:6], str(avg_at_min)[:6], min_date, str(min_price)[:6], str(change)[:8]])
                                # print("AVG AT MAX: {}, MAX DATE: {}, MAX: {}, AVG AT MIN: {}, MIN DATE: {}, MIN: {}, CHANGE: {}".format(avg_at_max, max_date, max_price, avg_at_min, min_date, min_price, change))
                            
                            if date_order(min_date, max_date):
                                min_price = 100000
                                min_date = ""
                                avg_at_min = 0
                            else:
                                max_price = 0
                                max_date = ""
                                avg_at_max = 0
                                
                        if curr_price > max_price:
                            max_price = curr_price
                            max_date = row["Date"]
                            avg_at_max = avg_price
                                
                    elif curr_price < avg_price:
                        if prev_price > avg_price and min_price < 100000 and max_price > 0:
                            change = 0
                            if date_order(min_date, max_date): # gain
                                change = (max_price - min_price)
                                change /= min_price 
                                change *= 100
                            else: # loss
                                change = (min_price - max_price)
                                change /= max_price
                                change *= 100
                                
                            if change >= 10:
                                gains.append([str(avg_at_min)[:6], min_date, str(min_price)[:6], str(avg_at_max)[:6], max_date, str(max_price)[:6], str(change)[:8]])
                                # print("AVG AT MIN: {}, MIN DATE: {}, MIN: {}, AVG AT MAX: {}, MAX DATE: {}, MAX: {} CHANGE: {}".format(avg_at_min, min_date, min_price, avg_at_max, max_date, max_price, change))
                            elif change < -10:
                                drops.append([str(avg_at_max)[:6], max_date, str(max_price)[:6], str(avg_at_min)[:6], min_date, str(min_price)[:6], str(change)[:8]])
                                # print("AVG AT MAX: {}, MAX DATE: {}, MAX: {}, AVG AT MIN: {}, MIN DATE: {}, MIN: {}, CHANGE: {}".format(avg_at_max, max_date, max_price, avg_at_min, min_date, min_price, change))
                            
                            if date_order(min_date, max_date):
                                min_price = 100000
                                min_date = ""
                            else:
                                max_price = 0
                                max_date = ""
                            
                        if curr_price < min_price:
                            min_price = curr_price
                            min_date = row["Date"]
                            avg_at_min = avg_price
                    
                prev_price = curr_price
                    
                row_counter += 1
        
        if min_price < 100000 and max_price > 0:
            change = 0
            if date_order(min_date, max_date): # gain
                change = max_price - min_price
                change /= min_price 
                change *= 100
            else: # loss
                change = min_price - max_price
                change /= max_price
                change *= 100
            
            if change >= 10:
                gains.append([str(avg_at_min)[:6], min_date, str(min_price)[:6], str(avg_at_max)[:6], max_date, str(max_price)[:6], str(change)[:8]])
            elif change < -10:
                drops.append([str(avg_at_max)[:6], max_date, str(max_price)[:6], str(avg_at_min)[:6], min_date, str(min_price)[:6], str(change)[:8]])
                            
    return gains, drops