from locale import normalize
import re
import streamlit as st
import scipy.stats as sp
import seaborn as sns
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.figure_factory as ff


def plot_distribution(dist_variates, title=""):
    fig = plt.figure(figsize=(10, 4))
    sns.distplot(dist_variates, bins=100,norm_hist=True)
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
st.markdown(
    "The Aurora driver is priced $0.50 per mile, equal to trucking labor. Long haul truck avg speed is 60 mph. It's a question of utilization.  ")
opp_twenty_four, opp_twenty_five, opp_twenty_six = st.tabs(
    ["2024 ARR build", "2025 ARR build", "2026 ARR build"])

with opp_twenty_four:
    st.markdown("By 2024, Aurora plans to fully launch the Aurora Driver, with about ~100-250 trucks. Trucks and utilization are distributed as follows:")
    with st.expander("Distributions for 2024:"):
    # distribution of trucks
        twenty_four_truck_mean = st.slider(
            "Expected amount of trucks in 2024", min_value=50, max_value=400, value=100)
        twenty_four_truck_dist = sp.t(
            100, loc=twenty_four_truck_mean).rvs(num_variates)
        plot_distribution(twenty_four_truck_dist,
                        f"Distribution of Trucks in 2024")
        # distribution of loads
        st.markdown(
            'By 2024, Aurora plans to be ~20% utilized. Truckers maximizing their ELD time are on the road 35\% of the year. ')
        twenty_four_loads_alpha = st.slider(
            'Positive bias on how many hours/year Aurora drivers are on the road in 2024 ', min_value=1, max_value=20, value=3)
        twenty_four_loads_beta = st.slider(
            'Negative bias on how many hours/year Aurora drivers are on the road in 2024 ', min_value=1, max_value=20, value=6)
        twenty_four_loads_var = st.slider(
            "Dispersion on how many hours/year Aurora drivers are on the road in 2024", min_value=0.01, max_value=0.2, value=0.1)
        twenty_four_util_dist = sp.beta(
            twenty_four_loads_alpha, twenty_four_loads_beta, loc=0.2, scale=twenty_four_loads_var).rvs(num_variates)
        plot_distribution(twenty_four_util_dist,
                        f"Distribution of Loads in 2024 (thousands), Mean: {round(twenty_four_util_dist.mean(),2)}")
        # distribution of revenue
        st.markdown(
            "This results in the following expected distribution of revenue for AUR in 2024: ")
        twenty_four_revenue = ( twenty_four_util_dist*365*24 )* (60*0.5)* twenty_four_truck_dist # % truck utilization * hours in year * 60 mph avg at 50c * trucks 

        plot_distribution(twenty_four_revenue,
                        f"Distribution of AUR 2024 ARR($mns), mean:{round(twenty_four_revenue.mean(),2)}")

with opp_twenty_five:
    st.markdown(
        "By 2025, Aurora plans to fully launch the Aurora Driver, with about ~250 trucks. Trucks are distributed as below:")
    # distribution of trucks
    with st.expander("Distributions for 2025:"):

        twenty_five_truck_mean = st.slider(
            "Expected amount of trucks in 2025", min_value=50, max_value=1000, value=500)
        twenty_five_truck_dist = sp.t(
            100, loc=twenty_five_truck_mean).rvs(num_variates)
        plot_distribution(twenty_five_truck_dist,
                        f"Distribution of Trucks in 2025")
        # distribution of loads
        st.markdown(
            'By 2025, Aurora plans to be 25\% utilized')
        twenty_five_loads_alpha = st.slider(
            'Positive bias on how many hours/year Aurora drivers are on the road in 2025 ', min_value=1, max_value=20, value=3)
        twenty_five_loads_beta = st.slider(
            'Negative bias on how many hours/year Aurora drivers are on the road  in 2025 ', min_value=1, max_value=20, value=3)
        twenty_five_loads_var = st.slider(
            "Dispersion on how many hours/year Aurora drivers are on the road in 2025", min_value=0.01, max_value=0.2, value=0.1)
        twenty_five_util_dist = sp.beta(
            twenty_five_loads_alpha, twenty_five_loads_beta, loc=.2, scale=twenty_five_loads_var).rvs(num_variates)
        plot_distribution(twenty_five_util_dist,
                        f"Distribution of truck utilization in 2025 (thousands), Mean: {round(twenty_five_util_dist.mean(),2)}")
        # distribution of revenue
        st.markdown(
            "This results in the following expected distribution of revenue for AUR in 2025:")
        twenty_five_revenue = ( twenty_five_util_dist*365*24 )* (60*0.5)* twenty_five_truck_dist *10**-6# % truck utilization * hours in year * 60 mph avg at 50c * trucks 
        plot_distribution(twenty_five_revenue,
                        f"Distribution of AUR 2025 ARR($mns), mean:{round(twenty_five_revenue.mean(),2)}")

