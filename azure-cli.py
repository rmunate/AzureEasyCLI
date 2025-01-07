import argparse
from lib.output import Console
from azure.cli_manager import Azure
from azure.config_file import Config

if __name__ == "__main__":

    # Create the argument parser
    parser = argparse.ArgumentParser(description="Script to execute backup or start a console in Azure CLI")
    parser.add_argument("--backup", action="store_true", help="Run backup mode")
    parser.add_argument("--console", action="store_true", help="Run console mode")

    # Parse the arguments
    args = parser.parse_args()

    try:
        # Load the connection configuration
        config = Config()

        # Initialize Azure service
        azure = Azure()

        # Log in to Azure with the provided tenant ID
        azure.login(tenant_id=config.tenant)

        # Set the subscription
        azure.setSubscription(subscription_id=config.subscription_id)

        # List available namespaces
        azure.listNamespaces(echo=config.namespace_echo)

        # Select the namespace to use
        azure.selectNamespace(namespace=config.namespace_select)

        # List deployments within the selected namespace
        azure.listDeployments(echo=config.deployments_echo)

        # Select the deployment to use
        azure.selectDeployment(deployment=config.deployments_select)

        # List available Pods
        azure.listPods(echo=config.pods_echo)

        # Select the Pod to use
        azure.selectPod(pod=config.pods_select)

        # Perform backup if the backup argument is provided
        if args.backup:
            azure.runBackup(folder=config.backup_folder, origin=config.backup_origin)

        # Start the terminal session if the console argument is provided
        if args.console:
            azure.startBash()

    except Exception as e:
        # Print the error message and terminate
        Console.fail(message=str(e), timestamp=True)

        # Print the full traceback for debugging
        raise ValueError(e)
