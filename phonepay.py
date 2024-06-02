import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import psycopg2
import plotly.express as ps
import requests
import json

#creating dataframes

#SQL connection
mydb=psycopg2.connect(host="localhost",
                      user="postgres",
                      port="5432",
                      database="Phonepe_Data",
                      password="12345678")
cursor=mydb.cursor()

#aggregated_transaction_dataframe

cursor.execute("SELECT * FROM aggregated_transaction")
mydb.commit()
table1=cursor.fetchall()
Aggregated_transaction=pd.DataFrame(table1,columns=("States","Years","Quarter","Transaction_type","Transaction_count","Transaction_amount"))

#aggregated_user_dataframe

cursor.execute("SELECT * FROM aggregated_user")
mydb.commit()
table2=cursor.fetchall()
Aggregated_user=pd.DataFrame(table2,columns=("States","Years","Quarter","Brands","Transaction_count","Percentage"))

#map_transaction_dataframe

cursor.execute("SELECT * FROM map_transaction")
mydb.commit()
table3=cursor.fetchall()
Map_transaction=pd.DataFrame(table3,columns=("States","Years","Quarter","Districts","Transaction_count","Transaction_amount"))

#map_user_dataframe

cursor.execute("SELECT * FROM map_user")
mydb.commit()
table4=cursor.fetchall()
Map_user=pd.DataFrame(table4,columns=("States","Years","Quarter","Districts","Registered_users","AppOpens"))

#top_transaction1_dataframe

cursor.execute("SELECT * FROM top_transaction1")
mydb.commit()
table5=cursor.fetchall()
Top_transaction1=pd.DataFrame(table5,columns=("States","Years","Quarter","Pincodes","Transaction_count","Transaction_amount"))

#top_transaction2_dataframe

cursor.execute("SELECT * FROM top_transaction2")
mydb.commit()
table6=cursor.fetchall()
Top_transaction2=pd.DataFrame(table6,columns=("States","Years","Quarter","Districts","Transaction_count","Transaction_amount"))

#top_user1_dataframe

cursor.execute("SELECT * FROM top_user1")
mydb.commit()
table7=cursor.fetchall()
Top_user1=pd.DataFrame(table7,columns=("States","Years","Quarter","Pincodes","Registered_users"))

#top_user2_dataframe

cursor.execute("SELECT * FROM top_user2")
mydb.commit()
table8=cursor.fetchall()
Top_user2=pd.DataFrame(table8,columns=("States","Years","Quarter","Districts","Registered_users"))


#aggre_trans_year
def Transaction_amount_count_year(df,year):

    tacy=df[df["Years"]==year]
    tacy.reset_index(drop=True,inplace=True)
    tacyg=tacy.groupby('States')[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:
        plot_amount=ps.bar(tacyg,x="States",y="Transaction_amount",title=f"{year}  TRANSACTION AMOUNT",
        color_discrete_sequence=ps.colors.sequential.Blackbody,height=500,width=500)
        st.plotly_chart(plot_amount)
   
    with col2:
        plot_count=ps.bar(tacyg,x="States",y="Transaction_count",title=f"{year}  TRANSACTION COUNT",
        color_discrete_sequence=ps.colors.sequential.Bluered_r,height=500,width=500)
        st.plotly_chart(plot_count)
    
    col1,col2=st.columns(2)
    with col1:

        url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response=requests.get(url)
        data1=json.loads(response.content)
        states=[]
        for feature in data1['features']:
            states.append(feature["properties"]['ST_NM'])
        states.sort()

        fig_1 = ps.choropleth(
            tacyg,
            geojson=url,
            featureidkey='properties.ST_NM',
            locations='States',
            color='Transaction_amount',
            color_continuous_scale='twilight')

        fig_1.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig_1)
    
    with col2:

        fig_2 = ps.choropleth(
        tacyg,
        geojson=url,
        featureidkey='properties.ST_NM',
        locations='States',
        color='Transaction_count',
        color_continuous_scale='twilight')

        fig_2.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig_2)

    return tacy

