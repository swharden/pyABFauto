:: deploy manually via the X-drive because the remote server does 
:: not have internet access and can't pull the latest code using git

rmdir X:\Software\pyABFauto /Q /S
robocopy ..\..\pyABFauto X:\Software\pyABFauto /E /NJH /NFL /NDL
rmdir X:\Software\pyABFauto\src\pyABFauto\__pycache__ /Q /S
rmdir X:\Software\pyABFauto\src\pyABFauto\analyses\__pycache__ /Q /S
pause