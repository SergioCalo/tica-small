import setuptools

setuptools.setup(
    name="streamlit-bokeh-events",
    version="0.1.3",
    long_description="",
    long_description_content_type="text/plain",
    url="",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[],
    python_requires=">=3.6",
    install_requires=[
        "bokeh>=2.4.1",
        "streamlit >= 0.63",
    ],
)
