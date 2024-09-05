<!-- markdownlint-disable -->

<a href="../src/github_runner_manager/errors.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `errors`
Errors used by the charm. 



---

<a href="../src/github_runner_manager/errors.py#L8"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `RunnerError`
Generic runner error as base exception. 





---

<a href="../src/github_runner_manager/errors.py#L12"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `RunnerCreateError`
Error for runner creation failure. 





---

<a href="../src/github_runner_manager/errors.py#L16"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `RunnerStartError`
Error for runner start failure. 





---

<a href="../src/github_runner_manager/errors.py#L20"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `MissingServerConfigError`
Error for unable to create runner due to missing server configurations. 





---

<a href="../src/github_runner_manager/errors.py#L24"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `IssueMetricEventError`
Represents an error when issuing a metric event. 





---

<a href="../src/github_runner_manager/errors.py#L29"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `MetricsStorageError`
Base class for all metrics storage errors. 





---

<a href="../src/github_runner_manager/errors.py#L33"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `SharedFilesystemError`
Base class for all shared filesystem errors. 





---

<a href="../src/github_runner_manager/errors.py#L37"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `CreateMetricsStorageError`
Represents an error when the metrics storage could not be created. 





---

<a href="../src/github_runner_manager/errors.py#L41"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `DeleteMetricsStorageError`
Represents an error when the metrics storage could not be deleted. 





---

<a href="../src/github_runner_manager/errors.py#L45"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `GetMetricsStorageError`
Represents an error when the metrics storage could not be retrieved. 





---

<a href="../src/github_runner_manager/errors.py#L49"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `QuarantineMetricsStorageError`
Represents an error when the metrics storage could not be quarantined. 





---

<a href="../src/github_runner_manager/errors.py#L53"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `SharedFilesystemMountError`
Represents an error related to the mounting of the shared filesystem. 





---

<a href="../src/github_runner_manager/errors.py#L57"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `RunnerMetricsError`
Base class for all runner metrics errors. 





---

<a href="../src/github_runner_manager/errors.py#L61"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `CorruptMetricDataError`
Represents an error with the data being corrupt. 





---

<a href="../src/github_runner_manager/errors.py#L65"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `GithubMetricsError`
Base class for all github metrics errors. 





---

<a href="../src/github_runner_manager/errors.py#L69"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `GithubClientError`
Base class for all github client errors. 





---

<a href="../src/github_runner_manager/errors.py#L73"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `GithubApiError`
Represents an error when the GitHub API returns an error. 





---

<a href="../src/github_runner_manager/errors.py#L77"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `TokenError`
Represents an error when the token is invalid or has not enough permissions. 





---

<a href="../src/github_runner_manager/errors.py#L81"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `JobNotFoundError`
Represents an error when the job could not be found on GitHub. 





---

<a href="../src/github_runner_manager/errors.py#L85"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `OpenStackError`
Base class for OpenStack errors. 





---

<a href="../src/github_runner_manager/errors.py#L89"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `OpenStackInvalidConfigError`
Represents an invalid OpenStack configuration. 





---

<a href="../src/github_runner_manager/errors.py#L93"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `SSHError`
Represents an error while interacting with SSH. 





---

<a href="../src/github_runner_manager/errors.py#L97"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `KeyfileError`
Represents missing keyfile for SSH. 





