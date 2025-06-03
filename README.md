# BT4BR_project

# Game - Escape Room

This project is an interactive educational experience that blends elements of game design with foundational concepts in bioinformatics. Designed as a digital "escape room", it challenges players to apply their knowledge in order to progress through a sequence of rooms—each containing puzzles, questions, and subtle clues inspired by real-world biological data analysis.

## Concept & Gameplay

Players navigate through a series of virtual rooms, each of which contains a unique question or interactive task rooted in topics such as sequence alignment, genetic databases, or protein structure. The interface is built using **Pygame**, allowing for smooth player movement, interactions with objects, and a dynamic game environment.

As players explore the environment, they encounter **key items** and **trigger zones**—these are not merely decorative, but essential for unlocking the path forward. A correct answer may cause a door to open, a new item to appear, or even an entire room to shift. The progression system is both educational and immersive, offering feedback through gameplay mechanics rather than static text alone.

## Educational integration

Questions have been designed with both **challenge and reinforcement** in mind. Rather than relying on rote memorization, the game encourages conceptual thinking: recognizing biological file formats, understanding algorithm outputs, and interpreting simplified datasets.

To enhance learning, the project integrates a lightweight feedback system. While still under active development, the game collects data such as time spent per question and accuracy, which is analyzed via **R scripts** located in the `/analysis` directory. These scripts generate visual insights into how players interact with each topic—supporting future refinements of question difficulty and pacing.

## Visualization & analysis

Although the core game is implemented in Python, a companion set of **R-based visualizations** ____________. These visualizations aim to identify patterns in response behavior, highlighting which concepts may require clearer framing or improved instructional scaffolding. _______________________

##  Development notes

The project has been developed iteratively with full use of Git version control. Each major feature—movement mechanics, room transitions, question parsing—was implemented and documented through well-structured commits. This has allowed for agile revisions and transparent tracking of development decisions throughout the process.

## Writing & documentation

All educational content has been written with clarity and accessibility in mind, with terminology that aligns with standard bioinformatics practice. The README itself is intended to evolve alongside the game and includes citations for all scientific materials and concepts used within.

## Project Structure

<pre> 
├── game.script/ # Final game builds 
│ ├── final_linux.py │ └── final_windows.py 
├── images/ # All custom illustrations and graphics 
├── other_files/ # Supplementary project files
├── BT4BR_project.tar # Compressed full game directory 
├── README.md # Project description and documentation 
├── game_playthrough.zip # Gameplay video </pre>
