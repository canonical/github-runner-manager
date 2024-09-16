<!-- markdownlint-disable -->

<a href="../src/github_runner_manager/reactive/consumer.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `reactive.consumer`
Module responsible for consuming jobs from the message queue. 


---

<a href="../src/github_runner_manager/reactive/consumer.py#L54"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `consume`

```python
consume(
    queue_config: QueueConfig,
    runner_manager: RunnerManager,
    github_client: GithubClient
) → None
```

Consume a job from the message queue. 

Log the job details and acknowledge the message. If the job details are invalid, reject the message and raise an error. 



**Args:**
 
 - <b>`queue_config`</b>:  The configuration for the message queue. 
 - <b>`runner_manager`</b>:  The runner manager used to create the runner. 
 - <b>`github_client`</b>:  The GitHub client to use to check the job status. 



**Raises:**
 
 - <b>`JobError`</b>:  If the job details are invalid. 


---

<a href="../reactive/consumer/signal_handler#L138"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `signal_handler`

```python
signal_handler(signal_code: Signals) → Generator[NoneType, NoneType, NoneType]
```

Set a signal handler and after the context, restore the default handler. 

The signal handler exits the process. 



**Args:**
 
 - <b>`signal_code`</b>:  The signal code to handle. 


---

<a href="../src/github_runner_manager/reactive/consumer.py#L26"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `JobPickedUpStates`
The states of a job that indicate it has been picked up. 



**Attributes:**
 
 - <b>`COMPLETED`</b>:  The job has completed. 
 - <b>`IN_PROGRESS`</b>:  The job is in progress. 





---

<a href="../src/github_runner_manager/reactive/consumer.py#L38"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `JobDetails`
A class to translate the payload. 



**Attributes:**
 
 - <b>`labels`</b>:  The labels of the job. 
 - <b>`run_url`</b>:  The URL of the job. 





---

<a href="../src/github_runner_manager/reactive/consumer.py#L50"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `JobError`
Raised when a job error occurs. 





