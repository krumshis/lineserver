from __future__ import absolute_import, print_function, unicode_literals

import os

from django.apps import AppConfig
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods

from .local_settings import BIG_FILE_NAME, CHUNK_SIZE, PROCESSED_INPUT_DIR

lines_registry = {}

class LinesConfig(AppConfig):
    name = 'lines'

    # From Django docs about method 'ready': "Override this method in
    # subclasses to run code when Django starts."
    def ready(self):
        preprocess_input()


# Read input text file line by line.
# Create multiple new input files with the following restrictions for their
# size: each file can not be larger than FILE_SIZE or 1 line (if 1 line is
# longer than that).
# Create a global dictionary in memory: key - line index in original input
# file, value - new file name and offset in bytes to the beginning of the
# line. For the sake of saving time the input file is big_filet in home
# directory, pocessed input files will be written to subdirectory
# processed_input under home directory.
def preprocess_input():
    global lines_registry
    cwd = os.getcwd()
    input_path = os.path.join(cwd, BIG_FILE_NAME)
    new_dir = os.path.join(cwd, PROCESSED_INPUT_DIR)
    current_file_number = 0
    current_file_size = 0
    current_path = os.path.join(new_dir, str(current_file_number))
    line_index = 0
    try:
        current_fp = open(current_path, "w")
    except Exception:
        print("Can't open %s" % current_path)
    with open(input_path, "r") as f:
        for line in f:
            # Can this line fit in the current file?
            # If not - cloe this one and open another.
            if current_file_size + len(line) > CHUNK_SIZE:
                current_file_number +=1
                current_file_size = 0
                try:
                    current_fp.close
                    current_path = os.path.join(new_dir, str(current_file_number))
                    current_fp = open(current_path, "w")
                except Exception:
                    print("Can't close or open file")
            # Write line to the file, write dictionary entry for the line.
            try:
                current_fp.write(line)
            except Exception:
                print("Can't write next line to file %s %s" % (current_path, line))
            lines_registry[line_index] = [current_path, current_file_size]
            current_file_size += len(line)
            line_index +=1


@require_http_methods(['GET'])
def get_line_by_index(request, line_index):
    global lines_registry
    total = len(lines_registry)
    index = int(line_index)
    if index >= total or index < 0:
        return HttpResponseBadRequest("Enter valid line index", 413)
    else:
        file_path = lines_registry[index][0]
        offset = lines_registry[index][1]
        try:
            fp = open(file_path, "r")
            fp.seek(offset, 0)
            line = fp.readline()
            fp.close()
        except Exception:
            return HttpResponseBadRequest("File error occured. Try again later.", 404)

        return HttpResponse(line, 200)
