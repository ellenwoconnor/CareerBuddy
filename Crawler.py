
from bs4 import BeautifulSoup
import urllib2
import csv

# import os

class JobCrawler():

    def __init__(self):
        self.link_element = 'app_link'
        self.next_element = 'instl confirm-nav next'
        self.root_url = 'http://www.indeed.com'

    def get_links(self, url):
        """Given some url, gets all of the links to resumes on the page."""

        target_elements = soup.find_all(class_ = self.link_element)
        hrefs = []

        for element in target_elements:
            hrefs.append(self.root_url + link.get('href'))

        return hrefs


    def crawl(self, url, results=[]):
        """Gets all the resume urls recursively from a given starting point"""

        response = urllib2.urlopen(url)
        soup = BeautifulSoup(response, 'html.parser')

        # Get all the links on the page
        results.extend(self.get_links(url))

        # Look for a next button
        next_btn = soup.find(class_ = self.next_element)

        # If there's no next bar, return the results of crawling
        if not next_btn:
            return results

        # Otherwise, recurse to the next link
        next_url = next_btn.get('href')
        return self.crawl(next_url, results)


    def scrape(self, urls):

        resume_id = 0
        resumes = {}

        for url in urls:

            response = urllib2.urlopen(url)
            soup = BeautifulSoup(response)

            work_descriptions = self.get_work_experience(soup)
            education = self.get_education(soup)
            skills = self.get_skills(soup)

            resumes[resume_id] = {'work': work_descriptions, 
                                  'education': education,
                                  'other': skills
                                  }
            resume_id += 1

        return resumes

    def get_work_experience(self, soup):
        """Given soupified html, returns relevant data associated with 
        the work experience."""

        # Get all of the job titles 

        # For each of the listings, save the job title, the job description
        # and the order of elements (chronologically last = 1, etc.)

        # Insert into csv: 
            # anonymous resume ID 
            # title
            # description
            # order within resume 

    def get_education(self, soup):
        """Takes in soupified html and returns the degrees listed on the 
        resume."""

        education_divs = soup.find_all(class_ = 'education-section')
        degrees = []

        if education_divs:
            for degree in education_divs:
                title = degree.find(class_ = 'edu_title').string
                school = degree.find(class_ = 'bold').string
                degrees.append((title, school))

        return degrees

    def get_skills(self, soup):











