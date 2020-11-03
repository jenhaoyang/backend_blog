from setuptools import find_packages, setup

setup(
    name='flask_project',
    version='1.0.0',
    packages=find_packages(),#告訴Python哪些package資料夾需要被include，find_packages會自動幫你尋找因此我們不須手動輸入
    include_package_data=True,#告訴Python要include data資料夾如static和template資料夾，藉由MANIFEST.in來告訴Python哪些是要被include的data 資料夾
    zip_safe=False,
    install_requires=[
        'flask'
    ]
)