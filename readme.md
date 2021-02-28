# sql2erd

Small script to generate erd-go code from sql database. Make sure to have [erd-go](https://github.com/kaishuu0123/erd-go) installed in your system.

## Example

```
python main.py --database foobar \
	| erd-go \
	| dot -Tpng -o output.png
```

![](https://raw.githubusercontent.com/mircodezorzi/sql2erd/master/output.png)
