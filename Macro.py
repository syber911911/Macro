Source_f = open("C:/Users/HEEJUN/Desktop/TEST SOURCE.txt" , "r")
Extend_f = open("C:/Users/HEEJUN/Desktop/TEXT EXTEND.txt" , "w")

Source_f_lines = Source_f.readlines()
Source_f_list = []
index = 0

Macro_name = []
Macro_name_index = 0

MDT = [] #MDT_dic의 value
MDT_new = [] #내용이 변경된 MDT
MDT_Dic = {} # key: Macro_name , value : MDT (매크로 내용)
FAT = [] #FAT_dic의 value
FAT_Dic = {} # key : Macro_name , value : FAT (형식인수)
AAT = [] #실인수
temp = []

for line in Source_f_lines:
    Source_f_list.append(line.rstrip("\n"))

while(("END" in Source_f_list[index]) == False):
    if("MACRO" in Source_f_list[index]):
        temp = Source_f_list[index].split()
        Macro_name.append(temp[0])
        if(len(temp) > 2):
            for i in range(2, len(temp)):
                FAT.append(temp[i].rstrip(","))
            temp_Dic = {Macro_name[Macro_name_index] : FAT[0:len(FAT)]}
            FAT_Dic.update(temp_Dic)
            FAT = []
        else:
            temp_Dic = {Macro_name[Macro_name_index] : ""}
            FAT_Dic.update(temp_Dic)
        index += 1
        while(("ENDM" in Source_f_list[index]) == False):
            MDT.append(Source_f_list[index])
            index += 1
        temp_Dic = {Macro_name[Macro_name_index] : MDT[0:len(MDT)]}
        MDT_Dic.update(temp_Dic)
        MDT = []
        Macro_name_index += 1
    index += 1

index = 0
while(("END" in Source_f_list[index]) == False):
    if("MACRO" in Source_f_list[index]):
        while(("ENDM" in Source_f_list[index]) == False):
            index += 1
    else:    
        for i in range(0,len(Macro_name)):
            if(Macro_name[i] in Source_f_list[index]):
                temp = Source_f_list[index].split()
                temp.pop(0)
                for AAT_item in temp:
                    AAT.append(AAT_item.rstrip(","))
                MDT_new = MDT_Dic[(Macro_name[i])]
                FAT_temp = FAT_Dic[Macro_name[i]]
                if(FAT_temp == ""):
                    AAT = []
                    FAT_temp = []
                if(len(FAT_temp) != len(AAT)):
                    print("인수전달 오류")
                    break
                else:
                    for MDT_item in range(0, len(MDT_new)):
                        for FAT_item in range(0, len(FAT_temp)):
                            if(FAT_temp[FAT_item] in MDT_new[MDT_item]):
                                MDT_new[MDT_item] = str(MDT_new[MDT_item]).replace(str(FAT_temp[FAT_item]), str(AAT[FAT_item]))
                    Source_f_list.pop(index)
                    for j in range(0, len(MDT_new)):
                        Source_f_list.insert(index, MDT_new[j])
                        index += 1
                    for MDT_item in range(0, len(MDT_new)):
                        for AAT_item in range(0, len(AAT)):
                            if(AAT[AAT_item] in MDT_new[MDT_item]):
                                MDT_new[MDT_item] = str(MDT_new[MDT_item]).replace(str(AAT[AAT_item]),str(FAT_temp[AAT_item]))
                    AAT = []                                   
    index += 1

for i in range(0, len(Source_f_list)):
    Extend_f.write(Source_f_list[i]+"\n")

Source_f.close()
Extend_f.close()