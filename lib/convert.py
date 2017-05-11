import re
import os

def sort_textnum(l):
    #sorting string which are mixture of text and numbers
    convert = lambda text: float(text) if text.isdigit() else text
    alphanum = lambda key: [ convert(c) for c in re.split('([-+]?[0-9]*\.?[0-9]*)', key) ]
    l.sort( key=alphanum )
    return l

def read_in_timepoints_one_folder_experiments_in_different_folders(master_folder):
    #timepoints are in different files in the same folder
    #each file can contain only one experiment
    #different experiments are in different folders
    experiments = {}
    for folder in sorted(os.listdir(master_folder)):
        if os.path.isdir(os.path.join(master_folder,folder)):
            experiments[folder] = {}
            experiments[folder]["wells"] = {}
            experiments[folder]["timepoints"] = []
            experiments[folder]["groups"] = {}
            for file in sorted(os.listdir(os.path.join(master_folder,folder))):
                if file.endswith(".txt"):
                    f_in = open(os.path.join(master_folder,folder,file),'r', encoding='utf-16-le')
                    data = f_in.read()
                    f_in.close()            
                    experiments[folder] = get_experiment_data(data,experiments[folder],file[:-4])
            #Testing existence of proper files
            if experiments[folder]["timepoints"] == []:
                print("No suitable files found in folder \""+folder+"\"")
                del experiments[folder] #removes created experiment as it is empty
    #Testing existence of folders:
    if experiments == {}:
        print("No subfolders in in folder \""+master_folder+"\"")
        print("Subfolders for different experiments are needed")
    return experiments

def read_in_timepoints_one_folder(folder):
    #timepoints are in different files in the same folder
    #each file can contain only one experiment
    experiments = {}
    experiments[""] = {}
    experiments[""]["wells"] = {}
    experiments[""]["timepoints"] = []
    experiments[""]["groups"] = {}
    if len(os.listdir(folder)) == 0:
        print("Folder is empty")
    for file in sorted(os.listdir(folder)):
        if file.endswith(".txt"):
            f_in = open(os.path.join(folder,file),'r', encoding='utf-16-le')
            data = f_in.read()
            f_in.close()            
            experiments[""] = get_experiment_data(data,experiments[""],file[:-4])
    #Testing existence of proper files
    if experiments[""]["timepoints"] == []:
        print("No suitable files found")
        del experiments[""] #removes created experiment as it is empty
    return experiments
            

def read_in_timepoints_one_file(file):
    #time points are in one file
    #can contain different experiments, while time points are as individual plates
    f_in = open(file,'r', encoding='utf-16-le')
    data = f_in.read()
    f_in.close()
    experiments = {}
    data_by_experiment = data.split("ries\n~End \nP")
    #print("A",len(data_by_experiment))
    for i,experiment_data in enumerate(data_by_experiment):
        experiments[str(i)] = get_experiment_data(experiment_data,None,None)

    return experiments

def get_experiment_data(experiment_data,dic,timepoint):
    #test the given input dictionary
    #need to differentiate different modes on input data
    if dic == None:
        dic={}
        dic["wells"] = {}
        dic["timepoints"] = []
        dic["groups"] = {}
    #get plates
    ##plate finding criteria
    start_plate = "late:" #"Plate" without P
    end_plate = "~End"
    find_plates = re.compile(r'%s.*?%s' % (start_plate,end_plate),re.S)
    ##get plate data
    for j,plate in enumerate(find_plates.findall(experiment_data)):
        plate = plate.split("\n")
        #print(plate)
        ##get/test timepoint name
        if timepoint == None: #time points comes from plate name
            ##get plate name
            plate_name = plate[0].strip().split("\t")[1]
            dic["timepoints"].append(plate_name)
            #print("A",plate_name)
        else: #timepoint comes from filename
            dic["timepoints"].append(timepoint)
        ##get wells
        well_names = plate[1].strip().split("\t")[1:]
        well_values = plate[2].strip().split("\t")[1:]
        for k, well in enumerate(well_names):
            if well not in dic["wells"]:
                dic["wells"][well] = [well_values[k]]
            else:
                dic["wells"][well].append(well_values[k])

    #get groups
    ##group finding criteria
    start_group = "Group:"
    end_group = "Group Summ"
    find_groups = re.compile(r'%s.*?%s' % (start_group,end_group),re.S)
    #print("C",len(find_groups.findall(experiment_data)))
    for l,group in enumerate(find_groups.findall(experiment_data)):
        group=group.split("\n")
        ##get group name
        print(group)
        print(group[0].strip().split(" "))
        #group_name = group[0].strip().split(" ")[1]
        group_name = group[0][7:]
        #print("B",group_name)
        group_wells = sort_textnum(list(set([x.split("\t")[1] for x in group[2:-1]])))
        #print(group_wells)
        if group_name not in dic["groups"]:
            dic["groups"][group_name]=group_wells
    return dic

