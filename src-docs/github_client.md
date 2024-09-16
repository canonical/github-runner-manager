<!-- markdownlint-disable -->

<a href="../src/github_runner_manager/github_client.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `github_client`
GitHub API client. 

Migrate to PyGithub in the future. PyGithub is still lacking some API such as remove token for runner. 


---

<a href="../src/github_runner_manager/github_client.py#L43"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `catch_http_errors`

```python
catch_http_errors(
    func: Callable[~ParamT, ~ReturnT]
) → Callable[~ParamT, ~ReturnT]
```

Catch HTTP errors and raise custom exceptions. 



**Args:**
 
 - <b>`func`</b>:  The target function to catch common errors for. 



**Returns:**
 The decorated function. 


---

<a href="../src/github_runner_manager/github_client.py#L82"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `GithubClient`
GitHub API client. 

<a href="../src/github_runner_manager/github_client.py#L85"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(token: str)
```

Instantiate the GiHub API client. 



**Args:**
 
 - <b>`token`</b>:  GitHub personal token for API requests. 




---

<a href="../src/github_runner_manager/github_client.py#L187"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `delete_runner`

```python
delete_runner(path: GitHubOrg | GitHubRepo, runner_id: int) → None
```

Delete the self-hosted runner from GitHub. 



**Args:**
 
 - <b>`path`</b>:  GitHub repository path in the format '<owner>/<repo>', or the GitHub organization  name. 
 - <b>`runner_id`</b>:  Id of the runner. 

---

<a href="../src/github_runner_manager/github_client.py#L267"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get`

```python
get(url: HttpUrl) → dict | list | str | int | float | bool | None
```

Make a GET call to the GitHub API. 



**Args:**
 
 - <b>`url`</b>:  The URL to call. 



**Raises:**
 
 - <b>`ValueError`</b>:  If the URL is not a GitHub API URL. 



**Returns:**
 The JSON response from the API. 

---

<a href="../src/github_runner_manager/github_client.py#L208"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_job_stats`

```python
get_job_stats(
    path: GitHubRepo,
    workflow_run_id: str,
    runner_name: str
) → JobStats
```

Get information about a job for a specific workflow run identified by the runner name. 



**Args:**
 
 - <b>`path`</b>:  GitHub repository path in the format '<owner>/<repo>'. 
 - <b>`workflow_run_id`</b>:  Id of the workflow run. 
 - <b>`runner_name`</b>:  Name of the runner. 



**Raises:**
 
 - <b>`TokenError`</b>:  if there was an error with the Github token crdential provided. 
 - <b>`JobNotFoundError`</b>:  If no jobs were found. 



**Returns:**
 Job information. 

---

<a href="../src/github_runner_manager/github_client.py#L94"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_runner_github_info`

```python
get_runner_github_info(path: GitHubOrg | GitHubRepo) → list[SelfHostedRunner]
```

Get runner information on GitHub under a repo or org. 



**Args:**
 
 - <b>`path`</b>:  GitHub repository path in the format '<owner>/<repo>', or the GitHub organization  name. 



**Returns:**
 List of runner information. 

---

<a href="../src/github_runner_manager/github_client.py#L164"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_runner_registration_token`

```python
get_runner_registration_token(path: GitHubOrg | GitHubRepo) → str
```

Get token from GitHub used for registering runners. 



**Args:**
 
 - <b>`path`</b>:  GitHub repository path in the format '<owner>/<repo>', or the GitHub organization  name. 



**Returns:**
 The registration token. 

---

<a href="../src/github_runner_manager/github_client.py#L142"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_runner_remove_token`

```python
get_runner_remove_token(path: GitHubOrg | GitHubRepo) → str
```

Get token from GitHub used for removing runners. 



**Args:**
 
 - <b>`path`</b>:  The Github org/repo path. 



**Returns:**
 The removing token. 


