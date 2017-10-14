# HW2	Report  R05725060 郭欣宜

### 執行環境 & 作業系統
- 執行環境
  - terminal
- 作業系統
  - Mac OS

### 程式語言,版本
- 程式語言
  - 版本 python3

### 執行方式
- python3 hw2.py

### 1.txt 和 2.txt 的 cosine similarity
- 0.18240843397014356

### 作業處理邏輯說明

#### import
![](https://i.imgur.com/DkNpC5b.png)
1. import 必要的library
2. import 上次的作業1(hw1.py)

#### 查看是否此檔案為直接被執行
![](https://i.imgur.com/DWO2RXU.png)
1. 如果是直接執行此檔案，就執行main function

#### main function
![](https://i.imgur.com/ncjGxA9.png)
1. 建立在IRTM資料夾底下所有文件的字典
2. 把建好的dictionary 讀進來
3. 把index的dictionary建好 : dictionary_of_index['term'] = index
4. 把df的dictionary建好 : dictionary_of_index['term'] = df
5. 把IRTM裡面的所有檔案算出它的tf-idf的unit vector
6. 算出1.txt和 2.txt的 cosine similarity

#### construct_dictionary function
![](https://i.imgur.com/VTfzfuj.png)
1. 取得現在執行file的資料夾位置
2. 把所有此資料夾的檔案存進documents的list
3. 建立 dictionary -> 用意為term的df
4. 針對每一個檔案先進行hw1的preprocessiong後算出把term存進dictionary，之後算出所有檔案term的df
5. 把所有term按照字母順序排列(sorted)
6. 最後把這個dictionary term 的list存進dictionary.txt

#### write_dictionary function
![](https://i.imgur.com/ekngdUP.png)

1. 寫dictoinary的header t_index[tab]term[tab]df
2. 把dictionary寫進dictionary.txt

#### read_dictionary function
![](https://i.imgur.com/7f2DD9w.png)

1. 把原本寫好的dictionary讀進來存在list

#### dictionary_index function
![](https://i.imgur.com/JG8SXLI.png)

1. 建立 index 的 dictionary 格式為 dictionary_of_index['term'] = index

#### dictionary_df function
![](https://i.imgur.com/9ZfksyB.png)

1. 建立 df 的 dictionary 格式為 dictionary_of_df['term'] = df

#### transfer_tfidf_unit_vector function
![](https://i.imgur.com/9eFn8gO.png)

1. 把IRTM裡面的所有檔案算出它的tf-idf的unit vector
2. 算出每個檔案term的tf
3. 把term的dictionary以字母大小排列(sorted)
4. 如果沒有unit_vector的資料夾就建立一個
5. 把檔案中擁有的term數量寫在document的第一行
6. 寫document的標頭 t_index[tab]tf-idf
7. 接下來是把算出的tf-idf值變成unit vector
8. 先把所有tf-idf平方得出的值加總
9. 再把每一個tf-idf的值除以剛剛加總得值就是最後要寫進document的tf-idf

#### count_tfidf function
![](https://i.imgur.com/sHaDpLK.png)

1. 算出給定的doument的tf-idf

#### cosine function
![](https://i.imgur.com/BWq1qym.png)

1. 把要算cosine similarity的兩個檔案讀進來
2. 刪除term的數量和標頭
3. 以tab作為分割符號
4. 因為兩個檔案都有sorted過
5. 所以比對兩個檔案的index
6. 看index哪個比較小就加那個index的值
7. 兩個檔案中所有相等的index相乘各自的unit vector tf-idf就為最後要得到的cosine similarity

### 作業的心得
這次的作業讓我體會到如果資料量一大，算的速率跟程式寫的好壞有相當大的關聯性，像python的count我覺得最好不要用，而且要善用dictionary的特性，找term會快很多。