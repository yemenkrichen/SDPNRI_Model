import random
from mesa import Agent as MesaAgent


class Agent(MesaAgent):

    def __init__(self, model=None, agent_id=None, user_data=None, **kwargs):
        super().__init__(model)

        self.id = (
            agent_id
            if agent_id is not None
            else kwargs.get("user_id", kwargs.get("id", self.unique_id))
        )

        data = user_data if user_data is not None else kwargs.get("activities", {})
        if isinstance(data, dict):
            self.timeline = data.get("timeline", data)
            self.political_bias = data.get("political_bias", 1.0)
        else:
            self.timeline = {}
            self.political_bias = 1.0

        self.state = "S"

        self.b_exponent = kwargs.get("b_exponent", 1.0)
        self.e_exponent = kwargs.get("e_exponent", 1.0)

        self.time_of_last_activity = None
        if "0" in self.timeline:
            self.time_of_last_activity = 0

    def update_current_activity(self, current_hour):
        str_hour = str(current_hour)
        if str_hour in self.timeline:
            self.time_of_last_activity = current_hour

    def step(self):
        current_hour = int(self.model.current_time_seconds / 3600)
        self.update_current_activity(current_hour)

        if self.state in ["D", "P", "N"]:
            if (
                self.time_of_last_activity is not None
                and (current_hour - self.time_of_last_activity) >= 12
            ):
                self.state = "R"
                return

        import parameters

        if self.state == "S":
            p_sd = parameters.transition_probabilities.get("S->D", 0.0)
            p_si = parameters.transition_probabilities.get("S->I", 0.0)
            p_sp = parameters.transition_probabilities.get("S->P", 0.0)
            p_sn = parameters.transition_probabilities.get("S->N", 0.0)

            cutoff_d = p_sd
            cutoff_p = cutoff_d + p_sp
            cutoff_n = cutoff_p + p_sn
            cutoff_i = cutoff_n + p_si

            roll = random.random()

            if roll < cutoff_d:
                self.state = "D"
                self.time_of_last_activity = current_hour
            elif roll < cutoff_p:
                self.state = "P"
                self.time_of_last_activity = current_hour
            elif roll < cutoff_n:
                self.state = "N"
                self.time_of_last_activity = current_hour
            elif roll < cutoff_i:
                self.state = "I"
                self.time_of_last_activity = current_hour

        elif self.state == "D":
            p_di = parameters.transition_probabilities.get("D->I", 0.0)
            p_dp = parameters.transition_probabilities.get("D->P", 0.0)

            roll = random.random()
            if roll < p_di:
                self.state = "I"
                self.time_of_last_activity = current_hour
            elif roll < (p_di + p_dp):
                self.state = "P"
                self.time_of_last_activity = current_hour

        elif self.state == "P":
            p_pd = parameters.transition_probabilities.get("P->D", 0.0)
            p_pi = parameters.transition_probabilities.get("P->I", 0.0)
            p_pn = parameters.transition_probabilities.get("P->N", 0.0)

            roll = random.random()
            if roll < p_pd:
                self.state = "D"
                self.time_of_last_activity = current_hour
            elif roll < (p_pd + p_pi):
                self.state = "I"
                self.time_of_last_activity = current_hour
            elif roll < (p_pd + p_pi + p_pn):
                self.state = "N"
                self.time_of_last_activity = current_hour

        elif self.state == "N":
            p_nd = parameters.transition_probabilities.get("N->D", 0.0)
            p_ni = parameters.transition_probabilities.get("N->I", 0.0)
            p_np = parameters.transition_probabilities.get("N->P", 0.0)

            roll = random.random()
            if roll < p_nd:
                self.state = "D"
                self.time_of_last_activity = current_hour
            elif roll < (p_nd + p_ni):
                self.state = "I"
                self.time_of_last_activity = current_hour
            elif roll < (p_nd + p_ni + p_np):
                self.state = "P"
                self.time_of_last_activity = current_hour


TwitterUser = Agent
