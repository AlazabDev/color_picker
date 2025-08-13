from setuptools import setup, find_packages

with open("requirements.txt") as f:
    install_requires = f.read().strip().split("\\n")

setup(
    name="color_picker",
    version="1.0.0",
    description="Advanced Color Picker Tool for Frappe/ERPNext",
    author="Azab Tools",
    author_email="info@azabtools.com",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=install_requires
)
