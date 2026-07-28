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
git clone https://github.com/yemenkrichen/SDPNRI_Model.git

# Navigate to the project directory
cd SDPNRI_Model

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment (Linux/macOS)
source venv/bin/activate

# Install project dependencies
pip install mesa pandas numpy nltk matplotlib networkx
```
## Project Structure
The repository is organized into three main components: the raw and processed datasets, the data processing pipeline, and the Agent-Based Model (ABM) simulation environment.
## Extracting Data
This project uses a subset of the **Augmented dataset of rumours and non-rumours for rumour detection** (PHEME-Aug v1.0), specifically the **2013 Boston Marathon Bombings** event.

> Han, S., Gao, J., & Ciravegna, F. (2019). *Augmented dataset of rumours and non-rumours for rumour detection* (Version 1.0) [Data set]. Zenodo.
> https://doi.org/10.5281/zenodo.3249977

This dataset augments the original PHEME dataset of rumours and non-rumours, and should also be cited alongside:

> Han, S., Gao, J., & Ciravegna, F. (2019). Data Augmentation for Rumor Detection Using Context-Sensitive Neural Language Model With Large-Scale Credibility Corpus. *7th International Conference on Learning Representations (ICLR) Learning from Limited Labeled Data Workshop*, New Orleans, LA, USA.
>
> Kochkina, E., Liakata, M., & Zubiaga, A. (2018). All-in-one: Multi-task Learning for Rumour Verification. *COLING*.

Dataset structure (as distributed): each event directory contains two subfolders, `rumours/` and `non-rumours/`, each containing one folder per tweet, named by tweet ID, holding a `source-tweet/` directory (the tweet itself) and a `reactions/` directory (replies to it).

The full dataset is not redistributed here, both due to size and to respect the dataset's original distribution channel.

### Reproducing the subset
To reproduce the subset I used Claude AI to go through all source-tweets in the `rumours/` and `non-rumours/` folders to extract what is relevant to the girl being killed in a marathon rumour.
The prompt used is attached.

1. Download `aug-rnr-data.tar.bz2` from
   https://zenodo.org/records/3249977 and extract it locally.
2. Locate the 2013 Boston marathon bombings event inside the folder `bostonbombings`.
3. Run:
```bash
python3 `src/compare_rumors.py`
```
4. Upload the obtained file all_tweets.txt to Claude AI and use src/Prompt to get the relevant folders.
5. Use `src/clean_non_rumours.py` and `src/clean_rumours.py` to delete the irrelevant folders for your data.
   
## Code
### src/

#### main.py :

The data processing pipeline converts the sorted PHEME Boston Marathon Bombing girl rumour dataset into structured files used for SDPNRI classification and ABM calibration.

The input dataset should be placed in:

```
data/aug-rnr-data_full/bostonbombings
```
Run:

```bash
python3 src/main.py
```

This script extracts tweet activity from rumor and non-rumor cascades, including tweet IDs, user IDs, timestamps, text, activity type, and time since the original source tweet.

The output is:

```
bostonbombings_clean.json
```

This file contains the chronological Twitter cascades used as input for the following processing steps.

#### sort_user.py :

Run:

```bash
python3 src/sort_user.py
```

This script reorganizes the cleaned Twitter cascade data from a thread-based structure into a user-based structure.

Instead of grouping activity by conversation thread, all tweets and reactions are grouped by individual user ID. This allows the model to track the sequence of actions performed by each user and analyze individual SDPNRI state transitions over time.

The output is saved as:

```
boston_users_database.json
```

This JSON file contains the complete activity history of each user and serves as the input for the SDPNRI classification step.

#### vader.py :

Run:

```bash
python3 src/vader.py
```

This script classifies each user activity into one of the SDPNRI compartments using a combination of manually validated classifications, VADER sentiment analysis, and language processing.

The classification process includes:

- Normalizing tweet text by removing URLs, formatting inconsistencies, and unnecessary characters.
- Using previously identified text with `src/text.only.py` classified with claud AI to identify doubtful (`D`) and immune/debunking (`I`) behaviors and irrelevant text using `src/Prompt2`
- Applying VADER sentiment analysis to determine emotional polarity:
  - Negative emotional reactions are classified as negatively infected (`N`).
  - Other emotional reactions are classified as positively infected (`P`).
- Translating non-English tweets into English before sentiment analysis.
- Removing irrelevant activities that do not contribute to the misinformation cascade.

Users are initially assigned to the susceptible (`S`) state. As they interact with the rumor, their state transitions are recorded chronologically.

The script also applies the restrained (`R`) transition rule. Users who remain inactive for more than 12 hours (`43200` seconds) after their last activity are classified as restrained.

The output is saved as:

```
boston_user_transitions.json
```

This file contains the complete SDPNRI state history of each user, including:

- User ID
- Tweet ID
- Timestamp
- SDPNRI state
- State transition
- Sentiment score
- Original and translated text (when translation is required)

Additionally, the script generates:

```
sdpnri_timeline_diagram.png
```

which visualizes the evolution of the SDPNRI compartments over time in the observed Twitter cascade.

#### series.py :

Run:

```bash
python3 src/series.py
```

This script converts individual user SDPNRI transitions into a population-level time series showing the number of users in each compartment over time.

The output is saved as:

```
compartment_timeseries.csv
```

This file is used for analyzing misinformation dynamics and calibrating the SDPNRI model.

#### calibration.py :

Run:

```bash
python3 src/calibration.py
```

This script calculates the transition rates between SDPNRI compartments using the observed user transitions and compartment population time series.

The output is saved as:

```
calibrated_rates.csv
```

This file contains the estimated transition rates used to parameterize the mathematical SDPNRI model.

### abm/ (Validation ABM) :

#### agent.py

Defines the Twitter user agents in the Agent-Based Model and implements their SDPNRI state transition behavior.

#### model.py

Defines the SDPNRI Agent-Based Model environment and manages agent initialization, time progression, and population state tracking.

#### parameters.py

Stores the model parameters, including transition rates, time step, and bias/emotion variables used by the Agent-Based Model.

#### run.py

Run:

```bash
python3 run.py
```

This script runs the SDPNRI Agent-Based Model simulation using the processed user timelines and calibrated transition parameters.

The outputs are:

```
abm_results.csv
sdpnri_cascade_plot.png
```

The CSV file contains the simulated SDPNRI compartment populations over time, while the plot visualizes the evolution of the misinformation cascade.

### abm2/ (Simulation ABM) :

#### agent.py

Defines the agents used in the simulation ABM and implements the effects of political bias and emotional contagion on SDPNRI state transitions.

#### model.py

Defines the simulation ABM environment, initializes the agent population, and tracks SDPNRI compartment dynamics over time.

#### parameters.py

Stores the simulation parameters, including population size, transition rates, simulation duration, and parameter sweep ranges.

#### run.py

Run:

```bash
python3 run.py
```

The simulation generates the following outputs:

debunker_threshold_results.csv`

