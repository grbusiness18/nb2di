# Prerequisites : 

### _Only in Local Environment set the following ENVIRONMENTAL Variables_.

DI_CLUSTER_URL="https://xxxxxxxxxxxxxxxxxx.sapdatahub.com:xxxx" <br>
DI_TENANT="di tenant" <br>
DI_USERNAME="DI logon User name" <br>
DI_PASSWORD="DI logon Password" <br>
DI_SCENARIO_ID="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"<br>

_The Notebooks in DI will get the connection details automatically._

### _Optional Environmental variable_

DI_PIPELINE_ID="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"<br>

_Pipeline can be set programmatically using_ `api.set_pipeline_by_id('xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx')`

<font color="red"> Any operations to DI needs the DI-MODE enabled. It can be done via `api.set_di_mode_on()` and can be switched off via `api.set_di_mode_off()` </font>