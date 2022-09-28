from tarfile import PAX_FIELDS
import streamlit as st
import scipy.stats as sp
import seaborn as sns
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px 
import plotly.figure_factory as ff


num_variates = 5000
st.header('IOT \~probabilistic\~ analysis')
st.text('Samsara (IoT) unit economics vary based on the volume of the cars they sell. ' )
st.text('From conversations with customers and their IPO roadshow, we have \n a general sense  of how they get 96% of their revenue -- from two products:\n Telematics and Vehicle Safety')

vehicle_safety_tab, telematics_tab = st.tabs(["Vehicle Safety", "Telematics"])
with vehicle_safety_tab:
    st.write("First, lets parameterize a beta distribution for their Vehicle Safety Product. Convos we've had centers price around $41 per car, skewing higher. ")
    with st.expander('Adjustments for Vehicle Safety ASP distribution:'):
        vehicle_safety_alpha = st.slider("Select the Alpha Parameter (Think right skew)", min_value=1,max_value=20,value=7)

        vehicle_safety_beta = st.slider("Select the Beta Parameter (Think left skew)", min_value=1,max_value=20,value=2)
        vehicle_safety_dist = sp.beta(vehicle_safety_alpha,vehicle_safety_beta,loc=40,scale=2).rvs(num_variates)

    fig = ff.create_distplot([vehicle_safety_dist],group_labels=['Vehicle Safety ASP'],# colors=colors,
                            bin_size=.05, show_rug=True)
    fig.update_layout(title_text='Distribution of Vehicle Safety ASP among customers')
    st.plotly_chart(fig)
with telematics_tab:
    st.write("Second, lets parameterize a beta distribution for their Telematics Product. Convos we've had centers price around $39 per car, skewing lower. ")
    with st.expander('Adjustments for Telematics ASP distribution:'):
        telematics_alpha = st.slider("Select the Alpha Parameter for Telematics Dist(Think right skew)", min_value=1,max_value=20, value= 2)

        telematics_beta = st.slider("Select the Beta Parameter for Telematics Dist (Think left skew)", min_value=1,max_value=20,value=6)
        telematics_dist = sp.beta(telematics_alpha,telematics_beta,loc=38,scale=1.5).rvs(num_variates)

    fig = ff.create_distplot([telematics_dist],group_labels=['Telematics ASP'],# colors=colors,
                            bin_size=.05, show_rug=True)
    fig.update_layout(title_text='Distribution of Telematics ASP among customers')
    st.plotly_chart(fig)
st.write("If a customer gets both Safety and Telematics, then the resulting distribution of ARR per car is:")
asp_dist = telematics_dist*12 + vehicle_safety_dist*12
fig = ff.create_distplot([asp_dist],group_labels=['Total ASP per car'],# colors=colors,
                        bin_size=.1, show_rug=True)
fig.update_layout(title_text='Distribution of IOT ARR per car')
st.plotly_chart(fig)


st.write('How big are IoTs customers?')
st.write("There's around 12.5 million commerical vehicles just in the US -- we can parameterize this as a *fat tailed t-distribution*")

with st.expander("parameters for Student-T distribution"):
    stu_t_dof = st.slider("Select the degree of freedom parameter for the Student-T dist",min_value=3,max_value=100,value=4)
    stu_t_mean = st.slider("Select # of commerical cars (in millions) accessible by IoT",min_value=5,max_value=60,value=12)
    total_cars_t = sp.t(stu_t_dof,loc=stu_t_mean).rvs(num_variates)
fig = ff.create_distplot([total_cars_t],group_labels=['Total Number of Cars'],# colors=colors,
                        bin_size=.1, show_rug=True)
fig.update_layout(title_text='Distribution of total cars as potential IOT endpoints')
st.plotly_chart(fig)

st.write("So we can get the total ARR opporunity for IOT (in Billions):")
total_arr_for_iot = np.multiply(asp_dist,total_cars_t)/1000 
fig = ff.create_distplot([total_arr_for_iot],group_labels=['Total ARR accessible to IoT'],bin_size=1/10,show_hist=False,)# colors=colors, show_rug=True)
fig.update_layout(title_text='Total ARR possible for IoT')
#fig.update_traces(line={'size':10})
st.plotly_chart(fig)

st.write("Currently IOT has ~650 mn of ARR. About 5% of the market. ")

##combined chart. Not fun unless u include variance! 
#fig = ff.create_distplot([telematics_dist,vehicle_safety_dist],group_labels=['Telematics ASP',"Vehicle Safety ASP"],# colors=colors,
#                            bin_size=.05, show_rug=True)
#fig.update_layout(title_text='ASP distributions among customers')
#st.plotly_chart(fig)


#make a plot of the total ARR for IOT
# 
def plotARRforIOT(ARR):
    fig = px.histogram(ARR, x=ARR, nbins=100, title='Total ARR for IoT')
    fig.update_xaxes(title_text='Total ARR for IoT (in Billions)')
    fig.update_yaxes(title_text='Number of Customers')
    st.plotly_chart(fig)



plotARRforIOT(total_arr_for_iot)


