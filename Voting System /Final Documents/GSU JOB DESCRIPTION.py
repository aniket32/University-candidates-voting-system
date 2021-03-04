from VotingSystemDatabase import VotingSystemDatabase
import Students
import os
import json

#GSU postion = candidatedata [1]

print("Enter GSU position: 1- President, 2- Faculty Officer, 3- GSU Officer")
job_description = int(input("Please select a choice between 1-3: "))
job_title = '"'
if job_description == 1:
  job_title = "President"
elif job_description == 2:
  job_title = "GSU Officer"
elif job_description == 3:
  job_title = "Faculty Officer"
else:
  print("This option does not exist ")
  exit()

with open ("GSU_job_description.txt", "a") as f:
  message = input("Enter job description: ")
  f.write(job_title + ": " + message + "\n");

