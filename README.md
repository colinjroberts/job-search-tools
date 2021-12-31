# job-search-tools
Tools for organizing and performing a job search

## General Goals
- Track companies I am interested in
  - Company name, jobs website, people I may want to talk to, notes about products and languages, company's goals/mission, etc. 
  - Track who I've talked to and when 
  - Periodically scrape for new jobs and alert me when something is available I might like
- Track jobs I'm interested in and steps in application process:
  - Job title and description (perhaps parsed from website)
  - Track when I applied and how, how far I got in the process, what decisions were made.
- Generate somewhat tailored cover letters and resumes. 
  - For each job entry I have, write about my accomplishments in a number of different ways
  - Then when I need a resume or cover letter, generate it based on the tags for the role.
    
## User Story Goals:
- I want to open my program and see a list of open positions posted by companies I've curated.
- I want to see positions I am actively in the process of applying to and where I am in the process.
- I want to not see (but be able to look up), roles I've not received.
- I want a place to take notes about a company that I can later look up.
- I want a repo of interview questions I've been asked from each company I can review and practice from.

## End-to-end examples:
1. Open app. Look at outstanding TODOs and dismiss any that have been completed. Run job scraper, go through newly found positions and save or dismiss them (dismissing means they will not show up again in future scrapes). For those saved, decide if I want to apply directly or try to contact people who work in the company for a chat first. Add outreach, practice, or little project tasks to TODO list. If I choose to reach out to someone, note who it is, their title, when I first reached out. When I talk to them, have spot for notes for company (with person as source) and notes specific to that person. 

## TODO:
- Milestone: Build manual version of E2E 1
  - Sketch a usable design for system using curses with the following screens:
    - Todo
    - People
    - Companies
    - Jobs
  - Build tables for people, companies, jobs, notes
  - Try adding a few jobs
- Milestone: Build job scraper