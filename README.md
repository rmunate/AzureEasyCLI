# **Manual de Conexión a Azure y Kubernetes**

Este manual ofrece instrucciones detalladas para conectar con Azure, configurar una suscripción, interactuar con un clúster de Kubernetes y gestionar los Pods y Deployments dentro del entorno.

---

## **1. Iniciar sesión en Azure**

Para iniciar sesión en Azure, ejecute el siguiente comando:

```bash
# En la Web
az login

# En el Local
az login --tenant <ID_TENANT>
```

Asegúrese de utilizar las credenciales adecuadas para su cuenta de Azure.

---

## **2. Configurar la suscripción**

Para trabajar con una suscripción específica, utilice el siguiente comando:

```bash
az account set --subscription <ID_SUSCRIPCION>
```

---

## **3. Obtener las credenciales del clúster Kubernetes**

Conéctese al clúster Kubernetes configurando las credenciales para el grupo de recursos y el nombre del clúster deseado:

```bash
az aks get-credentials --resource-group <GRUPO_RECURSOS> --name <CLUSTER_NAME> --overwrite-existing
```

---

## **4. Listar los Pods disponibles**

Para ver todos los Pods disponibles en el clúster, ejecute el siguiente comando:

```bash
kubectl get pods --all-namespaces -o wide
```

---

## **5. Listar todos los Deployments**

### Listar todos los Deployments en el clúster
```bash
kubectl get deployments --all-namespaces
```

### Listar Deployments en un espacio de nombres específico
Para filtrar por espacio de nombres, use el siguiente comando:

```bash
kubectl get deployments -n <NAMESPACE>
```

---

## **6. Identificar los espacios de nombres**

Si no conoce los espacios de nombres disponibles, liste todos con el siguiente comando:

```bash
kubectl get namespaces
```

---

## **7. Acceder a un Pod específico**

Para acceder a un Pod y trabajar en su entorno de CLI, ejecute el siguiente comando, reemplazando `<POD_NAME>` con el nombre del Pod deseado:

```bash
kubectl exec -it <POD_NAME> -n <NAMESPACE> -- /bin/bash
```

---

## **8. Comandos útiles dentro del Pod**

Una vez dentro del Pod, puede usar los siguientes comandos para navegar y gestionar archivos:

### **Navegación de directorios**
- Listar contenido del directorio actual:
  ```bash
  ls
  ```
- Listar contenido con detalles:
  ```bash
  ls -l
  ```
- Cambiar a otro directorio:
  ```bash
  cd <directorio>
  ```
- Volver al directorio anterior:
  ```bash
  cd ..
  ```

### **Gestión de archivos**
- Copiar un archivo:
  ```bash
  cp <archivo_origen> <archivo_destino>
  ```
- Mover o renombrar un archivo:
  ```bash
  mv <archivo_origen> <archivo_destino>
  ```
- Eliminar un archivo:
  ```bash
  rm <nombre_archivo>
  ```

### **Edición de archivos**
- Abrir un archivo con el editor de texto:
  ```bash
  nano <nombre_archivo>
  ```

### **Gestión de procesos**
- Ver los procesos en ejecución:
  ```bash
  ps aux
  ```

### **Otras utilidades**
- Ver el contenido de un archivo:
  ```bash
  cat <nombre_archivo>
  ```
- Limpiar la pantalla de la terminal:
  ```bash
  clear
  ```
- Crear un directorio:
  ```bash
  mkdir <nombre_directorio>
  ```
- Comprobar espacio en disco:
  ```bash
  df -h
  ```

---

## **Copiar Contenido Al Local**

Para copiar el contenido de un Pod a una ruta del equipo local, inicie sesión desde PowerShell, asegurándose de que el Azure CLI esté instalado previamente.

Ruta a copiar = `/var/www/app`
Pod = `<POD_NAME>`
Namespace = `<NAMESPACE>`

```bash
# Primero navegue hasta la ruta local donde desea copiar el contenido.
cd <ruta_local>

# Luego ejecute el comando de copia.
kubectl cp <NAMESPACE>/<POD_NAME>:/var/www/app ./<POD_NAME>/
```

---

## **Copiar Archivos Local Al POD**

Para copiar un archivo del equipo local al Pod, ejecute el siguiente comando:

```bash
kubectl cp <archivo_local> <NAMESPACE>/<POD_NAME>:/var/www/app/<ruta_destino>
```

---
