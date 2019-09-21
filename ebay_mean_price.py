# -*- coding: utf-8 -*-
"""
Created on Sat Apr  6  2019  by  http://bit.ly/GerhGithub

@author: GerH
"""

from selenium import webdriver
from time import sleep
import matplotlib.pyplot as plt 

#Change these values accordingly
searchTerms = ["iphone 8",
               "iphone 7",
               "iphone 6",
               "iphone 5",
               "iphone 4",
               "iphone 3",
               "iphone 2"]
pageAmounts = 20 # usually 50 entries per page
currencySign = "$"
wait = .5
#Limits (exclusive)
minPrice = 0.0
maxPrice = 10000.0

#Round a float number up
def roundUp(number):
    return int(( number * 100 ) + 0.5) / float(100)

#Calculate mean value
def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)

#Summary of all search terms
meansArray = []
sumArray = []
arrayNum = []
num = 1

#Go to Ebay
driver = webdriver.Firefox()
driver.get("https://www.ebay.com/")

#Click cookie warning away
sleep(10*wait)
driver.find_element_by_id("gdpr-banner-accept").click()
sleep(wait)

#Perform searches for all search terms
for searchTerm in searchTerms:
    
    #Fill out and click search form
    search_input = driver.find_element_by_class_name("gh-tb.ui-autocomplete-input")
    search_input.clear()
    search_input.send_keys(searchTerm)
    driver.find_element_by_class_name("btn.btn-prim.gh-spr").click()
    sleep(wait)
    
    if(pageAmounts<1):
        print("pageAmounts should be at least 1!")
        break
    
    sumPrices = 0.0
    prices = []
    entries = []
    entryNo = 1
    
    excludedPrices = 0
    
    currURL = ""
    prevURL = ""
    #start search
    for i in range(pageAmounts):
        currURL = driver.current_url.replace("#","")
        
        listingElems = driver.find_elements_by_class_name("s-item")
        #print("Amount: " + str(len(listingElems)))
        sleep(wait)
        
        for a in range(len(listingElems)):
            #find price, ignore sponsored listing
            try:
                titleElem = listingElems[a].find_element_by_xpath(".//h3[@class='s-item__title']").text
                priceText = listingElems[a].find_element_by_xpath(".//span[@class='s-item__price']").text
                if(priceText.startswith(currencySign) == True):
                    price = float(priceText.replace("to","").split(currencySign)[1])
                    if(minPrice < price and price < maxPrice):
                        sumPrices += price
                        prices.append(price)
                        entries.append(entryNo)
                        entryNo+=1
                    else:
                        excludedPrices+=1
            except:
                pass #print("Sponsored listing detected")
                
        #Go to next page
        try:
            if(currURL != prevURL):
                prevURL = currURL.replace("#","")
                driver.find_elements_by_class_name("x-pagination__control")[1].click()
            else:
                break
        except:
            print("No next page found!")
        sleep(wait)
        
    #Prepare results
    meanPrice = roundUp(mean(prices))
    sumPrices = roundUp(sumPrices)
    amountStr = str(len(prices))
    
    #Update summary arrays
    meansArray.append(meanPrice)
    sumArray.append(sumPrices)
    arrayNum.append(num)
    num+=1
    
    #Output results
    print("\n\nProduct: " + searchTerm)
    print("Amount:    " + amountStr)
    print("Sum:       " + currencySign + str(sumPrices))
    print("Mean:      " + currencySign + str(meanPrice))
    print("Excluded : " + str(excludedPrices))
    
    #Draw a plot
    x = entries
    y = prices
    plt.plot(x, y) 
    plt.xlabel('entry number') 
    plt.ylabel('price (in ' + currencySign + ', on ebay.com)') 
    plt.title(searchTerm) 
    plt.show() 
driver.close()

#Show info about different means values in a bar chart
left = arrayNum
height = meansArray
tick_label = searchTerms
plt.bar(left, height, tick_label = tick_label, 
        width = 0.8, color = ['red', 'blue']) 
plt.xlabel('products') 
plt.ylabel('mean price') 
plt.title('Overview (source: ebay.com)') 
plt.xticks(rotation='vertical')
plt.show() 

#amounts in a pie chart
activities = searchTerms
slices = sumArray
colors = ['r', 'y', 'g', 'b', 'yellowgreen', 'gold', 'lightskyblue', 'lightcoral'] 
plt.pie(slices, labels = activities, colors=colors,  
        startangle=90, shadow = True, 
        radius = 1.2, autopct = '%1.1f%%') 
plt.title('Sum of Prices (source: ebay.com)') 
#plt.legend() 
plt.show() 
