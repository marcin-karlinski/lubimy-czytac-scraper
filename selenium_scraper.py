from selenium import webdriver
import time
import pandas as pd

#please change the path of the geckodriver
gecko_path = 'C:/Users/marci/Desktop/UW/gekon/geckodriver'

url = 'https://lubimyczytac.pl/top100'

options = webdriver.firefox.options.Options()
options.headless = False

driver = webdriver.Firefox(options = options, executable_path = gecko_path)

driver.get(url)

#Here you can maximize web browser window
#driver.maximize_window()

time.sleep(7)

#closing a window informing about cookies
button = driver.find_element_by_xpath('//button[@id="onetrust-accept-btn-handler"]')
button.click()

#waiting for everything to load
time.sleep(7)

#Creating empty dictionary with data frame result for each month. I will later concatenate all of them into one data frame
lubimy_czytac = {}

#I'm getting list of all available months for which there is a record (April 2021 - May 2020)
months_list = driver.find_elements_by_xpath("//div[contains(@class, 'filtr__itemTitle')]")

#keys, which will be used in a loop and for concatenating data frames
months_keys = [month.text for month in months_list]

#loop over months names. Count is for naming data frames, which are a result of each loop. I have to find the right element in
#every iteration, rather than all at once and then loop over them,
#because they can change after refreshing the page and I will obtain "The element reference of element is stale" error
for count, i in enumerate(months_keys):

    time.sleep(1)
    #choose month from the top left corner
    month_to_click = driver.find_element_by_xpath("//div[contains(text(), '{0}')]".format(i))

    #I use this rather than element.click() to prevent "element is not clickable at point (x,y)" error
    driver.execute_script("arguments[0].click();", month_to_click)
    time.sleep(2)

    #empyt data frame to store results for each month
    results = pd.DataFrame({'position': [], 'title': [], 'author': [], 'rating': [],
                            'readers':[], 'opinions':[], 'no. of ratings': []})

    # Loop over pages. For every month there are around 137 books, however we will only take first 100. There are 20 books a page
    # so we need to scrap first 5 pages for each month
    for i in range(2, 7):

        #getting position of a book in the ranking
        position = driver.find_elements_by_xpath('//span[@class="authorAllBooks__singleImgInfoBottom"]')
        pos_list = []
        for ele in position:
            pos_list.append(ele.text.rsplit(" ", 1)[0])
        pos_list

        #getting its title
        title= driver.find_elements_by_xpath('//a[@class="authorAllBooks__singleTextTitle float-left"]')
        titles_list = []
        for ele in title:
            titles_list.append(ele.text)
        titles_list

        #author
        author = driver.find_elements_by_xpath('//div[@class="authorAllBooks__singleTextAuthor authorAllBooks__singleTextAuthor--bottomMore"]')
        authors_list = []
        for ele in author:
            authors_list.append(ele.text)
        authors_list

        #rating
        rating = driver.find_elements_by_xpath('//span[@class="listLibrary__ratingStarsNumber"]')
        rating_list = []
        for ele in rating:
            rating_ele = ele.text
            rating_list.append(rating_ele.strip('"'))
        rating_list

        #number of readers
        readers = driver.find_elements_by_xpath('//span[@class="small grey mr-2 mb-3"]')
        readers_list = []
        for ele in readers:
            no_of_readers = ele.text
            readers_list.append(no_of_readers.replace('Czytelnicy: ', ''))
        readers_list

        #number of opinions
        opinions = driver.find_elements_by_xpath('//span[@class="ml-2 small grey"]')
        opinions_list = []
        for ele in opinions:
            no_of_opinions = ele.text
            opinions_list.append(no_of_opinions.replace('Opinie: ', ''))
        opinions_list

        #number of ratings
        no_of_ratings = driver.find_elements_by_xpath('//div[@class="listLibrary__ratingAll"]')
        no_of_ratings_list = []
        for ele in no_of_ratings:
            no_of_ratings_str = ele.text
            no_of_ratings_list.append(no_of_ratings_str.replace(' ocen', ''))
        no_of_ratings_list

        #creating a temporary data frame with results from a single page
        temp_df = pd.DataFrame({'position': pos_list, 'title': titles_list,
                                'author': authors_list, 'rating': rating_list, 'readers': readers_list,
                                'opinions': opinions_list, 'no. of ratings': no_of_ratings_list})

        #appending results from a page to results from current month
        results = pd.concat([results, temp_df])

        #click on the next page. If we are already at 5th page, then don't
        if i != 6:
            page = driver.find_element_by_xpath("//a[@href = '/top100/" + str(i) + "']")
            driver.execute_script("arguments[0].click();", page)
            time.sleep(2)

    #add data frame with results of the current month to the dictionary
    lubimy_czytac["df{0}".format(count)] = results

#concatenating data frames from all the months to a single df based on keys
top100 = pd.concat([lubimy_czytac["df1"], lubimy_czytac["df2"], lubimy_czytac["df3"], lubimy_czytac["df4"],
                    lubimy_czytac["df5"], lubimy_czytac["df6"], lubimy_czytac["df7"], lubimy_czytac["df8"],
                    lubimy_czytac["df9"], lubimy_czytac["df10"], lubimy_czytac["df11"]], axis=1, keys=months_keys)

#uncomment if you want to save results to a .csv file
#top100.to_csv("C:/Users/marci/Desktop/UW/webscraping/lubimyCzytac_scrap.csv", encoding = "utf-8-sig")

# Close browser:
driver.quit()
