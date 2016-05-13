import unittest
import os
from project.project_class import Project

class TestProject(unittest.TestCase):
    def setUp(self):
        self.test_project = Project(path=os.getcwd()+"/test_files", file_extension=".rea", column_signal=1, column_annot=2, column_sample_to_sample=1)
        self.test_project.set_Poincare()
        self.test_project.set_runs()
        self.test_project.set_LS_spectrum()
        self.test_project.step_through_project_files()
        self.test_project2 = Project(path=os.getcwd()+"/test_files2", file_extension=".rea", column_signal=1, column_annot=2, column_sample_to_sample=1)
        self.test_project2.set_runs()
        self.test_project2.step_through_project_files()

    def test_files_list(self):
        self.test_project.get_files_list()
        local_files_list = [item.split("/")[-1] for item in self.test_project.files_list]
        self.assertEqual(local_files_list, ['firest.rea', 'second.rea', 'third.rea'])

    def test_project_runs(self):
        self.assertTrue(True)

    def test_write_state(self):
        self.assertTrue(self.test_project.write_state())
        temp = self.test_project.path
        self.test_project.path = "/"
        self.assertFalse(self.test_project.write_state())
        self.test_project.path = temp

    def test_read_state(self):
        self.test_write_state()
        self.assertTrue(self.test_project.read_state())
        self.assertEqual(self.test_project.Poincare_state, 1)

    def test_dump_Poincare(self):
        """
        dumps the Poincare results for the test files, tests if the dumped file exists and cleans up
        :return:
        """
        import os
        self.test_project.dump_Poincare()
        local_path = self.test_project.build_name(prefix="PPoincare_") # double P so as to fool the build_name method
        # into NOT adding _1 to the name
        local_path = local_path.replace("PPoincare", "Poincare")
        self.assertTrue(os.path.exists(local_path))
        os.remove(local_path)

    def test_build_name(self):
        """
        this is a pseudo test - I just want to know if it fails
        ;return:
        """
        self.test_project.build_name()
        self.assertTrue(True)

    # def test_dump_Poincare(self):
    #     """
    #     this is a pseudo test - I just want to know if it fails
    #     :return:
    #     """
    #     self.test_project.dump_Poincare()
    #     self.assertTrue(True)

    def test_longest_runs(self):
        """

        :return:
        """
        max_dec, max_acc, max_neutral = self.test_project2.find_longest_runs()
        self.assertTrue(max_dec, 3)
        self.assertTrue(max_acc, 4)
        self.assertTrue(max_neutral, 2)

    def test_dump_runs(self):
        import os
        self.test_project.dump_runs()
        local_path = self.test_project.build_name(prefix="rruns_")  # double 'r' so as to fool the build_name method
        # into NOT adding _1 to the name
        local_path = local_path.replace("rruns", "runs")
        self.assertTrue(os.path.exists(local_path))
        os.remove(local_path)

if __name__ == '__main__':
    unittest.main()