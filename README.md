# AzureFunctions

## this is a script to setup an Azure function with python 3.6 and do pip installs
I also added some basic example's I used for sample weekend projects ^__^


#### install

##### Prep Azure functon with Python 3.6 64x
* open KUDU
* go to Diagnostic Console

```shell
nuget.exe install -Source https://www.siteextensions.net/api/v2/ -OutputDirectory D:\home\site\tools python361x64  

mv /d/home/site/tools/python361x64.3.6.1.3/content/python361x64/* /d/home/site/tools/

D:\home\site\tools\python.exe -m pip install --upgrade -r D:\home\site\wwwroot\requirements.txt


```


### custom settings from dashboard
Go to Application settings from Azure Function dashboard 
Add to App settings : Key=YOURAPPSETTING Value=something

#### Good reads and for inspirations: 
https://github.com/yokawasa/azure-functions-python-samples
https://github.com/nmyster/python-alexa


#### Sources:
https://prmadi.com/running-python-code-on-azure-functions-app/
https://social.msdn.microsoft.com/Forums/azure/en-US/2a9c52a1-391c-4609-b133-ee56c2ad4b7e/access-app-settings-from-azure-function-with-python?forum=AzureFunctions


