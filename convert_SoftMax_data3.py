# script to convert SoftMax data
import re
import os
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import lib.convert
import lib.write
#import filedialog


     

def browse_input_file():
    #selects movie database and generates list of types, genres and movies
    global input_location_box
    input_location_box.delete("0.0","end")
    global input_location
    input_location = filedialog.askopenfilename(parent=root,title='Choose a file',filetypes=[('dbfiles', '.txt'), ('all files', '.*')])#,initialdir="./data")
    #test input emptiness
    if input_location =="":
        return
    #TEST INPUT
    if test_input_file_column(input_location):
        #change location
        input_location_box.insert("end", input_location.replace("/","\\")+"\n")
        #show output filenames
        change_output_filenames(1)
    else:
        #warning window
        open_warning("Wrong file type","input")

        
    
def browse_input_folder():
    #selects movie database and generates list of types, genres and movies
    global input_location_box
    input_location_box.delete("0.0","end")
    global input_location
    input_location = filedialog.askdirectory(parent=root,title='Choose a folder')#,initialdir="./data")
    #test input emptiness
    if input_location == "":
        return
    #TEST input type 2
    if input_types.index(var_input_type.get()) == 1:
        #test emptyness of folder
        if len(os.listdir(input_location)) != 0:
            #goes through all files
            for file in sorted(os.listdir(input_location)):
                if file.endswith(".txt"):
                    if test_input_file_column(os.path.join(input_location,file)):
                        #change location
                        input_location_box.insert("end", input_location.replace("/","\\")+"\n")
                        #show output filenames
                        change_output_filenames(1)
                        break
            else:
                open_warning("Folder does not contain proper files","input")
        else:
            open_warning("Folder is empty","input")
            
    #TEST input type 3
    elif input_types.index(var_input_type.get()) == 2:
        #test existence of folders in this folder
        if len(next(os.walk(input_location))[1]) != 0:
            #test subfolders for suitable file
            for folder in sorted(os.listdir(input_location)):
                #testing it is directory
                if os.path.isdir(os.path.join(input_location,folder)):
                    #testing files in subfolder
                    if len(os.listdir(os.path.join(input_location,folder))) != 0:
                        #goes through all files
                        for file in sorted(os.listdir(os.path.join(input_location,folder))):
                            #tests it is .txt file
                            if file.endswith(".txt"):
                                #tests it is suitable file
                                if test_input_file_column(os.path.join(input_location,folder,file)):
                                    break
                        else:
                            open_warning("Subfolder \""+folder+"\" does not contain proper files","input")
                            break
                    else:
                        open_warning("Subfolder \""+folder+"\" is empty","input")
                        break    
            #change location
            input_location_box.insert("end", input_location.replace("/","\\")+"\n")
            #show output filenames
            change_output_filenames(1)
            
        else:
            open_warning("No subfolders in selected folder:\n \""+input_location+"\"","input")


def open_warning(text,warning_type):
    print(text)
    ##root_warning = Toplevel()
    #root_warning.geometry(str(len(str(text)*8))+"x40")
    #root_warning.configure(background='red')
    #frame=Frame(root_warning,bg="red")
    #frame.place(x=0,y=0)
    #label_warning = Label(frame, text = text,
    #             font=18,bg="red")
    #label_warning.grid(row=0, column=0,sticky = N)
    #empty output and input names and labels
    messagebox.showinfo("Error",message=text)
    if warning_type == "input":
        global input_location
        input_location = ""
        change_output_filenames(1)
    
    

def change_output_filenames(arg):
    ##changing input filenames
    #show output filenames
    try:
        #to remove previous select_input button if exists
        global label_output_filenames2
        label_output_filenames2["text"]=""
    except:
        UnboundLocalError
    global input_location
    output_type_index = output_types.index(var_output_type.get())
    if input_location != "":
        if var_input_type.get().find("file") != -1:
            output_filenames2 = "converted_"+input_location.split("/")[-1][:-4]+"_XXX_"+output_types[output_type_index].split(" - ")[1]+".tsv"
            #label_output_filenames2 = Label(frame_output_type, text = "converted_"+input_location.split("/")[-1][:-4]+"_XXX_"+output_types[output_type_index].split(" - ")[1]+".tsv",bg="white")
        if var_input_type.get().find("folder") != -1:
            output_filenames2 = "converted_"+input_location.split("/")[-1]+"_XXX_"+output_types[output_type_index].split(" - ")[1]+".tsv"
            #label_output_filenames2 = Label(frame_output_type, text = "converted_"+input_location.split("/")[-1]+"_XXX_"+output_types[output_type_index].split(" - ")[1]+".tsv",bg="white")
        #label_output_filenames2.grid(row=8, column=0,sticky = W,padx=5)
        label_output_filenames2["text"]=output_filenames2
    #change output type description
    label_output_type_description_text["text"]=output_type_descriptions[output_types.index(var_output_type.get())]


