import unittest


suites = unittest.TestLoader().discover(".")
runner = unittest.TextTestRunner(verbosity=2)
runner.run(suites)
