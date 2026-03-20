This problem is trying to figure out what to do when we have some sort of situation that the computer is in.

Some sort of environment that an agent is in, and we would like for that agent to be able to somehow look for a solution.

# 1. Search Problems
---
First we will introduce some terminology

## Agent
---
Entity that perceives its environment and acts upon that environment.

- In the case of the driving directions, your agent might be some representation of a **car** that is trying to figure out what actions to take in order to arrive at a destination.

- In the case of the 15 puzzle with the sliding tiles, the agent might be the **AI or the person** that is trying to solve that puzzle by figuring out what tiles to move in order to get to that solution.

## State
---
A configuration of the agent and its environment.

In the 15 puzzle, any state might be any one of these three examples, which are just some configurations of the tiles.

![[Pasted image 20240120153704.png]]

Each state is different and is going to require a slightly different solution.
A different sequence of actions will be needed in each one of these in order to get from this initial state to the goal.

## Initial State
---
The state in which the agent begins.

![[Pasted image 20240120154115.png]]

This is going to be the starting point for our search algorithm and then to start to reason about it. What actions might we apply.

## Actions
---
Choices that can be made in a state.

In AI, We are always going to try to formalize these ideas a little bit more precisely such that we could program them a little bit more mathematically.

Si this will be a recurring them and we can more precisely define actions as **function**.

- ***ACTIONS (s)*** returns the set of actions that can be executed in state *s*

In the 15 puzzle example, there's generally going to be 4 possible actions that we can do most of the time:

![[Pasted image 20240120154612.png]]

Somehow our program needs some **encoding** of the state, which is often going to be in some numerical format and some encoding of these actions.

But it also needs some **encoding of the relationship between these things**.

##### How do the states and actions relate to one another?

We will introduce to our AI a transition model.

## Transition Model
---
A description of what state results from performing any applicable action in any state. 

We can define this more formally as a function
- ***RESULT (s, a)*** returns the state resulting from performing action *a* in state *s*

Let's take a look at an example:

Here's the state of the 15 puzzle
![[Pasted image 20240120155112.png]]

Here's the action, sliding the tile to the right
![[Pasted image 20240120155202.png]]

What happens if we pass these two things as parameters of our function?
![[Pasted image 20240120155236.png]]

We will get as a result a new state, which is the state we get after we take a tile and slide it to the right

![[Pasted image 20240120155340.png]]

If we had a different action and a different state, we'd get a different answer altogether
![[Pasted image 20240120155429.png]]

This is going to be our transition model that describes how it is that states and actions are related to each other. 

If we take this transition model and think about it more generally and across the entire problem, we can form what we might call a State Space

## State Space
---
The set of all states reachable from the initial state by any sequence of actions.

They are all of the states we can get from the initial state via any sequence of actions.

![[Pasted image 20240120155734.png]]

- Every state is represented by a game board.
- There are arrows that connect every state to every other state.
- We can get two from that state

We can simplify this representation as a graph

![[Pasted image 20240120160122.png]]
Some sequence of nodes and edges that connect nodes.
- Each node represents one of the states inside of our problem.
- The arrows represent the actions that we can take in any particular state, taking us from one particular state to another state

#### So now how do we know when the AI is done solving the problem?

The AI needs some way to know when it gets to the goal, that it has found the goal.

So we will need to **encode** into our artificial intelligence a **goal test**. Some way to determine whether a given state is a goal state.

## Goal Test
---
A way to determine whether a given state is a goal state.

Some problems might have a goal, like a maze where you have one initial position and one ending position and that's the goal

Imagine if we have multiple possible goals, that there are multiple ways to solve a problem. 

The computer wouldn't just care about finding a goal, but finding a goal well, or one with a low cost.

## Path cost function
---
Numerical cost associated with a given path.

In a case of driving directions, it could be pretty annoying if I said I wanted directions from point A to point B and the route the Google Maps gave me was a long route with lots of detours that were unnecessary, that took longer than it should have been to get to that destination.

That's why we'll often give every path some sort of numerical cost, some number telling us how expensive it is to take this particular option.

Then we will tell our AI that instead of just finding a solution, some way of getting from the initial state to the goal, we'd really like to find one that minimizes this path cost, that is less expensive, takes less time or minimizes some other numerical value.

We can represent this graphically:

![[Pasted image 20240120161736.png]]

Each number is associated to each of these arrows (actions) that we can take from one state to another state.

That number, is the path cost of this each particular action where some of the costs for any particular action might be more expensive than the cost for some other action.

Sometimes, the cost of any particular action is the same, like the 15 puzzle, where it doesn't really make a difference whether I'm moving right or left. 

The only thing that matters is the total number of steps that I have to take to get from point A to point B and each of those steps is of equal cost.


## Solution
---
A sequence of actions that leads from the initial state to a goal state

## Optimal Solution
---
A solution that has the lowest path cost among all solutions

So now we defined our problem, now we need to begin to figure out how it is that we're going to solve this kind of search problem

Our computer is going to need to represent a whole bunch of data about this particular problem. We need to represent data about where we are in the problem and oftentimes we need to package a whole bunch of data related to a state together.

That's why we will be using adata structure called a Node.


# Node
---
A data structure that keeps track of
- a state
- a parent (node that generated this node, a state before us)
- an action (action applied to parent to get node)
- a path cost (from initial state to node)

# Approach
---
