#!/usr/bin/env python

from argparse import ArgumentParser
from UserPackages import UserPackages


def main():
  """Display the user installed packages."""
  # Get the command line input arguments
  parser = ArgumentParser()
  parser.add_argument('--default', action='store_true', help='List manually installed packages using aptitude to identify potentially manual installed packages')
  parser.add_argument('--aptmark', action='store_true', help='List manually installed packages using apt-mark to identify potentially manual installed packages')
  
  input_arg = parser.parse_args()
  
  if input_arg.default: 
    # Create UserPackages object and set to use aptitude 
    # to get list of installed packages
    user_packages=UserPackages('default')
  elif input_arg.aptmark:
    # Create UserPackages object and set to use apt-mark 
    # to get list of installed packages
    user_packages=UserPackages('apt-mark')
  else:
    # Create UserPackages object and set to use aptitude 
    # to get list of installed packages
    user_packages=UserPackages('default')
    
  # Call class method to display the user installed packages  
  user_packages.display_user_installed()

if __name__ == '__main__':
  main()
