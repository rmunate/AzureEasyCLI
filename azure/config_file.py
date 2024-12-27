import json
import os

class Config:

    def __init__(self):
        """
        Inicializador de la clase
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
        self.backup = None
        self.backup_folder = None
        self.load()

    def load(self) -> dict:
        """
        Lectura del archivo de configuración.
        """
        try:

            self.path_file = os.path.join(os.path.dirname(__file__), '..', 'config.json')

            config = {}
            with (open(self.path_file, 'r')) as file:
                config = json.loads(file.read())

            # Nombre del Tenant
            self.tenant = config.get('tenant')

            # Subscripcion.
            self.subscription_id = config.get('subscription_id')

            # Credenciales.
            self.credentials = config.get('credentials')
            self.resource_group = self.credentials.get('resource-group')
            self.name = self.credentials.get('name')
            self.overwrite_existing = self.credentials.get('overwrite-existing')

            # Namespace
            self.namespaces = config.get('namespace')
            self.namespace_select = self.namespaces.get('select')
            self.namespace_echo = self.namespaces.get('echo')

            # Deployments
            self.deployments = config.get('deployments')
            self.deployments_select = self.deployments.get('select')
            self.deployments_echo = self.deployments.get('echo')

            # Deployments
            self.pods = config.get('pods')
            self.pods_select = self.pods.get('select')
            self.pods_echo = self.pods.get('echo')

            # Backup Folder
            self.backup = config.get('backup')
            self.backup_folder = self.backup.get('folder')

        except Exception as e:
            raise ValueError(f"Fail Read Config File: {str(e)}")

