import csv

def save_to_file(jobs):
    file = open("C:\python challenge\ch9_finale_graduation\jobs.csv", mode="w", encoding = "utf-8-sig")
    writer = csv.writer(file)
    writer.writerow(["title", "company", "link"])
    for job in jobs:
        writer.writerow(list(job.values()))
    return