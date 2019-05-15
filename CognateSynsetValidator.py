# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18 14:17:10 2019

@author: TAL-LAPTOP
"""
import csv

COGNATE_TO_LANGUAGE_FAMILY = "c:/Users/TAL-LAPTOP/Documents/Liat/Research/Cognates/cognates_info/cognates_origin.csv"
GERMANIC_ORIGIN = ["Iceland","Sweden","Germany","Austria","Netherlands","Norway","Finland","Denmark"]
ROMANCE_ORIGIN = ["Romania","Portugal","Spain","Italy","France","Mexico","Argentina","Brazil","Venezuela","Sardinia","Andorra"]
class CognateSynsetValidator():
    
    def __init__(self, cognate_origin_file):
        self.cognate_origin_file = cognate_origin_file
        self.synset_to_cognate_dict = {}
        self.synset_to_romance_germanic_count = {}
        self.create_synset_to_cognate_dict()
        self.create_synset_to_romance_germanic_ratio()
        
    def create_synset_to_cognate_dict(self):         
        with open(self.cognate_origin_file, 'r', encoding='utf-8', errors='ignore') as origin_file:                                
                csvreader = csv.reader(origin_file, delimiter=',')
                next(csvreader, None)
                for line in csvreader:                                         
                # user_name apears in the begining of every row inside []                    
                    if len(line) < 3:                        
                        continue                    
                    synset_number = line[0]                   
                    cognate = line[1]
                    origin = line[2]                    
                    if synset_number not in self.synset_to_cognate_dict.keys():
                        self.synset_to_cognate_dict[synset_number] = {}
                    self.synset_to_cognate_dict[synset_number][cognate] = origin
                    
       
    def create_synset_to_romance_germanic_ratio(self):
        for synset, synset_info in  self.synset_to_cognate_dict.items():
            for synset, synset_info in self.synset_to_cognate_dict.items():
                self.synset_to_romance_germanic_count[synset] = []
                if self.isSynsetValid(synset):
                    germanic_counter = 0
                    romance_counter = 0
                    other_counter = 0
                    total_counter = 0 
                    for cognate,origin in synset_info.items():
                        if origin == "Germanic":
                            germanic_counter += 1
                        elif origin == "Romance":
                            romance_counter += 1
                        else:
                            other_counter += 1
                        total_counter += 1
                    if germanic_counter > 0 and romance_counter > 0 :             
                        self.synset_to_romance_germanic_count[synset].append(germanic_counter)                
                        self.synset_to_romance_germanic_count[synset].append(romance_counter)
                        self.synset_to_romance_germanic_count[synset].append(other_counter)
                        self.synset_to_romance_germanic_count[synset].append(total_counter)
                            
                        
            
            
            
            
    def isSynsetValid(self,synset):
        synset_info = self.synset_to_cognate_dict[synset]
        if "Germanic" in synset_info.values() and "Romance" in synset_info.values():
            return True
        return False
    
    def write_valid_cognate_file(self, output_file):
        synset_counter = 1
        with open(output_file, "w+", encoding='utf-8') as output:
            output.write("synset,cognate,origin\n")
            for synset, synset_info in self.synset_to_cognate_dict.items():
                if self.isSynsetValid(synset):
                    output.write("{},".format(synset))
                    for cognate,origin in synset_info.items():
                        if origin not in ["Romance","Germanic"]:
                            origin = "Other"
                        output.write("{},{},".format(cognate,origin))
                    synset_counter += 1
                    germanic_count = self.synset_to_romance_germanic_count[synset][0]
                    romance_count = self.synset_to_romance_germanic_count[synset][1]
                    other_count = self.synset_to_romance_germanic_count[synset][2]
                    all_count = self.synset_to_romance_germanic_count[synset][3]
                    germanic_romance_count = germanic_count + romance_count                    
                    output.write("{},{},{},".format(germanic_count/all_count, romance_count/all_count, other_count/all_count))
                    output.write("{},{}\n".format(germanic_count/germanic_romance_count, romance_count/germanic_romance_count))
                    
    
    
def Main():   
    
    cog_synset_validator = CognateSynsetValidator(COGNATE_TO_LANGUAGE_FAMILY)   
    complete_cognage_data_structure={}
    germanic_users = {}
    romance_users = {}
    indexed_users = {}
    native_users = {}
    with open("native_valid_cognate_vectors.csv","r", encoding="utf-8") as valid_vectors:
        csvreader = csv.reader(valid_vectors, delimiter=',')
        users = next(csvreader, None)        
        user_index = 2
        for user in users:
            if "." not in user:
               continue
            start = user.find(".")
            country = (user[start+1: len(user)]).strip()
            if country not in native_users.keys():
                native_users[country] = {}
            native_users[country][user_index] = [0,0,0]
#            if country in GERMANIC_ORIGIN:
#                if country not in germanic_users.keys():
#                    germanic_users[country] = {}
#                germanic_users[country][user_index] = [0,0,0]
#            else:
#                 if country not in romance_users.keys():
#                    romance_users[country] = {}
#                 romance_users[country][user_index] = [0,0,0]
                
                
                        
#            complete_cognage_data_structure[user_index] = {}
           
            indexed_users[user_index] = []
            indexed_users[user_index].append(user)
            indexed_users[user_index].append(country)
            user_index += 1
#            print("{}:{}".format(user_index, user))
        
        for line in csvreader:
            synset = line[0]
            cognate =line[1].strip()
##            print(cognate)            
#            if synset not in complete_cognage_data_structure.keys():
#                complete_cognage_data_structure[synset]={}
#            complete_cognage_data_structure[synset][cognate] = {}
            
            for user_index in range(2,len(indexed_users.keys())+2): 
                country =  indexed_users[user_index][1]
                
                try:
                    origin = cog_synset_validator.synset_to_cognate_dict[synset][cognate]
                except:
                    origin = "Other"
#                print("{},{}".format(cognate, origin))
                cognate_count = int(line[user_index])
                if origin ==  "Germanic":
                    native_users[country][user_index][0] += cognate_count
                elif origin == "Romance":
                    native_users[country][user_index][1] += cognate_count
                else:
                    native_users[country][user_index][2] += cognate_count
                
#                count_array=[]
#                if country in GERMANIC_ORIGIN:
#                    count_array = germanic_users[country][user_index]
#                else:
#                    count_array = romance_users[country][user_index]
#                cognate_count = int(line[user_index])
#                if origin == "Germanic":
#                    count_array[0] += cognate_count
#                elif origin == "Romance":
#                    count_array[1] += cognate_count
#                else:
#                    count_array[2] += cognate_count
#        with open("non_native_cognate_count_per_origin.csv","w+",encoding="utf-8") as non_natives_diversion:  
        with open("native_cognate_count_per_origin.csv","w+",encoding="utf-8") as natives_diversion:  
#            non_natives_diversion.write("origin, country, user_index, user_name, germanic_count, romance_count, other_count\n")
            natives_diversion.write("country, user_index, user_name, germanic_count, romance_count, other_count\n")
            for country in native_users.keys():
                for user_index in native_users[country]:
                        natives_diversion.write("{},{},{},{},{},{}\n".format(country,user_index, indexed_users[user_index][0],native_users[country][user_index][0], native_users[country][user_index][1],native_users[country][user_index][2]))
#            for country in germanic_users.keys():
##                non_natives_diversion.write("{},".format(country))
##                print("***{}***:\n".format(country))
#                for user_index in germanic_users[country]:
##                    print("{},{},:".format(user_index, indexed_users[user_index][0]))
#                    non_natives_diversion.write("germanic,{},{},{},{},{},{}\n".format(country,user_index, indexed_users[user_index][0],germanic_users[country][user_index][0], germanic_users[country][user_index][1],germanic_users[country][user_index][2]))
##                    print ("germanic: {}, romanc: {}, other: {}".format(germanic_users[country][user_index][0], germanic_users[country][user_index][1],germanic_users[country][user_index][2]))
#            for country in romance_users.keys():
##                print("***{}***:".format(country))
##                non_natives_diversion.write("{},".format(country))
#                for user_index in romance_users[country]:
##                    print("{}. {}:".format(user_index, indexed_users[user_index][0]))                        
##                    print ("germanic: {}, romanc: {}, other: {}".format(romance_users[country][user_index][0], romance_users[country][user_index][1],romance_users[country][user_index][2]))
#                    non_natives_diversion.write("romance,{},{},{},{},{},{}\n".format(country,user_index, indexed_users[user_index][0],romance_users[country][user_index][0], romance_users[country][user_index][1],romance_users[country][user_index][2]))
#                complete_cognage_data_structure[synset][cognate][user_index] = 0                
##            print (synset)
#            user_index = 0
#            for cognate_count in range(2, len(line)):                 
#    ##                print(cognate_count)
#    ##                print(line[cognate_count])
#    ##                print(synset)
#    ##                print(user_index)
#                complete_cognage_data_structure[synset][cognate][user_index] = int(line[cognate_count])
#                user_index += 1
##            print(complete_cognage_data_structure[1])
#    with open("native_3way_normalized_cognate_vectors.csv", "w+", encoding = "utf-8") as norm3:            
#        norm3.write(",,")            
##        norm2.write(",,")            
#        for user_index in range(len(indexed_users.keys())):
#            norm3.write(indexed_users[user_index].strip() + ",,,")            
##            norm2.write(indexed_users[user_index].strip() + ",,")            
#        norm3.write("\n")
##        norm2.write("\n")
#        for synset,cognates_data in complete_cognage_data_structure.items():
#            norm3.write(synset+",")
##            norm2.write(synset+",")
#            for cognate in cognates_data.keys():
#                norm3.write("{};".format(cognate))                
##                norm2.write("{};".format(cognate))                
##            total = cog_synset_validator.synset_to_romance_germanic_count[synset][3] 
##            germanic_norm_ratio = cog_synset_validator.synset_to_romance_germanic_count[synset][0]/total
##            romance_norm_ratio = cog_synset_validator.synset_to_romance_germanic_count[synset][1]/total                
##            other_norm_ratio = cog_synset_validator.synset_to_romance_germanic_count[synset][2]/total
#            
#            user_cognate_counts = {}
#            user_cognate_counts.clear()
#            for cognate in cognates_data.keys():                           
#                for user_index in range(len(cognates_data[cognate])):
#                    if user_index not in user_cognate_counts.keys():
#                        user_cognate_counts[user_index] = {}                        
#                        user_cognate_counts[user_index]["germanic_count"] = 0
#                        user_cognate_counts[user_index]["romance_count"] = 0
#                        user_cognate_counts[user_index]["other_count"] = 0
#                        user_cognate_counts[user_index]["total_count"] = 0
#                    try:
#                        origin = cog_synset_validator.synset_to_cognate_dict[synset][cognate]
#                    except:
#                        origin = "Other"
#                    if origin == "Germanic":
#                       user_cognate_counts[user_index]["germanic_count"] += cognates_data[cognate][user_index]
#                    elif origin == "Romance":
#                        user_cognate_counts[user_index]["romance_count"] += cognates_data[cognate][user_index]
#                    else:
#                        user_cognate_counts[user_index]["other_count"] += cognates_data[cognate][user_index]
#                        continue
#                    user_cognate_counts[user_index]["total_count"] += cognates_data[cognate][user_index]
#                
#            for user_index in range(len(cognates_data[cognate])):
#                
#                total = user_cognate_counts[user_index]["total_count"]
#                if total == 0:
#                    total = 1                
#                germanic_ratio = user_cognate_counts[user_index]["germanic_count"]/total
#                romance_ratio = user_cognate_counts[user_index]["romance_count"]/total
#                other_ratio = user_cognate_counts[user_index]["other_count"]/total
#                
#
#                norm3.write(",{},{},{} ".format(round(germanic_ratio,3), round(romance_ratio,3),round(other_ratio,3))) 
##                norm2.write(",{},{}".format(round(germanic_ratio,3), round(romance_ratio,3))) 
#            norm3.write("\n")                    
##            norm2.write("\n")                    
#                    
#            

            
            
            
            
            
            
            
#            valid_vectors.write("{}\n".format(header))            
#            for line in csvreader: 
#                synset = line[0]
#                if cog_synset_validator.isSynsetValid(synset):
#                    valid_vectors.write(str(line) + "\n")
#        
#    non_native_users_to_valid_cognate_count = {}
#    with open("non_native_user_to_valid_cognate_count.csv","r",encoding="utf-8") as non_native_users:
#        for line in non_native_users:
#           [user,count] = line.split(",")
#           non_native_users_to_valid_cognate_count[user] = int(count)
#        print(len(non_native_users_to_valid_cognate_count.values()))

    
  
                    
                
            
                    
                    
#                valid_synsets.write("{}\n".format(synset))
        
#    cog_synset_validator.write_valid_cognate_file("revised_short_cognate_foucs_set.csv")
    
        
if __name__ == '__main__':
    Main()                
        
    