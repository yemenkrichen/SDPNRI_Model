import random
class Agent:
    def __init__(self, agent_id, model, bias, emotion, b_exp=1.0, e_exp=1.0):
        self.agent_id = agent_id
        self.model = model

        # Agent properties
        self.bias = bias
        self.emotion = emotion

        # Sensitivity settings
        self.b_exp = b_exp
        self.e_exp = e_exp

        # Possible states: S, D, P, N, I, R
        self.state = "S"
        self.start_time = None

    def get_weights(self):
        """Compute the positive and negative weights."""
        dist = abs(self.bias - 1.0)

        emo = (self.emotion * (1.0 + dist)) ** self.e_exp

        b = max(0.01, self.bias)

        pos = emo * (b ** self.b_exp)
        neg = emo * ((1.0 / b) ** self.b_exp)
        return pos, neg

    def step(self, t):
        """Update the agent for one time step."""
        # Active agents become restrained after 12 hours
        if self.state in ["D", "P", "N"] and self.start_time is not None:
            if t - self.start_time >= 12:
                self.state = "R"
                return

        if self.state == "S":

            pos, neg = self.get_weights()
            total = pos + neg

            # Base transition probabilities
            p_d = self.model.p_sd
            p_i = self.model.p_si

            # Bias changes the effective spreading rate
            dist = abs(self.bias - 1.0)
            beta = self.model.beta_0 * ((1.0 + dist) ** self.b_exp)

            if total > 0:
                p_p = beta * (pos / total)
                p_n = beta * (neg / total)
            else:
                p_p = beta / 2.0
                p_n = beta / 2.0

            r = random.random()

            if r < p_d:
                self.state = "D"
                self.start_time = t

            elif r < p_d + p_i:
                self.state = "I"
                self.start_time = t

            elif r < p_d + p_i + p_p:
                self.state = "P"
                self.start_time = t

            elif r < p_d + p_i + p_p + p_n:
                self.state = "N"
                self.start_time = t

            else:
                self.state = "S"
