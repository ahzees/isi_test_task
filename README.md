# ISI TEST TASK



## How to run test task



#### Firstly, you have to install poetry using this command
<br></br>
```{r test-python, engine='python'}
pip install poetry
```
<br></br>
### Then, you have to copy the github repo using
<br></br>
```{r test-python, engine='python'}
git clone git@github.com:ahzees/isi_test_task.git
```
<br></br>
### Install poetry dependecies. You must be at the root of the project
<br></br>
```{r test-python, engine='python'}
poetry install
```
<br></br>
### Run poetry shell
<br></br>
```{r test-python, engine='python'}
poetry shell
```
<br></br>
### Go to the isi_test_task/
<br></br>
```{r test-python, engine='python'}
cd isi_test_task/
```
<br></br>
### Run migrations. You must have an .env file in the root of your Django project
<br></br>
```{r test-python, engine='python'}
python manage.py makemigrations chat
python manage.py migrate
```
<br></br>
### Load dump.json
<br></br>
```{r test-python, engine='python'}
python manage.py loaddata dump.json
```
<br></br>
### Run the server
<br></br>
```{r test-python, engine='python'}
python manage.py runserver
```
<br></br>
