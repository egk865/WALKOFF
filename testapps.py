import unittest
import os
import argparse
import importlib


def cmd_line():
    parser = argparse.ArgumentParser("Test Apps")
    parser.add_argument('-a', '--apps', nargs='*', type=str, required=False,
                        help='List of apps for which you would like to test')
    parser.add_argument('-A', '--all', action='store_true', help='Test all apps')
    args = parser.parse_args()
    return args


def available_apps():
    return [f for f in os.listdir(os.path.join('.', 'apps')) if (os.path.isdir(os.path.join('.', 'apps', f))
                                                                 and not f.startswith('__'))]


def get_tests(app_name):
    tests_path = os.path.join('.', 'apps', app_name, 'test')
    if os.path.isdir(tests_path):
        test_files = [os.path.splitext(f)[0]
                      for f in os.listdir(tests_path) if (os.path.isfile(os.path.join(tests_path, f))
                                                          and f.endswith('.py')
                                                          and f != '__init__.py')]
        print(test_files)
        test_modules = [importlib.import_module('apps.{0}.test.{1}'.format(app_name, test_module))
                        for test_module in test_files]
        return test_modules
    else:
        print('App {0} has no test directory!'.format(app_name))


def test_app(app_name):
    test_modules = get_tests(app_name)
    if test_modules:
        suite = unittest.TestSuite()
        suite.addTests([unittest.TestLoader().loadTestsFromModule(test_module)
                        for test_module in test_modules])
        unittest.TextTestRunner(verbosity=1).run(suite)
    elif len(test_modules) == 0:
        print('App {0} has no tests')

if __name__ == '__main__':
    cmd_args = cmd_line()
    all_apps = available_apps()
    if cmd_args.all:
        for app in all_apps:
            test_app(app)
    else:
        for app in cmd_args.apps:
            if app in all_apps:
                test_app(app)
            else:
                print('App {0} not found!'.format(app))
