This app does following:
    - Fetch the XML from given URL
    - Parse the XML and download the first DLTINS zip file given
    - Extract the XML from the file
    - Convert the XML file to CSV file

Things couldn't be done due to time crunch
    - Use file streaming instead of directly loading everthing into memory
    - Write unit tests
    - Store CSV into S3


How to run:
1. Install dependencies
```bash
$ pip install -r requirements.txt
```

2. Run the app
```bash
$ python app.py
```

3. The app stores the resulting CSV file to `final.csv` into current
   directory
