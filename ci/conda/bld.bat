mkdir build
cd build

mkdir external
mkdir vsp

cd external

cmake -G "Visual Studio 14 2015 Win64" ^
    -DCMAKE_BUILD_TYPE=Release ^
    ../../Libraries

if errorlevel 1 exit 1

msbuild /m /verbosity:quiet VSP_LIBRARIES.sln
if errorlevel 1 exit 1

cd ../vsp

cmake -G "Visual Studio 14 2015 Win64" ^
    -DCMAKE_BUILD_TYPE=Release ^
    -DVSP_LIBRARY_PATH="%LIBRARY_PREFIX%/build/external" ^
    -DPYTHON_INCLUDE_DIR="%PYTHON%/include" ^
    -DPYTHON_LIBRARY="%PYTHON%/libs/python%PYTHON_VERSION%.lib" ^
    -DCMAKE_INSTALL_PREFIX="%LIBRARY_PREFIX%/install" ^
    ../../src

if errorlevel 1 exit 1

msbuild /m /verbosity:quiet INSTALL.vcxproj
if errorlevel 1 exit 1
