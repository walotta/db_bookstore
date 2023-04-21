> ## 要求
>
> 2～3人一组，做好分工，完成下述内容：
>
> 2.在完成前60%功能的基础上，继续实现后40%功能，要有接口、后端逻辑实现、数据库操作、代码测试。对所有接口都要写test case，通过测试并计算测试覆盖率（尽量提高测试覆盖率）。
>
> 3.尽量使用索引，对程序与数据库执行的性能有考量
>
> 4.尽量使用git等版本管理工具
>
> 5.不需要实现界面，只需通过代码测试体现功能与正确性
>
>## 报告内容
> 
>1.每位组员的学号、姓名，以及分工
> 
>3.对60%基础功能和40%附加功能的接口、后端逻辑、数据库操作、测试用例进行介绍，展示测试结果与测试覆盖率。
> 
>4.如果完成，可以展示本次大作业的亮点，比如要求中的“3 4”两点。
> 
>注：验收依据为报告，本次大作业所作的工作要完整展示在报告中。
> 
>
> ## 验收与考核准测
>
>- 提交 **代码+报告** 压缩包到 **作业提交入口**
> - 命名规则：2023_SJTU_PJ1_第几组(.zip)
>- 提交截止日期：**2023.4.22 23:59**
> 
> 考核标准：
> 
>1. 没有提交或没有实质的工作，得D
> 2. 完成"要求"中的第点，可得C
>3. 完成前3点，通过全部测试用例且有较高的测试覆盖率，可得B
> 4. 完成前2点的基础上，体现出第3 4点，可得A
> 5. 以上均为参考，最后等级会根据最终的工作质量有所调整

// TODO: remove above

# Bookstore Homework Report

> Group number: **2**
>
> GitHub Repo Links: [db_homework](https://github.com/walotta/db_bookstore)

## Team members

| Name          | Student number | GitHub Link                                   | Detail of the division of labor                              |
| ------------- | -------------- | --------------------------------------------- | ------------------------------------------------------------ |
| Nanyang Lin   | 520070910040   | [Fourest-lyn](https://github.com/Fourest-lyn) | add the test case, code, design implementation of API interface, doc of book searching API |
| Tian Xia      | 520030910315   | [cblmemo](https://github.com/cblmemo)         | add the test case, code,  design implementation of API interface, doc of book delivering and receiving  API, order querying  and canceling API |
| Zhongjing Wei | 520030910142   | [walotta](https://github.com/walotta)         | Modify database from SQLite to MongoDB (including coding and the design of database), add abstract API of the database call |

## Database design

| Collections | Documents                         | Document design reasons                                      | Index                        | Index design reasons                                         |
| ----------- | --------------------------------- | ------------------------------------------------------------ | ---------------------------- | ------------------------------------------------------------ |
| user        | [jump to detail](#document_user)  | Use to store the information of each user, store the index of order because of the need of getting the user's past order list | user_id                      | all the query is seeking the specific user_id's information  |
| store       | [jump to detail](#document_store) | Because the information of books belongs to the store they are sold by, the information of books is stored as a list belongs to the store. Because the limit size of each document is 16M and the need to search the book's information globally, book_info's storage uses a single collection and leave the id generated by MongoDB in the store's list of book. | (store_id,book_list.book_id) | the query is based on store_id or both store_id and book_id, so the composite index can accelerate these two kinds of query |
| book_info   | [jump to detail](#document_info)  | Just store the basic information of books                    | tags (not unique)            | because the most time-consuming task is tags matching searching, so the index of tags can accelerate this |
| new_order   | [jump to detail](#document_order) | Just store the needed information of orders                  | order_id                     | all the query is seeking the specific order_id's information |

### document structure

#### <a name="document_user">user</a>

```toml
[user]
user_id = str	# is unique
password = str
balance = int
token = str
terminal = str
order_id_list = list[str]
```

#### <a name="document_store">store</a>

```toml
[store]
store_id = str	# is unique
user_id = str		# used to record seller_id of the store

[[store.book_list]]
book_id = str
stock_level = int
book_info_id = str
```

#### <a name="document_info">book_info</a>

```toml
[book_info]
_id = mongo_id	# is unique
book_id = str
store_id = str
title = str
author = str
publisher = str
original_title = str
translator = str
pub_year = str
pages = int
price = int
currency_unit = int
binding = str
isbn = str
author_intro = str
book_intro = str
content = str
tags = List[str]
pictures = List[str]
```

#### <a name="document_order">new_order</a>

```toml
[new_order]
order_id = str	# is unique
user_id = str
store_id = str
create_time = int
status = [INIT, PAID, SHIPPED, RECEIVED, CANCELED]	# use int as enum

[[new_order.book_item]]
book_id = str
count = int
price = int
```

## Added API

### API description

[jump to ship order detail](doc/seller.md#商家发货)

[jump to receive order detail](doc/buyer.md#买家收货)

[jump to query order detail](doc/buyer.md#买家查询订单)

[jump to query order id list detail](doc/buyer.md#买家查询所有订单编号)

[jump to cancel order detail](doc/buyer.md#买家取消订单)

[jump to auto cancel expired order detail](doc/seller.md#自动取消所有超时订单)

### Backend logic implementation

#### ship / receive order

Add a `STATUS` for each order, and update the `STATUS` when the order is shipped or received. We still subtract stock level when the order is created, since the stock level represent all current availabe books. When an order is cancelled, its stock level are added back.

#### query order (id list)

Directly query through database.

#### cancel order

For manually cancel, just update the `STATUS` of the order to `CANCELED`. Notice only unpaid order (thus unshipped, unreceived and uncanceled) can be canceled.

For auto cancel, we provide an API to auto remove all expired order. Expiration time and current time are required by this API. Users are expected to launch a daemon to call this API each `expiration_time`. For example, if `expiration_time` is 1 hour, then the daemon should be launched every 1 hour.

### database operation design

// TODO

### Test case design

// TODO

## Collaborate with GitHub

collaborate with GitHub

* Collaborate with the GitHub repo: [db_homework](https://github.com/walotta/db_bookstore)
* Use **Pull requests** to merge code from different collaborators, see [here](https://github.com/walotta/db_bookstore/pulls)
* Use **Issus** to discuss the problems which are hard to decide, see [here](https://github.com/walotta/db_bookstore/issues)
* Use **GitHub Action** to auto-check the `Code Format` of the code by `black`, the `Type check` of code by `mypy`, and the `correctness` of the code by `pytest`, see the [GitHub action config](https://github.com/walotta/db_bookstore/tree/master/.github/workflows) and [action detail](https://github.com/walotta/db_bookstore/actions)
* Use **Branch** to make it possible for each collaborator can write and contribute code independently

## Test case coverage

// TODO: after lyn finishes his part, add the coverage


