# lubimy-czytac-scraper
A simple scraper to scrap data about the top 100 most popular books in recent months on the Polish site lubimyczytac.pl. Codes for both Selenium and Scrapy. 

Codes for Scrapy are located in the scrapy_project folder and for Selenium in selenium_scraper.

<br/><br/>

Guide for running Scrapy scraper:

1. To run scrapy scraper you need enter a command line and create a scrapy project with the following command:  
   ```
   scrapy startproject myproject [project_dir]
   ```

   in a directory of your choice.  

2. Then go to the specified directory with a command:  
   ```
   cd project_dir 
   ```

3. Please download the project_scrapy.py file and place it in the folder "spiders" inside the directory from the previous step. There is only a single spider to extract all the information about top 100 books for all the available monhts from the lubimyczytac.pl site. Spiders name is "scrapy_books" 

4. Run the spider with a command   
   ```
   scrapy crawl scrapy_books
   ```

   If you want to store the results in a .csv file you can add -o file_name.csv:   
   ```
   scrapy crawl scrapy_books
   ```

<br/><br/>

A sample output can be found in the books.csv file.
