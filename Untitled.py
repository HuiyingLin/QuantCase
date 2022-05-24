#!/usr/bin/env python
# coding: utf-8

# In[4]:


import pandas as pd
import numpy as np
import os

#!pip install --upgrade pip
get_ipython().system('pip install sympy')
from sympy import Eq, Symbol, solve


# In[12]:


#########################import data################

bond_Path = '~/downloads/FW__Programming_assignment/bond_portfolio.xlsx'
bond_data = pd.read_excel(bond_Path)
bond_data


yld_Path = '~/downloads/FW__Programming_assignment/yield_curve.csv'
yld_data = pd.read_csv(yld_Path, sep = ";")
yld_data


# In[13]:


bond_data


# In[14]:



def mktvalue(df):
    price = df['Price']
    coupon = df['Coupon']
    m = df['Maturity']*0.01   ##coupons in percenatge
    
    df['Market value'] = price*(1+coupon)**m
    
    return(df)


df = mktvalue(bond_data)


df["Maturity"] = pd.to_numeric(df["Maturity"], downcast="float")
df['Coupon'] = df['Coupon']*0.01          ###coupon in percentages
df


# In[15]:


yld_data['term diff'] = yld_data['Term'].diff()
yld_data['Rate diff'] = yld_data['Rate'].diff()
yld_data['annual diff'] = yld_data['Rate diff']/yld_data['term diff']
yld_data

yld_data["Term"] = pd.to_numeric(yld_data["Term"], downcast="float")
yld_data 


# In[17]:


###################part1: discounted market price###################

df['discount rate'] = 'other'


for i in range(0,len(df)):
    for j in range(0,len(yld_data)):

        if df.iloc[i,4] == yld_data.iloc[j,0]:
            
            df.iloc[i,7] = yld_data.iloc[j,1]
            
            

        if (df.iloc[i,4]>3) and (df.iloc[i,4]<5):
            df.iloc[i,7] = (df.iloc[i,4]-3)*yld_data.iloc[4,4] + yld_data.iloc[3,1]
        
        if (df.iloc[i,4]>5) and (df.iloc[i,4]<7):
            df.iloc[i,7] = (df.iloc[i,4]-5)*yld_data.iloc[5,4] + yld_data.iloc[4,1]
        if (df.iloc[i,4]>7) and (df.iloc[i,4]<10):
            df.iloc[i,7] = (df.iloc[i,4]-7)*yld_data.iloc[6,4] + yld_data.iloc[5,1]
        if (df.iloc[i,4]>10) and (df.iloc[i,4]<15):
            df.iloc[i,7] = (df.iloc[i,4]-10)*yld_data.iloc[7,4] + yld_data.iloc[6,1]
        if (df.iloc[i,4]>15) and (df.iloc[i,4]<20):
            df.iloc[i,7] = (df.iloc[i,4]-15)*yld_data.iloc[8,4] + yld_data.iloc[7,1]
        if (df.iloc[i,4]>20) and (df.iloc[i,4]<30):
            df.iloc[i,7] = (df.iloc[i,4]-20)*yld_data.iloc[9,4] + yld_data.iloc[8,1]
        
        
        else:
            pass
              
df['discount rate'] = df['discount rate']*0.01  ###rate in 100%? 
df['discounted price'] = df['Market value']/(1+df['discount rate'])
df





            
        


# In[21]:


######### part 2: get z spread###################


def zspread(p, maturity,coupon):    ##rate for zero coupon bond a year is 0.005
    summ = 0
    y = Symbol('y')
    for i in range(1,maturity-1):
        
        a = (p*(1+coupon)**i-p)/((1+(0.005+y)/2)**(2*i))
        summ = a+summ
    
    summ= summ + p*(1+coupon)**maturity/((1+(0.005+y)/2)**(2*maturity))
    
    
    eqn = Eq(summ, p)
    print(solve(eqn)[1])


zspread(102,5,0.02)


zs = []
for i in range(len(df)):
    p = df.iloc[i,1]
    maturity = int(df.iloc[i,4])
    coupon = df.iloc[i,2]
    zs.append(zspread(p, maturity,coupon))
    
#### didnt finish running coz running time is so long, prolly smt wrong 


# In[27]:


######### part3: implied spread for the whole pool############
## average of zs


# In[ ]:




