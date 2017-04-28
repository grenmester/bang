# Bang!

2D action platformer meets voice recognition in a frenzy of mayhem. In Bang!, words speak louder than actions.

Through a combination of supreme laziness and perhaps a modicum of ingenuity, we came to the conclusion that in this modern age, there is no reason we should be using controllers to play video games. Out of this ideology Bang! was born. Bang! combines the frantic fun of classic 2D action platformers with the added challenge of issuing every command by voice. It is in part a beckon to the earlier days of video games, when they were enjoyed in the company of friends not separated by computer screen, and a look into their future, when the input peripherals we know may very well cease to exist.

## What it does
Bang! is a multiplayer action platformer where all of the inputs you can give to your player are voice commands. Issue commands like "Bang!" to cause your player character to shoot or "Jump!" to make him jump. Our current demo features a player character controllable by voice command and a CPU to play against.

## How we built it
The game engine runs on Python 3 and `pygame` and was constructed to be as modular as possible so we could easily make tweaks to current settings and add new features. We created our sprites in Photoshop.

The web server was built on `node`, `socket.io` and `express.js`. Our goal for it was to provide a lightweight and fast medium between your mouth and your player, while still conveying useful information such as current ammo count and health.

## Links

Demo: [https://bang-163322.appspot.com/](https://bang-163322.appspot.com/)

Devpost: [https://devpost.com/software/bang-ish3rv](https://devpost.com/software/bang-ish3rv)

---

Bang! was created by Owen Gillespie, Cole Kurashige, Jacky Lee, and Danny Liu
