# convert_SoftMax_data
GUI to convert SoftMax 96-well plate reader data to "TSV" format.

## Requirements
1) Python 3+
 
    or

2) you can run also provided stand-alone executable without any prerequisites (single portable exe-file which works out of the box).
  
    Currently provided:
  
    [convert_SoftMax_data3_win8+.exe](https://github.com/luidale/convert_SoftMax_data/blob/master/convert_SoftMax_data3_win8+.exe)   - works at least in Windows 10 and Windows 8 (other OS-s not tested).

## Input
**Input has to be SoftMax output in column and txt format.**

**Wells have to be in groups, non groupped wells are discarded**

SoftMax output can be organized in different ways:

1) **One file**  -  Single file. 

    **Timepoints:** separate plates
    
    **Conditions:** separate experiments in a file

2) **One folder**  -  Single ore multiple files in one folder. 

    **Timepoints:** separate files 
    
    **Conditions:** just single condition

3) **One folder with subfolders**  -  Single ore multiple files in single or multiple subfolder. 
  
    **Timepoints:** separate files in one subfolder 
  
    **Conditions:** subfolders


## Output
**tsv format - can be opened with any spreadsheet application (eg. Excel, Calc) or text editors (eg. Notepad++).**

Data can be converted into different types:

1) **Wells**

    gr1-well-1,..,gr1-well-N,..,grN-well-1,..,grN-well-N

2) **Average**

    average_gr1,...,average_grN

3) **Wells+Average**

    gr1-well-1,..,gr1-well-N,average_gr1,space,..,grN-well-1,..,grN-well-N,average_grN
	
4) **Average+SD**

    average_gr1,...,average_grN,space,SD_gr1,...,SD_grN

You can request for other type of outputs
