from zipfile import ZipFile 

import os
import shutil

class Export(object):
    """docstring for Export"""
    def __init__(self, filename, cwd, port):
        super(Export, self).__init__()
        self.filename = filename
        self.origin = os.path.join(cwd, 'store', port)
        print('origin:', self.origin)
        self.destination = os.path.join(cwd, 'store')
        print('destination:', self.destination)
    
    def get_all_file_paths(self): 
        """get all file paths in the directory"""
        file_paths = []
        print('get all files', self.origin)

        # crawling through directory and subdirectories 
        for root, directories, files in os.walk(self.origin):
            for filename in files: 
                # join the two strings in order to form the full filepath. 
                filepath = os.path.join(root, filename) 
                file_paths.append(filepath) 

        # returning all file paths 
        return file_paths  
        
    def config(self):
        """zip and destroy dir"""
        try:
            file_paths = self.get_all_file_paths()
        except Exception as e:
            raise e
        
        os.chdir(self.destination)

        # writing files to a zipfile 
        with ZipFile(self.filename, 'w') as zip:
            # writing each file one by one
            for file in file_paths:
                zip.write(file)

        print('All files zipped successfully!')
        # shutil.rmtree(self.origin, ignore_errors=True, onerror=None)

        return 0
