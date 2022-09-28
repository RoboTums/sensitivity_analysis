from locale import normalize
import re
import streamlit as st
import scipy.stats as sp
import seaborn as sns
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")


def plot_distribution(dist_variates, title="",secondary_y=None):
    #dist_variates = dist_variates/dist_variates.sum()
    fig = plt.figure(figsize=(10, 4))
    if secondary_y is None:

        sns.distplot(dist_variates, bins=100,norm_hist=True)

        fig.suptitle(title, fontsize=16)
        return st.pyplot(fig)
    else:
        for var in [dist_variates,secondary_y]:
            sns.distplot(var, bins=100,norm_hist=True)

        fig.suptitle(title, fontsize=16)    
        return st.pyplot(fig)

sns.set_style('darkgrid')
num_variates = 5000
st.header('AUR Monte Carlo sensitivity analysis')
st.markdown('Aurora\'s stock heavily relies on a series of events going right, which I model out with monte carlo sims below.')
st.markdown("""
    There\'s three parts to the model below: 
    1. The opporunity: where we look at how much ARR + EBITDA AUR can make when their driver launches,  
    2. the cash burn: where we factor in delays and expected cash burn given their present circumstance
    3. the catastrophe: Autonomous driving can and has gone poorly. Here's where fat tails emerge. 
    
    All distirbutions have fat tails and excess kurtosis, and only  in some special choices or parameters resemble normal distributions.   
    """)
st.header('The Opportunity')

opp_truck,opp_rates,opp_util = st.tabs(["#Trucks build","rate build",'utilization build'])

with opp_truck:
    with st.expander("How many Trucks will AUR power?:"):
        twenty_four_truck_mean = st.slider(
            "Expected amount of trucks", min_value=50, max_value=10000, value=1000)
        truck_dist = sp.t(
            100, loc=twenty_four_truck_mean).rvs(num_variates)
        plot_distribution(truck_dist,
                        f"Distribution of Trucks")
        lease_to_own_pct = st.slider(
            "How many trucks are lease-to-own vs full price?", min_value=0.0, max_value=1.0, value=0.8)
        #price of lease to own
        lease_to_own_price = 20000# 20k 
        truck_own_price = 180000#180k
        fleet_cost = (lease_to_own_pct * truck_dist *lease_to_own_price  +  truck_dist * (1-lease_to_own_pct) * truck_own_price )*10**-6
        plot_distribution(fleet_cost,f"Distribution of fleet cost for AUR ($mns) , Mean:{ round(fleet_cost.mean(),2)}")

with opp_rates:
    with st.expander("How much does AUR get per mile / drive?"):
        st.markdown('AUR driver drives the speed of traffic, capped at 65 mph. Avg LTL rate is 50c /mile, but is higher on some routes')
        rates_alpha = st.slider(
            'Positive bias of rate per mile (dollars)', min_value=1, max_value=20, value=2)
        rates_beta = st.slider(
            'Negative bias of rate per mile (dollars) ', min_value=1, max_value=20, value=7)
        rate_var = st.slider(
            "Dispersion of rate per mile (dollars)",  min_value=0.01, max_value=0.2, value=0.1)
        rate_dist = sp.beta(rates_alpha, rates_beta,
                                    loc=.47, scale=rate_var).rvs(num_variates)
        plot_distribution(rate_dist,
                        f"Distribution of rate per mile (dollars), Mean: {round(rate_dist.mean(),2)}")
        mph_a = st.slider(
            'Positive bias of avg mph', min_value=1, max_value=20, value=2)
        mph_b = st.slider(
            'Negative bias of avg mph ', min_value=1, max_value=20, value=18)
        mph_var = st.slider(
            "Dispersion of avg mph",  min_value=1, max_value=10, value=2)
        mph_dist = sp.beta(mph_a, mph_b,
                                    loc=58, scale=mph_var).rvs(num_variates)
        plot_distribution(mph_dist,
                        f"Distribution of ravg mph, Mean: {round(mph_dist.mean(),2)}")
with opp_util:
    with st.expander("How much will these trucks get utilized?"):
        st.markdown('By 2026, Aurora plans to mass market at ~60\% utilization. Average LTL load in southern US is 500 miles')
        twenty_six_loads_alpha = st.slider(
            'Positive bias on on how many hours/year Aurora drivers are on the road  ', min_value=1, max_value=20, value=8)
        twenty_six_loads_beta = st.slider(
            'Negative bias on how many hours/year Aurora drivers are on the road  ', min_value=1, max_value=20, value=3)
        twenty_six_loads_var = st.slider(
            "Dispersion on how many hours/year Aurora drivers are on the road ",  min_value=0.01, max_value=0.2, value=0.1)
        twenty_six_util_dist = sp.beta(twenty_six_loads_alpha, twenty_six_loads_beta,
                                    loc=.4, scale=twenty_six_loads_var).rvs(num_variates)
        plot_distribution(twenty_six_util_dist,
                        f"Distribution of Utilization, Mean: {round(twenty_six_util_dist.mean(),2)}")

st.markdown("All of these inputs imply the following distribution of revenue:")
revenue_dist = twenty_six_util_dist* rate_dist * mph_dist*truck_dist * 365 *24 * 10**-6
plot_distribution(revenue_dist, f"Distribution of annual revenue ($mns), mean: {round(revenue_dist.mean(),2)}")

st.markdown('The distribution of years to pay off their trucks, with selected margin below is:')
ebitda_margin = st.slider(
            'AUR scale adj EBITDA margin ', min_value=0.0, max_value=1.0, value=.15)
days_to_payoff = fleet_cost / (revenue_dist* ebitda_margin )
humans_payoff_time = fleet_cost / (0.3* rate_dist * mph_dist*truck_dist * 365 *24 * 10**-6 * (ebitda_margin-0.04))
st.markdown("Payoff time for the fleet compared to working with humans(orange) vs AI drivers (Blue):")
plot_distribution(days_to_payoff,f'years to pay off fleet: mean: {round(days_to_payoff.mean(),2)}',humans_payoff_time)