#aggre_trans_year_quart
def Transaction_amount_count_year_quarter(df,quarter):

    tacy=df[df["Quarter"]==quarter]
    tacy.reset_index(drop=True,inplace=True)
    tacyg=tacy.groupby('States')[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:
                                     
        plot_amount=ps.bar(tacyg,x="States",y="Transaction_amount",title=f"{tacy['Years'].min()} {quarter} QUARTER TRANSACTION AMOUNT",
        color_discrete_sequence=ps.colors.sequential.Blackbody)
        st.plotly_chart(plot_amount)
    
    with col2:

        plot_count=ps.bar(tacyg,x="States",y="Transaction_count",title=f"{tacy['Years'].min()} {quarter} QUARTER TRANSACTION COUNT",
        color_discrete_sequence=ps.colors.sequential.Bluered_r)
        st.plotly_chart(plot_count)
    col1,col2=st.columns(2)
    with col1:

        url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response=requests.get(url)
        data1=json.loads(response.content)
        states=[]
        for feature in data1['features']:
            states.append(feature["properties"]['ST_NM'])
        states.sort()

        fig_1 = ps.choropleth(
            tacyg,
            geojson=url,
            featureidkey='properties.ST_NM',
            locations='States',
            color='Transaction_amount',
            color_continuous_scale='twilight')

        fig_1.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig_1)
    with col2:

        fig_2 = ps.choropleth(
        tacyg,
        geojson=url,
        featureidkey='properties.ST_NM',
        locations='States',
        color='Transaction_count',
        color_continuous_scale='twilight')

        fig_2.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig_2)
    return tacy

#aggre_trans_state
def Aggregated_transaction_type(df,state):
    tacy=df[df["States"]== state]
    tacy.reset_index(drop=True,inplace=True)
    tacyg=tacy.groupby('Transaction_type')[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)
    
    col1,col2=st.columns(2)
    with col1:

        plot_pie_1=ps.pie(data_frame=tacyg,names="Transaction_type",values="Transaction_amount",
                        width=500,title=f"{state.upper()} TRANSACTION_AMOUNT")
        st.plotly_chart(plot_pie_1)    
    with col2:  
        plot_pie_2=ps.pie(data_frame=tacyg,names="Transaction_type",values="Transaction_count",
                        width=500,title=f"{state.upper()} TRANSACTION_COUNT")
        st.plotly_chart(plot_pie_2)   
#agg_user_year
def Aggregated_user_brand(df,year):
    ubty=df[df["Years"]==year]
    ubty.reset_index(drop=True,inplace=True)
    aubty=pd.DataFrame(ubty.groupby("Brands")["Transaction_count"].sum())
    aubty.reset_index(inplace=True)


    plot_brands=ps.bar(aubty,x="Brands",y="Transaction_count", title=f"{year} BRANDS AND TRANSACTION COUNTS",
                    width=1000,color_discrete_sequence=ps.colors.sequential.Magenta_r)
    st.plotly_chart(plot_brands)
    
    return ubty    

#agg_user_quar
def aggregated_user_year_quarter(df,quarter):
    ubtyq=df[df["Quarter"]==quarter]
    ubtyq.reset_index(drop=True,inplace=True)
    ubtyqg=pd.DataFrame(ubtyq.groupby("Brands")["Transaction_count"].sum())
    ubtyqg.reset_index(inplace=True)

    plot_brands=ps.bar(ubtyqg,x="Brands",y="Transaction_count", title= f"QUARTER {quarter} BRANDS AND TRANSACTION COUNTS",
                width=1000,color_discrete_sequence=ps.colors.sequential.Mint_r)
    st.plotly_chart(plot_brands)


    return ubtyq
  
#aggre_user_yr_percent
def aggregated_user_year_states(df,state):
    auyqs=df[df["States"] == state]
    auyqs.reset_index(drop=True,inplace=True)
    plot_per=ps.line(auyqs,x="Brands",y="Transaction_count",hover_data="Percentage",
                    title=f"{state.upper()} TRANSACTION COUNT,BRANDS AND PERCENTAGE  OF STATES",markers=True,width=1000)
    st.plotly_chart(plot_per)


#map transaction districts
def map_transaction_district(df,state):
    macy=df[df["States"]== state]
    macy.reset_index(drop=True,inplace=True)
    macyg=macy.groupby('Districts')[["Transaction_count","Transaction_amount"]].sum()
    macyg.reset_index(inplace=True)
    col1,col2=st.columns(2)
    with col1:

        plot_bar_1=ps.bar(macyg,y="Transaction_amount",x="Districts",
                        title=f"{state.upper()} TRANSACTION_AMOUNT OF DISTRICTS",color_discrete_sequence=ps.colors.sequential.Agsunset,height=500,width=500)
        st.plotly_chart(plot_bar_1)   
    with col2:   
        plot_bar_2=ps.bar(macyg,x="Districts",y="Transaction_count",
                        title=f"{state.upper()} TRANSACTION_COUNT",color_discrete_sequence=ps.colors.sequential.Aggrnyl,height=500,width=500)
        st.plotly_chart(plot_bar_2)  