with opp_twenty_six:
    with st.expander("Distributions for 2026:"):
        st.markdown(
            "By 2026, Aurora plans to fully launch the Aurora Driver, with about 1000 trucks. Trucks are distributed as below:")
        # distribution of trucks
        twenty_six_truck_mean = st.slider(
            "Expected amount of trucks in 2026", min_value=50, max_value=3000, value=1550)
        twenty_six_truck_dist = sp.t(
            100, loc=twenty_six_truck_mean).rvs(num_variates)
        plot_distribution(twenty_six_truck_dist, f"Distribution of Trucks in 2026")
        # distribution of loads
        st.markdown('By 2026, Aurora plans to mass market at ~40\% utilization. Average LTL load in southern US is 500 miles')
        twenty_six_loads_alpha = st.slider(
            'Positive bias on on how many hours/year Aurora drivers are on the road  in 2026 ', min_value=1, max_value=20, value=8)
        twenty_six_loads_beta = st.slider(
            'Negative bias on how many hours/year Aurora drivers are on the road  in 2026 ', min_value=1, max_value=20, value=3)
        twenty_six_loads_var = st.slider(
            "Dispersion on how many hours/year Aurora drivers are on the road  in 2026",  min_value=0.01, max_value=0.2, value=0.1)
        twenty_six_util_dist = sp.beta(twenty_six_loads_alpha, twenty_six_loads_beta,
                                    loc=.4, scale=twenty_six_loads_var).rvs(num_variates)
        plot_distribution(twenty_six_util_dist,
                        f"Distribution of Utilization in 2026 (thousands), Mean: {round(twenty_six_util_dist.mean(),2)}")
        # distribution of revenue
        st.markdown(
            "This results in the following expected distribution of revenue for AUR in 2026:")
        twenty_six_revenue = ( twenty_six_util_dist*365*24 )* (60*0.5)* twenty_six_truck_dist *10**-6# % truck utilization * hours in year * 60 mph avg at 50c * trucks 

        plot_distribution(
            twenty_six_revenue, f"Distribution of AUR 2026 ARR ($mns), mean:{round(twenty_six_revenue.mean(),2)}")


st.markdown("Taking the fully diluted market cap of AUR (~2.6 bn), we can take the 2026 Price to ARR multiple Distribution")

plot_distribution((2.6*1000)/twenty_six_revenue,
                  f'Price/2026 ARR multiple distribution: Mean:{round(np.mean((2.6*1000)/ twenty_six_revenue),2)}')

st.header("The Cash Burn:")

st.markdown("Aurora has about 1.378 bn in cash, burning about 210 mn a quarter. After attending their investor day, they plan to significantly ramp up their S&M spend and keep R&D flat. Here's some ways that can play out:")
burn22, burn23, burn24, burn25, burn26 = st.tabs(
    ['2022 burn', "2023 burn", "2024 burn", "2025 burn", "2026 burn"])
with burn22:
    with st.expander("Burn distributions for 2022:"):

        st.markdown(
            "R&D spend is about 180 mn in Q2. Modelling it out for the rest of the year: ")
        rnd22 = st.slider("expected R&D burn ($mns) in 2H 2022",
                        min_value=300, max_value=500, value=420)
        rnd22_dist = sp.t(100, loc=rnd22).rvs(num_variates)
        sm22 = st.slider("expected S&GA burn ($mns) in 2H 2022",
                        min_value=40, max_value=80, value=62)
        sm22_dist = sp.t(100, loc=sm22).rvs(num_variates)
        st.markdown("This puts the opex burn in 2022 at:")
        opex22_dist = rnd22_dist+sm22_dist
        plot_distribution(opex22_dist, "Opex loss in 2022")
with burn23:
    with st.expander("Burn distributions for 2023:"):

        st.markdown("R&D spend supposed to stay constant in 2023: ")
        rnd23 = st.slider("expected R&D burn ($mns) in 2023",
                        min_value=400, max_value=1000, value=720)
        rnd23_dist = sp.t(100, loc=rnd23).rvs(num_variates)
        sm23 = st.slider("expected S&GA burn ($mns) in 2023",
                        min_value=120, max_value=160, value=130)
        sm23_dist = sp.t(100, loc=sm23).rvs(num_variates)
        st.markdown("This puts the opex burn in 2022 at:")
        opex23_dist = rnd23_dist+rnd23_dist
        plot_distribution(opex23_dist, "Opex loss in 2023")
