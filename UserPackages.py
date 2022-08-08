import subprocess
import re


class UserPackages:
  """
    A class to represent user installed packages.

    Attributes
    ----------
    installed_type : str
        Identifies method for finding installed packages

    Methods
    -------
    display_user_installed
      Get and display the user installed packages
    display_packages
      Displays the given packages to the screen
    get_installed_packages
      Get installed packages
    get_aptitude_packages
      Use aptitude to get installed packages
    get_aptmark_packages
      Use apt-mark to get installed packages
    get_manifest_packages
      Get list of packages included on manifest list
    get_user_installed_packages
      Get list of only packages installed by user
  """
  
  def __init__(self, installed_type):
    """Constructs attributes for user installed packages object."""
    self.installed_type = installed_type 
  
  def display_user_installed(self):
    """Display the user installed packages."""
    # get installed packages
    installed_packages = self.get_installed_packages()
    
    # get manifest packages
    manifest_packages = self.get_manifest_packages()
    
    # determine user installed packages
    user_installed = self.get_user_installed_packages(installed_packages, manifest_packages)
    
    # display the user installed packages
    self.display_packages(user_installed)
    
  def display_packages(self, user_installed):
    """Display the user installed packages.

    Inputs:
      - user_installed -- list of user installed packages
    """
    for package in user_installed:
      print(package)
    
  def get_installed_packages(self):
    """Determine and call method for getting installed packages.
    
    Uses command line argument to determine how to find the
    installed packages: by using aptitude or by using apt-mark.
    Default is to use aptitude.
    
    Returns:
      - list of installed packages.
    """
    match self.installed_type:
      case "default":
        installed_packages = self.get_aptitude_packages()
      case "apt-mark":
        installed_packages = self.get_aptmark_packages()
      case default:
        installed_packages = self.get_aptitude_packages()
    return installed_packages
    
  def get_aptitude_packages(self):
    """Return installed packages found using aptitude.
  
    Aptitude checks /var/lib/dpkg/status for installed packages.
    If aptitude is not installed, exits with code 1.
    
    Returns:
      - list of installed packages.
    """
    try:
      dpkg_packages=subprocess.run("aptitude search '~i !~M' -F '%p'| sed 's/ *$//'", capture_output=True, shell=True)
    except:
      print("An error occured running aptitude. Is aptitude installed?")
      exit(1)
    else:
      # Convert output into a list
      dpkg_list=dpkg_packages.stdout.decode().split('\n')
      return dpkg_list
  
  def get_aptmark_packages(self):
    """Return installed packages found using apt-mark.
    
    Returns:
      - list of installed packages.
    """
    apt_packages=subprocess.run("apt-mark showmanual | sort -u", capture_output=True, shell=True)
    # Convert output into a list
    apt_list=apt_packages.stdout.decode().split('\n')
    return apt_list
    
  def get_manifest_packages(self):
    """Return manifest package list.
    
    Uses the manifest list for Ubuntu 18.04.6 to identify which
    packages were installed as part of the initial install.
    If unable to read manifest list, exits with code 2.
    
    Returns:
      - list of packages installed as part of initial install as identified by manifest.
    """   
    try:
      manifest_packages=subprocess.run("wget -qO - https://releases.ubuntu.com/18.04/ubuntu-18.04.6-desktop-amd64.manifest | cut -f1 | sort -u", capture_output=True, shell=True)
    except:
      print("Unable to read manifest list.")
      exit(2)
    else:
      manifest_list=manifest_packages.stdout.decode().split('\n')
      # Clean up list by removing :amd64 from package names
      for i in range(len(manifest_list)):
        manifest_list[i] = re.sub(':amd64', '', manifest_list[i])
      return manifest_list
      
  def get_user_installed_packages(self, installed_packages, manifest_list):
    """Return list of user installed packages.
    
    Identifies user installed packages by starting with the installed_packages
    list and removing any packages that are in the manifest list (which 
    indicates that the package was installed with operating system initial
    install and was not user installed).
    
    Inputs:
      installed_packages -- list of installed packages
      manifest_list -- list of packages on the manifest
    Returns:
      - list of user installed packages.
    """
    manifest_set = set(manifest_list)
    user_packages = [x for x in installed_packages if x not in manifest_set]
    return user_packages
