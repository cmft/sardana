:: Install (py)tango + deps
conda install  -y  -c tango-controls pytango=9.2.1
:: Install itango
conda install -y -c tango-controls itango=0.1.6
:: Loging root env
activate
:: Install taurus
pip install taurus
:: Install the generated sardana wheel package to test it
:: Make sure it does not come from cache or pypi
:: At this point all install_requires dependencies MUST be installed
:: as this is installing only from dist/
pip install --pre --find-links dist/ --no-cache-dir --no-index sardana

:: Print Python info
pip list

:: Test import
python -c "import sardana"
:: TODO run testsuite
::sardanatestsuite
