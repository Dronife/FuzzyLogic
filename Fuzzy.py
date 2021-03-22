#!/usr/bin/env python
# coding: utf-8

# In[19]:


import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt

titleY = 1.35
textY = 1.05
inputY = 1.25
# In[3]:


def ConvertToAxisY(x_axis, shape):
    y = []
    if(len(shape) == 3):
        y = fuzz.trimf(x_axis, shape)
    else:
        y = fuzz.trapmf(x_axis, shape)
    return y


# In[4]:


def setAxis(axis, param, Text= None, Title = True, Left = None, Middle = None, Right = None, **kwargs):

    if(Left):
        low= ConvertToAxisY(param["x_axis"], param["low"])
        axis.plot(param["x_axis"], low, "DarkOrange", linewidth=1.5)
    if(Middle):
        mid= ConvertToAxisY(param["x_axis"], param["mid"])
        axis.plot(param["x_axis"], mid, "Green", linewidth=1.5)
    if(Right):
        high= ConvertToAxisY(param["x_axis"], param["high"])
        axis.plot(param["x_axis"], high, "DarkMagenta", linewidth=1.5)
    if(Text):
        axis.text(param["text_co"][0], textY, param["texts"][0], fontsize=12)
        axis.text(param["text_co"][1], textY, param["texts"][1], fontsize=12)
        axis.text(param["text_co"][2], textY, param["texts"][2], fontsize=12)
    if(Title):
        axis.set_title(param["title"], y=titleY, fontweight='bold')
    return axis
    


# In[5]:


def SlopeCalculate(x, a, b, goesUp):
    meter = 0.0
    
    if(not goesUp):
        meter = b-x
    else:
        meter = x-a
    return abs(meter/(b-a))
    


# In[6]:


#dependancy function for left side
#interpret that all the forms are made of trapeze
def TrapezeCalculationLeft(x, shapeCoords):
    if(x < shapeCoords[2]):
        return 1
    elif(shapeCoords[2] <= x and x < shapeCoords[3] ):
        return SlopeCalculate(x, shapeCoords[2], shapeCoords[3], False)
    else:
        return 0
        


# In[7]:


def TrapezeCalculationMiddle(x, shapeCoords):
    if(x <= shapeCoords[0]):
        return 0
    elif(shapeCoords[0] < x and x < shapeCoords[1] ):
        return SlopeCalculate(x, shapeCoords[0], shapeCoords[1], True)
    elif(shapeCoords[1] <= x and x < shapeCoords[2] ):
        return 1
    elif(shapeCoords[2] <= x and x < shapeCoords[3] ):
        return SlopeCalculate(x, shapeCoords[2], shapeCoords[3], False)
    else:
        return 0
    


# In[8]:


def TrapezeCalculationRight(x, shapeCoords):
    if(x <= shapeCoords[0]):
        return 0
    elif(shapeCoords[0] < x and x < shapeCoords[1] ):
        return SlopeCalculate(x, shapeCoords[0], shapeCoords[1], True)
    else:
        return 1


# In[9]:


def returnAllMemberships(x, lo, mi, hi):
    low = TrapezeCalculationLeft(x, lo)
    mid = TrapezeCalculationMiddle(x, mi)
    high = TrapezeCalculationRight(x, hi)
    return [low, mid, high]


# In[10]:


def ProbabilityToSellLow(price, speed, year):
    l1 = min(min(price[1],speed[0]),year[0])
    l2 = min(min(price[2],speed[0]),year[0])
    l3 = min(min(price[2],speed[1]),year[1])
    l4 = min(max(price[2],speed[1]),year[0])
    return sum([l1,l2,l3,l4])    


# In[11]:


def ProbabilityToSellAvg(price, speed, year):
    a1 = min(min(price[0],speed[0]),year[0])
    a2 = min(min(price[0],speed[1]),year[1])
    a3 = min(min(price[1],speed[1]),year[1])
    a4 = min(max(price[1],speed[1]),year[2])
    a5 = min(min(price[2],speed[2]),year[2])
    return sum([a1,a2,a3,a4,a5])


# In[12]:


def ProbabilityToSellHigh(price, speed, year):
    h1 = min(min(price[0],speed[2]),year[2])
    h2 = min(max(price[0],speed[2]),year[2])
    h3 = min(min(price[1],speed[2]),year[2])
    return sum([h1,h2,h3])
    


# In[13]:


def aggregation(low, avg, high, param):
    low_prob = ConvertToAxisY(param["x_axis"], param["low"])
    mid_prob = ConvertToAxisY(param["x_axis"], param["mid"])
    high_prob = ConvertToAxisY(param["x_axis"], param["high"])
    return np.fmax(low_prob * low, np.fmax(mid_prob * avg, high * high_prob))  


# In[ ]:


def fillForm(axis, x_axis, form, argument_probability, color, alp):
    formByAxisY = ConvertToAxisY(x_axis, form)
    probabilityFillY = np.fmin(argument_probability, formByAxisY)
    axis.fill_between(x_axis,probabilityFillY, facecolor=color, alpha = alp)
    return axis


# In[14]:


