# Investigating Political Bias and Emotional Contagion in Misinformation Cascades Using An Agent-Based SDPNRI Model
This repository contains the code, data processing pipeline, and simulation framework developed for my summer 2026 research project on modeling misinformation dynamics. The project uses an Agent-Based SDPNRI to investigate how emotional intensity and political bias influence misinformation diffusion, persistence, and debunking thresholds within online social networks.
The project answers the question: 
How does the introduction of political confirmation bias change the macroscopic density of active debunkers required to contain an online rumor compared to a purely emotional baseline?
## Project Overview
Classical epidemiological rumor models (like standard SIR or the recent 2024 SEDPNR framework) lack several important compartments that describe sociological impact of debunkers in rumor omission on social networks. SEDPNR for example, (Susceptible, Exposed, Doubtful, Positively-Infected, Negatively-Infected, Restrained) which was the starting point from my research, assumes that no one in the network can gain complete immunity to a rumour and can always fall back into the susceptible state.
To address these limitations this project introduces the SDPNRI model which removes the exposed state as it does not represent a real compartment phase such as in real disease spread where the individual is infected but not yet infectious. In misinformation modeling I believe that exposure to a misinformation is instant therefore for simplification purposes, E was removed. Additionally, I added the Immune compartment (I) representing active debunkers and people with expertise who can influence rumor participants toward restrained or immune states.
To tie the data and the math together, I am building a custom Agent-Based Model environment. Every unique agent on the virtual network reads their timeline and calculates their own action using a dynamic Retweet Probability Formula. All other factors such as follower count, age of the tweet, attractiveness of the post... will be held constant in purpose of studying the relationship between political bias and emotion contagion and debunkers thresholds.
Pretweet = Political Bias × Emotion (Vader score)
• In the baseline run, political bias is locked at neutral = 1, meaning the cascade is driven entirely by the emotion scores extracted from my dataset.
• In the conspiracy scenario, the text and network remain identical, but we activate the bimodal political bias variable which acts as a multiplier prompting the need of more debunkers.
## Dataset
For this project I will be working with a subset from the PHEME Twitter data from the 2013 Boston Marathon Bombings. The rumor claimed that an 8-year-old girl, who supposedly survived the Sandy Hook Elementary School shooting in December 2012, traveled to Boston four months later to run the marathon in remembrance of her classmates, and was tragically killed in the bombings.
## Installation and Setup

To run this project, clone the repository and install the required Python dependencies.

```bash
# Clone the repository
git clone https://github.com/yemenkrichen/Research-Internship.git

# Navigate to the project directory
cd Research-Internship

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment (Linux/macOS)
source venv/bin/activate

# Install project dependencies
pip install mesa pandas numpy nltk matplotlib networkx
```
## Project Structure
The repository is organized into three main components: the raw and processed datasets, the data processing pipeline, and the Agent-Based Model (ABM) simulation environment.
## Code
### src/

main.py : Parses and processes the Boston bombings dataset into a chronological timeline of source tweets and reactions, saving the cleaned data into a single JSON file.

sort_user.py : reorganizes the cleaned conversation data by grouping all tweets and reactions by user ID instead of thread ID, and saves the result into a new JSON file.

vader.py : Classifies each activity into its adequate SDPNRI compartment based on LLMs result and VADER which is sentiment-analysis tool specialized for social media text.

series.py : Processes user state transitions over time (using an epidemic-style compartmental model framework) and generates a time-series CSV file tracking how many users are in each compartment at any given moment.

calibration.py : Calculates the transition rates for your compartmental misinformation model by dividing the total number of times each state transition occurs by the total "person-seconds" spent in the source compartment, then saves the calibrated rates into a CSV file.
## Limitations
The model is calibrated a subset from the PHEME dataset tha represents a well-documented casey study. however, the findings may not generealize to other misinformation events.

Political bias is introduced as a controllable variable rather than being inferred from real user data. Consequently, the model explores hypothetical scenarios rather than reconstructing the true ideological characteristics of individual Twitter users.

Yemen Krichen, July 2026

Institute of Computing in Research
