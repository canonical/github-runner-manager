<!-- markdownlint-disable -->

<a href="../src/github_runner_manager/reactive/types_.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `reactive.types_`






---

<a href="../src/github_runner_manager/reactive/types_.py#L11"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `QueueConfig`
The configuration for the message queue. 



**Attributes:**
 
 - <b>`mongodb_uri`</b>:  The URI of the MongoDB database. 
 - <b>`queue_name`</b>:  The name of the queue. 





---

<a href="../src/github_runner_manager/reactive/types_.py#L23"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `RunnerConfig`
The configuration for the reactive runner to spawn. 



**Attributes:**
 
 - <b>`queue`</b>:  The queue configuration. 
 - <b>`runner_manager`</b>:  The runner manager configuration. 
 - <b>`runner`</b>:  The GitHub runner configuration. 
 - <b>`openstack_cloud`</b>:  The OpenStack cloud configuration. 
 - <b>`openstack_server`</b>:  The OpenStack server configuration. 





