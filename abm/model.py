import random
import parameters
from agent import TwitterUser
from mesa import Model


class SDPNRIModel(Model):

    def __init__(self, user_timelines, political_bias=None):
        super().__init__()

        self.current_time_seconds = 0
        self.step_count = 0

        if political_bias is None:
            political_bias = parameters.baseline_bias

        for user_id, timelines in user_timelines.items():
            user_data = {
                "timeline": timelines,
                "political_bias": (
                    political_bias.get(user_id, 1.0)
                    if isinstance(political_bias, dict)
                    else political_bias
                ),
            }
            TwitterUser(model=self, agent_id=user_id, user_data=user_data)

    def get_state_counts(self):
        counts = {"S": 0, "D": 0, "P": 0, "N": 0, "R": 0, "I": 0}

        for agent in self.agents:
            if agent.state in counts:
                counts[agent.state] += 1

        return counts

    def step(self):
        self.step_count += 1
        self.current_time_seconds += parameters.time_step

        agent_list = list(self.agents)
        random.shuffle(agent_list)
        for agent in agent_list:
            agent.step()
