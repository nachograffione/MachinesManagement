
# MachinesManagement
The Acronex challenge project.
## Set up
- Clone the repository
- Download and install Python 3 (from https://www.python.org/downloads/)
- Add python and site-packages paths to the environment path variable (usually the installer adds the first, and you only need to add the packages one, which is often \<installationPath\>/Lib/site-packages/)
- Open a terminal
- Navigate to the /.../MachinesManagement/ folder
- Run
    ```
    python -m pip install -r requirements.txt
    python manage.py migrate
    ```

### Start the server
- Open a terminal
- Navigate to the /.../MachinesManagement/ folder
- Run 
    ```
    python manage.py runserver	
    ```
(You will find it in http://localhost:8000/)

## Restful API

### Features
- For the client:
	 - CRUD operations with machines
	 - get the last working data of a certain machine
	 - get the existing machine classes
 - For the Admin only:
	 - CRUD operations with machine classes

### How to use

#### Create a superuser (Admin)
- Open a terminal
- Navigate to the /.../MachinesManagement/ folder
- Run 
    ```    
    python manage.py createsuperuser
    ```
- Follow the CLI steps

#### Admin panel

```
GET /admin/
```

#### Client API

```
GET /api/machines/
```

- Query params:
    - nameInclude (opt)
    - machineClassInclude (opt)
    - isWorking (opt) (values: 'true', 'false')
- The filters are ORed

```
POST /api/machines/
```

- Body fields:
    - name (required)
    - company (required)
    - machineClass (required) (values: one of the existing machine classes)

```
GET /api/machines/:id/
```

```
PATCH /api/machines/:id/
```

- Body fields:
    - name (opt)
    - company (opt)
    - machineClass (opt)

```
DELETE /api/machines/:id/
```

```
GET /api/machines/:id/last-working-data/
```

```
GET /api/machine-classes/
```

## Webpage

- Follow this link: http://localhost:8000/machines/