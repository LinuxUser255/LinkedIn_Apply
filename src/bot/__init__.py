"""
LinkedIn Apply Bot Package

This package contains the core functionality for the LinkedIn job application bot.
"""

from .linkedin import LinkedIn
from .config import (
    email,
    password,
    location,
    keywords,
    experienceLevels,
    datePosted,
    jobType,
    remote,
    salary,
    sort,
    blacklist,
    blackListTitles,
    onlyApply,
    onlyApplyTitles,
    followCompanies,
    country_code,
    phone_number,
    headless,
    browser
)
from .constants import (
    linkJobUrl,
    jobsPerPage,
    fast,
    medium,
    slow,
    botSpeed
)
from .utils import (
    LinkedinUrlGenerate,
    get_url_data_file,
    jobs_to_pages,
    url_to_keywords,
    write_results,
    print_info_mes,
    log_failed_job,
    append_url_for_manual_apply,
    get_applied_jobs,
    is_job_already_applied,
    check_job_location
)

__all__ = [
    # Classes
    'LinkedIn',
    'LinkedinUrlGenerate',
    
    # Config variables
    'email',
    'password',
    'location',
    'keywords',
    'experienceLevels',
    'datePosted',
    'jobType',
    'remote',
    'salary',
    'sort',
    'blacklist',
    'blackListTitles',
    'onlyApply',
    'onlyApplyTitles',
    'followCompanies',
    'country_code',
    'phone_number',
    'headless',
    'browser',
    
    # Constants
    'linkJobUrl',
    'jobsPerPage',
    'fast',
    'medium',
    'slow',
    'botSpeed',
    
    # Utility functions
    'get_url_data_file',
    'jobs_to_pages',
    'url_to_keywords',
    'write_results',
    'print_info_mes',
    'log_failed_job',
    'append_url_for_manual_apply',
    'get_applied_jobs',
    'is_job_already_applied',
    'check_job_location'
]