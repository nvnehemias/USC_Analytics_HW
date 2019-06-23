#!/usr/bin/env python
# coding: utf-8

# ### Heroes Of Pymoli Data Analysis
# * Of the 1163 active players, the vast majority are male (84%). There also exists, a smaller, but notable proportion of female players (14%).
# 
# * Our peak age demographic falls between 20-24 (44.8%) with secondary groups falling between 15-19 (18.60%) and 25-29 (13.4%).  
# -----

# ### Note
# * Instructions have been included for each segment. You do not have to follow them exactly, but they are included to help you think through the steps.

# In[1]:


# Dependencies and Setup
import pandas as pd
import numpy as np

# File to Load (Remember to Change These)
file_to_load = "Resources/purchase_data.csv"

# Read Purchasing File and store into Pandas data frame
purchase_data = pd.read_csv(file_to_load)


# ## Player Count

# * Display the total number of players
# 

# In[2]:


total = purchase_data.SN.nunique() 
Player_Count = pd.DataFrame([{"Total Player": total}])
Player_Count


# ## Purchasing Analysis (Total)

# * Run basic calculations to obtain number of unique items, average price, etc.
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display the summary data frame
# 

# In[3]:


items = purchase_data["Item ID"].nunique()
Purchase = purchase_data['Purchase ID'].count()
Total_Revenue = purchase_data['Price'].sum()
Price = Total_Revenue/Purchase

Table = pd.DataFrame([{"Number of Unique Items": items ,"Number of Purchases": Purchase,"Total Revenue":Total_Revenue, "Average Price" : Price}])
Table2 = Table[["Number of Unique Items","Average Price","Number of Purchases","Total Revenue"]]
Table2["Average Price"]= Table2["Average Price"].map("${:,.2f}".format)
Table2['Total Revenue'] = Table2['Total Revenue'].map("${:,.2f}".format)
Table2


# ## Gender Demographics

# * Percentage and Count of Male Players
# 
# 
# * Percentage and Count of Female Players
# 
# 
# * Percentage and Count of Other / Non-Disclosed
# 
# 
# 

# In[4]:


#We sort the table and then delete all the duplicates in the table
copy_Table1 = purchase_data.sort_values('SN',ascending =True)
copy_Table2 = copy_Table1.drop_duplicates(subset ="SN",keep = 'first')

#Sum of the total number of times Male, Female, and Other show up in the column "Gender"
Total = copy_Table2['Gender'].count()
Males = (copy_Table2['Gender']=='Male').sum()
Females = (copy_Table2['Gender']=='Female').sum()
Other_Non_Disclosed = (copy_Table2['Gender']=='Other / Non-Disclosed').sum()

#Taking the percentages for each Gender
MP = Males/Total*100
FP = Females/Total*100
OP = Other_Non_Disclosed/Total*100

#We print the dataframe with the values 
Genders = pd.Series(['Male','Female','Other / Non-Disclosed'])
Gender_Demographics = pd.DataFrame({"Total Count":[Males,Females,Other_Non_Disclosed],"Percentage of Players":[MP,FP,OP]})
Gender_Demographics["Percentage of Players"] = Gender_Demographics['Percentage of Players'].map("{:,.2f}".format)
Gender_Demographics = Gender_Demographics.set_index([Genders])

#Display DataFrame
Gender_Demographics


# 
# ## Purchasing Analysis (Gender)

# * Run basic calculations to obtain purchase count, avg. purchase price, avg. purchase total per person etc. by gender
# 
# 
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display the summary data frame

# In[5]:


#We group two times and setting them to seperate variables
Gender_Table1 = purchase_data.groupby("Gender").count()
Gender_Table2 = purchase_data.groupby("Gender").agg({"Price":sum })

#Merge the two variables
Gender_Table_Merge = pd.merge(Gender_Table1,Gender_Table2,on = "Gender")

#Calculate Average Purchase Price
Gender_Table_Merge["SN"] = (Gender_Table_Merge["Price_y"]/Gender_Table_Merge["Purchase ID"])

#Drop unnecessary columns in the DataFrame 
Gender_Table_Merge = Gender_Table_Merge.drop(columns = ["Age","Item ID","Item Name"])

#Rename Columns
Gender_Table_Merge = Gender_Table_Merge.rename(columns = {"Purchase ID" : "Purchase Count","SN": "Average Purchase Price","Price_y":"Total Purchase Value","Price_x": "Avg Total Purchase per Person"})

#ATPP = Gender_Table_Merge["Total Purchase Value"]/Gender_Demographics["Total Count"]
Gender_Table_Merge["Avg Total Purchase per Person"] = (Gender_Table_Merge["Total Purchase Value"]/Gender_Demographics["Total Count"])

