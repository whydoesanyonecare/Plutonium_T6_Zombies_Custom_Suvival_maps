@echo off

xcopy /i "%CD%\privategamelobby_project.lua" "%localappdata%\Plutonium\storage\t6\ui_mp\t6\menus" /y 

xcopy /i "%CD%\scripts" "%localappdata%\Plutonium\storage\t6\scripts\zm" /E /y

@echo Install Completed!

timeout 5

end