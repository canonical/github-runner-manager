<!-- markdownlint-disable -->

<a href="../src/github_runner_manager/reactive/runner_manager.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `reactive.runner_manager`
Module for managing reactive runners. 

**Global Variables**
---------------
- **PYTHON_BIN**
- **REACTIVE_RUNNER_SCRIPT_MODULE**
- **REACTIVE_RUNNER_CMD_LINE_PREFIX**
- **PID_CMD_COLUMN_WIDTH**
- **PIDS_COMMAND_LINE**
- **UBUNTU_USER**
- **RUNNER_CONFIG_ENV_VAR**

---

<a href="../src/github_runner_manager/reactive/runner_manager.py#L40"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `reconcile`

```python
reconcile(quantity: int, reactive_config: RunnerConfig) → int
```

Spawn a runner reactively. 



**Args:**
 
 - <b>`quantity`</b>:  The number of runners to spawn. 
 - <b>`reactive_config`</b>:  The reactive runner configuration. 

Raises a ReactiveRunnerError if the runner fails to spawn. 



**Returns:**
 The number of reactive runner processes spawned. 


---

<a href="../src/github_runner_manager/reactive/runner_manager.py#L36"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `ReactiveRunnerError`
Raised when a reactive runner error occurs. 