Contains the results of all parameter sweep experiments.

Each row represents one simulation scenario and includes:

- `b_exponent`: Political polarization sensitivity parameter.
- `debunker_rate`: Probability of transition into the immune/debunker (`I`) state.
- `avg_peak_attack_pct`: Average maximum percentage of users actively spreading misinformation (`P + N`).
- `R0`: Estimated reproduction number for the given scenario.

This file is used to analyze how political polarization and debunking effectiveness affect misinformation spread.

---

debunker_sweeps.png`

Shows the relationship between debunker effectiveness and the peak misinformation attack rate.

Each curve represents a different level of political polarization, allowing comparison of how polarization changes the required intervention strength.

---

critical_threshold_curve.png`

Shows the theoretical critical debunker threshold required to achieve:

$$R_0 \leq 1$$

as political polarization increases.

This illustrates how stronger polarization requires a larger proportion of immune/debunker agents to control misinformation spread.

---

compartment_evolution_grid.png`

Shows the time evolution of all SDPNRI compartments over the 72-hour simulation period.

The plot tracks changes in:

- Susceptible users (`S`)
- Doubtful users (`D`)
- Positive rumor spreaders (`P`)
- Negative rumor spreaders (`N`)
- Restrained users (`R`)
- Immune/debunker users (`I`)

---

recommended_threshold_dynamics.png`

Shows the SDPNRI dynamics when applying the theoretically calculated debunker threshold.

This output compares the mathematical prediction with the Agent-Based Model behavior to evaluate whether the theoretical threshold is effective in the simulated social network.

## Limitations
The model is calibrated a subset from the PHEME dataset that represents a well-documented case study. however, the findings may not generalize to other misinformation events.

Political bias is introduced as a controllable variable rather than being inferred from real user data. Consequently, the model explores hypothetical scenarios rather than reconstructing the true ideological characteristics of individual Twitter users.

Yemen Krichen, July 2026

Institute of Computing in Research