def browse_output_folder():
    #selects movie database and generates list of types, genres and movies
    global output_location
    output_location = filedialog.askdirectory(parent=root,title='Choose a folder',initialdir=".")
    #change location
    global text_output_location
    text_output_location.delete("0.0","end")
    text_output_location.insert("end", output_location.replace("/","\\")+"\n")   


def convert_file():
    #testing existence of input
    #global input_location
    if input_location == "":
        open_warning("No input chosen",None)
        return
    try:
        #to remove previous select_input button if exists
        global output_location
        if output_location == "":
            return
    except:
        open_warning("No output location chosen",None)
        return
        UnboundLocalError
    
    #converting
    print("Input")
    print("\ttype:")
    print("\t\t"+var_input_type.get())
    input_type = input_types.index(var_input_type.get())

    if input_type == 0:
        print("\tfile:")
        print("\t\t"+input_location)
        experiments=lib.convert.read_in_timepoints_one_file(input_location)
    if input_type == 1:
        print("\tfolder:")
        print("\t\t"+input_location)
        print("\t\tfile:")
        experiments=lib.convert.read_in_timepoints_one_folder(input_location)
    if input_type == 2:
        print("\tfolder:")
        print("\t\t"+input_location)
        experiments=lib.convert.read_in_timepoints_one_folder_experiments_in_different_folders(input_location)
    #writing to the file

    output_type = output_types.index(var_output_type.get())
    print("Output")
    print("\ttype:")
    print("\t\t"+var_output_type.get())
    print("\tfolder:")
    print("\t\t"+output_location)    
    print("\t\tfiles:")
    if output_type == 0:
        lib.write.write_output0(experiments,input_types,input_location,var_input_type,output_types,output_location)
    if output_type == 1:
        lib.write.write_output1(experiments,input_types,input_location,var_input_type,output_types,output_location)
    if output_type == 2:
        lib.write.write_output2(experiments,input_types,input_location,var_input_type,output_types,output_location)

def get_input_types(value):
    #to remove previous select_input button if exists
    try:
        global select_input_button
        select_input_button.destroy()
    except:
        UnboundLocalError

    #selecting rigth button text
    if input_types.index(var_input_type.get())==0:
        button_text = "Select input file"
        select_input_button = Button(frame_input_location, text=button_text, command=browse_input_file)
        sign_input_selected_text = "Selected file:"
    elif input_types.index(var_input_type.get())==1 or input_types.index(var_input_type.get())==2:
        button_text = "Select input folder"
        select_input_button = Button(frame_input_location, text=button_text, command=browse_input_folder)
        sign_input_selected_text = "Selected folder:"
    select_input_button.grid(row=1, column=0,sticky=W,padx=5,pady=2)

 
    label_input_type_description_text["text"]=input_type_descriptions[input_types.index(var_input_type.get())]

    #change previous selected file/folder label
    #global label_input_selected
    label_input_selected["text"]=sign_input_selected_text
    
    #clean input location box
    try:
        global input_location_box
        input_location_box.delete("0.0","end")
    except:
        ValueError
        
    #clean input location box
    try:
        global input_location
        input_location = ""
    except:
        ValueError
        
    #change output filenames
    try:
        #to remove previous select_input button if exists
        global label_output_filenames2
        label_output_filenames2["text"]=""
    except:
        UnboundLocalError

#testing input
def test_input_file_column(file):
    #testing existence of some simple texts
    f_in = open(file,'r', encoding='utf-16-le')
    data = f_in.read()
    f_in.close()
    #testing column setup
    start_test = "Plate:" 
    end_test = "A1\tA2"
    find_plates = re.compile(r'%s.*?%s' % (start_test,end_test),re.S)
    if len(find_plates.findall(data)) > 0:
        #testing Group setup
        start_test2 = "Group:" 
        end_test2 = "Sample\tWell\tConcentration\tValues\tMeanValue\tStd.Dev.\tCV%"
        find_groups = re.compile(r'%s.*?%s' % (start_test2,end_test2),re.S)       
        if len(find_groups.findall(data)) > 0:
            return True
        else:
            return False
    else:
        return False

