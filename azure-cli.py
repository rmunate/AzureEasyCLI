import argparse
from lib.output import Console
from azure.cli_manager import Azure
from azure.config_file import Config

if __name__ == "__main__":

    # Crear el analizador de argumentos
    parser = argparse.ArgumentParser(description="Script para ejecutar backup o iniciar consola en Azure CLI")
    parser.add_argument("--backup", action="store_true", help="Ejecuta el modo backup")
    parser.add_argument("--console", action="store_true", help="Ejecuta el modo consola")

    # Parsear los argumentos
    args = parser.parse_args()

    try:

        # Cargar la configuracion de conexión.
        config = Config()

        # Iniciar servicio de Azure.
        azure = Azure()

        # Iniciar Sesion
        azure.login(tenant_id = config.tenant)

        # Setear la suscripcion.
        azure.setSubscription(subscription_id=config.subscription_id)

        # Listar los nombres de espacio
        azure.listNamespaces(echo=config.namespace_echo)

        # Seleccionar el nombre de espacio a emplear.
        azure.selectNamespace(namespace=config.namespace_select)

        # Listar los deployments de ese namespace
        azure.listDeployments(echo=config.deployments_echo)

        # Seleccionar la implementacion a usar
        azure.selectDeployment(deployment=config.deployments_select)

        # Listar los PODS disponibles:
        azure.listPods(echo=config.pods_echo)

        # Seleccionar el POD
        azure.selectPod(pod=config.pods_select)

        # Ejecutar copia del codigo origen al local
        if args.backup:
            azure.runBackup(folder=config.backup_folder)

        # Iniciar Terminal
        if args.console:
            azure.start_bash()

    except Exception as e:

        # Imprimir el error y terminar.
        Console.fail(message=str(e), timestamp=True)
        raise ValueError(e)

