目录
=============
[TOC]

##插入

db.someset.insert({"name":"zhang", "age":22})

已转换成BSON >4MB 的文档不能存入数据库，查看文档转成BSON的大小，字节为单位：
Object.bsonsize(doc)



##删除

删除someset集合中的所有文档，但不删除集合本身，原有索引会保留。
db.someset.remove()


删除 mailing.list 集合中所有 "output" 为true
db.mailing.list.remove({"output": true})

删除数据是永久的，无法撤销和恢复。


db.drop_collection("someset")  删除整个集合，索引也被删。


##更新
更新操作是原子的，若两个更新并发，先到达服务器的先执行，然后执行另一个。
update操作有两个参数， 用来找出压迫更新的文档， 修改器modified文档

```
old 
{
	"_id" : ObjectId("55e128da631cab74a0eccc30"),
	"name" : "Bob",
	"friends" : 32,
        "families": 5,
}

new 
{
	"_id" : ObjectId("55e128da631cab74a0eccc30"),
	"username" : "Bob",
        "relationships":
	{
		"friends" : 32,
        	"families": 5,
	}
}
```

```
var bob = db.users.findOne({"name":"bob"});
bob.relationships = {"friends": bob.friends, "families": bob.families};

bob.username = bob.name;
delete bob.friends;
delete bob.families
delete bob.name

db.users.update({"name": "bob"}, bob)
```

如果查询条件匹配了多个文档，而更新的时候，由于modified的 "_id" 值一样，会报错。
数据库会先更改第一个找到的文档，更改第二个发现要更改的_id一样。。。最好通过_id来改。。
除shell外，一般程序是不会报错，除非用getLastError









