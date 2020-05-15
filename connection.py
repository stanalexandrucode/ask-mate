import csv



#Create
def add_in_csv(filename,new_data, data_header):
    """
    :param new_data:
        data (dictionary - type) to be appended in csv file
    :param filename:
        allows the selection of a specific file
    """
    with open(filename, 'a', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=data_header)
        csv_writer.writerow(new_data)
    return 'Submitted successful'

#Read
def get_data(filename, data_id =None):
    """
    :param data_id:
        If given, it will act as a filter and return the dictionary of one specific id
        If not given, it will return a list of dictionaries with all the details
    :param filename:
        allows the selection of a specific file
    """
    csv_dict_list = []
    with open(filename, encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            csv_dict_list.append(row)

    if data_id is not None:
        for dictionary in csv_dict_list:
            if dictionary['id'] == str(data_id):
                return dictionary
    return csv_dict_list


#Update
def update_in_csv(update_id,update_dict, filename, data_header):
    list_of_all = get_data(filename)
    with open(filename, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=data_header)
        csv_writer.writeheader()
        for csv_row in list_of_all:
            if csv_row['id'] == update_id:
                csv_row = update_dict
            csv_writer.writerow(csv_row)
    return "update succesfull"


#Delete
def delete_in_csv(delete_id, filename,data_header):
    list_of_all = get_data(filename)
    with open(filename, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=data_header)
        csv_writer.writeheader()
        for i in range(len(list_of_all)-1):
            if list_of_all[i]['id'] == delete_id:
                del list_of_all[i]
            csv_writer.writerow(list_of_all[i])
    return "delete succesfull"




