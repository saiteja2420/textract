import json
from pprint import pprint

table_relation_type = ["MERGED_CELL,","CELL","TABLE_TITLE","TABLE_FOOTER"]
type_of_cell = ["TABLE_TITLE", "TABLE_FOOTER", "TABLE_SECTION_TITLE", "COLUMN_HEADER","TABLE_SUMMARY"]


with open("costmanagement.json","r") as jsondata:
    jsonobject =json.load(jsondata)


def get_get_blocks_map_table_blocks(jsonobject):
    blocks_map = {}
    table_blocks = []

    for i in jsonobject:
        blocks = i["Blocks"]
        for block in blocks:
            blocks_map[block['Id']] = block
            if block['BlockType'] == "TABLE":
                # print(block["EntityTypes"])
                table_blocks.append(block)
        if len(table_blocks) <= 0:
            print("<b> NO Table FOUND </b>")

    return blocks_map,table_blocks
page_1 = []
for i in jsonobject:
    
    blocks = i["Blocks"]
    for block in blocks:
        if block['BlockType'] == "LINE":
            pageno = block["Page"]
            if pageno==1:
                page_1.append(block)

distanceval = []
for index, table in enumerate(page_1):
    # s = {}
    # print(int(table["Geometry"]["BoundingBox"]["Left"]*594.9599609375))
    dist =int(table["Geometry"]["BoundingBox"]["Left"]*594.9599609375)
    # word = table["Text"]
    # s[word] = dist
    # distance.append(s)
    distanceval.append(dist)

print( min(distanceval))

dist = min(distanceval)
# if min(distanceval) in [26,27]:
#     mainhead = [31,32,33]
#     subhead = [35,36,37]
#     subval = [45,46,47]

# if min(distanceval) in [29,30]:
#     mainhead = [34,35,36]
#     subhead =[39,40]
#     subval = [50,51]
mainhead = [4,5,6,7]
subhead = [8,9,10,11]
subval = [18,19,20,21,22]


def fetch_table_titles(blocks_map,table_blocks):
    table_titles = {}
    for index, table in enumerate(table_blocks):
        for relationship in table['Relationships']:
            title = ''
            if relationship['Type'] == 'TABLE_TITLE':
                table_id = table["Id"]
                # print("table_id:",table_id)
                for child_id in relationship['Ids']:
                    # print(child_id)
                    table_title = blocks_map[child_id]
                    if table_title['BlockType'] == 'TABLE_TITLE':
                        # print(table_title)
                        if 'Relationships' in table_title:
                            # print(count)
                            for relationship in table_title['Relationships']:
                                if relationship['Type'] == 'CHILD':
                                    for child_id in relationship['Ids']:
                                                word = blocks_map[child_id]
                                                if word['BlockType'] == 'WORD':
                                                    title += word['Text'] + ' '
                                                
                # print(title,"ssssss")
                table_titles[table_id] = title

    return table_titles


