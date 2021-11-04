from ShitMountainGenerator.shitter import Shitter

if __name__ == '__main__':
    shitter = Shitter.from_template("test_case.tmpl")
    r = shitter.shit({
            "fields"       : [
                    {
                            "py_name"      : "py_name1",
                            "py_type"      : "py_type1",
                            "py_class_name": "PyClassName1",
                            "json_name"    : "json_name_1",
                            "is_struct"    : True,
                            "is_list"      : False,
                            "name"         : "name1"
                    },
                    {
                            "py_name"      : "py_name2",
                            "py_type"      : "py_type2",
                            "py_class_name": "PyClassName2",
                            "json_name"    : "json_name_2",
                            "is_struct"    : False,
                            "is_list"      : False,
                            "name"         : "name2"
                    },
                    {
                            "py_name"      : "py_name3",
                            "py_type"      : "py_type3",
                            "py_class_name": "PyClassName3",
                            "json_name"    : "json_name_3",
                            "is_list"      : True,
                            "is_struct"    : True,
                            "name"         : "name3"
                    }
            ],
            "py_class_name": "PY_CLASS_NAME"
    })

    print(r)
