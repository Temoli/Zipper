# Zipper  

This script is related to this one: Zip_Uploader - https://github.com/Temoli/Zip_Uploader  

On first run scrip will create three folders: Units, Zips and Tmp  
User by selecting '1' in menu can add unit by providing _unit name_ and _unit code_. It will create directory tree in Units folder:  
```bash
└── Units  
   └── _unit_name_  
       ├── allied  
       │   ├── email  
       │   └── paper  
       ├── nallied  
       │   ├── email  
       │   └── paper  
       └── urgent  
           ├── email  
           └── paper  
```
Then documents should be placed in the _email_ or _paper_ folder e.g. Units/_unit name_/nallied/email/  
User may copy documents to multiple units folders at the same time 

Option '5' in menu will compress all documents. A few changes will be made during the process:  
  1 - document filename will be changed to meet server requirements  
  2 - list of documents will be created in txt file  
  3 - all files will be archived into a zip file
 
Before compression starts script will ask user about zip file start number  
User has o check if something is in waiting/ folder in Zip_Uploader script which is constantly running on our team shared drive. If folder is empty user types 1, if something is in queue user has to type the next number after that one in queue. For example if last file in waiting is 05_xxx.zip then user types 6  
Documents are compressed and zip files will appear in Zips/ folder. Then this file has to be moved to waiting/ folder in Zip_Uploader location
