from unittest import TestLoader
import unittest
import coverage

def run_unittests(do_coverage=True):
    loader = TestLoader()
    suite = loader.discover("unit", pattern='test_*.py')
    if do_coverage:
        cov = coverage.coverage(source=["coinpy"])
        cov.start()
    
    runner = unittest.TextTestRunner()
    runner.run(suite)
    if do_coverage:
        
        cov.stop()
        cov.save()
        cov.html_report(directory="coverage_html")
    
if __name__ == '__main__':
    run_unittests()