#Module contains al output writing scripts

import os

def write_output0(experiments,input_types,input_location,var_input_type,output_types,output_location):
    #wells: gr1-1,...,gr1-N,...,grN-1,...,grN-N
    for experiment in experiments:
        #Skipping dictionaries which are empty
        if input_types.index(var_input_type.get()) == 0: #removing file extention
            file_name = "converted_"+input_location.split("/")[-1][:-4]+"_"+experiment.split("/")[-1]+"_"+output_types[0].split(" - ")[1]+".tsv"
        else:
            file_name = "converted_"+input_location.split("/")[-1]+"_"+experiment.split("/")[-1]+"_"+output_types[0].split(" - ")[1]+".tsv"
        print("\t\t\t"+file_name)
        f_out_wells = open(os.path.join(output_location,file_name),"w")
        #header
        f_out_wells.write("Time_point")
        for group in sorted(experiments[experiment]["groups"]):
            for well in experiments[experiment]["groups"][group]:
               f_out_wells.write("\t"+group+"/"+well)
        f_out_wells.write("\n")
        #data
        for i, timepoint in enumerate(experiments[experiment]["timepoints"]):
            f_out_wells.write(timepoint)
            for group in sorted(experiments[experiment]["groups"]):
                well_number = len(experiments[experiment]["groups"][group])
                for well in experiments[experiment]["groups"][group]:
                    f_out_wells.write("\t"+experiments[experiment]["wells"][well][i])
            f_out_wells.write("\n")
        f_out_wells.close()

def write_output1(experiments,input_types,input_location,var_input_type,output_types,output_location):
    #average: average_gr1,...,average_grN
    for experiment in experiments:
        #Skipping dictionaries which are empty
        if input_types.index(var_input_type.get()) == 0: #removing file extention
            file_name = "converted_"+input_location.split("/")[-1][:-4]+"_"+experiment.split("/")[-1]+"_"+output_types[1].split(" - ")[1]+".tsv"
        else:
            file_name = "converted_"+input_location.split("/")[-1]+"_"+experiment.split("/")[-1]+"_"+output_types[1].split(" - ")[1]+".tsv"
        print("\t\t\t"+file_name)
        f_out_average = open(os.path.join(output_location,file_name),"w")
        #header
        f_out_average.write("Time_point")
        for group in sorted(experiments[experiment]["groups"]):
            f_out_average.write("\t"+group+"/Average")
        f_out_average.write("\n")
        #data
        for i, timepoint in enumerate(experiments[experiment]["timepoints"]):
            f_out_average.write(timepoint)
            for group in sorted(experiments[experiment]["groups"]):
                well_number = len(experiments[experiment]["groups"][group])
                average = round(sum([float(experiments[experiment]["wells"][x][i]) for x in experiments[experiment]["groups"][group]])/well_number,3)
                f_out_average.write("\t"+str(average))
            f_out_average.write("\n")

        f_out_average.close()


def write_output2(experiments,input_types,input_location,var_input_type,output_types,output_location):
    #wells: gr1-1,...,gr1-N,average_gr1,space,...,grN-1,...,grN-N,average_grN,space,
    for experiment in experiments:
        #Skipping dictionaries which are empty
        if input_types.index(var_input_type.get()) == 0: #removing file extention
            file_name = "converted_"+input_location.split("/")[-1][:-4]+"_"+experiment.split("/")[-1]+"_"+output_types[2].split(" - ")[1]+".tsv"
        else:
            file_name = "converted_"+input_location.split("/")[-1]+"_"+experiment.split("/")[-1]+"_"+output_types[2].split(" - ")[1]+".tsv"
        print("\t\t\t"+file_name)
        f_out_wells = open(os.path.join(output_location,file_name),"w")
        #header
        f_out_wells.write("Time_point")
        for group in sorted(experiments[experiment]["groups"]):
            for well in experiments[experiment]["groups"][group]:
               f_out_wells.write("\t"+group+"/"+well)
            f_out_wells.write("\t"+group+"/Average")
            f_out_wells.write("\t")
        f_out_wells.write("\n")
        #data
        for i, timepoint in enumerate(experiments[experiment]["timepoints"]):
            f_out_wells.write(timepoint)
            for group in sorted(experiments[experiment]["groups"]):
                well_number = len(experiments[experiment]["groups"][group])
                average = round(sum([float(experiments[experiment]["wells"][x][i]) for x in experiments[experiment]["groups"][group]])/well_number,3)
                for well in experiments[experiment]["groups"][group]:
                    f_out_wells.write("\t"+experiments[experiment]["wells"][well][i])
                f_out_wells.write("\t"+str(average))
                f_out_wells.write("\t")
            f_out_wells.write("\n")

        f_out_wells.close()  
