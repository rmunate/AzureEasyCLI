# ---------------------------------------------------------------------------- #
# Author: Raul Mauricio Uñate Castro                                           #
# GitHub: https://github.com/rmunate                                           #
# Date: January 7, 2025                                                        #
# ---------------------------------------------------------------------------- #

import re
import os
import json
import shutil
import subprocess
from pathlib import Path
from lib.output import Console
from lib.helpers import sanitize_folder_name

class Azure:

    def __init__(self):
        """
        Initializes the command interpreter service for connecting to Azure CLI.

        Prerequisites:
        - Azure CLI: Ensure Azure CLI is installed. Follow the guide here:
        https://learn.microsoft.com/en-us/cli/azure/install-azure-cli
        - kubectl: Ensure kubectl is installed. Follow the guide here:
        https://kubernetes.io/docs/tasks/tools/

        The initialization process will:
        1. Validate that the required tools are installed and accessible.
        2. Display the detected versions of Azure CLI and kubectl.
        3. Prepare the object for managing Azure CLI connections and Kubernetes namespaces.
        """

        #read Art:
        current_path = os.path.dirname(__file__)
        art_path = os.path.join(current_path, '..', 'lib', 'art.ascii')

        with(open(art_path, 'r')) as art:
            print(art.read())

        # Validate required tools
        tools = self.check_required_tools()

        # Display tool versions
        Console.info(
            message=f"Tools detected: Azure CLI {tools['Azure CLI']} | kubectl {tools['kubectl']}",
            timestamp=True
        )

        # Initialize connection data and namespaces
        self.data_connection = None
        self.namespaces = []
        self.deployments = []
        self.pods = []

    def check_required_tools(self):
        """
        Validates that the required dependencies (Azure CLI and kubectl) are installed and accessible.
        Raises an error with guidance links if any dependency is missing.

        Returns:
            dict: A dictionary containing the status and version of the tools.
        """
        tools_status = {}

        # Check Azure CLI
        try:
            command = "az version"
            result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
            az_version = json.loads(result.stdout).get("azure-cli", "Unknown")
            tools_status["Azure CLI"] = f"Installed (Version: {az_version})"
        except subprocess.CalledProcessError:
            raise RuntimeError(
                "Azure CLI is not installed. Please install it from: "
                "https://learn.microsoft.com/en-us/cli/azure/install-azure-cli"
            )
        except json.JSONDecodeError:
            raise RuntimeError("Failed to parse Azure CLI version information.")

        # Check kubectl
        try:
            command = "kubectl version --client --output=json"
            result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
            kubectl_version = json.loads(result.stdout)["clientVersion"]["gitVersion"]
            tools_status["kubectl"] = f"Installed (Version: {kubectl_version})"
        except subprocess.CalledProcessError:
            raise RuntimeError(
                "kubectl is not installed. Please install it from: "
                "https://kubernetes.io/docs/tasks/tools/"
            )
        except json.JSONDecodeError:
            raise RuntimeError("Failed to parse kubectl version information.")

        return tools_status

    def login(self, tenant_id=None):
        """
        Logs into Azure.

        Args:
            tenant_id (str, optional): The tenant ID for login. If not provided, performs a generic login.

        Raises:
            ValueError: If login is unsuccessful or the connection state is not enabled.
            RuntimeError: If an error occurs while executing the command.
        """
        try:
            # Build the command based on the presence of tenant_id
            command = f"az login --tenant {tenant_id}" if tenant_id else "az login"

            # Execute the command
            result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)

            # Parse the response as JSON
            connect_data = json.loads(result.stdout)[0]

            # Validate the connection state
            if connect_data.get('state') != "Enabled":
                raise ValueError("Login failed. Connection state is not enabled.")

            # Confirmation message
            tenant_message = f", Tenant: {connect_data.get('name')}" if tenant_id else ""
            Console.info(message=f"Successfully logged in{tenant_message}.", timestamp=True)

            # Store the connection data
            self.data_connection = connect_data

        except subprocess.CalledProcessError as e:
            # Log and re-raise for better error context
            error_message = f"Command execution failed: {e.stderr.strip()}"
            raise RuntimeError(error_message) from e

        except json.JSONDecodeError as e:
            error_message = "Invalid JSON response from Azure CLI."
            raise ValueError(error_message) from e

    def get_connection_data(self):
        """
        Retrieve the current connection data.

        This method returns the stored connection details if a successful login has occurred.
        It raises an exception if no active session is found.

        Returns:
            dict: The stored connection data, including information about the authenticated user and tenant.

        Raises:
            ValueError: If no active session is available (i.e., login has not been performed).
        """
        if not self.data_connection:
            raise ValueError("No active session found. Please log in first.")

        return self.data_connection

    def setSubscription(self, subscription_id):
        """
        Set the Azure subscription for the current context.

        This method updates the Azure CLI context to use the specified subscription ID.
        It raises an exception if the operation fails.

        Args:
            subscription_id (str): The subscription ID to set.

        Raises:
            ValueError: If the subscription could not be set due to an error.
        """
        try:
            # Execute the command to set the subscription
            command = f"az account set --subscription {subscription_id}"
            subprocess.run(command, shell=True, check=True, capture_output=True, text=True)

            # Log success message
            Console.info(
                message=f"Subscription [{subscription_id}] successfully set in the current context.",
                timestamp=True
            )
        except subprocess.CalledProcessError as e:
            # Capture command errors and raise with details
            error_message = f"Failed to set subscription [{subscription_id}]. Error: {e.stderr.strip()}"
            raise ValueError(error_message) from e
        except Exception as e:
            # Handle unexpected errors
            error_message = f"An unexpected error occurred while setting subscription [{subscription_id}]."
            raise ValueError(error_message) from e

    def listNamespaces(self, echo: bool = True):
        """
        List available Kubernetes namespaces.

        This method retrieves and displays the namespaces in the current Kubernetes context. 
        If `echo` is enabled, the namespaces are displayed in the console.

        Args:
            echo (bool, optional): If True, the namespaces are printed to the console. Defaults to True.

        Raises:
            ValueError: If no namespaces are found or the command fails.

        Returns:
            None
        """
        try:
            # Execute the command to retrieve namespaces
            command = "kubectl get namespaces"
            result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)

            # Check if valid data is returned
            if 'NAME' in result.stdout and 'STATUS' in result.stdout and 'AGE' in result.stdout:
                # Prepare namespace data
                raw_data = result.stdout.split()[3:]  # Exclude headers (NAME, STATUS, AGE)
                all_namespaces = []
                namespace_data = []

                # Process data into structured format
                for index, value in enumerate(raw_data, start=1):
                    if index % 3 == 0:  # Age column
                        value = value.replace('y', ' Years ').replace('d', ' Days ').replace('h', ' Hours ').replace('m', ' Minutes ')
                        namespace_data.append(value.strip())
                        all_namespaces.append(namespace_data)
                        namespace_data = []
                    else:  # Name or Status column
                        namespace_data.append(value)

                # Display the namespaces in the console if echo is True
                if echo:
                    Console.newLine()
                    Console.textSuccess("Available Kubernetes namespaces:")
                    Console.table(
                        headers=["Name", "Status", "Age"],
                        rows=all_namespaces
                    )
                    Console.newLine()

                # Store namespaces data
                self.namespaces = all_namespaces
                return

            # Error if no namespaces are found
            Console.fail("No namespaces found in the current Kubernetes context.")

        except subprocess.CalledProcessError as e:
            error_message = f"Failed to retrieve namespaces. Error: {e.stderr.strip()}"
            raise RuntimeError(error_message) from e

    def selectNamespace(self, namespace:str=None):
        """
        Prompt the user to select a Kubernetes namespace if none is configured.

        This method allows the user to select a namespace from the available options 
        or validates a provided namespace against the available list.

        Args:
            namespace (str, optional): The namespace to use. If not provided, 
                                    the user is prompted to select one.

        Raises:
            ValueError: If the provided namespace is not in the list of available namespaces.

        Returns:
            None
        """

        # Extract the list of namespace names
        if not self.namespaces:
            self.listNamespaces(echo=False)
        available_namespaces = [ns[0] for ns in self.namespaces]

        # Prompt the user if no namespace is provided
        if namespace is None:
            namespace = Console.choice(
                question="Which namespace would you like to use?",
                choices=available_namespaces
            )

        # Validate the namespace against the available options
        if namespace not in available_namespaces:
            error_message = f"The namespace [{namespace}] is not among the available options."
            raise ValueError(error_message)

        # Store the selected namespace
        self.namespace_selected = namespace

        # Display confirmation of the selected namespace
        Console.info(
            message=f"Namespace selected for use: [{self.namespace_selected}]",
            timestamp=True
        )

    def listDeployments(self, echo:bool = True):
        """
        List deployments in the selected Kubernetes namespace.

        This method retrieves and displays the deployments in the currently selected namespace.
        If `echo` is enabled, the deployments are displayed in a formatted table in the console.

        Args:
            echo (bool, optional): If True, the deployments are printed to the console. Defaults to True.

        Raises:
            RuntimeError: If no deployments are found or the `kubectl` command fails.

        Returns:
            None
        """
        try:
            # Execute the command to list deployments in the selected namespace
            command = f"kubectl get deployments -n {self.namespace_selected}"
            result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)

            # Check if valid deployment data is returned
            if 'NAME' in result.stdout and 'READY' in result.stdout and 'AGE' in result.stdout:
                # Prepare deployment data
                # Skip header row
                raw_data = result.stdout.splitlines()[1:]
                all_deployments = []

                for line in raw_data:
                    # Split each line into columns and normalize time units
                    columns = line.split()
                    columns[-1] = columns[-1].replace('y', ' Years ').replace('d', ' Days ').replace('h', ' Hours ').replace('m', ' Minutes ')
                    all_deployments.append(columns)

                # Display the deployments in the console if echo is True
                if echo:
                    Console.newLine()
                    Console.textSuccess(f"Deployments available in namespace [{self.namespace_selected}]:")
                    Console.table(
                        headers=['Name', 'Ready', 'Up-to-date', 'Available', 'Age'],
                        rows=all_deployments
                    )
                    Console.newLine()

                # Store the deployments data
                self.deployments = all_deployments
                return

            # Handle case where no deployments are found
            Console.fail(f"No deployments found in namespace [{self.namespace_selected}].")

        except subprocess.CalledProcessError as e:
            error_message = f"Failed to retrieve deployments for namespace [{self.namespace_selected}]. Error: {e.stderr.strip()}"
            raise RuntimeError(error_message) from e

    def selectDeployment(self, deployment:str=None):
        """
        Prompt the user to select a deployment if none is configured.

        This method allows the user to select a deployment from the available list 
        or validates a provided deployment against the available options.

        Args:
            deployment (str, optional): The deployment to use. If not provided, 
                                        the user is prompted to select one.

        Raises:
            ValueError: If the provided deployment is not in the list of available deployments.

        Returns:
            None
        """

        # Generate the list of available deployments
        if not self.deployments:
            self.listDeployments(echo=False)
        available_deployments = [d[0] for d in self.deployments]

        # Prompt the user to select a deployment if none is provided
        if deployment is None:
            deployment = Console.choice(
                question="Which deployment would you like to use?",
                choices=available_deployments
            )

        # Validate the provided deployment against the available options
        if deployment not in available_deployments:
            error_message = f"The deployment [{deployment}] is not among the available options."
            raise ValueError(error_message)

        # Store the selected deployment
        self.deployment_selected = deployment

        # Display confirmation of the selected deployment
        Console.info(
            message=f"Deployment selected for use: [{self.deployment_selected}]",
            timestamp=True
        )

    def listPods(self, echo: bool = True):
        """
        List the pods in the selected namespace and deployment.

        This method retrieves and displays the pods running in the selected namespace
        and deployment. If `echo` is enabled, the pods are printed to the console in a
        formatted table.

        Args:
            echo (bool, optional): If True, the pods are printed to the console. Defaults to True.

        Raises:
            RuntimeError: If no pods are found or the `kubectl` command fails.

        Returns:
            None
        """
        try:
            # Execute the command to get the pods in the selected namespace
            command = f"kubectl get pods -n {self.namespace_selected}"
            result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)

            # Check if valid pod data is returned
            if 'NAME' in result.stdout and 'READY' in result.stdout and 'AGE' in result.stdout:
                # Clean the output to remove unwanted timestamps
                cleaned_output = re.sub(r"\([^)]* ago\)", "", result.stdout)
                pod_data = cleaned_output.splitlines()[1:]  # Skip header row

                all_pods = []
                for line in pod_data:
                    columns = line.split()
                    # Replace time format and pod status
                    columns[-1] = columns[-1].replace('y', ' Years ').replace('d', ' Days ').replace('h', ' Hours ').replace('m', ' Minutes ').strip()
                    all_pods.append(columns)

                # Display the pod information in the console if echo is True
                if echo:
                    Console.newLine()
                    Console.textSuccess(f"Available Pods in namespace [{self.namespace_selected}] for deployment [{self.deployment_selected}]:")
                    Console.table(
                        headers=['Name', 'Ready', 'Status', 'Restarts', 'Age'],
                        rows=all_pods
                    )
                    Console.newLine()

                # Store the pod data
                self.pods = all_pods
                return

            # Handle case where no pods are found
            Console.fail(f"No pods registered in namespace [{self.namespace_selected}] for deployment [{self.deployment_selected}].")

        except subprocess.CalledProcessError as e:
            error_message = f"Failed to retrieve pods for namespace [{self.namespace_selected}] and deployment [{self.deployment_selected}]. Error: {e.stderr.strip()}"
            raise RuntimeError(error_message) from e

    def selectPod(self, pod:str=None):
        """
        Prompt the user to select a pod if none is already selected.

        This method allows the user to select a pod from the list of available pods.
        If a pod is already selected or provided, it skips the prompt. If a pod is not
        available in the list, it raises an error.

        Args:
            pod (str, optional): The name of the pod to select. If None, the user is prompted to choose.

        Raises:
            ValueError: If the provided pod name is not in the list of available pods.

        Returns:
            None
        """
        # Generate the list of available pods
        if not self.pods:
            self.listPods(echo=False)
        list_pods = [i_value[0] for i_value in self.pods]

        # If no pod is selected, prompt the user to choose one
        if pod is None:
            pod = Console.choice(
                question="Which POD would you like to access?",
                choices=list_pods
            )

        # Ensure the selected pod is available in the list
        if pod not in list_pods:
            raise ValueError(f"The POD [{pod}] does not exist in the available options.")

        # Store the selected pod for later use
        self.pod_selected = pod

        # Display the selected pod name in the console
        Console.info(
            message=f"Selected POD: [{self.pod_selected}]",
            timestamp=True
        )

    def clear_folder(self, folder_path):
        """Clears the contents of the specified folder."""
        for file in folder_path.iterdir():
            if file.is_dir():
                shutil.rmtree(file)
            else:
                file.unlink()

    def runBackup(self, folder: str = None, origin: str = '/var/www/app'):
        """
        This method performs a backup of the source code from the specified pod in the selected namespace.

        Args:
            folder (str, optional): The directory where the backup will be stored. If not specified, the default backup path is used.

        Raises:
            ValueError: If the pod or namespace is not properly selected or if the backup fails.
            subprocess.CalledProcessError: If the backup command fails during execution.
        """

        # Set the backup path
        if not folder:
            current_path = Path(__file__).resolve().parent
            backup_path = current_path.parent / 'backups' / sanitize_folder_name(self.pod_selected)
        else:
            backup_path = Path(folder).resolve()

        # Ensure the backup directory exists or create it
        backup_path.mkdir(parents=True, exist_ok=True)

        # Clear the folder if it contains any files
        if any(backup_path.iterdir()):
            self.clear_folder(backup_path)

        # Get the absolute path for backup
        backup_path = backup_path.as_posix()

        # Save the current working directory
        original_dir = Path.cwd()

        # Prepare the kubectl command to copy files from the pod
        kubectl_cmd = [
            "kubectl", "cp",
            f"{self.namespace_selected}/{self.pod_selected}:{origin}",
            str(backup_path)
        ]

        try:

            Console.info(
                message=f"Starting backup from pod '{self.pod_selected}'...",
                timestamp=True
            )
            result = subprocess.run(kubectl_cmd, capture_output=True, text=True, check=True)
            Console.info(
                message=f"Backup completed successfully: {result.stdout}",
                timestamp=True
            )

        except subprocess.CalledProcessError as e:
            raise ValueError(f"Backup failed for pod '{self.pod_selected}'. Please check the error above.") from e

        finally:
            os.chdir(original_dir)

    def startBash(self):
        """
        Starts an interactive bash session inside the selected pod in the specified namespace.

        This method uses `kubectl exec` to initiate a shell session within the pod and provides user-friendly feedback.
        If the session is interrupted, it handles the `KeyboardInterrupt` gracefully.
        """
        try:
            # Construct the kubectl command for the interactive bash session
            cmd = [
                "kubectl", "exec", "-it", self.pod_selected, "-n", self.namespace_selected, "--", "/bin/bash"
            ]

            Console.textWarning("Initiating session...")

            # Start the bash session
            subprocess.run(cmd, check=True, text=True)

            Console.textSuccess("Session started successfully.")

        except KeyboardInterrupt:
            # Graceful exit if the user interrupts the session
            Console.info(message="\nExiting interactive session...", timestamp=True)

        except subprocess.CalledProcessError as e:
            # Specific error handling for subprocess-related issues
            raise ValueError(f"Command execution failed: {e}")

        except Exception as e:
            # General error handler for any other issues
            raise ValueError(f"An unexpected error occurred: {e}")
