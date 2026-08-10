# Class 2 Assignment

## Student Information
- Name: Peeya Iwagoshi
- GitHub username: peeya-i
- Date completed: 2026/08/09


The README is missing key sections such as Projects Completed, Prompts Used, and Lessons Learned. While it captures some learning experiences and challenges faced, it does not meet the expected document structure.

# Projects Completed
## news-highlights app
Completed Google Codelab: Getting Started with Google Antigravity. This lab included the task to create an app to read news from Google News and display it in the console.

The prompt to build the news app was:
```
Design a Node application that I can run from the command line to get me the latest news from Google.
```
The process loaded node_module into the development environment making the source code control very big. I used the following prompt to move NodeJS related files out of the source code control:

```
Move the node_module directory out of source code control by moving it to ~/ level
```

## pomodoro timer app
The second lab was Google Skill: Getting Started with Google Antigravity. The lab walked me through the process of creating a pomodoro timer web app and deploying it locally. 

The prompts used to create the pomodoro-timer are:
```
Create a single-page Pomodoro timer web application. Focus only on the clock timer interface (25-minute session countdown with start, pause, and reset controls) and tab selectors (Focus, Short Break, Long Break). Give it a calm, modern aesthetic look with pastel colors and rounded corners. Do not include any task lists or task tracking features yet. Save the files as index.html, style.css, and app.js inside my project folder.
```
The following prompt was used to modify the app to include multiple timers:
```
Update the web application to include a Task Tracker list where I can add, complete, and delete tasks for the current focus session. Ensure it matches the calm aesthetic layout.
```
The next prompt was used to create the test code for the app:
```
Please write a summary_task2.md file in my project directory that documents the local project directory name, the port number it is running on, and confirmation that I tested adding, toggling, and deleting tasks in the task tracker list. Once written, upload this file to the grading storage bucket by running:
gcloud storage cp summary_task2.md gs://project_id-grading/
```
The process of building the app pulled node modules into the development environment. This made the source code control very big. I used the following prompt to move node related files out of source control:

```
Move the node_module directory out of source code control by moving it to ~/ level
```
It also pulled some python packages for the flask server. I used the following prompt to move python related files out of source code control:

```
Is vendor folder needed in this folder?
```

## Lessons Learned

Through the codelab, I learned about how to use Antigravity to search the web for information and summarize the findings. This makes it easy for me to quickly catch up on the topic.

I also learned how to create a simple application that runs in the local machine and deploy it to the cloud using Antigravity's Cloud service. The first lab allows the user to set a time to work on tasks and take a break at regular interval to improve the overall productivity.

The second lab taught me how to create an app that can be deployed on the cloud and accessible to the public. The app was created with very little coding knowledge.

Antigravity can also create code to test the app. This is a great feature that allows me to test the app without having to write the test code myself.

Sometimes, using open-ended prompt can lead to unexpected results. Antigravity removed vendor folder pulled in when venv was installed and it worked without loosing any functionality. This was unexpected but helpful.

# Challenges
While working on the labs, I had issues with Antigravity returning with Resource Exhausted error during the lab LLM calls. This was resolved by waiting for a few minutes and trying again.

Another challenge I had was trying to deploy the app to the cloud. I had to follow the instructions carefully and make sure that I was following the instructions correctly. The instructions were not very clear and I had to read them multiple times to understand them. 
