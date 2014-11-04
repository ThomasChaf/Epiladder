# Epiladder

Epiladder is a simple ladder use to rank the Epitech students.

## Requirements ##

 * Worked with Python 3 - Python3.4
 * [PyCurl](http://pycurl.sourceforge.net/) for http request

## Install

    $ git clone https://github.com/ThomasChaf/Epiladder.git

## Usage

#### Configuration

##### Input file

Make a list with all the names of the students that you want to rank.
Some default list are already available in the Config folder.

The expected format is as follow:

    login_x
    login2_x
    EOF

##### Fill the auth section in the config file (Config/config.json)

    "login" : "LOGIN",
    "password" : "PASSWORD",

#### Launch it

    $ ./epilader --file="results.txt" --verbose < Config/sample.txt

## Credits

  - [Thomas Chafiol](http://github.com/ThomasChaf) <[t-chafiol.fr](http://t-chafiol.fr)>
