import random
import parameters as p
from agent import Agent

class SDPNRIModel:
    def __init__(self, num_agents=p.num_agents, p_si=p.p_si_empirical, b_exp=1.0, e_exp=1.0, beta=p.beta_0):
        self.num_agents = num_agents
        self.current_time = 0
        
        # Transition Probabilities driven by parameters.py calibrated rates
        self.p_sd = p.p_sd
        self.p_si = p_si
        self.beta_0 = beta
        
        # Sensitivity Exponents
        self.b_exp = b_exp
        self.e_exp = e_exp
        
        self.agents = []
        self._initialize_population()
        
        # History metrics
        self.history = {'S': [], 'D': [], 'P': [], 'N': [], 'I': [], 'R': []}
        self._record_counts()

    def _initialize_population(self):
        """Creates 482 agents with bimodal political bias and skewed emotional scores."""
        for i in range(self.num_agents):
            if random.random() < 0.5:
                bias = random.gauss(0.4, 0.15)
            else:
                bias = random.gauss(1.6, 0.15)
            
            bias = max(0.05, min(1.95, bias))
            emotion = random.betavariate(2, 5)
            
            agent = Agent(
                agent_id=i,
                model=self,
                bias=bias,
                emotion=emotion,
                b_exp=self.b_exp,
                e_exp=self.e_exp
            )
            self.agents.append(agent)

    def _record_counts(self):
        counts = {'S': 0, 'D': 0, 'P': 0, 'N': 0, 'I': 0, 'R': 0}
        for agent in self.agents:
            counts[agent.state] += 1
            
        for state in counts:
            self.history[state].append(counts[state])

    def step(self):
        self.current_time += 1
        random.shuffle(self.agents)
        for agent in self.agents:
            agent.step(self.current_time)
        self._record_counts()

    def run_simulation(self, steps=72):
        for _ in range(steps):
            self.step()
        return self.history
