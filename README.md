# 💩Shit Mountain Generator

A general purpose template driven code generator  
Contribute shits to your company's shit mountain more efficiently!

## Quick Start

### Install

`pip3 install shit_mountain_generator`

### vscode Template Language Highlighting

The vscode extension for shit template language highlight support is now on marketplace!
search for `Shit Template Language` in vscode extension tab to install

### Create a generator script

```python
from ShitMountainGenerator import Shitter

shitter = Shitter.from_template(path="/path/to/template.tmpl")
shits = shitter.shit(context={"your": "variable", "loop_contexts": [{"loop": "context"}, {"and": "more"}]})
print(shits)
```

## Writing Templates

Currently, templates has the following supports:

- variable
- loop
- Sub-template
- Condition (Select-Case)

So, we will be starting with the `main` template:

```xml
<tmpl name="$main$">
  your template content
</tmpl>
```

The name attribute can be omitted for the main template

Just relax and use indent to make it look neat. The first indent will be removed when parsing. However, please note that you should only use tab character, AKA `\t`, or 4 spaces to indent since the parser is assuming 4 spaces or a tab as one indent.

Now, maybe we need to replace some parts of the template with variables. So, we are going to use the variable syntax:

```xml
<tmpl name="$main$">
  email = "{{ user_email }}"
</tmpl>
```

`{{ user_email }}` represents the content of the variable `user_email`, which will be replaced later. 

So, we have gone so far that we are able to generate some super simple codes.

Since the complexity of our business logic, we may need to loop over some list and generate corresponding code. And here is when sub-templates and loop operation come in.

Imagine that we are converting some data structure from a language to another, for instance, a go struct, to python data class. And we have the following structure:

```go
type User struct {
  Id       string   `json:"id"`
  Name     string   `json:"name"`
  Password string   `json:"name"`
  Email    string   `json:"email"`
  Friends  []string `json:"friends"`
}
```

The above struct is exported and loaded into a parsing function of python, and we are getting the following result

```python
context = {
  "struct_name": "User",
  "members": [
    {"name": "Id", "py_name": "id", "py_type": "str", "is_list": False},
    {"name": "Name", "py_name": "name", "py_type": "str", "is_list": False},
    {"name": "Password", "py_name": "password", "py_type": "str", "is_list": False},
    {"name": "Email", "py_name": "email", "py_type": "str", "is_list": False},
    {"name": "Friends", "py_name": "friends", "py_type": "List[str]", "is_list": True},
  ]
}
```

As you may noticed that we have mentioned about `context` in the quick-start section above. Right! We are putting this dict into the Shitter so that it shits the correct shit.

Now, we looking at some more complicated stuff. There are list of class members to generate and we apparent don't want to copy and paste these lines. So, we are gonna use the loop operation. But wait! We have got some variant for the "is_list" key! Luckily, we have condition rendering. Let's put these stuff together. And we will have the...

## Complete Template Sample

```xml
<select name="class_member_select" var="is_list">
  <case test="True">
    []
  </case>
  <case test="False">
  	""
  </case>
</select>

<tmpl name="class_member_tmpl">
  {{ name }}: {{ py_type }} = {{ use(class_member_select) }}
</tmpl>

<tmpl name="$main$">
  class {{ struct_name }}:
  	{% class_member_tmpl <- members %}
</tmpl>
```

In the above template, we have two sub-templates, `class_member_tmpl` and the main template and one select statement.

A `select` statement requires a `name` attribute to be referenced later in a template and a `var` attribute to specify which variable we are testing with. Inside the select statement, we can have unlimited numbers of `case` statements and one optional `default` statement. However, only the first matched case will be returned if we have more than one matching cases. 

In the `case` statement, a `test` attribute is required. When comparing the variable and the test value, the test value will be automatically type converted to the target variable type. If a failure accurs while convering, it is assumed unequal.

If none of the specified cases are matched, the generator will go look for the `default` statement and an Exception will be thrown out if no defaults were found.

A `select` statement is referenced using the `use()` function with the `select` statement's name as argument

Sub-templates are used for loops. Use a `{% %}` tag to tell the generator to loop. The left side of the arrow is the sub-template to use and the right side is the context to loop over. The specified context must be an iterable and there must be `Dict[str, Any]` inside the context.

The sub-template is automatically fed with items of the list as context. So just go and use the variables inside that item.

## LICENSE

This project is licenced under The MIT License

Feel free to use it for whatever you are working with
