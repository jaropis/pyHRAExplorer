import unittest
import os
from project.project_class import Project

class TestProject(unittest.TestCase):
    def setUp(self):
        self.test_project = Project(path=os.getcwd()+"/test_files", file_extension=".rea", column_signal=1, column_annot=2, column_sample_to_sample=1)

    def test_files_list(self):
        self.test_project.get_files_list()
        local_files_list = [item.split("/")[-1] for item in self.test_project.files_list]
        self.assertEqual(local_files_list, ['firest.rea', 'second.rea', 'third.rea'])

    def test_project_runs(self):
        self.test_project.set_Poincare()
        self.test_project.set_runs()
        self.test_project.set_LS_spectrum()
        self.test_project.step_through_project_files()
        self.assertTrue(True)

    # def test_write_state(self):
    #     self.assertTrue(self.test_project.write_state())
    #     temp = self.test_project.path
    #     self.test_project.path = "/"
    #     self.assertFalse(self.test_project.write_state())
    #     self.test_project.path = temp

    # def test_read_state(self):
    #     self.test_write_state()
    #     self.assertTrue(self.test_project.read_state())
    #     self.assertEqual(self.test_project.Poincare_state, 0)
if __name__ == '__main__':
    unittest.main()