#map_user_year
def map_user_years(df,year):
    muy=df[df["Years"]==year]
    muy.reset_index(drop=True,inplace=True)
    muyg=(muy.groupby("States")[["Registered_users", "AppOpens"]].sum())
    muyg.reset_index(inplace=True)
    plot_per=ps.line(muyg,x="States",y=["Registered_users","AppOpens"],
                    title=f"{year} REGISTERED USERS AND APPOPENS OF STATES",markers=True,width=1000,height=700)
    st.plotly_chart(plot_per)

    return muy         

#map_user_quarter
def map_user_quarter(df,quarter):
    muyq=df[df["Quarter"]==quarter]
    muyq.reset_index(drop=True,inplace=True)
    muyqg=(muyq.groupby("States")[["Registered_users", "AppOpens"]].sum())
    muyqg.reset_index(inplace=True)
    plot_per=ps.line(muyqg,x="States",y=["Registered_users","AppOpens"],
                    title=f"{df['Years'].min()} {quarter} QUARTER REGISTERED USERS AND APPOPENS OF QUARTERS",markers=True,width=1000,height=700,color_discrete_sequence=ps.colors.sequential.Hot_r)
    st.plotly_chart(plot_per)

    return muyq

#map_user_year_states
def map_user_states(df,state):

    muyqs=df[df["States"]==state]
    muyqs.reset_index(drop=True,inplace=True)

    col1,col2=st.columns(2)

    with col1:
        plot_map_user1=ps.bar(muyqs,y="Registered_users",x="Districts",title=f"{state.upper()} REGISTERED USER",height=500,width=500,color_discrete_sequence=ps.colors.sequential.Bluered_r)
        st.plotly_chart(plot_map_user1)
    with col2:

        plot_map_user2=ps.bar(muyqs,y="AppOpens",x="Districts",title=f"{state.upper()} APPOPENS",height=500,width=500,color_discrete_sequence=ps.colors.sequential.amp_r)
        st.plotly_chart(plot_map_user2)

#top_transaction1 state
def top_transaction1(df,state):
    tty=df[df["States"]== state]
    tty.reset_index(drop=True,inplace=True)
    col1,col2=st.columns(2)
    with col1:

        plot_top_tran1=ps.bar(tty,x="Quarter",y="Transaction_amount",hover_data="Pincodes",title="TRANSACTION AMOUNT",height=600,width=500,color_discrete_sequence=ps.colors.sequential.Purples_r)
        st.plotly_chart(plot_top_tran1)
    with col2:

        plot_top_tran2=ps.bar(tty,x="Quarter",y="Transaction_count",hover_data="Pincodes",title="TRANSACTION COUNT",height=600,width=500,color_discrete_sequence=ps.colors.sequential.Brwnyl_r)
        st.plotly_chart(plot_top_tran2)

#top user1 year quarter
def top_user1_year_quarter(df,year):
    tuy=df[df["Years"]==year]
    tuy.reset_index(drop=True,inplace=True)
    tuyg=pd.DataFrame(tuy.groupby(["States","Quarter"])["Registered_users"].sum())
    tuyg.reset_index(inplace=True)

    plot_top_user1=ps.bar(tuyg,x="States",y="Registered_users",color="Quarter",height=1000,width=1000,
                          title=f"{year} REGISTERED USERS")
    st.plotly_chart(plot_top_user1)

    return tuy

#top_user1_year
def top_user1_state(df,state):
    tus=df[df["States"]==state]
    tus.reset_index(drop=True,inplace=True)
    plot_top_user1=ps.bar(tus,x="Quarter",y="Registered_users",hover_data="Pincodes",title=f"{state.upper()} QUARTER AND REGISTERED USERS IN TOP",height=900,width=900
                        ,color="Registered_users",color_continuous_scale=ps.colors.sequential.Pinkyl_r)
    st.plotly_chart(plot_top_user1)

#top_transaction2
def top_transaction2(df,state):
    tty=df[df["States"]== state]
    tty.reset_index(drop=True,inplace=True)
    col1,col2=st.columns(2)
    with col1:
        plot_top_tran1=ps.bar(tty,x="Quarter",y="Transaction_amount",hover_data="Districts",title="TRANSACTION AMOUNT",height=500,width=500,color_discrete_sequence=ps.colors.sequential.Greens_r)
        st.plotly_chart(plot_top_tran1)
    with col2:
        plot_top_tran2=ps.bar(tty,x="Quarter",y="Transaction_count",hover_data="Districts",title="TRANSACTION COUNT",height=500,width=500,color_discrete_sequence=ps.colors.sequential.dense_r)
        st.plotly_chart(plot_top_tran2)


