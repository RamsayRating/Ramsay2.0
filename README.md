# Ramsay2.0

## Inspiration
Through the course of a rapid ideation session, we found ourselves defining several unique learning goals for HackHarvard 2017. These goals included practicing working with text mining, linear algebra concepts, new APIs and web-app creation, which none of us had much previous experience with.

## What it Does
Our web-app takes a photo of food as input and returns one of Gordon Ramsay's tweets expressing his "likely" opinion of the food.

## How It Works
Our web-app uses Google's Vision API to analyze the photo for an understanding of what it shows. We were originally going to search Google for another photo which contains those concepts, compares these two photos using linear algebra. However, by using the vision API, we were able to get a correlation value between the photo and the top search result. We then analyze Gordon Ramsay's tweets using sentiment analysis, and search for a tweet that has a comparable value (of positive-to-negative) to the correlation of the images.

## Accomplishments that we're proud of
Surviving our first hackathon on a team of complete newbies, creating a reasonably aesthetic front-end, sleeping at least 4 hours/team-member/night, tackling a totally unknown set of challenges and persevering to build a functional proof of concept, and the substantial amount of time we spent laughing throughout the weekend.

## What we learned
Almost everything in the project as we had minimal experience with all elements. But more specifically, the Google Vision API was a great new challenge to tackle, and front-end development was something no one was particularly excited about, and we ended up feeling much more excited about it by the end. 