#Reordering the column in the DataFrame 
Gender_Table_Merge = Gender_Table_Merge[["Purchase Count","Average Purchase Price","Total Purchase Value","Avg Total Purchase per Person"]]

# #Clean up data with correct decimal places and currency sign
Gender_Table_Merge["Average Purchase Price"] = Gender_Table_Merge["Average Purchase Price"].map("${:,.2f}".format)
Gender_Table_Merge["Total Purchase Value"] = Gender_Table_Merge["Total Purchase Value"].map("${:,.2f}".format)
Gender_Table_Merge["Avg Total Purchase per Person"] = Gender_Table_Merge["Avg Total Purchase per Person"].map("${:,.2f}".format)

#Display DataFrame
Gender_Table_Merge


# ## Age Demographics

# * Establish bins for ages
# 
# 
# * Categorize the existing players using the age bins. Hint: use pd.cut()
# 
# 
# * Calculate the numbers and percentages by age group
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: round the percentage column to two decimal points
# 
# 
# * Display Age Demographics Table
# 

# In[6]:


player_demos = purchase_data.loc[:,["Gender","SN","Age"]]
player_demos = player_demos.drop_duplicates()

# Create the bins in which Data will be held  
bins = [0, 10, 15, 20, 25, 30, 35, 40, 1000]

# Create the names for the four bins
group_names = ["<10", "10-14", "15-19", "20-24", "25-29","30-34", "35-39","40+"]
player_demos["Age Group"] = pd.cut(player_demos["Age"], bins, labels=group_names,right=False)
AgeTable = player_demos.groupby("Age Group").count()
AgeTable = AgeTable.rename(columns = {"Gender":"Total Count"})

#We take the total number of counts and use Total_Age to divide the value for each Age Group
Total_Age = AgeTable["Total Count"].sum()
AgeTable["SN"] = (AgeTable["Total Count"]/Total_Age*100).map("{:,.2f}".format)

#Drop and rename columns 
AgeTable = AgeTable.drop(columns = "Age")
AgeTable = AgeTable.rename(columns = {"SN": "Percentage of Players"})

#Display new table 
AgeTable


# ## Purchasing Analysis (Age)

# * Bin the purchase_data data frame by age
# 
# 
# * Run basic calculations to obtain purchase count, avg. purchase price, avg. purchase total per person etc. in the table below
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display the summary data frame

# In[7]:


player_demos = purchase_data.loc[:,["Gender","SN","Age","Price"]]
# Create the bins in which Data will be held  
bins = [0,10, 15, 20, 25, 30, 35, 40, 1000]
# Create the names for the four bins
group_names = ["<10", "10-14", "15-19", "20-24", "25-29","30-34", "35-39","40+"]
player_demos["Age Group"] = pd.cut(player_demos["Age"], bins, labels=group_names,right=False)
NewTable = player_demos.groupby("Age Group").count()
Age_Table = player_demos.groupby("Age Group").agg({"Price":sum })

#Merge tables together
Age_Merge = pd.merge(NewTable,Age_Table, on = "Age Group")

#Rename columns in new table
Age_Merge = Age_Merge.rename(columns = {"Gender":"Purchase Count","Price_y":"Total Purchase Value","SN":"Average Purchase Price"})
Age_Merge["Average Purchase Price"] = Age_Merge["Total Purchase Value"]/Age_Merge["Purchase Count"]

#Drop unecessary columns 
Age_Merge = Age_Merge.drop(columns = ["Price_x"])

#Calculate Avg Total Purchase per Person
Age_Merge["Age"] = Age_Merge["Total Purchase Value"]/AgeTable["Total Count"]

#Renaming column
Age_Merge = Age_Merge.rename(columns = {"Age": "Avg Total Purchase per Person"})

#Reordering columns in the DataFrame
Age_Merge = Age_Merge[["Purchase Count","Average Purchase Price","Total Purchase Value","Avg Total Purchase per Person"]]

#Clean dataframe with correct decimal place and currency sign
Age_Merge["Average Purchase Price"] = Age_Merge["Average Purchase Price"].map("${:,.2f}".format)
Age_Merge["Total Purchase Value"] = Age_Merge["Total Purchase Value"].map("${:,.2f}".format)
Age_Merge["Avg Total Purchase per Person"] = Age_Merge["Avg Total Purchase per Person"].map("${:,.2f}".format)

#Move rows around 
Age_Merge = Age_Merge.loc[["10-14","15-19","20-24","25-29","30-34","35-39","40+","<10"]]

#Display DataFrame
Age_Merge


# ## Top Spenders

# * Run basic calculations to obtain the results in the table below
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Sort the total purchase value column in descending order
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display a preview of the summary data frame
# 
# 

