# **Manual de Conexión a Azure y Kubernetes**

Este manual proporciona instrucciones detalladas para iniciar sesión en Azure, configurar la suscripción, interactuar con un clúster de Kubernetes, y navegar por los Pods y Deployments en el entorno.

---

## **1. Iniciar sesión en Azure**

Ejecute el siguiente comando para iniciar sesión en Azure:

```bash
# En la Web
az login

# En el Local
az login --tenant 18ad3eec-bc5b-4390-9f15-d679a3c24e9e
```

Asegúrese de usar las credenciales asociadas a la cuenta `@participacionbogota.gov.co`.

---

## **2. Configurar la suscripción**

Para trabajar con un Tenant específico, seleccione la suscripción correspondiente utilizando el siguiente comando:

```bash
az account set --subscription 4fc0d55a-5909-4ee6-b2f3-e1dee8fa95eb
```

---

## **3. Obtener las credenciales del clúster Kubernetes**

Conéctese al clúster Kubernetes configurando las credenciales para el grupo de recursos `idpac_kubernetes` y el clúster `ProductionAKSCluster`:

```bash
az aks get-credentials --resource-group idpac_kubernetes --name ProductionAKSCluster --overwrite-existing
```

---

## **4. Listar los Pods disponibles**

Para ver todos los Pods disponibles en el clúster, use el siguiente comando:

```bash
kubectl get pods --all-namespaces -o wide
```

### **PODS relevantes para el área de comunicaciones**

| **Espacio de nombres** | **Nombre del Pod**              | **IP del Pod** | **Nodo asignado**                  |
|-------------------------|---------------------------------|----------------|-------------------------------------|
| idpac-develop           | cms-nginx-7db6989cc4-c7tlg     | 10.244.0.27    | aks-d4sv5-37625573-vmss00000o      |
| idpac-develop           | cms-nginx-7db6989cc4-ff5k4     | 10.244.2.31    | aks-d4sv5-37625573-vmss00000c      |
| idpac-develop           | cms-nginx-7db6989cc4-gg925     | 10.244.2.40    | aks-d4sv5-37625573-vmss00000c      |
| idpac-develop           | cms-php-d9c6ddd48-4jsrc        | 10.244.2.15    | aks-d4sv5-37625573-vmss00000c      |
| idpac-develop           | cms-php-d9c6ddd48-mvsl2        | 10.244.3.72    | aks-d4sv5-37625573-vmss00000e      |
| idpac-develop           | cms-php-d9c6ddd48-tlwkm        | 10.244.2.32    | aks-d4sv5-37625573-vmss00000c      |

---

## **5. Listar todos los Deployments**

### Listar todos los Deployments en el clúster
```bash
kubectl get deployments --all-namespaces
```

### Listar Deployments en un espacio de nombres específico
Para filtrar por espacio de nombres, use el siguiente comando:

```bash
kubectl get deployments -n idpac-develop
```

---

## **6. Identificar los espacios de nombres**

Si no conoce los espacios de nombres disponibles, liste todos con el siguiente comando:

```bash
kubectl get namespaces
```

---

## **7. Acceder a un Pod específico**

Para acceder a un Pod y trabajar en su entorno de CLI, ejecute el siguiente comando, reemplazando `cms-php-d9c6ddd48-4jsrc` con el nombre del Pod deseado:

```bash
kubectl exec -it cms-php-d9c6ddd48-4jsrc -n idpac-develop -- /bin/bash
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
  cd <nombre_del_directorio>
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
  rm <nombre_del_archivo>
  ```

### **Edición de archivos**
- Abrir un archivo con el editor de texto predeterminado:
  ```bash
  nano <nombre_del_archivo>
  ```

### **Gestión de procesos**
- Ver los procesos en ejecución:
  ```bash
  ps aux
  ```

### **Otras utilidades**
- Ver el contenido de un archivo:
  ```bash
  cat <nombre_del_archivo>
  ```
- Limpiar la pantalla de la terminal:
  ```bash
  clear
  ```
- Crear un directorio:
  ```bash
  mkdir <nombre_del_directorio>
  ```
- Comprobar espacio en disco:
  ```bash
  df -h
  ```

---

## **Copiar Contenido Al Local**

Para poder copiar el contenido del POD a una ruta del PC local del desarrollador, es escencial que la sesion se inicie desde un PowerShell de manera local teniendo instalo previamente el azure-cli.

Ruta a copiar = /var/www/app
Pod = cms-php-d9c6ddd48-4jsrc
Namespace = idpac-develop

```bash
# Primero Iremos a la ruta a donde queremos copiar el contenido.
cd C:\Users\runate\eclipse\Documents\AzureData

# Luego estando allí ejecutamos el comando de copia.
# kubectl cp idpac-develop/cms-nginx-7db6989cc4-gg925:/var/www/app ./cms-nginx-7db6989cc4-gg925/
C:\Users\runate\eclipse\Documents\AzureData> kubectl cp idpac-develop/cms-php-d9c6ddd48-4jsrc:/var/www/app ./cms-php-d9c6ddd48-4jsrc/

# Este proceso tomará ciertos minutos mientros se ejecuta, solo es cuestion de esperar.
```

---

## Copiar Archivos Local Al POD:

Copiar un archivo del local al POD.

```bash
kubectl cp header_buscar_boton.png idpac-main/cms-php-7697c45779-7h2v4:/var/www/app/web/sites/idpac/files/imagenes/header_buscar_boton.png

kubectl cp . idpac-main/cms-php-7697c45779-7h2v4:/var/www/app/web/api/
```

---

## Información del Autor

- **Fecha**: 31 de Octubre de 2024
- **Ingeniero**: Raúl Mauricio Uñate Castro