This is a Readme for a Terminal Screen Saver called 3000 (tui000).

History: 
I had the idea one day just relaxing and thinking about Johnny Castaway. 
I had already ported it to as many platforms as I was interested in.
What I really missed was that feeling of fun and writing software. 

Some of my best work was made famous not by my original intention.
Rather, it was the creativity of others that brought purpose to "meaningless" software. 
After all these years, I keep coming back to the terminal. 

So, in an attempt to recreate that feeling, in the terminal, here's the start and the pitch.

Design:
Constraints: Must target / be usable in 80x24 terminal window. 

Launching the app spawns a character.
The character makes choices, indicated by colors which map to life categories. 
These choices add up to weave the tapestry of each life, the colorful headstone.
When the character dies, each is written out to a json file in ./graveyard/

Running the App:
Run with python after installing requirements.txt

Pass the -debug flag for more logging and 100x speed

Instructions During Use: 
Press the "i" key for info, right now that's just your terminal size. 
Press the "r" key to re-spawn a new character. 
Press the "g" key to enter/exit graveyard mode
While in graveyard mode, press the "right" and "left" keys to walk through the aisles of the graveyard.
While in graveyard mode, press Up and Down to highlight tombstones.
Press "q" to Quit. 


Version Just Like The Concept
![Play Screen](concept_art/play_screen.png)

![Graveyard](concept_art/death_screen.png)



Early Version -> 

![Early Version](screenshots/early.png)

