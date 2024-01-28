# Jay Bot (Team Binary #52)

## Project Contributors

-   Ethan Lajeunesse - lajeunessee@etown.edu
-   Yusuke Satani - sataniy@etown.edu

## Target School for Solution

-   [Elizabethown College, PA](https://etown.edu)

## Demo Url

-   Click [Here](https://client-production-4ef4.up.railway.app/) For Demo
-   NOTE: This project was only for the **chat bubble (bottom right)** + related UI elements. The etown.edu website is not ours. It is only used for demo purposes and is shown with an iframe.

## Inspiration

Having outdated information on websites can be damaging, and college websites are no different. As high school students are searching for their next school, colleges want to ensure they are seeing information about them presented in the best ways.

## What it does

This project scrapes text data using links from Elizabethtown College's [sitemap](https://etown.edu/sitemap.xml). We deployed a GPT-35-turbo model on Azure AI that connects to Azure Search. This Azure Search has access to the scraped data that is uploaded more than once a day.

## How we built it

We started with the front end, and we knew we wanted it to be present on the college's main website - [etown.edu](etown.edu). Based on that, we created a blue and white conversation button that sits on the bottom right of the screen. Clicking on that opens a larger modal that users can type their questions into and the Azure AI bot responds to.

## Challenges we ran into

We ran into trouble deploying the Azure AI services and connecting to them in the code. From technical issues with the shared subscriptions as other users and limitations, to recent changes in OpenAI's APIs that resulted in lots of documentation and examples to become out of date. On top of that, we had issues accessing our MongoDB database that stored all of the chats due to it being blocked on the hacker WiFi.

## Accomplishments that we're proud of

Although it took us quite a bit, we were able to successfully deploy Azure AI services on the cloud and connect to them in the code. We were able to find a solution to having outdated information in chatbots and felt that it was also a great accomplishment.

## What we learned

We learned a lot at this hackathon. Not only did our knowledge of cloud services expand, but so did our knowledge of AI, how it works, and how to solve problems with it.

## What's next for Jay Bot

The next steps for Jay Bot is to present it to the Office of Marketing and Communication at Elizabethtown College as they are in charge of the etown.edu website. We'd also like to monitor the scraping process more to ensure we're not scraping data too often, and might come up with even better solutions for getting up to date information. Lastly, something that would have been awesome but we didn't have time for is to take advantage of the message streams that are returned from OpenAI. Doing so would allow for text to show up 1 word at a time rather than all at once when it's finished processing.
