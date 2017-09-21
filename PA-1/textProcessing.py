
# coding: utf-8

# In[4]:

inputFile = open('news.txt', 'r', encoding='UTF-8')
outputFile = open('result.txt','w', encoding='UTF-8')

for line in inputFile:     
    outputFile.write(line.lower())
    
inputFile.close()
outputFile.close()


# In[ ]:



