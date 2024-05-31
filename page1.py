import json
file = '/home/prasanna/Documents/learnings/bills-textract/CS-master-Oct.json'
with open("costmanagement.json","r") as jsondata:
    jsonobject =json.load(jsondata)

count = 0
blocks_map = {}
table_blocks = []
page_1 = []
for i in jsonobject:
    
    blocks = i["Blocks"]
    for block in blocks:
        blocks_map[block['Id']] = block
        if block['BlockType'] == "LINE":
            pageno = block["Page"]
            if pageno==1:
                page_1.append(block)

            
            # print(block["EntityTypes"])
            table_blocks.append(block)
    if len(table_blocks) <= 0:
        print("<b> NO Table FOUND </b>")
        
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

values = []
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
                            type_word =None
                            if 'Relationships' in cell:
                                for relationship in cell['Relationships']:
                                    if relationship['Type'] == 'CHILD': 
                                            for child_id in relationship['Ids']:
                                                    while k < 1:
                                                        word = blocks_map[child_id]
                                                        if word['BlockType'] == 'WORD':
                                                            val = int(word["Geometry"]["BoundingBox"]["Left"]*594.9599609375)
                                                            # print(word['Text'])
                                                            values.append(val)
                                                            print(int(word["Geometry"]["BoundingBox"]["Left"]*594.9599609375),' ----------------',word["Text"])   
                                                            print(word["Geometry"]["BoundingBox"]["Left"]) 
                                                            with open("isnideloop-word.json",'a') as f:
                                                                f.write(json.dumps({word["Text"]:int(word["Geometry"]["BoundingBox"]["Left"]*594.9599609375)}))
                                                            if val in [31,32,33]:
                                                                type_word = "Main_head"
                                                            if val in [35,36,37]:
                                                                type_word = "Sub_head"
                                                            if val in [45,46,47]:
                                                                type_word = "Sub_val"                                                               
                                                            if val in [29,30]:
                                                                type_word = "Heading"                                                            
                                                            # print(int(word["Geometry"]["BoundingBox"]["Left"]*594.9599609375),' ----------------',word["Text"])
                                                            k = k+1
                                                            # print("type_word col1:",type_word)
                                                            rows[row_index]["type_word"] = type_word
                            else:
                                rows[row_index]["type_word"] = "Sub_val"
                                print(cell)
                                # if "EntityTypes" in cell:
                                #     print(cell["EntityTypes"])
                        else:
                            pass

                except Exception as e:
                    print(e)
        
print(set(values))

# for index, table in enumerate(page_1):
#      for relationship in table['Relationships']:
#         if relationship['Type'] == 'TABLE_TITLE':
#              for child_id in relationship['Ids']:
#                  cell = blocks_map[child_id]
#                 #  print(cell)
#                 #  print("**********")
#                 #  print(int(cell["Geometry"]["BoundingBox"]["Left"]*594.9599609375))
#                 #  if cell['BlockType'] == 'TABLE_TITLE':
                    
# distance = []
# distanceval = []
# for index, table in enumerate(page_1):
#     s = {}
#     # print(int(table["Geometry"]["BoundingBox"]["Left"]*594.9599609375))
#     dist =int(table["Geometry"]["BoundingBox"]["Left"]*594.9599609375)
#     word = table["Text"]
#     s[word] = dist
#     distance.append(s)
#     distanceval.append(dist)
#     #  for relationship in table['Relationships']:
#     #     if relationship['Type'] == 'TABLE_TITLE':
#     #          for child_id in relationship['Ids']:
#     #              cell = blocks_map[child_id]
#     #              print(cell)
#     #              print("**********")
#     #              print(int(cell["Geometry"]["BoundingBox"]["Left"]*594.9599609375))
# print(min(distanceval))
# with open("isnideloopoct.json","w") as f:
#     f.write(json.dumps(distance))