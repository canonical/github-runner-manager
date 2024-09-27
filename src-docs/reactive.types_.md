<!-- markdownlint-disable -->

<a href="../src/github_runner_manager/reactive/types_.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `reactive.types_`
Module containing reactive scheduling related types. 



---

<a href="../src/github_runner_manager/reactive/types_.py#L14"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `QueueConfig`
The configuration for the message queue. 



**Attributes:**
 
 - <b>`mongodb_uri`</b>:  The URI of the MongoDB database. 
 - <b>`queue_name`</b>:  The name of the queue. 





---

<a href="../src/github_runner_manager/reactive/types_.py#L26"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `RunnerConfig`
The configuration for the reactive runner to spawn. 



**Attributes:**
 
 - <b>`queue`</b>:  The queue configuration. 
 - <b>`runner_manager`</b>:  The runner manager configuration. 
 - <b>`cloud_runner_manager`</b>:  The OpenStack runner manager configuration. 
 - <b>`github_token`</b>:  str 
 - <b>`supported_labels`</b>:  The supported labels for the runner. 





