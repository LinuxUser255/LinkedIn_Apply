"""
Utilities
"""
import math, constants, config
from typing import List
import time
import os


def get_url_data_file() -> List[str]:
    url_data: List[str] = []
    try:
        with open('data/urlData.txt', 'r', encoding='utf-8') as file:
            url_data = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        text = ("FileNotFound: data/urlData.txt file is not found. Please ensure ./data folder exists and check "
                "config.py values. Then run the bot again")
        print(text)
    return url_data

def jobs_to_pages(num_of_jobs: str) -> int:
    """
    Convert a LinkedIn job count string to number of pages.
    Handles formats like:
    - "1,234 results"
    - "100+ results"
    - "100+"
    - "25"
    Returns 0 when no numeric value is found.
    Caps pages at 40.
    """
    import re

    text = (num_of_jobs or '').strip()
    if not text:
        return 0

    m = re.search(r'(\d[\d,]*)', text)
    if not m:
        return 0

    try:
        total_jobs_int = int(m.group(1).replace(',', ''))
    except Exception:
        return 0

    number_of_pages = max(1, math.ceil(total_jobs_int / constants.jobsPerPage))
    if number_of_pages > 40:
        number_of_pages = 40

    return number_of_pages

def url_to_keywords(url: str) -> List[str]:
    keyword_url = url[url.index("keywords=") + 9:]
    keyword = keyword_url[0:keyword_url.index("&")]
    location_url = url[url.index("location=") + 9:]
    location = location_url[0:location_url.index("&")]
    return [keyword, location]


def write_results(text: str) -> None:
    os.makedirs('data', exist_ok=True)
    time_str = time.strftime("%Y%m%d")
    file_name = "Applied Jobs DATA - " + time_str + ".txt"
    try:
        with open(os.path.join("data", file_name), 'r', encoding="utf-8") as file:
            lines = []
            for line in file:
                if "----" not in line:
                    lines.append(line)

        with open(os.path.join("data", file_name), 'w', encoding="utf-8") as f:
            f.write("---- Applied Jobs Data ---- created at: " + time_str + "\n")
            f.write(
                "---- Number | Job Title | Company | Location | Work Place | Posted Date | Applications | Result " + "\n")
            for line in lines:
                f.write(line)
            f.write(text + "\n")

    except FileNotFoundError:
        with open(os.path.join("data", file_name), 'w', encoding="utf-8") as f:
            f.write("---- Applied Jobs Data ---- created at: " + time_str + "\n")
            f.write(
                "---- Number | Job Title | Company | Location | Work Place | Posted Date | Applications | Result " + "\n")
            f.write(text + "\n")


def print_info_mes(bot: str) -> None:
    print("ℹ️ " + bot + " is starting soon... ")


def log_failed_job(link: str, reason: str = "") -> None:
    os.makedirs('data', exist_ok=True)
    path = os.path.join('data', 'failed_jobs.txt')
    with open(path, 'a', encoding='utf-8') as f:
        line = f"{link}"
        if reason:
            line += f" | {reason}"
        f.write(line + "\n")


def append_url_for_manual_apply(link: str) -> None:
    """Append a job URL to data/urlData.txt for manual follow-up if Easy Apply is unavailable."""
    try:
        os.makedirs('data', exist_ok=True)
        with open(os.path.join('data', 'urlData.txt'), 'a', encoding='utf-8') as f:
            f.write(link + "\n")
    except Exception:
        pass


def check_job_location(job: str) -> str:
    job_loc = "&location=" + job
    if job.casefold() == "asia":
        job_loc += "&geoId=102393603"
    elif job.casefold() == "europe":
        job_loc += "&geoId=100506914"
    elif job.casefold() == "northamerica":
        job_loc += "&geoId=102221843"
    elif job.casefold() == "southamerica":
        job_loc += "&geoId=104514572"
    elif job.casefold() == "australia":
        job_loc += "&geoId=101452733"
    elif job.casefold() == "africa":
        job_loc += "&geoId=103537801"

    return job_loc

