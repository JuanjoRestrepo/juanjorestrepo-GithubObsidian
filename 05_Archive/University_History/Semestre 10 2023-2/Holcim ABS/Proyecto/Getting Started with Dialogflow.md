---
banner: https://hectobot.com/wp-content/uploads/2023/03/Google-Dialogflow-Tutorial.png
---

Dialogflow is an end-to-end tool powered by NLU to facilitate rich and natural conversations

# High-level Architecture

![[Pasted image 20230815143957.png|700]]

Dialogflow sits in the middle of the stack:

![[Pasted image 20230815144048.png|300]]

An user can interface with it via all the common channels, including text, websites, apps, messengers and smart voice devices like Google Home. Basically, Dialogflow handles the job of ***transalting Natural Language into machine-readable data using Machine Learning model trained by OUR EXAMPLES***

![[Pasted image 20230815144517.png|300]]

Once Dialogflow identifies what the user is talking about, it can **hand this data to the back-end** where you can use it **to make stuff happen**

At the back-end, one can fulfill (perform, carry out, execute) the request 
by integrating it with other services, databases, or even third party tools like the own CRM (**Customer relationship management**)

![[Pasted image 20230815144537.png|350]]
_________________________________________________________
# Steps

## 1. Create an Agent
- An Agent is basically your entire chatbot application which collects what the user is saying.
- It maps it to an ***intent*** taking an action on it
- Then provides the user with the response

It all starts with the trigger event known as *Utterance*

![[Pasted image 20230815144947.png|600]]

### Utterances:
- It is how our users invoke the chatbot.
- For example, if I say: *"Hey Google, play some music"* -> This is an Utterance
- But the phrase *"Hey Google"* -> Trigger
![[Pasted image 20230815145225.png|350]]

In another example, the phrase *"talk to Smart Scheduler"* is the invocation phrase for our chatbot and *"Smart Scheduler"* is the invocation name
![[Pasted image 20230815145309.png|400]]

Once the bot is activated and has collected the user utterance, **we need to understand what the user's intent is.**

## Why do they want to talk to our bot?

## 2. Intent

When you say: *"I want to set up an appointment"* or if you ask *"What are your hours of operation"*

![[Pasted image 20230815145807.png|350]]

Here the *"set up an appointment"* and *"hours of operation"* are the **intents**

To control all of this, you provide Dialogflow with different examples/samples of user's intent
![[Pasted image 20230815145950.png|500]]

### Intent Matching
Dialogflow **trains the machine learning model with many more similar phrases** and finally **maps the user's phrase to the right intent**


After matching the intent, we need to know **WHAT TO DO WITH THE INTENT** to give the user a **Response**


## 3. Actions and Parameters
+ Here we define what variables we want to collect and store
+ For example, if we say: "Set an appointment for 5am tomorrow" -> 5am and tomorrow are two key pieces of information in the statement. These are the entities
![[Pasted image 20230815150613.png|400]]

Once We have the variables, we may use to provide a static response to the user either by backend to take some actions or other ways

![[Pasted image 20230815151600.png|500]]

# Context
It is the method for our Chatbot to store and access variables so it can exchange information from one intent to another in a conversation

_________________________________________________________
# Fulfillment

Dialogflow has inbuilt integration with Google Cloud Functions to interface you with back-end

![[Pasted image 20230815151920.png|500]]

It also allows you to provide another HTTPS endpoint and Dialogflow will connect to it automatically

![[Pasted image 20230815152007.png|500]]

