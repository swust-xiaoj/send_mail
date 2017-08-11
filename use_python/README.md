## send_mail

### use

`python main.py`

### tips

#### main.conf 配置邮件

```
[common]
smtp_server = smtp.gmail.com
smtp_port = 587
start = 1
step = 3
language = en

[zh]
mail_subject = hello hello
receive_list_file = main.xlsx
mail_content_file = main.html
attachment_file = none

[en]
mail_subject = welcome to python
receive_list_file = main.xlsx
mail_content_file = main.html
attachment_file = this is attachment
```

#### main.html
 
```
     <p>hello <#name#>:</p>
    <p>this mail send by python, use SMTP.</p>
    <p>I'm <#send_name#></p>
```

上面模板中，带有`<#xxx#>`为可替换的锚点，在`main.xlsx`中定义，可为空

#### main.xlsx

```
from_addr |	password |	to_addr |	persontag |	key1 |	key2 |	key3| ...
```

`from_addr`、`password`、 `to_addr`为不可改变的字段，之后的为`html`文件中的锚点

__`main.html main.xlsx`文件名需要与`main.conf` 中名字的配置对应