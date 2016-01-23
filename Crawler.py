from bs4 import BeautifulSoup
import urllib2
import csv

class JobCrawler():

    def __init__(self, link_element='app_link', 
                       next_element='instl confirm-nav next',
                       root_url = 'http://www.indeed.com'):
        self.link_element = link_element
        self.next_element = next_element
        self.root_url = root_url


    def get_soup(self, url):
        """Makes a request for a URL and parses the response into soup."""

        request = urllib2.Request(url, headers={'User-Agent':'Mozilla/5.0'})
        response = urllib2.urlopen(request)
        soup = BeautifulSoup(response, 'html.parser')

        return soup


    def get_links(self, soup):
        """Gets all of the links to resumes from some HTML."""

        target_elements = soup.find_all(class_ = self.link_element)
        hrefs = []

        for element in target_elements:
            hrefs.append(self.root_url + link.get('href'))

        return hrefs


    def crawl(self, url, results=[]):
        """Gets all the resume urls recursively from a given starting point
        on the search page."""

        # Parse the html for the URL 
        soup = self.get_soup(url)

        # Get all the links on the page
        results.extend(self.get_links(soup))

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

            soup = self.make_soup(url)

            work_descriptions = self.get_work_experience(soup)
            education = self.get_education(soup)
            skills = self.get_skills(soup)

            resumes[resume_id] = {'work': work_descriptions, 
                                  'education': education,
                                  'other': skills}
            resume_id += 1

        return resumes


    def get_work_experience(self, soup):
        """Given soupified html, returns relevant data associated with 
        the work experience."""

        # Get all of the job titles 

        # For each of the listings, save the job title, the job description
        # and the order of elements (chronologically last = 1, etc.)

        work_divs = soup.find_all(class_ = 'work-experience-section')
        jobs = []
        order = 1

        if work_divs:
            for job in work_divs:
                title = job.find(class_ = 'work_title').get_text()
                company = job.find(class_ = 'bold').get_text()
                text = job.find(class_ = 'work_description').get_text()
                jobs.append((order, title, company, text))
                order += 1

        return jobs


    def get_education(self, soup):
        """Takes in soupified html and returns the degrees listed on the 
        resume."""

        education_divs = soup.find_all(class_ = 'education-section')
        degrees = []

        if education_divs:
            for degree in education_divs:
                title = degree.find(class_ = 'edu_title')
                school = degree.find(class_ = 'bold')
                degrees.append((title, school))

        return degrees


    # def get_skills(self, soup):

    #     skills = soup.find(class_ = 'skill_text').string
    #     other = soup.find(class_ = 'additionalInfo-content')

    #     text = ""

if __name__ == '__main__':

    test = JobCrawler()
    soup = test.get_soup('http://www.indeed.com/r/Anwar-Akbar/347f76578f1dd1b3')
    work_exp = test.get_work_experience(soup)
    print work_exp
    # education = test.get_education(soup)
    # print education



