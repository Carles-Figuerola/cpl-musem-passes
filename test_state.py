import unittest
from state import find_diff, State

base_state = {
    "Chicago Children's Museum": {
        "West Loop": 2
    }, 
    "Museum of Science and Industry": {
        "Merlo": 1,
        "Near North": 1
    },
    "Shedd Aquarium": {}
}


class TestState(unittest.TestCase):
    def test_find_diff_no_change(self):
        new = {
            "Chicago Children's Museum": {
                "West Loop": 2
            }, 
            "Museum of Science and Industry": {
                "Merlo": 1,
                "Near North": 1
            },
            "Shedd Aquarium": {}
        }

        diff = {}
        result, output = find_diff(base_state, new)
        
        self.assertFalse(result)
        self.assertDictEqual(output, diff)

    def test_find_diff_one_more_pass_existing_library(self):
        new = {
            "Chicago Children's Museum": {
                "West Loop": 2
            }, 
            "Museum of Science and Industry": {
                "Merlo": 2,
                "Near North": 1
            },
            "Shedd Aquarium": {}
        }

        diff = {
            "Museum of Science and Industry": {
                "Merlo": 1
            }
        }
        result, output = find_diff(base_state, new)
        
        self.assertTrue(result)
        self.assertDictEqual(output, diff)

    def test_find_diff_one_less_pass_existing_library(self):
        new = {
            "Chicago Children's Museum": {
                "West Loop": 1
            }, 
            "Museum of Science and Industry": {
                "Merlo": 1,
                "Near North": 1
            },
            "Shedd Aquarium": {}
        }
        
        diff = {
            "Chicago Children's Museum": {
                "West Loop": -1
            }
        }
        
        result, output = find_diff(base_state, new)
        
        self.assertTrue(result)
        self.assertDictEqual(output, diff)

    def test_find_diff_added_library(self):
        new = {
            "Chicago Children's Museum": {
                "West Loop": 2,
                "Water Works": 1
            }, 
            "Museum of Science and Industry": {
                "Merlo": 1,
                "Near North": 1
            },
            "Shedd Aquarium": {}
        }
        
        diff = {
            "Chicago Children's Museum": {
                "Water Works": 1
            }
        }
        
        result, output = find_diff(base_state, new)
        
        self.assertTrue(result)
        self.assertDictEqual(output, diff)

    def test_find_diff_removed_library(self):
        new = {
            "Chicago Children's Museum": {
                "West Loop": 2
            },
            "Museum of Science and Industry": {
                "Near North": 1
            },
            "Shedd Aquarium": {}
        }
        
        diff = {
            "Museum of Science and Industry": {
                "Merlo": -1
            }
        }
        
        result, output = find_diff(base_state, new)
        
        self.assertTrue(result)
        self.assertDictEqual(output, diff)

    def test_find_diff_empty_museum_new_library(self):
        new = {
            "Chicago Children's Museum": {
                "West Loop": 2
            }, 
            "Museum of Science and Industry": {
                "Merlo": 1,
                "Near North": 1
            },
            "Shedd Aquarium": {
                "Water Works": 1
            }
        }
        
        diff = {
            "Shedd Aquarium": {
                "Water Works": 1
            }
        }
        
        result, output = find_diff(base_state, new)
        
        self.assertTrue(result)
        self.assertDictEqual(output, diff)


    def test_find_diff_museum_with_libraries_remove_all(self):
        new = {
            "Chicago Children's Museum": {
                "West Loop": 2
            }, 
            "Museum of Science and Industry": {},
            "Shedd Aquarium": {}
        }
        
        diff = {
            "Museum of Science and Industry": {
                "Merlo": -1,
                "Near North": -1
            }
        }
        
        result, output = find_diff(base_state, new)
        
        self.assertTrue(result)
        self.assertDictEqual(output, diff)


    def test_has_changes_simple(self):
        file = 'testfiles/simple_state.json'
        current = {
            "Chicago Children's Museum": {
                "available": {
                    "West Loop": [
                        {"something": "here"},
                        {"something": "else"},
                    ]
                }
            }, 
            "Museum of Science and Industry": {
                "available": {
                    "Merlo": [
                        {"something": "here"}
                    ],
                    "Near North": [
                        {"something": "here"}
                    ]
                }
            },
            "Shedd Aquarium": {
                "available": {}
            }
        }
        state = State(file)
        result, output = state.has_changes(current)

        self.assertFalse(result)
        self.assertDictEqual(output, {})

    def test_has_changes_new_empty_museum(self):
        file = 'testfiles/simple_state.json'
        current = {
            "Chicago Children's Museum": {
                "available": {
                    "West Loop": [
                        {"something": "here"},
                        {"something": "else"},
                    ]
                }
            }, 
            "Museum of Science and Industry": {
                "available": {
                    "Merlo": [
                        {"something": "here"}
                    ],
                    "Near North": [
                        {"something": "here"}
                    ]
                }
            },
            "Shedd Aquarium": {
                "available": {}
            },
            "Chicago Botanic Gardens": {
                "available": {}
            }
        }
        state = State(file)
        result, output = state.has_changes(current)

        self.assertFalse(result)
        self.assertDictEqual(output, {})

    def test_has_changes_removed_empty_museum(self):
        file = 'testfiles/simple_state.json'
        current = {
            "Chicago Children's Museum": {
                "available": {
                    "West Loop": [
                        {"something": "here"},
                        {"something": "else"},
                    ]
                }
            }, 
            "Museum of Science and Industry": {
                "available": {
                    "Merlo": [
                        {"something": "here"}
                    ],
                    "Near North": [
                        {"something": "here"}
                    ]
                }
            }
        }
        state = State(file)
        result, output = state.has_changes(current)

        self.assertFalse(result)
        self.assertDictEqual(output, {})

    def test_has_changes_new_museum_with_availability(self):
        file = 'testfiles/simple_state.json'
        current = {
            "Chicago Children's Museum": {
                "available": {
                    "West Loop": [
                        {"something": "here"},
                        {"something": "else"},
                    ]
                }
            }, 
            "Museum of Science and Industry": {
                "available": {
                    "Merlo": [
                        {"something": "here"}
                    ],
                    "Near North": [
                        {"something": "here"}
                    ]
                }
            },
            "Shedd Aquarium": {
                "available": {}
            },
            "Chicago Botanic Gardens": {
                "available": {
                    "Uptown": [
                        {"something": "here"}
                    ]
                }
            }
        }
        diff = {
            "Chicago Botanic Gardens": {
                "Uptown": 1
            }
        }

        state = State(file)
        result, output = state.has_changes(current)

        self.assertTrue(result)
        self.assertDictEqual(output, diff)

    def test_has_changes_removed_museum_with_availability(self):
        file = 'testfiles/simple_state.json'
        current = {
            "Museum of Science and Industry": {
                "available": {
                    "Merlo": [
                        {"something": "here"}
                    ],
                    "Near North": [
                        {"something": "here"}
                    ]
                }
            },
            "Shedd Aquarium": {
                "available": {}
            }
        }
        diff = {
            "Chicago Children's Museum": {
                "West Loop": -2
            }
        }

        state = State(file)
        result, output = state.has_changes(current)

        self.assertTrue(result)
        self.assertDictEqual(output, diff)

if __name__ == '__main__':
    unittest.main()