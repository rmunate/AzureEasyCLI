# ---------------------------------------------------------------------------- #
# Author: Raul Mauricio Uñate Castro                                           #
# GitHub: https://github.com/rmunate                                           #
# Date: January 7, 2025                                                        #
# ---------------------------------------------------------------------------- #

import json
import os

class Config:
    """
    Class to manage and load configuration settings from a JSON file.
    """

    def __init__(self):
        """
        Initializes the Config object and loads the configuration from a file.
        """
        self.tenant = None
        self.credentials = None
        self.resource_group = None
        self.name = None
        self.overwrite_existing = None
        self.namespaces = None
        self.namespace_select = None
        self.namespace_echo = True
        self.deployments = None
        self.deployments_select = None
        self.deployments_echo = True
        self.pods = None
        self.pods_select = None
        self.pods_echo = True
        self.backup = None
        self.backup_folder = None
        self.backup_origin = None

        # Load configuration settings
        self.load()

    def load(self) -> dict:
        """
        Reads the configuration file and sets class attributes based on its contents.

        Returns:
            dict: A dictionary with configuration data loaded from the file.

        Raises:
            ValueError: If there is an error reading or parsing the configuration file.
        """
        try:
            # Define the path for the configuration file
            config_file_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')

            # Load the JSON content from the config file
            with open(config_file_path, 'r') as file:
                config_data = json.load(file)

            # Tenant and Subscription Information
            self.tenant = config_data.get('tenant')
            self.subscription_id = config_data.get('subscription_id')

            # Credentials
            self.credentials = config_data.get('credentials', {})
            self.resource_group = self.credentials.get('resource-group')
            self.name = self.credentials.get('name')
            self.overwrite_existing = self.credentials.get('overwrite-existing')

            # Namespace configuration
            self.namespaces = config_data.get('namespace', {})
            self.namespace_select = self.namespaces.get('select')
            self.namespace_echo = self.namespaces.get('echo', True)

            # Deployment configuration
            self.deployments = config_data.get('deployments', {})
            self.deployments_select = self.deployments.get('select')
            self.deployments_echo = self.deployments.get('echo', True)

            # Pod configuration
            self.pods = config_data.get('pods', {})
            self.pods_select = self.pods.get('select')
            self.pods_echo = self.pods.get('echo', True)

            # Backup configuration
            self.backup = config_data.get('backup', {})
            self.backup_folder = self.backup.get('folder')
            self.backup_origin = self.backup.get('origin')

        except (FileNotFoundError, json.JSONDecodeError) as e:
            raise ValueError(f"Failed to read or parse the config file: {str(e)}")

        except Exception as e:
            raise ValueError(f"Unexpected error while loading config: {str(e)}")
