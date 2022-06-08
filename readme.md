# NYPLMSFileFetcher

A multithreaded Python tool to download files from [POLITEMall](https://politemall.polite.edu.sg) (Brightspace) automatically using the BrightSpace API.
Supports 2FA .

Extra features:
- Create PDFs of file and module metadata (requires `wkhtmltopdf`)
- Automatically convert .ppt and .pptx files to .pdf (requires `unoconv`)

**LICENSE**: [WTFPL](https://en.wikipedia.org/wiki/WTFPL)

## Setup
 
```
sudo apt install wkhtmltopdf # Optional
sudo apt install unoconv # Optional
git clone https://github.com/Mctmarcus3/NYPLMSFileFetcher
cd NYPLMSFileFetcher
pip3 install .
```

You can now run the setup.
```
nyplmsfilefetcher setup
```

![](images/setup.png)

### Development environment

```
python3 -m venv venv
source venv/bin/activate
pip install -e . 
```


## Usage

### Sync

Will sync the configured courses to the configured output directory as specified in the config file. This will ignore files that have already been downloaded.

```
nyplmsfilefetcher sync <config>
```

![](images/sync.png)

Config files can be generated with `nyplmsfilefetcher setup`, but can also be manually created following this layout:

```
{
    "output_directory": "./Modules/",
    "courses": [
        438620,
        442195,
        438596,
        450000
    ],
    "credentials": {
        "email": "foo.bar@mymail.nyp.edu.sg",
        "password": "azerty123",
        "otc_secret": "pppmmmvvv"
        "browser": "chrome"
    }
}

```


### List courses


```
nyplmsfilefetcher courses <config>
```

### Download course

Will download a specific course to the specified output directory. Use the previous command to find out the id of your 
courses.

```
nyplmsfilefetcher download <course_id> <config> [output_dir]
```

### Show help

```
nyplmsfilefetcher help
```