def open_manual():
    import webbrowser
    url = "https://github.com/luidale/convert_SoftMax_data"
    webbrowser.open(url, new=0, autoraise=True)

def open_aboutDialog():
    import lib.aboutDialog
    lib.aboutDialog.AboutDialog(root,"About SoftMax data converter")
    
######GUI#######
###General

    
root = Tk()
root.geometry("530x800")
root.title("convert_SoftMax_data")

###Create menus
menubar = Menu(root)
helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="Manual", command=open_manual)
helpmenu.add_command(label="About", command=open_aboutDialog)
menubar.add_cascade(label="Help", menu=helpmenu)
root.config(menu=menubar)

###Input data frame
frame_input=Frame(root,bg="white")
frame_input.place(x=20,y=20)
label_input_data = Label(frame_input, text = "Input data", pady=5,font=(None,16, "bold"),bg="white")
label_input_data.grid(row=0, column=0,sticky = W,padx=5)
frame_input.grid_rowconfigure(1, minsize=200)
frame_input.grid_columnconfigure(1, minsize=375)

##Input type frame
frame_input_type=Frame(frame_input,bg="white")
frame_input_type.place(x=10,y=40)
label_input_type = Label(frame_input_type,text = "Type",bg="white",font=(None,9, "bold"))
label_input_type.grid(row=0, column=0,sticky = W,padx=5)
#Input type optionmenu
input_types =["1 - one file","2 - one folder","3 - one folder with subfolders"]
var_input_type = StringVar()
var_input_type.set(input_types[0])
menu_input_type = OptionMenu(frame_input_type,var_input_type,*input_types,command = get_input_types)
menu_input_type.grid(row=1, column=0,sticky = W,padx=5)
frame_input_type.grid_rowconfigure(2, minsize=10)
#Input type description
label_input_type_description_label = Label(frame_input_type, text = "Type description:",bg="white",font=(None,9, "bold"))
label_input_type_description_label.grid(row=3, column=0,sticky = W,padx=5)
input_type_descriptions =["Single \".txt\" file in a column format.\n\tTime points: separate plates \n\tConditions: separate experiments in a file",\
                          "Single or multiple \".txt\" files in a column format in one folder.\n\tTime points: separate files \n\tConditions: just single condition",\
                          "Single or multiple \".txt\" files in a column format in single or multiple subfolders.\n\tTime points: separate files in one subfolder\n\tConditions: subfolders"]
label_input_type_description_text = Label(frame_input_type, text = input_type_descriptions[input_types.index(var_input_type.get())],bg="white",justify=LEFT)
label_input_type_description_text.grid(row=4, column=0,sticky = W,padx=5)
frame_input_type.grid_rowconfigure(5, minsize=10)
#Selected file
label_input_selected = Label(frame_input_type, text = "Selected file:",bg="white",font=(None,9, "bold"))
label_input_selected.grid(row=6, column=0,sticky = W,padx=5)
frame_input.grid_rowconfigure(6, minsize=20)
#Selected file text
yscrollbar_location = Scrollbar(frame_input_type)
yscrollbar_location.grid(row=7, column=1, sticky=N+S)
input_location_box = Text(frame_input_type,width=55, height=2,yscrollcommand = yscrollbar_location.set)
yscrollbar_location.config(command=input_location_box.yview)
input_location_box.grid(row=7, column=0, sticky=N+S+E+W,padx=5)

##Location frame
frame_input_location=Frame(frame_input,bg="white")
frame_input_location.place(x=250,y=40)
label_input_location = Label(frame_input_location, text = "Location",bg="white",font=(None,9, "bold"))
label_input_location.grid(row=0, column=0,sticky = W,padx=5)
#Location selection button
input_location = ""
get_input_types(1)



###Output data frame
frame_output=Frame(root,bg="white")
frame_output.place(x=20,y=290)
label_output_data = Label(frame_output, text = "Output data", pady=5,font=(None,16, "bold"),bg="white")
label_output_data.grid(row=0, column=0,sticky = W,padx=5)
frame_output.grid_rowconfigure(1, minsize=198)
frame_output.grid_columnconfigure(1, minsize=356)

