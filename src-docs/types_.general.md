<!-- markdownlint-disable -->

<a href="../src/github_runner_manager/types_/general.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `types_.general`
Module containing a collection of unrelated types. 



---

<a href="../src/github_runner_manager/types_/general.py#L11"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `ReactiveConfig`
Represents the configuration for reactive scheduling. 



**Attributes:**
 
 - <b>`mq_uri`</b>:  The URI of the MQ to use to spawn runners reactively. 





---

<a href="../src/github_runner_manager/types_/general.py#L21"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `ProxyConfig`
Proxy configuration. 



**Attributes:**
 
 - <b>`aproxy_address`</b>:  The address of aproxy snap instance if use_aproxy is enabled. 
 - <b>`http`</b>:  HTTP proxy address. 
 - <b>`https`</b>:  HTTPS proxy address. 
 - <b>`no_proxy`</b>:  Comma-separated list of hosts that should not be proxied. 
 - <b>`use_aproxy`</b>:  Whether aproxy should be used for the runners. 


---

#### <kbd>property</kbd> aproxy_address

Return the aproxy address. 



---

<a href="../src/github_runner_manager/types_/general.py#L55"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>classmethod</kbd> `check_use_aproxy`

```python
check_use_aproxy(use_aproxy: bool, values: dict) → bool
```

Validate the proxy configuration. 



**Args:**
 
 - <b>`use_aproxy`</b>:  Value of use_aproxy variable. 
 - <b>`values`</b>:  Values in the pydantic model. 



**Raises:**
 
 - <b>`ValueError`</b>:  if use_aproxy was set but no http/https was passed. 



**Returns:**
 Validated use_aproxy value. 


---

<a href="../src/github_runner_manager/types_/general.py#L84"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `SSHDebugConnection`
SSH connection information for debug workflow. 



**Attributes:**
 
 - <b>`host`</b>:  The SSH relay server host IP address inside the VPN. 
 - <b>`port`</b>:  The SSH relay server port. 
 - <b>`rsa_fingerprint`</b>:  The host SSH server public RSA key fingerprint. 
 - <b>`ed25519_fingerprint`</b>:  The host SSH server public ed25519 key fingerprint. 





---

<a href="../src/github_runner_manager/types_/general.py#L100"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `RepoPolicyComplianceConfig`
Configuration for the repo policy compliance service. 



**Attributes:**
 
 - <b>`token`</b>:  Token for the repo policy compliance service. 
 - <b>`url`</b>:  URL of the repo policy compliance service. 





