import os
import re
import pytest
import cli.utils

VIRTUALENVS_DIR="./virtualenvs-dummy"


class TestUtils(object):
    """
    Unit Tests for PipelineWise CLI utility functions
    """
    def test_json_detectors(self):
        """Testing JSON detector functions"""
        assert cli.utils.is_json("{Invalid JSON}") == False

        assert cli.utils.is_json("[]") == True
        assert cli.utils.is_json("{}") == True
        assert cli.utils.is_json('{"prop": 123}') == True
        assert cli.utils.is_json('{"prop-str":"dummy-string","prop-int":123,"prop-bool":true}') == True

        assert cli.utils.is_json_file("./dummy-json") == False
        assert cli.utils.is_json_file("{}/resources/example.json".format(os.path.dirname(__file__))) == True


    def test_json_loader(self):
        """Testing JSON loader functions"""
        # Loading JSON file that not exist should return None
        assert cli.utils.load_json("/invalid/location/to/json") is None

        # Loading JSON file with invalid JSON syntax should raise exception
        with pytest.raises(Exception):
            cli.utils.load_json("{}/resources/invalid.json".format(os.path.dirname(__file__)))

        # Loading JSON should return python dict
        assert (
            cli.utils.load_json("{}/resources/example.json".format(os.path.dirname(__file__))),
            {
                "glossary": {
                    "title": "example glossary",
                    "GlossDiv": {
                        "title": "S",
                        "GlossList": {
                            "GlossEntry": {
                                "ID": "SGML",
                                "SortAs": "SGML",
                                "GlossTerm": "Standard Generalized Markup Language",
                                "Acronym": "SGML",
                                "Abbrev": "ISO 8879:1986",
                                "GlossDef": {
                                    "para": "A meta-markup language, used to create markup languages such as DocBook.",
                                    "GlossSeeAlso": ["GML", "XML"]
                                },
                                "GlossSee": "markup"
                            }
                        }
                    }
                }
            })


    def test_yaml_detectors(self):
        """Testing YAML detector functions"""
        assert cli.utils.is_json("{Invalid YAML}") == False

        assert cli.utils.is_yaml("id: 123") == True
        assert cli.utils.is_yaml("""
            id: 123
            details:
                - prop1: 123
                - prop2: 456
            """) == True

        assert cli.utils.is_yaml_file("./dummy-yaml") == False
        assert cli.utils.is_yaml_file("{}/resources/example.yml".format(os.path.dirname(__file__))) == True 


    def test_yaml_loader(self):
        """Testing YAML loader functions"""
        # Loading YAML file that not exist should return None
        assert cli.utils.load_yaml("/invalid/location/to/yaml") is None

        # Loading YAML file with invalid YAML syntax should raise exception
        with pytest.raises(Exception):
            cli.utils.load_yaml("{}/resources/invalid.yml".format(os.path.dirname(__file__)))

        assert (
            cli.utils.load_yaml("{}/resources/example.yml".format(os.path.dirname(__file__))),
            ['Apple', 'Orange', 'Strawberry', 'Mango'])


    def test_sample_file_path(self):
        """Sample files must be a tap, target YAML or README file"""
        for sample in cli.utils.get_sample_file_paths():
            assert os.path.isfile(sample) == True
            assert (
                re.match(".*[tap|target]_.*.yml.sample$", sample) or re.match(".*README.md$", sample))


    def test_extract_log_attributes(self):
        """Log files must match to certain pattern with embedded attributes in the file name"""
        assert (
            cli.utils.extract_log_attributes("snowflake-fx-20190508_000038.singer.log.success"),
            {
                'filename': 'snowflake-fx-20190508_000038.singer.log.success',
                'target_id': 'snowflake',
                'tap_id': 'fx',
                'timestamp': '2019-05-08T00:00:38',
                'sync_engine': 'singer',
                'status': 'success'
            })

        assert (
            cli.utils.extract_log_attributes("snowflake-fx-20190508_231238.fastsync.log.running"),
            {
                'filename': 'snowflake-fx-20190508_231238.fastsync.log.running',
                'target_id': 'snowflake',
                'tap_id': 'fx',
                'timestamp': '2019-05-08T23:12:38',
                'sync_engine': 'fastsync',
                'status': 'running'
            })

        assert (
            cli.utils.extract_log_attributes("dummy-log-file.log"),
            {
                'filename': 'dummy-log-file.log',
                'target_id': 'unknown',
                'tap_id': 'unknown',
                'timestamp': '1970-01-01T00:00:00',
                'sync_engine': 'unknown',
                'status': 'unknown'
            })
        

    def test_fastsync_bin(self):
        """..."""
        assert (
            cli.utils.get_fastsync_bin(VIRTUALENVS_DIR, 'mysql', 'snowflake'),
            "{}/mysql-to-snowflake/bin/mysql-to-snowflake".format(VIRTUALENVS_DIR))