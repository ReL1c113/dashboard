# -*- coding: utf-8 -*-
"""
Spyder Editor

Piyush

This is a temporary script file.
"""
import pandas as pd
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np


st.set_page_config(page_title='Report Dashboard',layout='wide',page_icon='favicon.ico')
col1, col2, col3 = st.columns([1,2,3])


#PLOT FUNCTIONS

col1_background_color = "lightblue"
col1 = st.sidebar
col1.markdown(f"""
    <style>
        .sidebar .sidebar-content {{
            background-color: {col1_background_color},
            width: 400px;;
        }}
    </style>
""", unsafe_allow_html=True)

def wrangle(filepath):
    df=pd.read_excel(filepath,sheet_name=None)
    
    sheet_name='metrics'
    first_sheet='Sheet1'
    live='live'
    backtest='backtest'
    
    
# =============================================================================
    df_live=df[live]
    df_live['Token no.']=df_live['Unnamed: 0']
    df_live.drop(columns='Unnamed: 0',inplace=True)
    df_live.set_index('Token no.',inplace=True)
#     df_backtest=df[backtest]
#     
    df_live.dropna(inplace=True)
#     df_backtest.dropna(inplace=True)
#     
#     df_backtest['date']=df_backtest['date'].astype(str)
#     df_backtest['selltime']=df_backtest['selltime'].astype(str)
#     df_backtest['buytime']=df_backtest['buytime'].astype(str)
#     
#     df_backtest['entry_time']=pd.to_datetime(df_backtest['date']+' '+df_backtest['selltime'])
#     df_backtest['buy_time']=pd.to_datetime(df_backtest['date']+' '+df_backtest['buytime'])
#     df_live['date']=pd.to_datetime(df_live['date'])
#     df_backtest['date']=pd.to_datetime(df_backtest['date'])
#     df_live.set_index('date',inplace=True)
#     df_backtest.set_index('date',inplace=True)
#     common_dates=df_live.index.unique()
#     selected_rows_backtest=df_backtest[df_backtest.index.isin(common_dates)]
#     df_live['entrytime']=pd.to_datetime(df_live['entrytime'])
#     df_live.sort_values(by='entrytime',ascending=True,inplace=True)
#     
# =============================================================================

    
    df_sheet=df[sheet_name]
    df_sheet.fillna('     ',inplace=True)
    df_sheet[['Value','Value.2','Value.1']]=df_sheet[['Value','Value.2','Value.1']].astype(str)
    df=df[first_sheet]
    
    df.set_index('Date',inplace=True)
    df.fillna(0,inplace=True)
    
    #Creating New Column 'Difference' But Only considering columns where Actual Returns !=0
    df['Difference'] = df.apply(lambda row: row['Actual returns'] - row['Backtested returns'] if row['Actual returns'] != 0 else 0, axis=1)
    
    
    #Creating a New df whose 'Difference' value is >0.5 or<-0.5.
    empty_list=[]
    mask_positive=df[df['Difference']>0.5]
    mask_negative=df[df['Difference']<-0.5]
    empty_list.append(mask_positive)
    empty_list.append(mask_negative)
    df_slipage=pd.concat(empty_list)

# =============================================================================
# for i in range(len(df_slipage)):
#         currentcandle=df_slipage.iloc[i]
#         index=df_slipage.index
#         data1= {
#              'Backtest Selltime':selected_rows_backtest['entry_time'].loc[str(currentcandle.name)],
#              'Actual Selltime':df_live['entrytime'].loc[str(currentcandle.name)],
#              'Backtest Sellprice':selected_rows_backtest['sellprice'].loc[str(currentcandle.name)],
#              'Actual Sellprice':df_live['entryprice'].loc[str(currentcandle.name)],
#              }
#         df_comp1=pd.DataFrame(data1,index=index)
#         data2={
#             'Backtest Buytime':selected_rows_backtest['buy_time'].loc[str(currentcandle.name)],
#             'Actual Buytime':df_live['exittime'].loc[str(currentcandle.name)],
#             'Backtest Buyprice':selected_rows_backtest['buyprice'].loc[str(currentcandle.name)],
#             'Actual Buyprice':df_live['exitprice'].loc[str(currentcandle.name)],
#             }
# 
# =============================================================================

    
    #Finding Total no. of days when Trades took place
    Trade_Days=0
    for i in df['Actual returns']:
        if i!=0:
            Trade_Days=Trade_Days+1
        else:
            continue
        
    with col2:
        #Total Trade Days
        st.markdown(f"<h3 style='text-align: edge;'>Total Trade Days</h3>", unsafe_allow_html=True)
        st.header(Trade_Days)
        
        #Sum Difference
        st.markdown(f"<h3 style='text-align: edge;'>Total Slipage</h3>", unsafe_allow_html=True)
        st.header(round(df['Difference'].sum(),2))
        
        
        
        
    with col3:
        #Sum Backtested Ignoring when Actual = 0
        st.markdown(f"<h3 style='text-align: edge;'>Total Backtested return</h3>", unsafe_allow_html=True)
        for column in df.columns:
            if column == 'Backtested returns':
        # Ignore bactested when actual is 0
                column_sum = df.loc[df['Actual returns'] != 0, column].sum()
        st.header(round(column_sum,2))
       
        # Sum Actual Return
        st.markdown(f"<h3 style='text-align: edge;'>Total Actual return</h3>", unsafe_allow_html=True)
        a = round(df['Actual returns'].sum(),2)
    
        st.header(a)
        
        
    
    #BAR PLOT
    st.markdown(f"<h5 align='center'>Backtested vs Actual Returns</h5>", unsafe_allow_html=True)
    fig=px.bar(df[['Backtested returns','Actual returns']],barmode='group')
    fig.update_layout(width=900,height=400)
    st.plotly_chart(fig)
      
    
    
    with col1:
        #Initial dataframe
        st.header('DataFrame')
        st.dataframe(df)
        
        
        #High Slipage DataFrame
        st.header('High Slipage Data')
        st.dataframe(df_slipage)
    
        
    #LINEPLOT
    st.markdown(f"<h5 align='center'>Backtested vs Actual Returns</h5>", unsafe_allow_html=True)
    fig=px.line(df[['Backtested returns','Actual returns']],labels={'value':'Returns'})
    fig.update_layout(width=900,height=400,title='Line Plot')
    st.plotly_chart(fig)
    
    
    #BARPLOT
    st.markdown(f"<h5 align='center'>Difference in Return</h5>", unsafe_allow_html=True)
    fig=px.bar(np.abs(df['Difference']),labels={'value':'Difference in Positive'})
    fig.update_layout(width=900,height=400,title='BarPlot')
    st.plotly_chart(fig)
     

    st.markdown(f"<h5 style='text-align: center;'>Analytics</h5>", unsafe_allow_html=True)
    st.dataframe(df_sheet)
