# Azure CLI

Azure Easy CLI - Simplifying Azure Management

This project allows you to interact with Azure Kubernetes Service (AKS) to manage namespaces, deployments, pods, and perform backup operations through a simple and user-friendly command-line interface (CLI). You can perform actions such as:

- Listing namespaces.
- Selecting namespaces, deployments, and pods.
- Performing backups of source code from pods.
- Starting an interactive session (console) in a pod.

## Prerequisites

Before you begin, make sure the following requirements are met:

1. **Python 3.11+**
2. **Azure CLI** installed and authenticated (https://learn.microsoft.com/en-us/cli/azure/install-azure-cli).
3. **kubectl** installed and configured to access your AKS cluster (https://kubernetes.io/docs/tasks/tools/).
4. **config.json** with your Azure and Kubernetes details (provided below).

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/rmunate/AzureEasyCLI.git
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate your environment:
   ```bash
   venv/scripts/activate  # Windows
   source venv/bin/activate  # Linux/MacOS
   ```

4. Install the required dependencies (Not required, currently has no dependencies.):
   ```bash
   pip install -r requirements.txt
   ```

Note: Make sure that `kubectl` and `az` are authenticated and configured to access your Kubernetes cluster.

## Configuration

The script relies on a `config.json` file located in the root directory of the project. The structure of the `config.json` file is as follows:

```json
{
    "tenant" : "your-tenant-id",
    "subscription_id" : "your-subscription-id",
    "credentials" : {
        "resource-group" : "your-resource-group-name",
        "name" : "your-cluster-name",
        "overwrite-existing" : true
    },
    "namespace" : {
        "echo": false,
        "select" : "your-namespace-name"
    },
    "deployments" : {
        "echo": false,
        "select" : "your-deployment-name"
    },
    "pods" : {
        "echo": false,
        "select" : "your-pod-name"
    },
    "backup" : {
        "folder" : "path/to/backup/folder",
        "origin" : "/var/www/app"
    }
}
```

### Key Configuration Fields

- **tenant**: Your Azure tenant ID.
- **subscription_id**: Your Azure subscription ID.
- **credentials**: Contains the Azure credentials needed to interact with your AKS cluster:
  - **resource-group**: The Azure resource group where your AKS cluster is located.
  - **name**: The name of your AKS cluster.
  - **overwrite-existing**: If `true`, it will overwrite existing resources.
- **namespace**: Specifies the namespace to interact with.
  - **echo**: Set to `false` if you don't want to display namespaces in the console.
  - **select**: The default namespace to select.
- **deployments**: Specifies the deployment to interact with.
  - **echo**: Set to `false` if you don't want to display deployments in the console.
  - **select**: The default deployment to select.
- **pods**: Specifies the pod to interact with.
  - **echo**: Set to `false` if you don't want to display pods in the console.
  - **select**: The default pod to select.
- **backup**: Configuration for backup operations.
  - **folder**: The local folder where backups will be stored.
  - **origin**: The folder inside the pod to back up (defaults to `/var/www/app`).

## Usage

### Run a Backup

To create a backup of the source code from the selected pod:

```bash
python -B .\azure-cli.py --backup
```

This will execute the backup to the folder specified in the `config.json` file.

### Start an Interactive Bash Session

To start an interactive console session in the selected pod:

```bash
python -B .\azure-cli.py --console
```

This will open a Bash shell inside the selected pod, allowing you to interact with it directly.

### Script Flow

1. The script will load the configuration from the `config.json` file.
2. It will authenticate with Azure and set the subscription and resource group.
3. It will list the namespaces, deployments, and pods, and prompt you to select which ones to use (if not specified in the configuration).
4. The backup will execute if the `--backup` argument is provided.
5. An interactive Bash session will start in the selected pod if the `--console` argument is provided.

### Example

```bash
python -B .\azure-cli.py --backup  # Perform the backup of the selected pod to the configured local folder
python -B .\azure-cli.py --console  # Start an interactive session in the selected pod
```

## Error Handling

- The script will display relevant error messages if issues arise during execution, including configuration errors or network issues with Azure or Kubernetes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.