import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from model import SDPNRIModel
import parameters as p

plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 11


def calculate_peak_attack_rate(history):
    p_vals = np.array(history['P'])
    n_vals = np.array(history['N'])
    active = p_vals + n_vals
    return (np.max(active) / p.num_agents) * 100.0


def run_parameter_sweeps():
    results = []
    total = len(p.polarization_exponents) * len(p.debunker_rates)
    done = 0

    print(f"Running {total} scenarios...\n")

    for b_exp in p.polarization_exponents:
        threshold = p.calculate_psi_threshold_for_r0(b_exp)
        print(f"b={b_exp:.1f}: threshold={threshold * 100:.2f}%")
    print()

    for b_exp in p.polarization_exponents:
        for p_si in p.debunker_rates:

            peaks = []

            for _ in range(p.num_runs):

                model = SDPNRIModel(
                    num_agents=p.num_agents,
                    p_si=p_si,
                    b_exp=b_exp,
                    e_exp=1.0,
                    beta=p.beta_0
                )

                history = model.run_simulation(steps=p.simulation_hours)

                peaks.append(calculate_peak_attack_rate(history))

            avg_peak = np.mean(peaks)

            beta = p.beta_0 * ((1.0 + 0.6) ** b_exp)
            exit = p.mu + p_si
            r0 = beta / exit

            results.append({
                'b_exponent': b_exp,
                'debunker_rate': p_si,
                'debunker_pct_label': f"{round(p_si * 100, 1)}%",
                'avg_peak_attack_pct': round(avg_peak, 2),
                'R0': round(r0, 3)
            })

            done += 1

            print(f"{done}/{total} | b={b_exp} | p_si={p_si:.3f} | peak={avg_peak:.2f}%")

    df = pd.DataFrame(results)

    df.to_csv("debunker_threshold_results.csv", index=False)

    print("\nSaved debunker_threshold_results.csv")

    return df


def generate_primary_plots(df):
    print("\nGenerating figure 1...")

    fig1, ax1 = plt.subplots(figsize=(9, 6), dpi=300)

    colors = {0.0: '#2b5c8f', 0.5: '#2a9d8f', 1.0: '#e76f51', 2.0: '#d62828'}
    markers = {0.0: 'o', 0.5: 's', 1.0: '^', 2.0: 'D'}

    for b_exp in p.polarization_exponents:

        subset = df[df['b_exponent'] == b_exp].sort_values('debunker_rate')

        x = subset['debunker_rate'] * 100.0
        y = subset['avg_peak_attack_pct']

        ax1.plot(
            x,
            y,
            label=f'Polarization b = {b_exp}',
            color=colors.get(b_exp, '#333333'),
            marker=markers.get(b_exp, 'o'),
            linewidth=2.5,
            markersize=7
        )

        threshold = p.calculate_psi_threshold_for_r0(b_exp) * 100.0

        if b_exp == 2.0 and threshold > 0:

            ax1.axvline(
                x=threshold,
                color='#d62828',
                linestyle='--',
                linewidth=1.5,
                label=f'$R_0 \\leq 1.0$ Threshold (b=2.0, {threshold:.1f}%)'
            )

    ax1.set_title(
        "Rumor Peak Attack Rate vs. Debunker Rate ($p_{SI}$) with $R_0 \\leq 1.0$ Threshold",
        fontsize=13,
        fontweight='bold',
        pad=15
    )

    ax1.set_xlabel("Debunker Rate ($p_{SI}$) [%]", fontsize=11, labelpad=10)
    ax1.set_ylabel("Peak Active Rumor Population ($P + N$) [%]", fontsize=11, labelpad=10)

    ax1.set_ylim(0, max(df['avg_peak_attack_pct']) + 10)

    ax1.legend(
        frameon=True,
        facecolor='white',
        framealpha=0.9,
        fontsize=10
    )

    plt.tight_layout()

    fig1.savefig(
        "figure1_debunker_sweeps.png",
        dpi=300
    )

    print("Saved figure1_debunker_sweeps.png")


def plot_critical_threshold_curve():
    print("\nGenerating Figure: Critical Debunker Threshold Curve...")

    fig, ax = plt.subplots(figsize=(9, 5), dpi=300)

    b_values = p.polarization_exponents
    
    thresholds = [
        p.calculate_psi_threshold_for_r0(b) * 100.0
        for b in b_values
    ]

    purple_color = '#5c2250'
    ax.plot(
        b_values,
        thresholds,
        marker='o',
        color=purple_color,
        linewidth=3.0,
        markersize=9,
        label='Required $I^*$'
    )
    ax.fill_between(b_values, thresholds, color=purple_color, alpha=0.15)

    ax.set_title(
        "Critical Debunker Threshold ($I^*$) as a Function of Political Bias ($b$)",
        fontsize=13,
        fontweight='bold',
        pad=15
    )
    ax.set_xlabel("Political Polarization Exponent ($b$)", fontsize=11, labelpad=10)
    ax.set_ylabel("Required Debunker Threshold ($I^*$) [%]", fontsize=11, labelpad=10)

    ax.set_xticks(b_values)
    ax.grid(True, linestyle='--', alpha=0.5)

    ax.legend(
        frameon=True,
        facecolor='white',
        framealpha=0.9,
        fontsize=10,
        loc='upper left'
    )

    plt.tight_layout()
    fig.savefig("figure2_critical_threshold_curve.png", dpi=300)
    print("Saved figure2_critical_threshold_curve.png")


