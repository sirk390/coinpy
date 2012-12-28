from unittest import TestLoader
import unittest
import coverage

def run_unittests(do_coverage=True):
    loader = TestLoader()
    if do_coverage:
        cov = coverage.coverage(source=["coinpy"], branch=True)
        cov.start()
    suite = loader.discover("unit", pattern='test_*.py')
    
    runner = unittest.TextTestRunner()
    runner.run(suite)
    if do_coverage:
        
        cov.stop()
        cov.save()
        cov.html_report(directory="coverage_html")
    
if __name__ == '__main__':
    run_unittests()