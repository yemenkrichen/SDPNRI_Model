import math

baseline_bias = 1.0
bias_exponent = 1.0
emotion_exponent = 1.0

time_step = 3600

restraint_time_steps = 12
restraint_time = 12 * time_step

transition_rates = {
    "S->D": 9.24527898496082E-07,
    "S->I": 1.08632028073290E-05,
    "S->N": 1.23655606423851E-05,
    "S->P": 3.69811159398433E-06,

    "D->I": 1.62666692693338E-06,
    "D->P": 1.62666692693338E-06,

    "N->D": 5.74889537849750E-07,
    "N->I": 3.44933722709850E-07,
    "N->P": 1.83964652111920E-06,

    "P->D": 2.85040937579455E-07,
    "P->I": 5.70081875158910E-07,
    "P->N": 5.70081875158910E-07
}

transition_probabilities = {
    transition: 1.0 - math.exp(-rate * time_step)
    for transition, rate in transition_rates.items()
}

transition_probabilities["S->PN_pool"] = (
    transition_probabilities["S->P"] + transition_probabilities["S->N"]
)