#top user2 year quarter
def top_user2_year_quarter(df,year):
    tuy=df[df["Years"]==year]
    tuy.reset_index(drop=True,inplace=True)
    tuyg=pd.DataFrame(tuy.groupby(["States","Quarter"])["Registered_users"].sum())
    tuyg.reset_index(inplace=True)

    plot_top_user2=ps.bar(tuyg,x="States",y="Registered_users",color="Quarter",height=1000,width=1000,
                        title=f"{year} REGISTERED USERS")
    st.plotly_chart(plot_top_user2)

    return tuy
#top user2 year

def top_user2_state(df,state):
    tus=df[df["States"]==state]
    tus.reset_index(drop=True,inplace=True)
    plot_top_user2=ps.bar(tus,x="Quarter",y="Registered_users",hover_data="Districts",title=f"{state.upper()} QUARTER AND REGISTERED USERS IN TOP",height=900,width=900
                        ,color="Registered_users",color_continuous_scale=ps.colors.sequential.amp_r)
    st.plotly_chart(plot_top_user2)

#streamlit 

st.set_page_config(layout='wide')
st.title("PHONEPE DATA VISUALISATION AND EXPLORATION")

with st.sidebar:
    
    select=option_menu("Main Menu",["Home","Data Exploration"])

if select == "Home":
    pass
