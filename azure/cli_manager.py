import re
import os
import json
import shutil
import subprocess
from lib.output import Console
from lib.helpers import clear_folder, sanitize_folder_name

class Azure:
    """
    Clase para gestionar la conexión a Azure mediante Azure CLI.
    """

    def __init__(self):
        """
        Constructor de la clase Azure.
        """

        # Información de la conexión actual
        self.data_connection = None
        self.namespaces = []

    def login(self, tenant_id=None):
        """
        Inicia sesión en Azure.

        Args:
            tenant_id (str, optional): ID del tenant para iniciar sesión. Si no se proporciona, inicia sesión de forma genérica.

        Raises:
            ValueError: Si no se puede iniciar sesión correctamente.
            RuntimeError: Si ocurre un error durante la ejecución del comando.
        """
        try:
            # Construir el comando según la presencia de tenant_id
            command = f"az login --tenant {tenant_id}" if tenant_id else "az login"

            # Ejecutar el comando
            result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)

            # Cargar la respuesta como JSON
            connect_data = json.loads(result.stdout)[0]

            # Validar el estado de la conexión
            if connect_data.get('state') != "Enabled":
                raise ValueError("Imposible iniciar sesión. Estado de conexión no habilitado.")

            # Mensaje de confirmación
            tenant_message = f", Tenant: {connect_data.get('name')}" if tenant_id else ""
            Console.info(message=f"Sesión iniciada correctamente{tenant_message}.", timestamp=True)

            # Almacenar la conexión
            self.data_connection = connect_data

        except subprocess.CalledProcessError as e:
            raise ValueError(f"Error al ejecutar el comando: {e.stderr}")

        except json.JSONDecodeError as e:
            raise ValueError("La respuesta del comando no es un JSON válido.")

    def get_connection_data(self):
        """
        Retorna la información de la conexión actual.

        Returns:
            dict: Datos de la conexión almacenada.

        Raises:
            ValueError: Si no se ha iniciado sesión.
        """
        if not self.data_connection:
            raise ValueError("No se ha iniciado sesión.", timestamp=True)

        return self.data_connection

    def setSubscription(self, subscription_id):
        """Ejecutar el seteo de la suscripcion correspondiente"""
        try:
            subprocess.run(f"az account set --subscription {subscription_id}", shell=True, check=True, capture_output=True, text=True)
            Console.info(message=f"Subscripción [{subscription_id}] seteada en el contexto exitosamente.", timestamp=True)
        except Exception as e:
            raise ValueError(f"Error al setear la subscripción [{subscription_id}]", timestamp=True)

    def listNamespaces(self, echo:bool = True):
        """Listar los nombres de espacio disponibles."""

        # Ejecutar la consulta de los namespaces
        result = subprocess.run("kubectl get namespaces", shell=True, check=True, capture_output=True, text=True)

        # Validar si retorno datos de espacios de nombre.
        if 'NAME' in result.stdout and 'STATUS' in result.stdout and 'AGE' in result.stdout:

            # Preparar los datos
            lst = result.stdout.split()[3:]

            # Valores para logica de la sepracion de datos.
            iteration = 0
            multiple = 3
            iteration_data = []
            all_namespace = []

            # Crear la lista de valores a mostrar traducida al español.
            for value in lst:
                iteration += 1
                if iteration % multiple == 0:
                    value = value.replace('y', ' Años ').replace('d', ' Dias').replace('h', ' Horas ').replace('m', ' Minutos ')
                    iteration_data.append(value)
                    all_namespace.append(iteration_data)
                    iteration_data = []
                else:
                    value = value.replace('Inactive', 'Inactivo').replace('Active', 'Activo')
                    iteration_data.append(value)

            # Generar la salida en consola.
            if echo:
                Console.newLine()
                Console.textSuccess(
                    message='Nombres de espacios disponibles.'
                )
                Console.table(
                    headers=['Nombre', 'Estado', 'Edad'],
                    rows=all_namespace
                )
                Console.newLine()

            # ALojar los datos de los Namespace.
            self.namespaces = all_namespace

            # Finalizar el Metodo
            return

        # Lanzar excepcion de no encontrar namespace disponibles.
        raise ValueError("No se encontraron espacios de nombre disponibles.")

    def selectNamespace(self, namespace:str=None):
        """Solicitarle al usuario la seleccion de un namespace en caso de no haber uno configurado."""

        # Generar el listado de los Namespaces.
        list_namespaces = []
        for i_namespace in self.namespaces:
            list_namespaces.append(i_namespace[0])

        # Si no existe un namespace por defecto solicitarle al usuario cual emplear.
        if namespace is None:

            # Solicitar la seleccion.
            namespace = Console.choice(
                question="¿Que espacio deseas emplear?",
                choices=list_namespaces
            )

        # Garantizar que el namespace este dentro de las opciones disponibles
        # En especial cuando es suministrado por el usuario
        if namespace not in list_namespaces:
            raise ValueError(f"No existe el namespace [{namespace}] dentro de las opciones disponibles.")

        # Alojar el valor del namespace a emplear.
        self.namespace_selected = namespace

        # Mostrar el nombre del nombre de espacio seleccionado
        Console.info(
            message=f"Nombre del espacio seleccionado para uso [{self.namespace_selected}]",
            timestamp=True
        )

    def listDeployments(self, echo:bool = True):
        """Este metodop lista los deployments del namespace seleccionado."""
        result = subprocess.run(f"kubectl get deployments -n {self.namespace_selected}", shell=True, check=True, capture_output=True, text=True)

        # Validar si retorno datos de espacios de nombre.
        if 'NAME' in result.stdout and 'READY' in result.stdout and 'AGE' in result.stdout:

            # Preparar los datos
            lst = result.stdout.split()[5:]

            # Valores para logica de la sepracion de datos.
            iteration = 0
            multiple = 5
            iteration_data = []
            all_deployments = []

            # Crear la lista de valores a mostrar traducida al español.
            for value in lst:
                iteration += 1
                if iteration % multiple == 0:
                    value = value.replace('y', ' Años ').replace('d', ' Dias').replace('h', ' Horas ').replace('m', ' Minutos ')
                    iteration_data.append(value)
                    all_deployments.append(iteration_data)
                    iteration_data = []
                else:
                    iteration_data.append(value)

            # Generar la salida en consola.
            if echo:
                Console.newLine()
                Console.textSuccess(
                    message='Nombres de implementaciones disponibles.'
                )
                Console.table(
                    headers=['Nombre', 'Preparado(s)', 'Actualizado', 'Disponible', 'Edad'],
                    rows=all_deployments
                )
                Console.newLine()

            # ALojar los datos de los Deployments.
            self.deployments = all_deployments

            # Finalizar el Metodo
            return

        # Lanzar el error de no existencia de implementaciones
        Console.newLine()
        Console.info(f"No registran implementaciones en [{self.namespace_selected}]")
        Console.newLine()

    def selectDeployment(self, deployment:str=None):
        """Solicitarle al usuario la seleccion de un deployment en caso de no haber uno configurado."""

        # Generar el listado de los deployments.
        list_deployment = []
        for i_value in self.deployments:
            list_deployment.append(i_value[0])

        # Si no existe un namespace por defecto solicitarle al usuario cual emplear.
        if deployment is None:

            # Solicitar la seleccion.
            deployment = Console.choice(
                question="¿Que implementación deseas emplear?",
                choices=list_deployment
            )

        # Garantizar que la implementacion este presente.
        if deployment not in list_deployment:
            raise ValueError(f"No existe la implemtación con el nombre [{deployment}] dentro de las opciones disponibles.")

        # Alojar el valor del namespace a emplear.
        self.deployment_selected = deployment

        # Mostrar el nombre del nombre de espacio seleccionado
        Console.info(
            message=f"Implementación seleccionada para uso [{self.deployment_selected}]",
            timestamp=True
        )

    def listPods(self, echo:bool = True):
        """Este metodop lista los pods del deployments y del namespace seleccionado."""
        result = subprocess.run(f"kubectl get pods -n {self.namespace_selected}", shell=True, check=True, capture_output=True, text=True)

        # Validar si retorno datos de espacios de nombre.
        if 'NAME' in result.stdout and 'READY' in result.stdout and 'AGE' in result.stdout:

            # Preparar los datos
            resultado = re.sub(r"\([^)]* ago\)", "", result.stdout)
            lst = resultado.split()[5:]

            # Valores para logica de la sepracion de datos.
            iteration = 0
            multiple = 5
            iteration_data = []
            all_pods = []

            # Crear la lista de valores a mostrar traducida al español.
            for value in lst:
                iteration += 1
                if iteration % multiple == 0:
                    value = str(value).replace('y', ' Años ').replace('d', ' Dias').replace('h', ' Horas ').replace('m', ' Minutos ')
                    iteration_data.append(value)
                    all_pods.append(iteration_data)
                    iteration_data = []
                else:
                    if value in ['Running', 'Stoped']:
                        value = value.replace('Running', 'En Ejecución').replace('Stoped', 'Detenido')
                    iteration_data.append(value)

            # Generar la salida en consola.
            if echo:
                Console.newLine()
                Console.textSuccess(
                    message='Nombres de Pods disponibles.'
                )
                Console.table(
                    headers=['Nombre', 'Preparado(s)', 'Estado', 'Reinicios', 'Edad'],
                    rows=all_pods
                )
                Console.newLine()

            # ALojar los datos de los Deployments.
            self.pods = all_pods

            # Finalizar el Metodo
            return

        # Lanzar el error de no existencia de implementaciones
        Console.newLine()
        Console.info(f"No registran Pods en: {self.namespace_selected}//app:{self.deployment_selected}")
        Console.newLine()

    def selectPod(self, pod:str=None):
        """Solicitarle al usuario la seleccion de un pod en caso de no haber uno configurado."""

        # Generar el listado de los deployments.
        list_pods = []
        for i_value in self.pods:
            list_pods.append(i_value[0])

        # Si no existe un namespace por defecto solicitarle al usuario cual emplear.
        if pod is None:

            # Solicitar la seleccion.
            pod = Console.choice(
                question="¿Que POD deseas acceder?",
                choices=list_pods
            )

        # Garantizar que la implementacion este presente.
        if pod not in list_pods:
            raise ValueError(f"No existe el POD con el nombre [{pod}] dentro de las opciones disponibles.")

        # Alojar el valor del namespace a emplear.
        self.pod_selected = pod

        # Mostrar el nombre del nombre de espacio seleccionado
        Console.info(
            message=f"POD seleccionado: [{self.pod_selected}]",
            timestamp=True
        )

    def runBackup(self, folder: str = None):
        """
        Este método se encarga de crear un backup de forma local del código fuente.
        """
        # Definir ruta de backup si no se especifica una
        if not folder:
            current_path = os.path.dirname(__file__)
            backup_path = os.path.join(
                current_path, '..', 'backups', sanitize_folder_name(self.pod_selected)
            )
        else:
            backup_path = folder

        # De no existir el folder crearlo.
        os.makedirs(backup_path, exist_ok=True)

        # Si la carpeta no está vacía, limpiar su contenido
        if os.listdir(backup_path):
            clear_folder(backup_path)

        # Obtener la ruta absoluta
        backup_path = os.path.abspath(backup_path).replace("\\", "/")

        # Guardar el directorio actual
        original_dir = os.getcwd()

        # Iniciaremos la copia de seguridad
        os.chdir(backup_path)
        kubectl_cmd = [
            "kubectl", "cp",
            f"{self.namespace_selected}/{self.pod_selected}:/var/www/app",
            "./"
        ]

        # Ejecutar Accion.
        try:
            Console.info(
                message=f"Ejecutando copia de seguridad desde el pod '{self.pod_selected}'...",
                timestamp=True
            )
            result = subprocess.run(kubectl_cmd, capture_output=True, text=True, check=True)
            Console.info(
                message=f"Copia de seguridad completada: {result.stdout}",
                timestamp=True
            )
        except subprocess.CalledProcessError as e:
            Console.fail(
                message=f"Error al realizar la copia de seguridad: {e.stderr}",
                timestamp=True
            )
            raise
        finally:
            # Volver al directorio original
            os.chdir(original_dir)

    def start_bash(self):
        try:
            # Construimos el comando completo
            cmd = ["kubectl", "exec", "-it", self.pod_selected, "-n", self.namespace_selected, "--", "/bin/bash"]
            Console.textWarning("Iniciando Sesión...")
            Console.textSuccess("Sesion Iniciada Exitosamente.")
            # Ejecutamos el comando en el shell del sistema operativo
            subprocess.run(cmd, shell=True)
        except KeyboardInterrupt:
            Console.info(message="\nSaliendo de la sesión interactiva...", timestamp=True)
        except Exception as e:
            Console.fail(message=f"Error al ejecutar el comando: {e}", timestamp=True)