def get_text_heading(blocks_map,table_blocks,table_titles):
    list_count = []
    rows_list = []
    row_count = 0 
    service_name = ""
    previous_type_word=""
    location = ""
    output_val = []
    soluion_provide = "Solution Provider Program Discounts"

    for index, table in enumerate(table_blocks):
        rows = {}    
        for relationship in table['Relationships']:
            if relationship['Type'] == 'CHILD':
                type_word =None
                table_id = table["Id"]
                for child_id in relationship['Ids']:
                    try:
                        k = 0 
                        cell = blocks_map[child_id]
                        if cell['BlockType'] == 'CELL':
                            row_index = cell['RowIndex']
                            col_index = cell['ColumnIndex']
                            if row_index not in rows:
                                rows[row_index] = {}
                            if col_index == 1:
                                if 'Relationships' in cell:
                                    for relationship in cell['Relationships']:
                                        if relationship['Type'] == 'CHILD': 
                                                for child_id in relationship['Ids']:
                                                        while k < 1:
                                                            word = blocks_map[child_id]
                                                            if word['BlockType'] == 'WORD':
                                                                val = (int(word["Geometry"]["BoundingBox"]["Left"]*594.9599609375)-dist)
                                                                if val in mainhead:
                                                                    # print(word['Text'])
                                                                # print(int(word["Geometry"]["BoundingBox"]["Left"]*594.9599609375),' ----------------',word["Text"])    
                                                                    type_word = "Main_head"
                                                                if val in subhead:
                                                                    type_word = "Sub_head"
                                                                if val in subval:
                                                                    type_word = "Sub_val"                                                               
                                                                if val in [29,30]:
                                                                    type_word = "Heading"                                                            
                                                                # print(int(word["Geometry"]["BoundingBox"]["Left"]*594.9599609375),' ----------------',word["Text"])
                                                                k = k+1
                                                                # print("type_word col1:",type_word)
                                                                rows[row_index]["type_word"] = type_word
                                else:
                                    rows[row_index]["type_word"] = "Sub_val"
                                    # print(cell)
                                    # if "EntityTypes" in cell:
                                    #     print(cell["EntityTypes"])
                            else:
                                pass
                                # type_word = ""
                                # print("else:",type_word)
                        

                        #extract text
                            text = ''
                            if 'Relationships' in cell:
                                for relationship in cell['Relationships']:
                                    if relationship['Type'] == 'CHILD':
                                        for child_id in relationship['Ids']:
                                            try:
                                                word = blocks_map[child_id]
                                                if word['BlockType'] == 'WORD':
                                                    text += word['Text'] + ' '
                                                if word['BlockType'] == 'SELECTION_ELEMENT':
                                                    if word['SelectionStatus'] == 'SELECTED':
                                                        text += 'X '
                                            except KeyError:
                                                print("Error extracting Table data - {}:".format(KeyError))
                            # print("assign:",type_word)
                            text = text[:-1] if text.endswith(" ") else text
                            rows[row_index][col_index] = text
                            
                            if table_id in table_titles:
                                rows["table_tile"] = table_titles[table_id]
                                # rows["type_word"] = type_word

                            # print(text)


                        # print(cell)
                    except KeyError:
                        print("Error extracting Table data - {}:".format(KeyError))
                        pass
        # rows_list.append(json.dumps(rows))
        rows =json.dumps(rows)
        rows =json.loads(rows)
        # print(rows,type(rows))
        if isinstance(rows, dict): 
            # print("AAAAAAAAAA") # Ensure that i is a dictionary
            row_count += 1  # Increment row count
            for row_index, cols in rows.items():
                
                if row_index =="table_tile":
                    # print(cols)

                    pass
                else:
                    if isinstance(cols, dict):
                        # print(cols)  # Ensure that cols is a dictionary
                        if "type_word" not in cols:
                            continue
                        for col_index, text in cols.items():

                            if col_index == "type_word":
                                # if cols["type_word"] == 'null':
                                    # print(cols,"None")
                                if cols["type_word"] == "Main_head":
                                    # print(cols)
        #                             #Ignore if main head has description or empty value
                                    if cols["1"] != "Description" and cols["1"] != "":
                                        
        #                                 #if special word "Solution Provider Program Discounts" found in heading convert it into a discount row. 
                                        if cols["1"]==soluion_provide:
                                            print("soluion_provide",cols.get("3", ""))
                                            row_data = {
                                                "row_count": row_count,
                                                "service_name": service_name,
                                                "location": location,
                                                "sub_service_name": sub_service_name,
                                                "description": cols.get("1", ""),
                                                "usage": "1",
                                                "Amount": cols.get("3", "")
                                            }
                                            output_val.append(row_data)
                                            continue  # no more main head so continuing here on
        #                                 # if "3" in cols:
        #                                 #     print(cols)
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
                                    elif count > 3:
                                        service_name = list_count[-2]
                                        location = list_count[-1]
                                    else:
                                        pass
                                        # print(count)
                                    list_count = []
                                    previous_type_word=cols["type_word"]
                                if cols["type_word"] == "Sub_val":
                                    # If any two out of "cols['1']", "cols['2']", and "cols['3']" are empty,
                                    # update the values of the last entry in output_val
                                    if ("1" in cols and "2" in cols and "3" in cols):
                                        if ((cols["1"] != "" or cols["2"] != "") and cols["3"]==""):
                                            last_entry = output_val[-1]
                                            last_entry["description"] = last_entry["description"] +cols["1"]
                                            last_entry["usage"] =last_entry["usage"]+ cols["2"]
                                        elif ((cols["1"] == "" or cols["2"] == "") and cols["3"]!=""): 
                                            pass
                                      
                                        
                                        # if cols["1"] == "" or cols["2"] == "" or cols["3"] == "":
                                        # if (cols["1"] != "" or cols["2"] != "") and cols["3"]=="": 
                                        #     last_entry = output_val[-1]
                                        #     last_entry["description"] = last_entry["description"] +cols["1"]
                                        #     last_entry["usage"] =last_entry["usage"]+ cols["2"]
                                            # last_entry["Amount"] =last_entry["Amount"]+ cols["3"] 
                                            
                                        # elif cols["1"] == "" and cols["3"] == "":
                                        #     last_entry = output_val[-1]
                                        #     last_entry["usage"] =last_entry["usage"]+ cols["2"]
                                        # elif cols["2"] == "" and cols["3"] == "":
                                        #     last_entry = output_val[-1]
                                        #     last_entry["description"] = last_entry["description"] +cols["1"]
                                        else:
                                            # print("else",cols.get("3", ""))
                                            val = cols.get("3", "")
                                            if val=='':
                                                val = "0.00"   
                                            val = val.replace("USD", "").replace(" ", "")
                                            if "(" in val and ")" in val:
                                                val = "-" + val.replace("(", "").replace(")", "")
                                            if "," ==val[-3]:
                                                val = val[:-3] +val[-3:].replace(",",'.')
                                            val = val.replace(",","")
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
                                    list_count = []
                                    previous_type_word=cols["type_word"]
                                            
                            else:
                                pass
                                # print(text)


    return output_val


blocks_map,table_blocks=get_get_blocks_map_table_blocks(jsonobject)
table_titles=fetch_table_titles(blocks_map,table_blocks)
rows_list = get_text_heading(blocks_map,table_blocks,table_titles)
# print(rows_list)
# output_val = respose_parser(rows_list)
# print(rows_list)
with open("costmanagement_outout_val_1.json","w") as r:
    r.write(json.dumps(rows_list))
