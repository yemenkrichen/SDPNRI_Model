num_agents = 482
simulation_hours = 72

# Hourly transition rates
p_sd = 0.00332
p_si_empirical = 0.03836
beta_0 = 0.05624

cooldown_hours = 12.0
mu = 1.0 / cooldown_hours


def calculate_psi_threshold_for_r0(b_exp, bias_dist=0.6, beta=beta_0, mu=mu):
    beta_eff = beta * ((1.0 + bias_dist) ** b_exp)
    p_si_needed = beta_eff - mu
    return max(0.0, p_si_needed)


# Parameter sweeps
debunker_rates = [0.01, 0.023, 0.03836, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30]
polarization_exponents = [0.0, 0.5, 1.0, 2.0]

num_runs = 20
