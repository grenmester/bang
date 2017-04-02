# Title
Bang!

# Elevator Pitch
2D action platformer meets voice recognition in a frenzy of mayhem. In Bang!, words speak louder than actions.

# Tags
python, pygame, node.js, socket.io, websockets, express.js, google-web-speech-api, google-speech-to-text-api

# Body
## Inspiration
All four of our lives have been enhanced by speech recognition in some way. Owen barks orders to his Echo Dot when he needs an alarm or a change of music. With one of his hands in a cast, Cole has found a very useful aide in his Apple Watch. Danny and Jacky both make use of Siri on their phones and computers on a daily basis.

Through a combination of supreme laziness and perhaps a modicum of ingenuity, we came to the conclusion that in this modern age, there is no reason we should be using controllers to play video games. Out of this ideology Bang! was born. Bang! combines the frantic fun of classic 2D action platformers with the added challenge of issuing every command by voice. It is in part a beckon to the earlier days of video games, when they were enjoyed in the company of friends not separated by computer screen, and a look into their future, when the input peripherals we know may very well cease to exist.
## What it does

## How we built it
Bang! is built into two components: the game engine and the

## Challenges we ran into
LÖVE 2D and Lua proved to be too janky to work even in the context of a Hackathon. Our solution? After roughly 12 hours of work on the game engine in this awful, awful environment, we completely overhauled and transitioned into Python and pygame. Jacky woke up from his midday nap to find that we were now developing the same game in a completely different language.

We also faced issues with the node.js server and Python failing to communicate well and so overhauled the way we performed communication in order to prevent data from being dropped between the two.
## Accomplishments that we're proud of
We are most proud of the transition we made one third of the way through into the hackathon from one game engine and language to another.

## What we learned
We've learned a lot of things. One, Lua is awful for us (we really are sorry if you like it, it just did not work well for us). Two, it's worth it to try different things, even if you think you're committed to one particular method. We experimented with Python and pygame and Javascript and an OpenGL-based 3D engine at the same time when we decided that LÖVE 2D was not going to work.
## What's next for Bang!
Mobile apps, for sure. Both of the APIs we were looking at either had limited or no functionality on mobile devices (if this were a month or two later, they probably would work) and we weren't comfortable enough in either iOS or Android development to implement apps from the get-go. Our vision is of a group of friends sitting around a TV speaking into their phones and controlling the characters on the screen.

# Try it out!
[Github repo](https://github.com/grenmester/bang)
[Website](https://bang-ga.me)
