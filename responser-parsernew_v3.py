import json 

#with open("rows_tittle_v1.json") as f:
with open("/home/prasanna/Music/cloudevolve/pdf-textract/updated_pdf_textract/costmanagement_rows_tittle_v1.json") as f:
    jsondata = json.load(f)
output_val = []
Main_head = ""
Sub_head = ""
location = ""
Sub_val = ""
list_count = []
max_length = 0
soluion_provide = "Solution Provider Program Discounts"
service_name = ""
sub_service_name=""
previous_type_word=""
row_count = 0  # Initialize row count
for i in jsondata:
    if isinstance(i, dict):  # Ensure that i is a dictionary
        row_count += 1  # Increment row count
        
        for row_index, cols in i.items():

            
            if row_index =="table_tile":
                pass
            else:
                if isinstance(cols, dict):  # Ensure that cols is a dictionary
                    if "type_word" not in cols:
                        continue
                    
                    for col_index, text in cols.items():
                        if col_index == "type_word":
                            if "3" in cols:
                                val = cols["3"]
                                if val=='':
                                    val = "0.00"   
                                    val = val.replace("USD", "").replace(" ", "")
                                    if "(" in val or ")" in val:
                                        val = "-" + val.replace("(", "").replace(")", "")
                                    if "," ==val[-3]:
                                        val = val[:-3] +val[-3:].replace(",",'.')
                                    val = val.replace(",","")
                            if cols["type_word"] == "Main_head":
                                #Ignore if main head has description or empty value
                                if cols["1"] != "Description" and cols["1"] != "":
                                    #if special word "Solution Provider Program Discounts" found in heading convert it into a discount row. 
                                    if cols["1"]==soluion_provide:
                                        row_data = {
                                            "row_count": row_count,
                                            "service_name": service_name,
                                            "location": location,
                                            "sub_service_name": sub_service_name,
                                            "description": cols.get("1", ""),
                                            "usage": "1",
                                            "Amount": val
                                        }
                                        output_val.append(row_data)
                                        continue  # no more main head so continuing here on
                                    # if "3" in cols:
                                    #     print(cols)
                                    list_count.append(cols["1"])
                                    previous_type_word=cols["type_word"]
                                    continue  
                            elif cols["type_word"] == "Sub_head" or (previous_type_word=="Main_head" and cols["type_word"]!="Main_head"):
                                sub_service_name=cols["1"]
                                count = len(list_count)
                                if count == 1:
                                    #location = cols["1"]
                                    location = list_count[0]
                                elif count == 2:
                                    service_name = list_count[0]
                                    location = list_count[1]
                                elif count >2:
                                    service_name = list_count[-2]
                                    location = list_count[-1]
                                else:
                                    print(count)
                                list_count = []
                                previous_type_word=cols["type_word"]
                            if cols["type_word"] == "Sub_val":
                                # If any two out of "cols['1']", "cols['2']", and "cols['3']" are empty,
                                # update the values of the last entry in output_val
                                if ("1" in cols and "2" in cols and "3" in cols):
                                    # if cols["1"] == "" or cols["2"] == "" :
                                    #     print("inside subval2",cols)
                                    # if (cols["1"] == "" or cols["2"] == "") or (cols["1"] != "" and cols["2"] != "" and cols["3"] == "") :
                                    if ((cols["1"] != "" or cols["2"] != "") and cols["3"]==""):
                                        last_entry = output_val[-1]
                                        last_entry["description"] = last_entry["description"] +cols["1"]
                                        last_entry["usage"] =last_entry["usage"]+ cols["2"]
                                    elif ((cols["1"] == "" or cols["2"] == "") and cols["3"]!=""): 
                                        pass
                                      
                                        # last_entry["Amount"] =last_entry["Amount"]+ cols["3"] 
                                        
                                    # elif cols["1"] == "" and cols["3"] == "":
                                    #     last_entry = output_val[-1]
                                    #     last_entry["usage"] =last_entry["usage"]+ cols["2"]
                                    # elif cols["2"] == "" and cols["3"] == "":
                                    #     last_entry = output_val[-1]
                                    #     last_entry["description"] = last_entry["description"] +cols["1"]
                                    else:
                                        row_data = {
                                            "row_count": row_count,
                                            "service_name": service_name,
                                            "location": location,
                                            "sub_service_name": sub_service_name,
                                            "description": cols.get("1", ""),
                                            "usage": cols.get("2", ""),
                                            "Amount": val
                                        }
                                        output_val.append(row_data)
                                previous_type_word=cols["type_word"]
                                list_count = []        
                        else:
                            pass
                            # print(text)

with open("output_costmanagement_rows_tittle_v1.json","w") as r:
    r.write(json.dumps(output_val))
