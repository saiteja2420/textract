import json
from pprint import pprint

table_relation_type = ["MERGED_CELL,","CELL","TABLE_TITLE","TABLE_FOOTER"]
type_of_cell = ["TABLE_TITLE", "TABLE_FOOTER", "TABLE_SECTION_TITLE", "COLUMN_HEADER","TABLE_SUMMARY"]

def get_text(result, blocks_map):
    text = ''
    if 'Relationships' in result:
        for relationship in result['Relationships']:
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

    return text

def get_rows_columns_map(table_result, blocks_map):
    rows = {}
    for relationship in table_result['Relationships']:
        if relationship['Type'] == 'CHILD':
            for child_id in relationship['Ids']:
                try:
                    cell = blocks_map[child_id]
                    if cell['BlockType'] == 'CELL':
                        row_index = cell['RowIndex']
                        col_index = cell['ColumnIndex']
                        if row_index not in rows:
                            # create new row
                            rows[row_index] = {}

                        # get the text value
                        rows[row_index][col_index] = get_text(cell, blocks_map)
                except KeyError:
                    print("Error extracting Table data - {}:".format(KeyError))
                    pass
    return rows

def get_table_csv_results(blocks):

    pprint(blocks)

    blocks_map = {}
    table_blocks = []
    for block in blocks:
        blocks_map[block['Id']] = block
        if block['BlockType'] == "TABLE":
            table_blocks.append(block)

    if len(table_blocks) <= 0:
        return "<b> NO Table FOUND </b>"

    csv = ''
    for index, table in enumerate(table_blocks):
        global count
        count = count+1
        csv += generate_table_csv(table, blocks_map, count)
        csv += '\n\n'
        # In order to generate separate CSV file for every table, uncomment code below
        #inner_csv = ''
        #inner_csv += generate_table_csv(table, blocks_map, index + 1)
        #inner_csv += '\n\n'
        #output_file = file_name + "___" + str(index) + ".csv"
        # replace content
        #with open(output_file, "at") as fout:
        #    fout.write(inner_csv)

    return csv
def generate_table_csv(table_result, blocks_map, table_index):
    rows = get_rows_columns_map(table_result, blocks_map)

    table_id = 'Table_' + str(table_index)

    # get cells.
    csv = 'Table: {0}\n\n'.format(table_id)

    for row_index, cols in rows.items():

        for col_index, text in cols.items():
            csv += '{}'.format(text) + ","
        csv += '\n'

    csv += '\n\n\n'
    return csv

with open("costmanagement.json","r") as jsondata:
    jsonobject =json.load(jsondata)

count = 0
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

rows = {}
chlid_relations = []
table_titles = {}
rows_list = []

cout = 0
csv__ = ''
count = 0
for index, table in enumerate(table_blocks):
    rows = {}

    for relationship in table['Relationships']:
        title = ''
        
        if relationship['Type'] == 'TABLE_TITLE':
            table_id = table["Id"]
            print("table_id:",table_id)
            for child_id in relationship['Ids']:
                print(child_id)
                table_title = blocks_map[child_id]
                if table_title['BlockType'] == 'TABLE_TITLE':
                    # print(table_title)
                    if 'Relationships' in table_title:
                        count = count+1
                        # print(count)
                        for relationship in table_title['Relationships']:
                            if relationship['Type'] == 'CHILD':
                                for child_id in relationship['Ids']:
                                            word = blocks_map[child_id]
                                            if word['BlockType'] == 'WORD':
                                                title += word['Text'] + ' '
                                            
            print(title,"ssssss")
            table_titles[table_id] = title

# print(table_titles)
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
                                                            # print(int(word["Geometry"]["BoundingBox"]["Left"]*594.9599609375),' ----------------',word["Text"])   
                                                            # print(word["Geometry"]["BoundingBox"]["Left"]) 
                                                            # with open("isnideloop.json",'a') as f:
                                                            #     f.write(json.dumps({word["Text"]:int(word["Geometry"]["BoundingBox"]["Left"]*594.9599609375)}))
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
    count = count +1

    rows_list.append(rows)

with open("costmanagement_rows_tittle_v1.json","w") as r:
    r.write(json.dumps(rows_list))
#     table_id = 'Table_' + str(count)
#     csv = 'Table: {0}\n\n'.format(table_id)
#     for row_index, cols in rows.items():

#         for col_index, text in cols.items():
#             csv += '{}'.format(text) + ","
#         csv += '\n'

#     csv += '\n\n\n'
#     csv__ +=  csv
#     csv__ += '\n\n'
# output_file = "file_name" + ".csv"
# output_file = "file_name" + ".csv"
# # replace content
# with open(output_file, "at") as fout:
#     fout.write(csv__)


    # print(rows)
    # print(count)
            
# print(table_blocks)
# json.dump(chlid_relations, open("childrelationship.json", "w"))
# json.dump(table_blocks, open("tableblocks.json", "w"))
# json.dump(blocks_map, open("blockmap.json", "w"))





