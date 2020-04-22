::%windir%\System32\cmd.exe "/K" C:\ProgramData\Anaconda3\Scripts\activate.bat C:\ProgramData\Anaconda3
::conda activate mimiibaseTF2GPU

cd /d %~dp0
cd /d ..
cd /d ..

set root=C:\ProgramData\Anaconda3

call %root%\Scripts\activate.bat %root%

call conda activate mimiibaseTF2GPU

call jupyter notebook
pauses