##output type frame
frame_output_type=Frame(frame_output,bg="white")
frame_output_type.place(x=10,y=40)
label_output_type = Label(frame_output_type,text = "Type",bg="white",font=(None,9, "bold"))
label_output_type.grid(row=0, column=0,sticky = W,padx=5)
#output type optionmenu
output_types =["1 - wells","2 - average","3 - wells+average"]
var_output_type = StringVar()
var_output_type.set(output_types[0])
menu_output_type = OptionMenu(frame_output_type,var_output_type,*output_types,command=change_output_filenames)#,command = get_output_location)
menu_output_type.grid(row=1, column=0,sticky = W,padx=5)
frame_output_type.grid_rowconfigure(2, minsize=10)

#Input type description
label_output_type_description_label = Label(frame_output_type, text = "Type description:",bg="white",font=(None,9, "bold"))
label_output_type_description_label.grid(row=3, column=0,sticky = W,padx=5)
output_type_descriptions =["gr1-well-1,..,gr1-well-N,..,grN-well-1,..,grN-well-N",\
                          "average_gr1,...,average_grN",\
                          "gr1-well-1,..,gr1-well-N,average_gr1,space,..,grN-well-1,..,grN-well-N,average_grN"]

label_output_type_description_text = Label(frame_output_type, text = output_type_descriptions[output_types.index(var_output_type.get())],bg="white",justify=LEFT)
label_output_type_description_text.grid(row=4, column=0,sticky = W,padx=5)
frame_output_type.grid_rowconfigure(5, minsize=10)

#Selected file
label_output_selected = Label(frame_output_type, text = "Selected folder:",bg="white",font=(None,9, "bold"))
label_output_selected.grid(row=6, column=0,sticky = W,padx=5)
frame_output.grid_rowconfigure(3, minsize=20)
#Selected file text
yscrollbar_text_output_location = Scrollbar(frame_output_type)
yscrollbar_text_output_location.grid(row=7, column=1, sticky=N+S)
text_output_location = Text(frame_output_type,width=55, height=2,yscrollcommand = yscrollbar_text_output_location.set)
yscrollbar_text_output_location.config(command=text_output_location.yview)
text_output_location.grid(row=7, column=0, sticky=N+S+E+W,padx=5)
frame_output.grid_rowconfigure(5, minsize=20)
#File names
frame_output_type.grid_rowconfigure(8, minsize=10)
label_output_selected = Label(frame_output_type, text = "Output files:",font=(None,9, "bold"),bg="white")
label_output_selected.grid(row=9, column=0,sticky = W,padx=5)
label_output_filenames2 = Label(frame_output_type, text = "",bg="white")
label_output_filenames2.grid(row=10, column=0,sticky = W,padx=5)

##Location frame
frame_output_location=Frame(frame_output,bg="white")
frame_output_location.place(x=250,y=40)
label_output_location = Label(frame_output_location, text = "Location",bg="white",font=(None,9, "bold"))
label_output_location.grid(row=0, column=0,sticky = W,padx=5)
#Location selection button
button_output_select = Button(frame_output_location, text="Select output folder", command=browse_output_folder)
button_output_select.grid(row=1, column=0,sticky=W,padx=5,pady=2)

###Convert data frame
frame_convert=Frame(root)
frame_convert.place(x=180,y=572)
button_convert = Button(frame_convert, text="Convert data",font=(None,16, "bold"), command=convert_file)
button_convert.grid(row=0, column=0,sticky=W)


###Output frame
frame_run=Frame(root)
frame_run.place(x=20,y=620)
yscrollbar_text_run = Scrollbar(frame_run)
yscrollbar_text_run.grid(row=1, column=1, sticky=N+S)
text_run = Text(frame_run,width=59, height=10,yscrollcommand = yscrollbar_text_run.set)
yscrollbar_text_run.config(command=text_run.yview)
text_run.grid(row=1, column=0, sticky=N+S+E+W,padx=1)



#Directs all printings to "text_run" box
def redirector(inputStr):
    text_run.insert(INSERT, inputStr)
    text_run.yview(END) #shows last lines

sys.stdout.write = redirector
sys.stderr.write = redirector

mainloop()