class LinkedinUrlGenerate:
    def generate_url_links(self) -> List[str]:
        path = []
        for location in config.location:
            for keyword in config.keywords:
                url = constants.linkJobUrl + "?f_AL=true&keywords=" + keyword + self.job_type() + self.remote() + check_job_location(
                    location) + self.job_exp() + self.date_posted() + self.salary() + self.sort_by()
                path.append(url)
        return path

    @staticmethod
    def job_exp() -> str:
        job_exp_array = config.experienceLevels
        first_job_exp = job_exp_array[0]
        job_exp = ""

        if first_job_exp == "Internship":
            job_exp = "&f_E=1"
        elif first_job_exp == "Entry level":
            job_exp = "&f_E=2"
        elif first_job_exp == "Associate":
            job_exp = "&f_E=3"
        elif first_job_exp == "Mid-Senior level":
            job_exp = "&f_E=4"
        elif first_job_exp == "Director":
            job_exp = "&f_E=5"
        elif first_job_exp == "Executive":
            job_exp = "&f_E=6"

        for index in range(1, len(job_exp_array)):
            if job_exp_array[index] == "Internship":
                job_exp += "%2C1"
            elif job_exp_array[index] == "Entry level":
                job_exp += "%2C2"
            elif job_exp_array[index] == "Associate":
                job_exp += "%2C3"
            elif job_exp_array[index] == "Mid-Senior level":
                job_exp += "%2C4"
            elif job_exp_array[index] == "Director":
                job_exp += "%2C5"
            elif job_exp_array[index] == "Executive":
                job_exp += "%2C6"

        return job_exp

    @staticmethod
    def date_posted() -> str:
        date_posted = ""
        if config.datePosted[0] == "Any Time":
            date_posted = ""
        elif config.datePosted[0] == "Past Month":
            date_posted = "&f_TPR=r2592000&"
        elif config.datePosted[0] == "Past Week":
            date_posted = "&f_TPR=r604800&"
        elif config.datePosted[0] == "Past 24 hours":
            date_posted = "&f_TPR=r86400&"
        return date_posted

    @staticmethod
    def job_type() -> str:
        """job_type_array = config.job_type"""
        job_type_array = config.jobType
        firstjob_type = job_type_array[0]
        job_type = ""
        if firstjob_type == "Full-time":
            job_type = "&f_JT=F"
        elif firstjob_type == "Part-time":
            job_type = "&f_JT=P"
        elif firstjob_type == "Contract":
            job_type = "&f_JT=C"
        elif firstjob_type == "Temporary":
            job_type = "&f_JT=T"
        elif firstjob_type == "Volunteer":
            job_type = "&f_JT=V"
        elif firstjob_type == "Intership":
            job_type = "&f_JT=I"
        elif firstjob_type == "Other":
            job_type = "&f_JT=O"

        for index in range(1, len(job_type_array)):
            if job_type_array[index] == "Full-time":
                job_type += "%2CF"
            elif job_type_array[index] == "Part-time":
                job_type += "%2CP"
            elif job_type_array[index] == "Contract":
                job_type += "%2CC"
            elif job_type_array[index] == "Temporary":
                job_type += "%2CT"
            elif job_type_array[index] == "Volunteer":
                job_type += "%2CV"
            elif job_type_array[index] == "Intership":
                job_type += "%2CI"
            elif job_type_array[index] == "Other":
                job_type += "%2CO"

        job_type += "&"
        return job_type

    @staticmethod
    def remote() -> str:
        """replacing the match statement with if else statement"""
        remote_array = config.remote
        first_job_remote = remote_array[0]
        job_remote = ""
        if first_job_remote == "On-site":
            job_remote = "f_WT=1"
        elif first_job_remote == "Remote":
            job_remote = "f_WT=2"
        elif first_job_remote == "Hybrid":
            job_remote = "f_WT=3"

        for index in range(1, len(remote_array)):
            if remote_array[index] == "On-site":
                job_remote += "%2C1"
            elif remote_array[index] == "Remote":
                job_remote += "%2C2"
            elif remote_array[index] == "Hybrid":
                job_remote += "%2C3"

        return job_remote

    @staticmethod
    def salary() -> str:
        salary = ""
        if config.salary[0] == "$40,000+":
            salary = "&f_SB2=1&"
        elif config.salary[0] == "$60,000+":
            salary = "&f_SB2=2&"
        elif config.salary[0] == "$80,000+":
            salary = "&f_SB2=3&"
        elif config.salary[0] == "$100,000+":
            salary = "&f_SB2=4&"
        elif config.salary[0] == "$120,000+":
            salary = "&f_SB2=5&"
        elif config.salary[0] == "$140,000+":
            salary = "&f_SB2=6&"
        elif config.salary[0] == "$160,000+":
            salary = "&f_SB2=7&"
        elif config.salary[0] == "$180,000+":
            salary = "&f_SB2=8&"
        elif config.salary[0] == "$200,000+":
            salary = "&f_SB2=9&"

        return salary

    @staticmethod
    def sort_by() -> str:
        sort_by = ""
        if config.sort[0] == "Recent":
            sort_by = "&sort_by=DD"
        elif config.sort[0] == "Relevent":
            sort_by = "&sort_by=R"
        return sort_by

    def util_run(self):
        # Your main function code goes here
        # For example, you can call the LinkedinUrlGenerate class and its methods
        url_generator = LinkedinUrlGenerate()
        urls = url_generator.generate_url_links()
        for url in urls:
            print(url)

    if __name__ == "__main__":
        util_run()