with burn24:
    with st.expander("Burn distributions for 2024:"):

        st.markdown(
            "R&D spend likely gets cut in 2024, but with S&M rising as loads need to be met. ")
        rnd24 = st.slider("expected R&D burn ($mns) in 2024",
                        min_value=300, max_value=1000, value=700)
        rnd24_dist = sp.t(100, loc=rnd24).rvs(num_variates)
        sm24 = st.slider("expected S&GA burn ($mns) in 2024",
                        min_value=100, max_value=250, value=160)
        sm24_dist = sp.t(100, loc=sm24).rvs(num_variates)
        st.markdown("This puts the opex burn in 2024 at:")
        opex24_dist = rnd24_dist+sm24_dist
        plot_distribution(opex24_dist, "Opex loss in 2024")

with burn25:
    with st.expander("Burn distributions for 2025:"):

        st.markdown(
            "If AUR is able to go to market, I  that they'll focus getting this out, and keeping expenses flat")
        rnd25 = st.slider("expected R&D burn ($mns) in 2025",
                        min_value=300, max_value=1000, value=700)
        rnd25_dist = sp.t(100, loc=rnd25).rvs(num_variates)
        sm25 = st.slider("expected S&GA burn ($mns) in 2025",
                        min_value=100, max_value=250, value=160)
        sm25_dist = sp.t(100, loc=sm25).rvs(num_variates)
        st.markdown("This puts the opex burn in 2025 at:")
        opex25_dist = rnd25_dist+sm25_dist
        plot_distribution(opex25_dist, "Opex loss in 2025")

with burn26:
    with st.expander("Burn distributions for 2026"):
        st.markdown(
            "Similiarly with 2025, I wager that they'll focus getting this out, and keeping expenses flat")
        rnd26 = st.slider("expected R&D burn ($mns) in 2026",
                        min_value=300, max_value=1000, value=700)
        rnd26_dist = sp.t(100, loc=rnd26).rvs(num_variates)
        sm26 = st.slider("expected S&GA burn ($mns) in 2026",
                        min_value=100, max_value=250, value=160)
        sm26_dist = sp.t(100, loc=sm26).rvs(num_variates)
        st.markdown("This puts the opex burn in 2026 at:")
        opex26_dist = rnd26_dist+sm26_dist
        plot_distribution(opex25_dist, "Opex loss in 2026")

st.markdown(
    "Summing the opex distributions together, we get the following expected total burn over 2026:"
    )
total_burn = opex22_dist + opex23_dist+opex24_dist + opex25_dist + opex26_dist
with st.expander("Total cash spent in operating expenses by 2026:"):
    plot_distribution(total_burn, f"Expected cash spent in operating expenses by 2026, mean: {round(total_burn.mean(),2)}")

st.header("EBITDA Profitability:")
st.markdown("Using what we've modelled, by 2025, can we expect to see EBITDA profitability? ")
ebitda_2025 = twenty_five_revenue - opex25_dist
with st.expander("2025  Adj EBITDA distribution: "):
    plot_distribution(ebitda_2025,f"Expected EBITDA in 2025. Mean:{round(ebitda_2025.mean(),2)}")

st.markdown("This puts the Price / EBITDA in 2026?")
ebitda_2026 = twenty_six_revenue - opex26_dist
price26_ebitda_dist =(2.6 * 10**3) / ebitda_2026
plot_distribution(price26_ebitda_dist, f"Expected Price/ 2026 EBITDA. Mean: {round(ebitda_2026.mean(),2)}")


st.header("Incorporating a catastrophe")
st.markdown("Self driving trucking is hard, and it might not take much to get them banned off the roads if there's a catastrophe, where AUR makes no revenue for a year. ")

catas_mean = st.slider("Mean Probability of a disaster per year",min_value=0.001,max_value=0.2,value=0.005 )
prob_catas = (1 -catas_mean)**4 #2023,2024,2025,2026
weighted_ARR_multiple =  ((2.6*1000) /(prob_catas *twenty_six_revenue))
st.metric("Probability of no disaster in four years:", str(round(prob_catas,2)*100) + "%")
plot_distribution( weighted_ARR_multiple, "Disaster adjusted 2026 P/ARR multiple")


