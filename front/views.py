from django.shortcuts import render
from django.http import HttpResponse
from .models import Book, Author, BookOrder
from django.db.models import Avg, Count, Max, Min, Sum, F, Q
from django.db import connection


# 所有的聚合函数都放在django.db.models中
# 聚合函数不能单独执行 需要放在可执行聚合函数的方法下面中去执行。比如 aggregate 即如下操作

def index(request):
    # 获取所有图书定价的平均价  "price_avg = "是取别名
    result = Book.objects.aggregate(price_avg = Avg("price")) # aggregate 返回的是一个字典 ：{'price__avg': 97.25}

    print(result)
    print(connection.queries)  #[{'sql': 'SELECT @@SQL_AUTO_IS_NULL', 'time': '0.000'}, {'sql': 'SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED', 'time': '0.000'}, {'sql': 'SELECT AVG(`book`.`price`) AS `price__avg` FROM `book`', 'time': '0.000'}]

    return HttpResponse("index")

def index2(request):
    # 获取每一本图书的销售平局价格
    # result = Book.objects.aggregate(avg=Avg("bookorder__price"))
    # print(result)
    # print(connection.queries)

    books = Book.objects.annotate(avg=Avg("bookorder__price"))

    for book in books:
        print("%s/%s" % (book.name, book.avg))  # 三国演义/89.33333333333333 水浒传/93.5 西游记/None 红楼梦/None
    print(connection.queries)
    return HttpResponse("index2")

def index3(requesst):
    # book表中总共有多少本书
    # result = Book.objects.aggregate(book_nums=Count("id"))
    # print(result)
    # print(connection.queries)

    # 统计作者表中有多少个不同的邮箱
    # result = Author.objects.aggregate(email_nums=Count("email", distinct=True))
    # print(result)
    # print(connection.queries)


    # annotate
    # 统计没本书的销量
    books = Book.objects.annotate(book_nums = Count("bookorder__id"))
    print(books)
    for book in books:
        print("%s/%s" % (book.name, book.book_nums))
    print(books.query)  # SELECT `book`.`id`, `book`.`name`, `book`.`pages`, `book`.`price`, `book`.`rating`, `book`.`author_id`, `book`.`publisher_id`, COUNT(`book_order`.`id`) AS `book_nums` FROM `book` LEFT OUTER JOIN `book_order` ON (`book`.`id` = `book_order`.`book_id`) GROUP BY `book`.`id` ORDER BY NULL
    return HttpResponse("index3")

def index4(request):
    # author = Author.objects.aggregate(max=Max("age"), min=Min("age"))
    # print(author)
    # print(connection.queries)

    # 获取每一本图书售卖的最大价格以及最小价格
    books = Book.objects.annotate(max=Max("bookorder__price"), min=Min("bookorder__price"))
    for book in  books:
        print("%s/%s/%s" % (book.name, book.max, book.min))
    print(books.query)
    return HttpResponse("index4")

# sum
def index5(request):
    # 1.求所有图书的销售总额
    # result = BookOrder.objects.aggregate(total = Sum("price"))
    # print(result)
    # print(connection.queries)

    # 2.求每一本图书的销售总额
    # results = Book.objects.annotate(total = Sum("bookorder__price"))
    # for result in results:
    #     print("%s/%s" % (result.name, result.total))
    # print(results.query)

    # 3.求2020年度图书的销售总额
    # 先返回一个QuerySet对象，再实现聚合函数
    # result = BookOrder.objects.filter(create_time__year=2020).aggregate(total=Sum("price"))
    # print(result)
    # print(connection.queries)

    # 4.求每一本图书在2020年的销售总额
    books = Book.objects.filter(bookorder__create_time__year=2020).annotate(total=Sum("bookorder__price"))
    for book in books:
        print("%s/%s" % (book.name, book.total))

    print(connection.queries)


    return HttpResponse("index5")

def index7(request):
    # 1.获取价格大于100并且评分再4.85分以上的图书
    # books = Book.objects.filter(price__gte=90, rating__gte=4.85)
    books = Book.objects.filter((Q(price__gte=90) & Q(rating__gte=4.85)))
    print(books)
    for book in books:
        print("%s %s %s" % (book.name, book.price, book.rating))
    return HttpResponse("index7")

def index8(request):
    return HttpResponse("index8")