def plot_baseline_compartment_evolution(p_si_target=p.p_si_empirical):

    print("\nGenerating figure 2...")

    fig, axes = plt.subplots(
        2,
        2,
        figsize=(14, 10),
        dpi=300,
        sharex=True,
        sharey=True
    )

    axes = axes.flatten()

    colors = {
        'S': '#2b5c8f',
        'D': '#e9c46a',
        'P': '#e76f51',
        'N': '#d62828',
        'I': '#2a9d8f',
        'R': '#6c757d'
    }

    labels = {
        'S': 'Susceptible (S)',
        'D': 'Doubtful (D)',
        'P': 'Positive Rumor (P)',
        'N': 'Negative Rumor (N)',
        'I': 'Debunked/Immune (I)',
        'R': 'Restrained (R)'
    }

    for idx, b_exp in enumerate(p.polarization_exponents):

        ax = axes[idx]

        model = SDPNRIModel(
            num_agents=p.num_agents,
            p_si=p_si_target,
            b_exp=b_exp,
            e_exp=1.0,
            beta=p.beta_0
        )

        history = model.run_simulation(
            steps=p.simulation_hours
        )

        hours = list(range(p.simulation_hours + 1))

        for state in ['S', 'D', 'P', 'N', 'I', 'R']:

            pct_history = [
                (count / p.num_agents) * 100.0
                for count in history[state]
            ]

            ax.plot(
                hours,
                pct_history,
                label=labels[state],
                color=colors[state],
                linewidth=2
            )

        ax.set_title(
            f"Polarization Exponent $b = {b_exp}$",
            fontsize=12,
            fontweight='bold'
        )

        ax.set_ylabel(
            "Population Share (%)",
            fontsize=10
        )

        ax.set_ylim(0, 100)

        ax.grid(
            True,
            linestyle='--',
            alpha=0.6
        )

    axes[2].set_xlabel("Time (Hours)", fontsize=11)
    axes[3].set_xlabel("Time (Hours)", fontsize=11)

    handles, legend_labels = axes[0].get_legend_handles_labels()

    fig.legend(
        handles,
        legend_labels,
        loc='upper center',
        bbox_to_anchor=(0.5, 1.02),
        ncol=6,
        frameon=True,
        facecolor='white',
        fontsize=10
    )

    plt.suptitle(
        f"72-Hour SDPNRI Compartment Dynamics across Polarization Levels (Debunker Rate $p_{{SI}} = {round(p_si_target*100, 1)}\\%$)",
        y=1.05,
        fontsize=14,
        fontweight='bold'
    )

    plt.tight_layout()

    fig.savefig(
        "figure2_compartment_evolution_grid.png",
        dpi=300,
        bbox_inches='tight'
    )

    print("Saved figure2_compartment_evolution_grid.png")


def plot_recommended_threshold_compartment_evolution():

    print("\nGenerating figure 3...")

    fig, axes = plt.subplots(
        2,
        2,
        figsize=(14, 10),
        dpi=300,
        sharex=True,
        sharey=True
    )

    axes = axes.flatten()

    colors = {
        'S': '#2b5c8f',
        'D': '#e9c46a',
        'P': '#e76f51',
        'N': '#d62828',
        'I': '#2a9d8f',
        'R': '#6c757d'
    }

    labels = {
        'S': 'Susceptible (S)',
        'D': 'Doubtful (D)',
        'P': 'Positive Rumor (P)',
        'N': 'Negative Rumor (N)',
        'I': 'Debunked/Immune (I)',
        'R': 'Restrained (R)'
    }

    for idx, b_exp in enumerate(p.polarization_exponents):

        ax = axes[idx]

        p_si_rec = p.calculate_psi_threshold_for_r0(b_exp)

        model = SDPNRIModel(
            num_agents=p.num_agents,
            p_si=p_si_rec,
            b_exp=b_exp,
            e_exp=1.0,
            beta=p.beta_0
        )

        history = model.run_simulation(
            steps=p.simulation_hours
        )

        hours = list(range(p.simulation_hours + 1))

        for state in ['S', 'D', 'P', 'N', 'I', 'R']:

            pct_history = [
                (count / p.num_agents) * 100.0
                for count in history[state]
            ]

            lw = 3.0 if state == 'I' else 1.8

            ax.plot(
                hours,
                pct_history,
                label=labels[state],
                color=colors[state],
                linewidth=lw
            )

        ax.set_title(
            f"Polarization $b = {b_exp}$ | Theoretical $p_{{SI}} = {round(p_si_rec*100, 2)}\\%$",
            fontsize=11,
            fontweight='bold'
        )

        ax.set_ylabel(
            "Population Share (%)",
            fontsize=10
        )

        ax.set_ylim(0, 100)

        ax.grid(
            True,
            linestyle='--',
            alpha=0.6
        )

    axes[2].set_xlabel("Time (Hours)", fontsize=11)
    axes[3].set_xlabel("Time (Hours)", fontsize=11)

    handles, legend_labels = axes[0].get_legend_handles_labels()

    fig.legend(
        handles,
        legend_labels,
        loc='upper center',
        bbox_to_anchor=(0.5, 1.02),
        ncol=6,
        frameon=True,
        facecolor='white',
        fontsize=10
    )

    plt.suptitle(
        "72-Hour SDPNRI Compartment Dynamics at Theoretical $R_0 \\leq 1.0$ Debunker Intervention Rates",
        y=1.05,
        fontsize=14,
        fontweight='bold'
    )

    plt.tight_layout()

    fig.savefig(
        "figure3_recommended_threshold_dynamics.png",
        dpi=300,
        bbox_inches='tight'
    )

    print("Saved figure3_recommended_threshold_dynamics.png")


if __name__ == "__main__":

    results = run_parameter_sweeps()

    generate_primary_plots(results)

    plot_critical_threshold_curve()

    plot_baseline_compartment_evolution(
        p.p_si_empirical
    )

    plot_recommended_threshold_compartment_evolution()

    print("\nDone.")
