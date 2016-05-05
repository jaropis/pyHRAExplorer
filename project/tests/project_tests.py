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

    def test_project_runs(self):
        self.test_project.step_through_project_files()
        self.assertTrue(True)

    def test_write_state(self):
        self.assertTrue(self.test_project.write_state())
        temp = self.test_project.path
        self.test_project.path = "/"
        self.assertFalse(self.test_project.write_state())
        self.test_project.path = temp
if __name__ == '__main__':
    unittest.main()