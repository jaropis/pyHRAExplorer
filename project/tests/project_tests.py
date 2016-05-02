import unittest
import os
from project.project_class import Project

class TestProject(unittest.TestCase):
    def setUp(self):
        self.test_project = Project(path=os.getcwd()+"/test_files", file_extension=".rea")

    def test_files_list(self):
        self.test_project.get_files_list()
        local_files_list = [item.split("/")[-1] for item in self.test_project.files_list]
        self.assertEqual(local_files_list, ['firest.rea', 'second.rea', 'third.rea'])

if __name__ == '__main__':
    unittest.main()