# =============================================================================       
#     st.markdown(f"<h5 style='text-align: center;'>Backtested Trades</h5>", unsafe_allow_html=True)
#     st.dataframe(selected_rows_backtest)
#     
#     
#     st.markdown(f"<h5 style='text-align: center;'>Slipage Trade Comparison</h5>", unsafe_allow_html=True)
#     st.dataframe(df_comp1)
#     st.dataframe(df_comp2)
# =============================================================================

    st.markdown(f"<h5 style='text-align: center;'>Actual Trades</h5>", unsafe_allow_html=True)
    st.dataframe(df_live)

        
    return df


option = ['HA_NF_21_CX','HRly_BNF_51','HRly_BNF_52','HA_NF_21_NX','NF_SOS','BNF_SOS','S_05_NF','S_05_BNF',
         'BNF_SS_10_1.5_10','BNF_SS_10_1.5_15','NF_SS_10_2_10','NF_SS_10_3_15']


sum_backtest=0
sum_actual=0
for k in option:
    
    path = r"C:\Users\piyush.raj\Desktop\Report\{}.xlsx".format(k)
    dx=pd.read_excel(path)
    for column in dx.columns:
        if column == 'Backtested returns':
    # Ignore bactested when actual is 0
            column_sum = dx.loc[dx['Actual returns'] != 0, column].sum()
    sum_backtest=sum_backtest+column_sum
    sum_actual=sum_actual+dx['Actual returns'].sum()
    
    
    
with col2:
   st.metric(label='Sum_Backtest',value=round(sum_backtest,2))
with col3:
   st.metric(label='Sum_Actual',value=round(sum_actual,2))    
    


# Create a dropdown with custom labels


with col1:
    selected_option=st.selectbox('Select Stratergy Name',option)
    
if selected_option=='HA_NF_21_CX':
    wrangle(r'C:\Users\piyush.raj\Desktop\Report\HA_NF_21_CX.xlsx')
    
if selected_option=='HRly_BNF_51':
    wrangle(r'C:\Users\piyush.raj\Desktop\Report\Hrly_BNF_51.xlsx')
    
if selected_option=='HRly_BNF_52':
    wrangle(r'C:\Users\piyush.raj\Desktop\Report\Hrly_BNF_52.xlsx')
    
if selected_option=='HA_NF_21_NX':
    wrangle(r'C:\Users\piyush.raj\Desktop\Report\HA_NF_21_NX.xlsx')
    
if selected_option=='NF_SOS':
     wrangle(r'C:\Users\piyush.raj\Desktop\Report\NF_SOS.xlsx')
    
if selected_option=='BNF_SOS':
    wrangle(r'C:\Users\piyush.raj\Desktop\Report\BNF_SOS.xlsx')
    
if selected_option=='S_05_NF':
    wrangle(r'C:\Users\piyush.raj\Desktop\Report\S_05_NF.xlsx')
    
if selected_option=='BNF_SS_10_1.5_10':
    pass
    #wrangle(r'C:\Users\piyush.raj\Desktop\Report\BNF_SS_10_1.5_10.xlsx')
    
if selected_option=='BNF_SS_10_1.5_15':
    pass
    #wrangle(r'C:\Users\piyush.raj\Desktop\Report\BNF_SS_10_1.5_15.xlsx')
    
if selected_option=='S_05_BNF':
    pass
    #wrangle(r'C:\Users\piyush.raj\Desktop\Report\S_05_BNF.xlsx')
    
if selected_option=='NF_SS_10_2_10':
    pass
    #wrangle(r'C:\Users\piyush.raj\Desktop\Report\NF_SS_10_2_10.xlsx')
    
if selected_option=='NF_SS_10_3_15':
    pass
    #wrangle(r'C:\Users\piyush.raj\Desktop\Report\NF_SS_10_3_15.xlsx')
    

        


    