def fillAxis(axis, parameters, argument_probabilities, Left = None, Middle = None, Right = None, **kwargs):
    alp = 0.6
    if(Left):
        fillForm(axis, parameters['x_axis'], parameters['low'], argument_probabilities[0], 'orange', alp)
        
    if(Middle):
        fillForm(axis, parameters['x_axis'], parameters['mid'], argument_probabilities[1], 'g', alp)
    
    if(Right):
        fillForm(axis, parameters['x_axis'], parameters['high'], argument_probabilities[2], 'm', alp)
    
    return axis


# In[15]:


def setLine(axis, x):
    axis.plot([x,x], [0,inputY+0.1], color='aqua')
    axis.text(x, inputY+0.2 ,x, fontsize=12, color='aqua', ha = 'center')
    return axis


# In[16]:


def drawProbobilities(axis, x_variable, parameters, memberships):
    axis = setAxis(axis, parameters, Text = True,Left= True, Middle= True,Right= True)
    axis = setLine(axis, x_variable)
    axis = fillAxis(axis, parameters, memberships,Left= True, Middle= True,Right= True)
    return axis


# In[17]:


def reSellProbability(axis,ReSellChance, parameters, title):
    reSellProbabilityMem =returnAllMemberships(ReSellChance, parameters['low'], parameters['mid'], parameters['high'])
    axis = drawProbobilities(axis, ReSellChance,parameters, reSellProbabilityMem)
    axis.set_title(title, y=titleY, fontweight='bold')
    return axis


# In[20]:



# Creating all the necessary input variables(creating shapes in graph)
#in this case all the shapes are trapeze
price_params = {
    "x_axis" : np.arange(50, 1000, 2),
    "low" : [50, 50,150, 400],
    "mid" : [350, 400 ,600, 750],
    "high" : [600, 800, 1000,1000],
    "texts": ["Cheap", "Average", "Expensive"],
    "text_co": [50,400,800],
    "title" : "Price",
}

speed_params = {
    "x_axis" : np.arange(1, 10, 0.01),
    "low" : [1, 1,3, 5],
    "mid" : [4, 5, 7,8],
    "high" : [7, 8, 10, 10],
    "texts": ["Slow", "Normal", "Fast"],
    "text_co": [1,5,8],
    "title" : "Speed"
}

year_params = {
    "x_axis" : np.arange(2015, 2022, 0.01),
    "low" : [2014, 2014,2016, 2018],
    "mid" : [2016, 2017,2019, 2020],
    "high" : [2018, 2020, 2022,2022],
    "texts": ["Old", "Aged", "Almost as new"],
    "text_co": [2015, 2017.5,2020],
    "title" : "Computer Build Year"
}


probaility_params = {
    "x_axis" : np.arange(0, 100, 0.05),
    "low" : [0, 0,20, 40],
    "mid" : [29, 30,60, 70],
    "high" : [60, 70, 100,100],
    "texts": ["Low", "Average", "High"],
    "text_co": [0,40,70],
    "title" : "Chance of re-selling"
}


# In[24]:


# In[22]:
xPlotSize = 6
yPlotSize = 4

price = 365
speed = 7.5
year_of_build = 2019

# returns array of probability of atribute
# e.g.: price = 380:
#     <0> cheap -> 0.35;
#     <1> Mid -> 0.8;
#     <2> Expensive -> 0.0
price_memberships = returnAllMemberships(price, price_params['low'],price_params['mid'],price_params['high'])
speed_memberships = returnAllMemberships(speed, speed_params['low'],speed_params['mid'],speed_params['high'])
year_memberships = returnAllMemberships(year_of_build, year_params['low'],year_params['mid'],year_params['high'])

# Each returns whole float of probability of succeeding of re-selling 
probability_low_prob = ProbabilityToSellLow(price_memberships, speed_memberships,year_memberships)
probability_avg_prob = ProbabilityToSellAvg(price_memberships, speed_memberships,year_memberships)
probability_high_prob = ProbabilityToSellHigh(price_memberships, speed_memberships,year_memberships)

print("Implication:\n Low probability to sell:",probability_low_prob,"\n Average probability to sell:",
      probability_avg_prob,"\n High probability to sell:", probability_high_prob)

aggregated = aggregation(probability_low_prob, probability_avg_prob, probability_high_prob, probaility_params)
probability_COA = fuzz.defuzz(probaility_params["x_axis"], aggregated, 'centroid')
probability_MOM = fuzz.defuzz(probaility_params["x_axis"], aggregated, 'mom')

print(" Probability to sell(COA)", probability_COA)
print(" Probability to sell(MOM)", probability_MOM)


# In[23]:

fig_prob, (input_params) = plt.subplots(3, figsize=(xPlotSize, yPlotSize+1))

input_params[0] = drawProbobilities(input_params[0], price, price_params, price_memberships)
input_params[1] = drawProbobilities(input_params[1], speed, speed_params, speed_memberships)
input_params[2] = drawProbobilities(input_params[2], year_of_build, year_params, year_memberships)
fig_prob.tight_layout()
#plot probability of reselling
fig_resell_prob, (resell_probability) = plt.subplots(2, figsize=(xPlotSize, yPlotSize+1))
resell_probability[0] = reSellProbability(resell_probability[0], probability_COA, probaility_params, (probaility_params['title']+" (COA)"))
resell_probability[1] = reSellProbability(resell_probability[1], probability_MOM, probaility_params, (probaility_params['title']+" (MOM)"))
fig_resell_prob.tight_layout()
plt.show()
