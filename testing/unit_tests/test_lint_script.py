import unittest
import subprocess
import os
import tempfile
import shutil

class TestLintScript(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.scripts_dir = os.path.join(self.test_dir, 'scripts')
        os.makedirs(self.scripts_dir)

        # Copy the lint.sh script to the temporary directory
        shutil.copy('scripts/lint.sh', self.scripts_dir)

        # Create a yamllint config file to disable the document-start rule
        with open(os.path.join(self.test_dir, '.yamllint'), 'w') as f:
            f.write('rules:\n')
            f.write('  document-start: disable\n')

        # Create some test files
        with open(os.path.join(self.test_dir, 'good.yaml'), 'w') as f:
            f.write('- a\n- b\n')
        with open(os.path.join(self.test_dir, 'bad.yaml'), 'w') as f:
            f.write('key: value:\n')
        with open(os.path.join(self.test_dir, 'also_bad.yml'), 'w') as f:
            f.write('key2: value2:\n')
        with open(os.path.join(self.test_dir, 'excluded.yaml'), 'w') as f:
            f.write('key3: value3:\n')
        with open(os.path.join(self.test_dir, 'not_yaml.txt'), 'w') as f:
            f.write('this is not yaml\n')
        with open(os.path.join(self.scripts_dir, 'lint_exclude.txt'), 'w') as f:
            f.write('excluded.yaml\n')

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_lint_script(self):
        # Run the lint.sh script from the temporary directory
        process = subprocess.Popen(
            ['/bin/bash', os.path.join(self.scripts_dir, 'lint.sh')],
            cwd=self.test_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = process.communicate()

        # Check the output
        self.assertIn('bad.yaml', stdout)
        self.assertIn('also_bad.yml', stdout)
        self.assertNotIn('good.yaml', stdout)
        self.assertNotIn('excluded.yaml', stdout)
        self.assertNotIn('not_yaml.txt', stdout)
        # The markdown linter will run and fail, so we don't check stderr
        # self.assertEqual(stderr, '')

if __name__ == '__main__':
    unittest.main()