# In[8]:


#Change the column name from Purchase ID to Purchase Count 
purchase_data2 = purchase_data.rename(columns = {"Purchase ID":"Purchase Count"})

#Group purchase_data2 by 'SN' and count the values of the new index
group1 = purchase_data2.groupby("SN").count()

#Take the sum of each SN value and sum of the total purchase value 
group2 = purchase_data2.groupby("SN").agg({"Price":sum })

#Merge the two DataFrames on "SN"
merge1 = pd.merge(group1,group2,on = "SN")

#Sort the new DataFrame by Price_y
merge1 = merge1.sort_values("Price_y", ascending = False)

#Rename the column "Price_y" to Total Purchase Value 
merge1 = merge1.rename(columns = {'Price_y':"Total Purchase Value"})

#Take Total Purchase Value and divide it by Purchase count to get the Average Purchase Price and append that series in the DataFrame
merge1["Price_x"] = (merge1["Total Purchase Value"]/merge1["Purchase Count"]).map("${:,.2f}".format)
merge1 = merge1.drop(columns = ["Age","Gender","Item ID","Item Name"])
merge1 = merge1.rename(columns = {"Price_x" : "Average Purchase Price"})
merge1["Total Purchase Value"] = merge1["Total Purchase Value"].map("${:,.2f}".format)

#Display DataFrame
merge1.head()


# ## Most Popular Items

# * Retrieve the Item ID, Item Name, and Item Price columns
# 
# 
# * Group by Item ID and Item Name. Perform calculations to obtain purchase count, item price, and total purchase value
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Sort the purchase count column in descending order
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display a preview of the summary data frame
# 
# 

# In[9]:


purchase_data3 = purchase_data.rename(columns = {"Purchase ID": "Purchase Count"})
#Create two variable that will hold two tables with the same groupby
grouping1 = purchase_data3.groupby(["Item ID","Item Name"]).count()
grouping2 = purchase_data3.groupby(["Item ID","Item Name"]).agg({"Price":sum})

#Sort the values in the first groupby table
grouping1 = grouping1.sort_values("Purchase Count",ascending = False)

#Merge the two tables
mergeing1 = pd.merge(grouping1,grouping2, on = ["Item ID","Item Name"])

#Rename the columns in the merge 
mergeing1 = mergeing1.rename(columns = {"Price_y": "Total Purchase Value"})

#Clean up and format the merge 
mergeing1['Price_x'] = (mergeing1["Total Purchase Value"]/mergeing1["Purchase Count"]).map("${:,.2f}".format)

#Drop unnecessary columns
mergeing1 = mergeing1.drop(columns = ["SN","Age","Gender"])

#Rename columns 
mergeing1 = mergeing1.rename(columns = {"Price_x": "Item Price"})

#Clean up and format the merge 
mergeing1["Total Purchase Value"] = mergeing1["Total Purchase Value"].map("${:,.2f}".format)

#Print the final table
mergeing1.head()


# ## Most Profitable Items

# * Sort the above table by total purchase value in descending order
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display a preview of the data frame
# 
# 

# In[11]:


#----------------------Same steps as before-------------------------------------------------------------------
purchase_data3 = purchase_data.rename(columns = {"Purchase ID": "Purchase Count"})
grouping1 = purchase_data3.groupby(["Item ID","Item Name"]).count()
grouping2 = purchase_data3.groupby(["Item ID","Item Name"]).agg({"Price":sum})
grouping1 = grouping1.sort_values("Purchase Count",ascending = False)
mergeing1 = pd.merge(grouping1,grouping2, on = ["Item ID","Item Name"])
mergeing1 = mergeing1.rename(columns = {"Price_y": "Total Purchase Value"})
mergeing1['Price_x'] = (mergeing1["Total Purchase Value"]/mergeing1["Purchase Count"]).map("${:,.2f}".format)
mergeing1 = mergeing1.drop(columns = ["SN","Age","Gender"])
mergeing1 = mergeing1.rename(columns = {"Price_x": "Item Price"})
#---------------------------------------------------------------------------------------------------------------
#Sort the table by Total Purchase Value
mergeing1 = mergeing1.sort_values("Total Purchase Value",ascending = False)

#Format the table
mergeing1["Total Purchase Value"] = mergeing1["Total Purchase Value"].map("${:,.2f}".format)

#Print the table 
mergeing1.head()


# ## written description of three observable trends based on the data.

# * The data shows that there are a greater number of males that play this game and have a higher total purchase value than other genders.
# 
# * The data demonstrates that the Total Purchase Value for some of the categories does not exceed $51.00
# 
# * The data also shows the average price for whichever category or grouping does not exceed $4.00. 
# 
# 
# 