elif select == "Data Exploration":
    tab1,tab2,tab3,tab4=st.tabs(["Aggregated Analysis","Map Analysis","Top Analysis of Pincodes","Top analysis of Districts"])
     
    with tab1:
        analysis1=st.radio("SELECT THE ANALYSIS",["Transaction Analysis","User Analysis"])
        
        if analysis1=="Transaction Analysis":
            col1,col2=st.columns(2)
            with col1:

                years=st.slider("Select the Year",Aggregated_transaction["Years"].min(),Aggregated_transaction["Years"].max(),Aggregated_transaction["Years"].min())
            Tacyg=Transaction_amount_count_year(Aggregated_transaction,years)

            col1,col2=st.columns(2)
            with col1:

                states=st.selectbox("Select the state",Tacyg["States"].unique())
            Aggregated_transaction_type(Tacyg,states)

            col1,col2=st.columns(2)
            with col1:
                
                quarters=st.slider("Select the Quarter",Tacyg["Quarter"].min(),Tacyg["Quarter"].max(),Tacyg["Quarter"].min())
            Tacyg_quarter= Transaction_amount_count_year_quarter(Tacyg,quarters) 

            col1,col2=st.columns(2)
            with col1:

                states=st.selectbox("Select the state_type",Tacyg_quarter["States"].unique())
            Aggregated_transaction_type(Tacyg_quarter,states)


        elif analysis1=="User Analysis":

            col1,col2=st.columns(2)
            with col1:

                years=st.slider("Select Year",Aggregated_user["Years"].min(),Aggregated_user["Years"].max(),Aggregated_user["Years"].min())
            aggre_user_year=Aggregated_user_brand(Aggregated_user,years)

            col1,col2=st.columns(2)
            with col1:
                
                quarters=st.slider("Select Quarter",aggre_user_year["Quarter"].min(),aggre_user_year["Quarter"].max(),aggre_user_year["Quarter"].min())
            aggre_user_year_quarter= aggregated_user_year_quarter(aggre_user_year,quarters) 

            col1,col2=st.columns(2)
            with col1:

                states=st.select_slider("Select state_type",aggre_user_year_quarter["States"].unique())
            aggregated_user_year_states(aggre_user_year_quarter,states) 
                        

    with tab2:
        analysis2=st.radio("SELECT THE ANALYIS",["Transaction Analysis","User Analysis"])

        if analysis2=="Transaction Analysis":
            col1,col2=st.columns(2)
            with col1:

                years=st.slider("Select the year of map",Map_transaction["Years"].min(),Map_transaction["Years"].max(),Map_transaction["Years"].min())
            map_trans_year=Transaction_amount_count_year(Map_transaction,years)

            col1,col2=st.columns(2)
            with col1:

                states=st.selectbox("Select the state of map",map_trans_year["States"].unique())
            map_transaction_district(map_trans_year,states)

            col1,col2=st.columns(2)
            with col1:
                
                quarters=st.slider("Select the Quarter of map",  map_trans_year["Quarter"].min(),map_trans_year["Quarter"].max(),map_trans_year["Quarter"].min())
            map_transaction_quarter= Transaction_amount_count_year_quarter(map_trans_year,quarters) 

            col1,col2=st.columns(2)
            with col1:

                states=st.selectbox("Select the state_type of map",map_transaction_quarter["States"].unique())
            map_transaction_district(map_transaction_quarter,states)

        elif analysis2=="User Analysis":
            col1,col2=st.columns(2)
            with col1:

                years=st.slider("Select year of map",Map_user["Years"].min(),Map_user["Years"].max(),Map_user["Years"].min())
            map_user_year=map_user_years(Map_user,years)

            col1,col2=st.columns(2)
            with col1:
                
                quarters=st.slider("Select Quarter of map",map_user_year["Quarter"].min(),map_user_year["Quarter"].max(),map_user_year["Quarter"].min())
            map_user_quarters= map_user_quarter(map_user_year,quarters) 

            col1,col2=st.columns(2)
            with col1:

                states=st.select_slider("Select the state_type of map",map_user_quarters["States"].unique())
            map_user_quart_states=map_user_states(map_user_quarters,states) 
        
    
    with tab3:
        analysis3=st.radio("SELECT THE ANALYSIS",["Transaction Analysis of Pincodes","User Analysis of pincodes"])

        if analysis3=="Transaction Analysis of Pincodes":
            col1,col2=st.columns(2)
            with col1:

                years=st.slider("Select the year of top",Top_transaction1["Years"].min(),Top_transaction1["Years"].max(),Top_transaction1["Years"].min())
            top_trans1_year=Transaction_amount_count_year(Top_transaction1,years)

            col1,col2=st.columns(2)
            with col1:

                states=st.selectbox("Select the state_type of top1",top_trans1_year["States"].unique())
            top_trans1_states=top_transaction1(top_trans1_year,states) 

            col1,col2=st.columns(2)
            with col1:
                
                quarters=st.slider("Select Quarter of top",top_trans1_year["Quarter"].min(),top_trans1_year["Quarter"].max(),top_trans1_year["Quarter"].min())
            top_trans1_quarters=Transaction_amount_count_year_quarter(top_trans1_year,quarters) 
  
        elif analysis3=="User Analysis of pincodes":
            
            col1,col2=st.columns(2)
            with col1:

                years=st.slider("Select year of top",Top_user1["Years"].min(),Top_user1["Years"].max(),Top_user1["Years"].min())
            top_user1_year=top_user1_year_quarter(Top_user1,years)

            col1,col2=st.columns(2)
            with col1:

                states=st.selectbox("Select the state_type of top",top_user1_year["States"].unique())
            top_user1_state=top_user1_state(top_user1_year,states)
            
    with tab4:
        analysis4=st.radio("SELECT THE ANALYSIS",["Transaction Analysis of Districts","User Analysis of Districts"])

        if analysis4=="Transaction Analysis of Districts":
            col1,col2=st.columns(2)
            with col1:

                years=st.slider("Select the year of the top",Top_transaction2["Years"].min(),Top_transaction2["Years"].max(),Top_transaction2["Years"].min())
            top_trans2_year=Transaction_amount_count_year(Top_transaction2,years)

            col1,col2=st.columns(2)
            with col1:
                
                quarters=st.slider("Select Quarter of the top",top_trans2_year["Quarter"].min(),top_trans2_year["Quarter"].max(),top_trans2_year["Quarter"].min())
            top_trans2_quarters=Transaction_amount_count_year_quarter(top_trans2_year,quarters) 

        
            col1,col2=st.columns(2)
            with col1:

                states=st.selectbox("Select the state_type of top2",top_trans2_year["States"].unique())
            top_tran2_states=top_transaction2(top_trans2_year,states) 
   

        elif analysis4=="User Analysis of Districts":
            col1,col2=st.columns(2)
            with col1:

                years=st.slider("Select year of top2",Top_user2["Years"].min(),Top_user2["Years"].max(),Top_user2["Years"].min())
            top_user2_year=top_user2_year_quarter(Top_user2,years)

            col1,col2=st.columns(2)
            with col1:

                states=st.selectbox("Select state_type of top",top_user2_year["States"].unique())
            top_user2_state=top_user2_state(top_user2_year,states)

