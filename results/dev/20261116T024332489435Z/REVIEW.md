# Xem lại 51 lượt dev

Nhãn chất lượng chưa chấm. Đây là đầu ra model thật; không phải đáp án chuẩn chỉ vì có citation. Các lỗi vẫn giữ phản hồi gốc để đọc.

## dense

### D01 — answered

Muốn viết đường dẫn Windows mà các ký tự như \n và \t không bị hiểu là xuống dòng hoặc tab, tiền tố chuỗi nào được tài liệu hướng dẫn?

**Đáp án mong đợi:** Đặt tiền tố r trước dấu nháy để tạo raw string.

**Đầu ra:**
Tài liệu hướng dẫn dùng tiền tố r để tạo raw string, đặt trước dấu nháy đầu tiên, nhờ đó các ký tự sau dấu \ không bị hiểu là ký tự đặc biệt (ví dụ \t là tab, \n là xuống dòng). Ví dụ: print(r'C:\this\name') in ra C:\this\name. Lưu ý: raw string không thể kết thúc bằng số lẻ ký tự \ [5046e99636180b57c2960fedf1d3566c].

**Query tìm tài liệu:**
- `raw string prefix backslash Windows path not escape newline tab`
- `string literals raw strings r prefix escape sequences`

**Context cuối:**
```text
[5046e99636180b57c2960fedf1d3566c | https://docs.python.org/3.14/tutorial/introduction.html | page python-3.14-ch03-u003]
If you don’t want characters prefaced by \ to be interpreted as special characters, you can use raw strings by adding an r before the first quote:

>>> print('C:\this\name')  # here \t means tab, \n means newline
C:      his
ame
>>> print(r'C:\this\name')  # note the r before the quote
C:\this\name

There is one subtle aspect to raw strings: a raw string may not end in an odd number of \ characters; see the FAQ entry for more information and workarounds.
```

### D02 — answered

Khi đánh chỉ số chuỗi từ phía cuối, -1 và -2 chỉ ký tự nào? Vì sao không bắt đầu bằng -0?

**Đáp án mong đợi:** -1 chỉ ký tự cuối, -2 chỉ ký tự áp cuối; -0 bằng 0 nên chỉ số âm bắt đầu từ -1.

**Đầu ra:**
Theo tài liệu, với chuỗi 'Python' (word), word[-1] là ký tự cuối cùng ('n') và word[-2] là ký tự áp chót ('o'); tài liệu cũng lưu ý rằng vì -0 giống hệt 0 nên các chỉ số âm bắt đầu từ -1 [07eab24fdef0d6f3c82bb56fb67407ce].

**Query tìm tài liệu:**
- `negative indices string -1 -2 last character why not -0`
- `indexing strings from the end negative index`

**Context cuối:**
```text
[07eab24fdef0d6f3c82bb56fb67407ce | https://docs.python.org/3.14/tutorial/introduction.html | page python-3.14-ch03-u004]
>>> word[-1]  # last character
'n'
>>> word[-2]  # second-last character
'o'
>>> word[-6]
'P'

Note that since -0 is the same as 0, negative indices start from -1.

In addition to indexing, slicing is also supported. While indexing is used to obtain individual characters, slicing allows you to obtain a substring:

>>> word[0:2]  # characters from position 0 (included) to 2 (excluded)
'Py'
>>> word[2:5]  # characters from position 2 (included) to 5 (excluded)
'tho'
```

### D03 — answered

Ví dụ list(range(5, 10)) trong tài liệu cho ra danh sách nào?

**Đáp án mong đợi:** [5, 6, 7, 8, 9]; cận 10 không được lấy.

**Đầu ra:**
Theo tài liệu, `list(range(5, 10))` cho ra `[5, 6, 7, 8, 9]` [5b0389b2014ead261047a7ea77039951].

**Query tìm tài liệu:**
- `list(range(5, 10)) example output`
- `range function arguments start stop step examples`

**Context cuối:**
```text
[5b0389b2014ead261047a7ea77039951 | https://docs.python.org/3.14/tutorial/controlflow.html | page python-3.14-ch04-u002]
>>> list(range(5, 10))
[5, 6, 7, 8, 9]

>>> list(range(0, 10, 3))
[0, 3, 6, 9]

>>> list(range(-10, -100, -30))
[-10, -40, -70]

To iterate over the indices of a sequence, you can combine range() and len() as follows:

>>> a = ['Mary', 'had', 'a', 'little', 'lamb']
>>> for i in range(len(a)):
...     print(i, a[i])
...
0 Mary
1 had
2 a
3 little
4 lamb

In most such cases, however, it is convenient to use the enumerate() function, see Looping Techniques.
```

### D04 — abstain

Nếu có vòng lặp for lồng trong while, break nằm trong for sẽ thoát vòng nào theo quy tắc của tài liệu?

**Đáp án mong đợi:** Thoát vòng for ở trong cùng bao quanh break, không tự động thoát cả vòng while bên ngoài.

**Đầu ra:**
Không đủ bằng chứng trong tài liệu để trả lời: context hiện có chỉ nói về else clause của vòng lặp và break, không nêu quy tắc break trong for lồng trong while sẽ thoát vòng nào [e09df3f01953e055de669d3402d7ddac].

**Query tìm tài liệu:**
- `break statement in nested for loop inside while loop which loop does it exit`
- `break statement terminates innermost enclosing for or while loop`
- `break statement breaks out of the innermost enclosing loop`

**Context cuối:**
```text
[e09df3f01953e055de669d3402d7ddac | https://docs.python.org/3.14/tutorial/controlflow.html | page python-3.14-ch04-u002]
4.5. else Clauses on Loops

In a for or while loop the break statement may be paired with an else clause. If the loop finishes without executing the break, the else clause executes.

In a for loop, the else clause is executed after the loop finishes its final iteration, that is, if no break occurred.

In a while loop, it’s executed after the loop’s condition becomes false.
```

### D05 — answered

Các đối số bổ sung được gom bởi *args trong định nghĩa hàm có kiểu cấu trúc dữ liệu gì?

**Đáp án mong đợi:** Một tuple chứa các đối số vị trí bổ sung.

**Đầu ra:**
Theo tài liệu, các đối số bổ sung được gom bởi *args sẽ được "wrapped up in a tuple" — tức là gói lại trong một tuple (xem mục Tuples and Sequences) [72ba98c7f88046b6519961423f685ff5].

**Query tìm tài liệu:**
- `*args arbitrary arguments tuple function definition`
- `arbitrary argument list packed into tuple keyword arguments dictionary`

**Context cuối:**
```text
[72ba98c7f88046b6519961423f685ff5 | https://docs.python.org/3.14/tutorial/controlflow.html | page python-3.14-ch04-u012]
4.9.4. Arbitrary Argument Lists

Finally, the least frequently used option is to specify that a function can be called with an arbitrary number of arguments. These arguments will be wrapped up in a tuple (see Tuples and Sequences). Before the variable number of arguments, zero or more normal arguments may occur.

def write_multiple_items(file, separator, *args):
    file.write(separator.join(args))
```

### D06 — answered

Tham số **name nhận những đối số nào và lưu trong kiểu dữ liệu gì?

**Đáp án mong đợi:** Nhận các keyword arguments không ứng với tham số hình thức đã khai báo và lưu thành dictionary.

**Đầu ra:**
Tham số cuối dạng **name nhận một dictionary (kiểu dict) chứa tất cả các keyword argument, trừ những đối số tương ứng với một tham số hình thức (formal parameter) đã có; nó có thể kết hợp với tham số dạng *name (nhận tuple các đối số vị trí vượt quá danh sách tham số hình thức), và *name phải đứng trước **name [a406cc7dac32b6727ecb688a6d3b9286].

**Query tìm tài liệu:**
- `keyword argument name string type`
- `**name parameter accepts what arguments stored as what type`

**Context cuối:**
```text
[a406cc7dac32b6727ecb688a6d3b9286 | https://docs.python.org/3.14/tutorial/controlflow.html | page python-3.14-ch04-u009]
When a final formal parameter of the form **name is present, it receives a dictionary (see Mapping Types — dict) containing all keyword arguments except for those corresponding to a formal parameter. This may be combined with a formal parameter of the form *name (described in the next subsection) which receives a tuple containing the positional arguments beyond the formal parameter list. (*name must occur before **name.) For example, if we define a function like this:
```

### D07 — error

Muốn tạo tuple chỉ chứa chuỗi hello thì chỉ viết ngoặc quanh giá trị có đủ không? Cú pháp cần thêm gì?

**Đáp án mong đợi:** Không đủ; phải có dấu phẩy sau giá trị, ví dụ ('hello',) hoặc 'hello',.

**Đầu ra:**
(không có câu trả lời được chấp nhận)

**Phản hồi model cuối — không được runner chấp nhận:**
```json
{"answer":"Không đủ bằng chứng trong tài liệu để trả lời câu hỏi này: context hiện có chỉ nêu định nghĩa chung rằng tuple gồm các giá trị phân tách bằng dấu phẩy và ví dụ về tuple nhiều phần tử, không đề cập trường hợp tuple một phần tử hay việc có cần thêm dấu phẩy sau giá trị khi đặt trong ngoặc hay không [251bd803e4ae5442e342a474a44971ae].","citations":["251bd803e4ae5442e342a474a44971ae"],"abstain":true}
```

**Query tìm tài liệu:**
- `tuple with one item single element trailing comma`
- `tuples parentheses special case singleton`
- `constructing tuple containing one item empty tuple parentheses`

**Context cuối:**
```text
[178fb9b1e55df551dfbf80471cced12a | https://docs.python.org/3.14/tutorial/datastructures.html | page python-3.14-ch05-u005]
>>> t = 12345, 54321, 'hello!'
>>> t[0]
12345
>>> t
(12345, 54321, 'hello!')
>>> # Tuples may be nested:
>>> u = t, (1, 2, 3, 4, 5)
>>> u
((12345, 54321, 'hello!'), (1, 2, 3, 4, 5))
>>> # Tuples are immutable:
>>> t[0] = 88888
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: 'tuple' object does not support item assignment
>>> # but they can contain mutable objects:
>>> v = ([1, 2, 3], [3, 2, 1])
>>> v
([1, 2, 3], [3, 2, 1])

[251bd803e4ae5442e342a474a44971ae | https://docs.python.org/3.14/tutorial/datastructures.html | page python-3.14-ch05-u005]
A tuple consists of a number of values separated by commas, for instance:
```

### D08 — answered

a.pop() không truyền index sẽ xóa và trả về phần tử nào? Điều gì xảy ra nếu a rỗng?

**Đáp án mong đợi:** Xóa và trả về phần tử cuối; nếu list rỗng thì phát sinh IndexError.

**Đầu ra:**
a.pop() không truyền index sẽ xóa và trả về phần tử cuối cùng của list. Nếu list rỗng (hoặc index nằm ngoài phạm vi list), nó sẽ ném ra IndexError [e4976e7c8c03d1c6a37a18f46e14e9dd].

**Query tìm tài liệu:**
- `list.pop() remove and return last item empty list IndexError`
- `pop method list data structures`

**Context cuối:**
```text
[e4976e7c8c03d1c6a37a18f46e14e9dd | https://docs.python.org/3.14/tutorial/datastructures.html | page python-3.14-ch05-u001]
Remove the item at the given position in the list, and return it. If no index is specified, a.pop() removes and returns the last item in the list. It raises an IndexError if the list is empty or the index is outside the list range.

list.clear()

Remove all items from the list. Similar to del a[:].

list.index(value[, start[, stop]])

Return zero-based index of the first occurrence of value in the list. Raises a ValueError if there is no such item.
```

### D09 — answered

Khi duyệt dictionary, dùng phương thức nào để lấy đồng thời khóa và giá trị tương ứng?

**Đáp án mong đợi:** Dùng phương thức items(), ví dụ for k, v in d.items().

**Đầu ra:**
Dùng phương thức items(): khi lặp qua dictionary, khóa và giá trị tương ứng có thể được lấy đồng thời bằng items(), ví dụ `for k, v in knights.items():` [fa52d5bbb11517433573b8febe0a1876].

**Query tìm tài liệu:**
- `looping techniques dictionary items method key and value`
- `dictionary items() iterate keys and values simultaneously`

**Context cuối:**
```text
[fa52d5bbb11517433573b8febe0a1876 | https://docs.python.org/3.14/tutorial/datastructures.html | page python-3.14-ch05-u007]
5.6. Looping Techniques

When looping through dictionaries, the key and corresponding value can be retrieved at the same time using the items() method.

>>> knights = {'gallahad': 'the pure', 'robin': 'the brave'}
>>> for k, v in knights.items():
...     print(k, v)
...
gallahad the pure
robin the brave

When looping through a sequence, the position index and corresponding value can be retrieved at the same time using the enumerate() function.
```

### D10 — answered

Có hai sequence cần duyệt đồng thời thành từng cặp phần tử tương ứng. Tài liệu giới thiệu hàm nào?

**Đáp án mong đợi:** Dùng zip() để ghép các phần tử tương ứng khi duyệt hai hoặc nhiều sequence.

**Đầu ra:**
Tài liệu giới thiệu hàm zip(). Để duyệt hai hoặc nhiều sequence cùng lúc, các phần tử có thể được ghép cặp bằng hàm zip(), ví dụ: for q, a in zip(questions, answers): ... [d0465c0ebf1bcc71b35de11057f991e9]

**Query tìm tài liệu:**
- `loop over two sequences simultaneously pairs of elements zip`
- `zip function iterate two lists at the same time`

**Context cuối:**
```text
[d0465c0ebf1bcc71b35de11057f991e9 | https://docs.python.org/3.14/tutorial/datastructures.html | page python-3.14-ch05-u008]
To loop over two or more sequences at the same time, the entries can be paired with the zip() function.

>>> questions = ['name', 'quest', 'favorite color']
>>> answers = ['lancelot', 'the holy grail', 'blue']
>>> for q, a in zip(questions, answers):
...     print('What is your {0}?  It is {1}.'.format(q, a))
...
What is your name?  It is lancelot.
What is your quest?  It is the holy grail.
What is your favorite color?  It is blue.
```

### D11 — answered

dir() không truyền đối số liệt kê những tên nào? Nó có tự liệt kê tên hàm và biến built-in không?

**Đáp án mong đợi:** Liệt kê các tên đang được định nghĩa như biến, module và hàm; không liệt kê các tên hàm và biến built-in.

**Đầu ra:**
Khi không truyền đối số, dir() liệt kê các tên bạn đã định nghĩa hiện tại (mọi loại tên: biến, module, hàm, v.v.), ví dụ ['__builtins__', '__name__', 'a', 'fib', 'fibo', 'sys'] [653c279748bae8969296f00bc2941191]. Tuy nhiên dir() KHÔNG liệt kê tên của các hàm và biến built-in; muốn có danh sách đó thì chúng được định nghĩa trong module chuẩn builtins [653c279748bae8969296f00bc2941191].

**Query tìm tài liệu:**
- `dir() without arguments list names built-in functions variables`
- `built-in function dir returns sorted list of names in current local scope`

**Context cuối:**
```text
[653c279748bae8969296f00bc2941191 | https://docs.python.org/3.14/tutorial/modules.html | page python-3.14-ch06-u005]
Without arguments, dir() lists the names you have defined currently:

>>> a = [1, 2, 3, 4, 5]
>>> import fibo
>>> fib = fibo.fib
>>> dir()
['__builtins__', '__name__', 'a', 'fib', 'fibo', 'sys']

Note that it lists all types of names: variables, modules, functions, etc.

dir() does not list the names of built-in functions and variables. If you want a list of those, they are defined in the standard module builtins:

[6fab6ff982d8770e87310f8101a2f523 | https://docs.python.org/3.14/tutorial/modules.html | page python-3.14-ch06-u005]
6.3. The dir() Function

The built-in function dir() is used to find out which names a module defines. It returns a sorted list of strings:
```

### D12 — answered

Python dựa vào thông tin nào của file nguồn để quyết định module đã biên dịch có lỗi thời và cần biên dịch lại?

**Đáp án mong đợi:** So sánh ngày/giờ sửa đổi của mã nguồn với phiên bản đã biên dịch.

**Đầu ra:**
Python kiểm tra ngày sửa đổi (modification date) của file nguồn so với phiên bản đã biên dịch để xem module đã biên dịch có lỗi thời và cần biên dịch lại hay không; đây là quá trình hoàn toàn tự động [4b9311d6dabb880f0d9037d258d191b8].

**Query tìm tài liệu:**
- `compiled module out of date recompile source file timestamp`
- `bytecode cache invalidation source mtime size`

**Context cuối:**
```text
[4b9311d6dabb880f0d9037d258d191b8 | https://docs.python.org/3.14/tutorial/modules.html | page python-3.14-ch06-u004]
Python checks the modification date of the source against the compiled version to see if it’s out of date and needs to be recompiled. This is a completely automatic process. Also, the compiled modules are platform-independent, so the same library can be shared among systems with different architectures.
```

### D13 — answered

Với file vừa mở để đọc và đang ở đầu file, bỏ size hoặc truyền size âm cho f.read(size) sẽ đọc bao nhiêu? Rủi ro bộ nhớ được tài liệu nhắc là gì?

**Đáp án mong đợi:** Đọc toàn bộ nội dung file; file quá lớn có thể vượt bộ nhớ máy.

**Đầu ra:**
Khi bỏ size hoặc truyền size âm cho f.read(size), toàn bộ nội dung file sẽ được đọc và trả về (chuỗi ở text mode, bytes ở binary mode) [b2e4e2a1efb032538c84a9e87be3cfb4]. Rủi ro bộ nhớ mà tài liệu nhắc là: "it's your problem if the file is twice as large as your machine's memory" — tức nếu file lớn gấp đôi bộ nhớ máy thì đó là vấn đề của bạn [b2e4e2a1efb032538c84a9e87be3cfb4].

**Query tìm tài liệu:**
- `f.read(size) omit size or negative size read entire file memory risk`
- `reading and writing files read size omitted negative reads whole file`

**Context cuối:**
```text
[b2e4e2a1efb032538c84a9e87be3cfb4 | https://docs.python.org/3.14/tutorial/inputoutput.html | page python-3.14-ch07-u005]
To read a file’s contents, call f.read(size), which reads some quantity of data and returns it as a string (in text mode) or bytes object (in binary mode). size is an optional numeric argument. When size is omitted or negative, the entire contents of the file will be read and returned; it’s your problem if the file is twice as large as your machine’s memory. Otherwise, at most size characters (in text mode) or size bytes (in binary mode) are read and returned. If the end of the file has been 
```

### D14 — answered

Giá trị f.tell() trong binary mode và text mode có ý nghĩa khác nhau thế nào?

**Đáp án mong đợi:** Binary mode: số byte tính từ đầu file. Text mode: một số opaque biểu diễn vị trí, không nên hiểu là số byte.

**Đầu ra:**
Trong binary mode, f.tell() trả về một số nguyên là vị trí hiện tại của file object, được biểu diễn bằng số byte tính từ đầu file. Trong text mode, f.tell() trả về một "opaque number" (con số không minh bạch về ý nghĩa byte) [9c4ec9a68dac484801d37366b0214e51]. Liên quan đến điều này, với text file (mở không có 'b' trong chuỗi mode), chỉ cho phép seek tương đối so với đầu file (ngoại lệ là seek tới cuối file với seek(0, 2)), và các giá trị offset hợp lệ duy nhất là những giá trị do f.tell() trả về, hoặc 0; mọi offset khác gây ra hành vi không xác định [dbb1c2a57f3bdb25359e5a45739375d9].

**Query tìm tài liệu:**
- `f.tell() binary mode text mode opaque number`
- `tell() text files return opaque number byte position`

**Context cuối:**
```text
[9c4ec9a68dac484801d37366b0214e51 | https://docs.python.org/3.14/tutorial/inputoutput.html | page python-3.14-ch07-u006]
f.tell() returns an integer giving the file object’s current position in the file represented as number of bytes from the beginning of the file when in binary mode and an opaque number when in text mode.

[dbb1c2a57f3bdb25359e5a45739375d9 | https://docs.python.org/3.14/tutorial/inputoutput.html | page python-3.14-ch07-u006]
In text files (those opened without a b in the mode string), only seeks relative to the beginning of the file are allowed (the exception being seeking to the very file end with seek(0, 2)) and the only valid offset values are those returned from the f.tell(), or zero. Any other offset value produces undefined behaviour.
```

### D15 — answered

Trong try...except, khối else phải đặt sau phần nào và được dùng khi nào?

**Đáp án mong đợi:** Đặt sau tất cả các except; dùng cho code chỉ chạy khi khối try không phát sinh ngoại lệ.

**Đầu ra:**
Khối else là tùy chọn của câu lệnh try … except; khi có mặt, nó phải đặt sau tất cả các khối except. Nó hữu ích cho đoạn mã phải được thực thi nếu khối try không ném ra ngoại lệ (tức là chạy khi không có ngoại lệ xảy ra) [89cb0b58f013c40c3ef13c336fcb8792].

**Query tìm tài liệu:**
- `try except else clause must follow which clause and when is it executed`
- `try statement else clause executed if no exception occurs`

**Context cuối:**
```text
[89cb0b58f013c40c3ef13c336fcb8792 | https://docs.python.org/3.14/tutorial/errors.html | page python-3.14-ch08-u003]
The try … except statement has an optional else clause, which, when present, must follow all except clauses. It is useful for code that must be executed if the try clause does not raise an exception. For example:

[e029e5d8abe70414636c4b8d53ae1e44 | https://docs.python.org/3.14/tutorial/controlflow.html | page python-3.14-ch04-u003]
When used with a loop, the else clause has more in common with the else clause of a try statement than it does with that of if statements: a try statement’s else clause runs when no exception occurs, and a loop’s else clause runs when no break occurs. For more on the try statement and exceptions, see Handling Exceptions.
```

### D16 — abstain

Chỉ dựa trên tài liệu đã cung cấp, khi một task trong asyncio.TaskGroup lỗi, các task còn lại được hủy và chờ kết thúc như thế nào?

**Thiếu bằng chứng trong corpus:** Corpus không có phần giải thích asyncio hoặc TaskGroup. Các mục vòng lặp/ngoại lệ không quy định ngữ nghĩa hủy task bất đồng bộ.

**Đầu ra:**
Không đủ bằng chứng trong tài liệu để trả lời: context hiện tại chỉ chứa danh sách tên ngoại lệ/hàm tích hợp của Python, không có nội dung nào về asyncio.TaskGroup hay cách hủy và chờ các task còn lại khi một task lỗi.

**Query tìm tài liệu:**
- `asyncio TaskGroup one task fails cancel remaining tasks wait for them to finish`
- `TaskGroup exception handling cancel sibling tasks ExceptionGroup`
- `asyncio TaskGroup tasks cancelled when one raises exception`

**Context cuối:**
```text
[f56f1b83badcd52d685382d45a8001a6 | https://docs.python.org/3.14/tutorial/modules.html | page python-3.14-ch06-u006]
 'StopIteration', 'SyntaxError', 'SyntaxWarning', 'SystemError',
 'SystemExit', 'TabError', 'TimeoutError', 'True', 'TypeError',
 'UnboundLocalError', 'UnicodeDecodeError', 'UnicodeEncodeError',
 'UnicodeError', 'UnicodeTranslateError', 'UnicodeWarning', 'UserWarning',
 'ValueError', 'Warning', 'ZeroDivisionError', '_', '__build_class__',
 '__debug__', '__doc__', '__import__', '__name__', '__package__', 'abs',
 'all', 'any', 'ascii', 'bin', 'bool', 'bytearray', 'bytes', 'callable',

```

### D17 — abstain

Tài liệu đã cung cấp hướng dẫn dùng @dataclass(frozen=True) để ngăn gán lại thuộc tính như thế nào và phát sinh ngoại lệ gì khi cố gán?

**Thiếu bằng chứng trong corpus:** dataclasses chỉ được nhắc làm ví dụ lớp có thứ tự thuộc tính trong match; frozen xuất hiện trong tên built-in frozenset. Không có hướng dẫn frozen=True hoặc ngoại lệ khi gán.

**Đầu ra:**
Không đủ bằng chứng trong tài liệu để trả lời: ngữ cảnh hiện có chỉ nói về xử lý ngoại lệ/chaining trong tutorial errors, không có nội dung về @dataclass(frozen=True) hay ngoại lệ khi cố gán lại thuộc tính.

**Query tìm tài liệu:**
- `dataclass frozen=True prevent assignment attribute raises exception`
- `frozen dataclass FrozenInstanceError cannot assign to field`
- `dataclasses frozen instance immutable fields`

**Context cuối:**
```text
[22301843e855f993ff0daa2a245506d0 | https://docs.python.org/3.14/tutorial/errors.html | page python-3.14-ch08-u005]
    raise RuntimeError('Failed to open database') from exc
RuntimeError: Failed to open database

[ff3919a7aecf66d4113ecfab1a1fe6b0 | https://docs.python.org/3.14/tutorial/errors.html | page python-3.14-ch08-u005]
It also allows disabling automatic exception chaining using the from None idiom:

>>> try:
...     open('database.sqlite')
... except OSError:
...     raise RuntimeError from None
...
Traceback (most recent call last):
  File "<stdin>", line 4, in <module>
    raise RuntimeError from None
RuntimeError

For more information about chaining mechanics, see Built-in Exceptions.
```

## tfidf

### D01 — answered

Muốn viết đường dẫn Windows mà các ký tự như \n và \t không bị hiểu là xuống dòng hoặc tab, tiền tố chuỗi nào được tài liệu hướng dẫn?

**Đáp án mong đợi:** Đặt tiền tố r trước dấu nháy để tạo raw string.

**Đầu ra:**
Tài liệu hướng dẫn dùng tiền tố r (raw string) trước dấu nháy đầu tiên, ví dụ r'C:\this\name', để các ký tự sau \ không bị hiểu là ký tự đặc biệt như \t (tab) hay \n (xuống dòng) [5046e99636180b57c2960fedf1d3566c]. Lưu ý: raw string không thể kết thúc bằng số lẻ ký tự \ [5046e99636180b57c2960fedf1d3566c].

**Query tìm tài liệu:**
- `raw string prefix backslash not escape newline tab Windows path`
- `string literal prefixes r raw strings escape sequences`

**Context cuối:**
```text
[5046e99636180b57c2960fedf1d3566c | https://docs.python.org/3.14/tutorial/introduction.html | page python-3.14-ch03-u003]
If you don’t want characters prefaced by \ to be interpreted as special characters, you can use raw strings by adding an r before the first quote:

>>> print('C:\this\name')  # here \t means tab, \n means newline
C:      his
ame
>>> print(r'C:\this\name')  # note the r before the quote
C:\this\name

There is one subtle aspect to raw strings: a raw string may not end in an odd number of \ characters; see the FAQ entry for more information and workarounds.
```

### D02 — answered

Khi đánh chỉ số chuỗi từ phía cuối, -1 và -2 chỉ ký tự nào? Vì sao không bắt đầu bằng -0?

**Đáp án mong đợi:** -1 chỉ ký tự cuối, -2 chỉ ký tự áp cuối; -0 bằng 0 nên chỉ số âm bắt đầu từ -1.

**Đầu ra:**
Theo tài liệu, với chuỗi 'Python' (word), word[-1] là ký tự cuối cùng ('n') và word[-2] là ký tự áp chót ('o'). Tài liệu giải thích rằng vì -0 giống hệt 0, nên các chỉ số âm bắt đầu từ -1 [07eab24fdef0d6f3c82bb56fb67407ce].

**Query tìm tài liệu:**
- `string indexing negative indices -1 -2 last character why not -0`
- `negative index counts from the right end of string`

**Context cuối:**
```text
[07eab24fdef0d6f3c82bb56fb67407ce | https://docs.python.org/3.14/tutorial/introduction.html | page python-3.14-ch03-u004]
>>> word[-1]  # last character
'n'
>>> word[-2]  # second-last character
'o'
>>> word[-6]
'P'

Note that since -0 is the same as 0, negative indices start from -1.

In addition to indexing, slicing is also supported. While indexing is used to obtain individual characters, slicing allows you to obtain a substring:

>>> word[0:2]  # characters from position 0 (included) to 2 (excluded)
'Py'
>>> word[2:5]  # characters from position 2 (included) to 5 (excluded)
'tho'
```

### D03 — answered

Ví dụ list(range(5, 10)) trong tài liệu cho ra danh sách nào?

**Đáp án mong đợi:** [5, 6, 7, 8, 9]; cận 10 không được lấy.

**Đầu ra:**
Trong tài liệu, ví dụ `list(range(5, 10))` cho ra danh sách `[5, 6, 7, 8, 9]` [5b0389b2014ead261047a7ea77039951].

**Query tìm tài liệu:**
- `list(range(5, 10)) example output`
- `range function arguments start stop step examples`

**Context cuối:**
```text
[5b0389b2014ead261047a7ea77039951 | https://docs.python.org/3.14/tutorial/controlflow.html | page python-3.14-ch04-u002]
>>> list(range(5, 10))
[5, 6, 7, 8, 9]

>>> list(range(0, 10, 3))
[0, 3, 6, 9]

>>> list(range(-10, -100, -30))
[-10, -40, -70]

To iterate over the indices of a sequence, you can combine range() and len() as follows:

>>> a = ['Mary', 'had', 'a', 'little', 'lamb']
>>> for i in range(len(a)):
...     print(i, a[i])
...
0 Mary
1 had
2 a
3 little
4 lamb

In most such cases, however, it is convenient to use the enumerate() function, see Looping Techniques.

[f06c308a2755b1e4528c19472880db2d | https://docs.python.org/3.14/tutorial/inputoutput.html | page python-3.14-ch07-u002]
Some examples:
```

### D04 — error

Nếu có vòng lặp for lồng trong while, break nằm trong for sẽ thoát vòng nào theo quy tắc của tài liệu?

**Đáp án mong đợi:** Thoát vòng for ở trong cùng bao quanh break, không tự động thoát cả vòng while bên ngoài.

**Đầu ra:**
(không có câu trả lời được chấp nhận)

**Phản hồi model cuối — không được runner chấp nhận:**
```json
{"answer":"Không đủ bằng chứng trong tài liệu để trả lời: context hiện có chỉ nói về else clause đi kèm break trong vòng lặp for/while, không nêu quy tắc break trong for lồng trong while sẽ thoát vòng nào [e09df3f01953e055de669d3402d7ddac].","citations":["e09df3f01953e055de669d3402d7ddac"],"abstain":true}
```

**Query tìm tài liệu:**
- `break statement in nested for loop inside while loop which loop does it exit`
- `break statement terminates innermost enclosing for or while loop`
- `break statement breaks out of the innermost enclosing loop`

**Context cuối:**
```text
[e09df3f01953e055de669d3402d7ddac | https://docs.python.org/3.14/tutorial/controlflow.html | page python-3.14-ch04-u002]
4.5. else Clauses on Loops

In a for or while loop the break statement may be paired with an else clause. If the loop finishes without executing the break, the else clause executes.

In a for loop, the else clause is executed after the loop finishes its final iteration, that is, if no break occurred.

In a while loop, it’s executed after the loop’s condition becomes false.
```

### D05 — answered

Các đối số bổ sung được gom bởi *args trong định nghĩa hàm có kiểu cấu trúc dữ liệu gì?

**Đáp án mong đợi:** Một tuple chứa các đối số vị trí bổ sung.

**Đầu ra:**
Các đối số bổ sung được gom bởi *args sẽ được đóng gói (wrapped up) trong một tuple [72ba98c7f88046b6519961423f685ff5].

**Query tìm tài liệu:**
- `*args arbitrary argument list tuple function definition`
- `arbitrary arguments packed into a tuple keyword arguments dictionary`

**Context cuối:**
```text
[72ba98c7f88046b6519961423f685ff5 | https://docs.python.org/3.14/tutorial/controlflow.html | page python-3.14-ch04-u012]
4.9.4. Arbitrary Argument Lists

Finally, the least frequently used option is to specify that a function can be called with an arbitrary number of arguments. These arguments will be wrapped up in a tuple (see Tuples and Sequences). Before the variable number of arguments, zero or more normal arguments may occur.

def write_multiple_items(file, separator, *args):
    file.write(separator.join(args))

[563b2a10f1a146b6dabbe575bdc0c257 | https://docs.python.org/3.14/tutorial/controlflow.html | page python-3.14-ch04-u011]
TypeError: combined_example() got some positional-only arguments passed as keyword arguments: 'pos_only'
```

### D06 — abstain

Tham số **name nhận những đối số nào và lưu trong kiểu dữ liệu gì?

**Đáp án mong đợi:** Nhận các keyword arguments không ứng với tham số hình thức đã khai báo và lưu thành dictionary.

**Đầu ra:**
Không đủ bằng chứng trong tài liệu để trả lời: context hiện tại chỉ nói về zip() và thông báo lỗi, không có nội dung về tham số **name hay kiểu dữ liệu mà nó lưu.

**Query tìm tài liệu:**
- `keyword argument name what arguments does it accept and what data type is it stored in`
- `**name parameter accepts arguments stored as dictionary`
- `arbitrary keyword arguments **name receives a dictionary of keyword arguments`

**Context cuối:**
```text
[d0465c0ebf1bcc71b35de11057f991e9 | https://docs.python.org/3.14/tutorial/datastructures.html | page python-3.14-ch05-u008]
To loop over two or more sequences at the same time, the entries can be paired with the zip() function.

>>> questions = ['name', 'quest', 'favorite color']
>>> answers = ['lancelot', 'the holy grail', 'blue']
>>> for q, a in zip(questions, answers):
...     print('What is your {0}?  It is {1}.'.format(q, a))
...
What is your name?  It is lancelot.
What is your quest?  It is the holy grail.
What is your favorite color?  It is blue.

[ccd74f4ce5ef674a7504052027780c6d | https://docs.python.org/3.14/tutorial/errors.html | page python-3.14-ch08-u001]
The rest of the line provides detail based on the type of exception and what caused it.
```

### D07 — answered

Muốn tạo tuple chỉ chứa chuỗi hello thì chỉ viết ngoặc quanh giá trị có đủ không? Cú pháp cần thêm gì?

**Đáp án mong đợi:** Không đủ; phải có dấu phẩy sau giá trị, ví dụ ('hello',) hoặc 'hello',.

**Đầu ra:**
Không đủ. Chỉ đặt ngoặc quanh một giá trị là không đủ để tạo tuple một phần tử; cần thêm dấu phẩy theo sau giá trị (trailing comma). Ví dụ: singleton = 'hello',  # chú ý dấu phẩy cuối, kết quả là ('hello',) với len bằng 1. Tuple rỗng thì tạo bằng cặp ngoặc rỗng (). [a14a0c62dbc9ade9275bb1cfd18bbc57]

**Query tìm tài liệu:**
- `tuple with one item single element trailing comma`
- `tuples parentheses special case singleton`

**Context cuối:**
```text
[a14a0c62dbc9ade9275bb1cfd18bbc57 | https://docs.python.org/3.14/tutorial/datastructures.html | page python-3.14-ch05-u005]
A special problem is the construction of tuples containing 0 or 1 items: the syntax has some extra quirks to accommodate these. Empty tuples are constructed by an empty pair of parentheses; a tuple with one item is constructed by following a value with a comma (it is not sufficient to enclose a single value in parentheses). Ugly, but effective. For example:

>>> empty = ()
>>> singleton = 'hello',    # <-- note trailing comma
>>> len(empty)
0
>>> len(singleton)
1
>>> singleton
('hello',)
```

### D08 — answered

a.pop() không truyền index sẽ xóa và trả về phần tử nào? Điều gì xảy ra nếu a rỗng?

**Đáp án mong đợi:** Xóa và trả về phần tử cuối; nếu list rỗng thì phát sinh IndexError.

**Đầu ra:**
a.pop() không truyền index sẽ xóa và trả về phần tử cuối cùng trong list. Nếu list rỗng (hoặc index nằm ngoài phạm vi list), nó sẽ ném ra IndexError [e4976e7c8c03d1c6a37a18f46e14e9dd].

**Query tìm tài liệu:**
- `list.pop() remove and return last item IndexError empty list`
- `pop method list data structures`

**Context cuối:**
```text
[e4976e7c8c03d1c6a37a18f46e14e9dd | https://docs.python.org/3.14/tutorial/datastructures.html | page python-3.14-ch05-u001]
Remove the item at the given position in the list, and return it. If no index is specified, a.pop() removes and returns the last item in the list. It raises an IndexError if the list is empty or the index is outside the list range.

list.clear()

Remove all items from the list. Similar to del a[:].

list.index(value[, start[, stop]])

Return zero-based index of the first occurrence of value in the list. Raises a ValueError if there is no such item.
```

### D09 — error

Khi duyệt dictionary, dùng phương thức nào để lấy đồng thời khóa và giá trị tương ứng?

**Đáp án mong đợi:** Dùng phương thức items(), ví dụ for k, v in d.items().

**Đầu ra:**
(không có câu trả lời được chấp nhận)

**Phản hồi model cuối — không được runner chấp nhận:**
```json
{"answer":"Không đủ bằng chứng trong tài liệu để trả lời: context hiện tại chỉ mô tả dictionary là tập các cặp key: value và cách tạo dictionary, không nêu phương thức nào để lấy đồng thời khóa và giá trị khi duyệt dictionary [22d13ffc003595146adb41b1a1676227].","citations":["22d13ffc003595146adb41b1a1676227"],"abstain":true}
```

**Query tìm tài liệu:**
- `looping techniques dictionary items() key value pairs`
- `iterate over dictionary retrieve key and value simultaneously`
- `items() method loop through dictionary keys and values at the same time`

**Context cuối:**
```text
[22d13ffc003595146adb41b1a1676227 | https://docs.python.org/3.14/tutorial/datastructures.html | page python-3.14-ch05-u006]
It is best to think of a dictionary as a set of key: value pairs, with the requirement that the keys are unique (within one dictionary). A pair of braces creates an empty dictionary: {}. Placing a comma-separated list of key:value pairs within the braces adds initial key:value pairs to the dictionary; this is also the way dictionaries are written on output.
```

### D10 — abstain

Có hai sequence cần duyệt đồng thời thành từng cặp phần tử tương ứng. Tài liệu giới thiệu hàm nào?

**Đáp án mong đợi:** Dùng zip() để ghép các phần tử tương ứng khi duyệt hai hoặc nhiều sequence.

**Đầu ra:**
Không đủ bằng chứng trong tài liệu để trả lời: context hiện có chỉ nhắc tới hàm zip trong ví dụ `list(zip(*matrix))` để chuyển vị ma trận, không có đoạn nào giới thiệu hàm dùng để duyệt đồng thời hai sequence thành từng cặp phần tử tương ứng.

**Query tìm tài liệu:**
- `loop over two sequences simultaneously pairs of elements zip`
- `zip function iterate two lists at the same time`
- `zip() function pairs elements from sequences looping technique`

**Context cuối:**
```text
[22d13ffc003595146adb41b1a1676227 | https://docs.python.org/3.14/tutorial/datastructures.html | page python-3.14-ch05-u006]
It is best to think of a dictionary as a set of key: value pairs, with the requirement that the keys are unique (within one dictionary). A pair of braces creates an empty dictionary: {}. Placing a comma-separated list of key:value pairs within the braces adds initial key:value pairs to the dictionary; this is also the way dictionaries are written on output.

[05405500dec053b3c7600a61076a5941 | https://docs.python.org/3.14/tutorial/datastructures.html | page python-3.14-ch05-u004]
>>> list(zip(*matrix))
[(1, 5, 9), (2, 6, 10), (3, 7, 11), (4, 8, 12)]

See Unpacking Argument Lists for details on the asterisk in this line.
```

### D11 — answered

dir() không truyền đối số liệt kê những tên nào? Nó có tự liệt kê tên hàm và biến built-in không?

**Đáp án mong đợi:** Liệt kê các tên đang được định nghĩa như biến, module và hàm; không liệt kê các tên hàm và biến built-in.

**Đầu ra:**
Khi không truyền đối số, dir() liệt kê các tên bạn đã định nghĩa hiện tại (ví dụ ['__builtins__', '__name__', 'a', 'fib', 'fibo', 'sys']), và nó liệt kê mọi loại tên: biến, module, hàm, v.v. [653c279748bae8969296f00bc2941191] Tuy nhiên, dir() KHÔNG liệt kê tên của các hàm và biến built-in; muốn có danh sách đó thì chúng được định nghĩa trong module chuẩn builtins [653c279748bae8969296f00bc2941191].

**Query tìm tài liệu:**
- `dir() without arguments lists names built-in functions variables`
- `built-in function dir returns sorted list of names in current local scope`

**Context cuối:**
```text
[653c279748bae8969296f00bc2941191 | https://docs.python.org/3.14/tutorial/modules.html | page python-3.14-ch06-u005]
Without arguments, dir() lists the names you have defined currently:

>>> a = [1, 2, 3, 4, 5]
>>> import fibo
>>> fib = fibo.fib
>>> dir()
['__builtins__', '__name__', 'a', 'fib', 'fibo', 'sys']

Note that it lists all types of names: variables, modules, functions, etc.

dir() does not list the names of built-in functions and variables. If you want a list of those, they are defined in the standard module builtins:

[6fab6ff982d8770e87310f8101a2f523 | https://docs.python.org/3.14/tutorial/modules.html | page python-3.14-ch06-u005]
6.3. The dir() Function

The built-in function dir() is used to find out which names a module defines. It returns a sorted list of strings:
```

### D12 — answered

Python dựa vào thông tin nào của file nguồn để quyết định module đã biên dịch có lỗi thời và cần biên dịch lại?

**Đáp án mong đợi:** So sánh ngày/giờ sửa đổi của mã nguồn với phiên bản đã biên dịch.

**Đầu ra:**
Python kiểm tra ngày sửa đổi (modification date) của file nguồn so với phiên bản đã biên dịch để xem module đã biên dịch có lỗi thời và cần biên dịch lại hay không; đây là quá trình hoàn toàn tự động [4b9311d6dabb880f0d9037d258d191b8].

**Query tìm tài liệu:**
- `how does Python decide compiled module is out of date and needs recompilation source file timestamp`
- `compiled Python module cache invalidation source mtime size hash pyc`

**Context cuối:**
```text
[4b9311d6dabb880f0d9037d258d191b8 | https://docs.python.org/3.14/tutorial/modules.html | page python-3.14-ch06-u004]
Python checks the modification date of the source against the compiled version to see if it’s out of date and needs to be recompiled. This is a completely automatic process. Also, the compiled modules are platform-independent, so the same library can be shared among systems with different architectures.

[5232afaeda65d6380749218d8b7fbbe6 | https://docs.python.org/3.14/tutorial/modules.html | page python-3.14-ch06-u003]
6.1.3. “Compiled” Python files
```

### D13 — answered

Với file vừa mở để đọc và đang ở đầu file, bỏ size hoặc truyền size âm cho f.read(size) sẽ đọc bao nhiêu? Rủi ro bộ nhớ được tài liệu nhắc là gì?

**Đáp án mong đợi:** Đọc toàn bộ nội dung file; file quá lớn có thể vượt bộ nhớ máy.

**Đầu ra:**
Khi bỏ size hoặc truyền size âm cho f.read(size), toàn bộ nội dung của file sẽ được đọc và trả về (dưới dạng chuỗi ở text mode hoặc bytes ở binary mode) [b2e4e2a1efb032538c84a9e87be3cfb4]. Rủi ro bộ nhớ mà tài liệu nhắc là: "it's your problem if the file is twice as large as your machine's memory" — tức là nếu file lớn gấp đôi bộ nhớ máy thì đó là vấn đề của bạn [b2e4e2a1efb032538c84a9e87be3cfb4].

**Query tìm tài liệu:**
- `f.read(size) omit size or negative size read entire file memory risk`
- `reading and writing files read size negative reads whole file`

**Context cuối:**
```text
[b2e4e2a1efb032538c84a9e87be3cfb4 | https://docs.python.org/3.14/tutorial/inputoutput.html | page python-3.14-ch07-u005]
To read a file’s contents, call f.read(size), which reads some quantity of data and returns it as a string (in text mode) or bytes object (in binary mode). size is an optional numeric argument. When size is omitted or negative, the entire contents of the file will be read and returned; it’s your problem if the file is twice as large as your machine’s memory. Otherwise, at most size characters (in text mode) or size bytes (in binary mode) are read and returned. If the end of the file has been 

[1dc34e861c5e5fadc4724e725df10931 | https://docs.python.org/3.14/tutorial/inputoutput.html | page python-3.14-ch07-u005]
reached, f.read() will return an empty string ('').
```

### D14 — answered

Giá trị f.tell() trong binary mode và text mode có ý nghĩa khác nhau thế nào?

**Đáp án mong đợi:** Binary mode: số byte tính từ đầu file. Text mode: một số opaque biểu diễn vị trí, không nên hiểu là số byte.

**Đầu ra:**
Theo tài liệu: f.tell() trả về một số nguyên cho biết vị trí hiện tại của file object trong file — ở binary mode đó là số byte tính từ đầu file, còn ở text mode đó là một "opaque number" (con số không mang ý nghĩa trực tiếp, không phải số byte) [9c4ec9a68dac484801d37366b0214e51].

**Query tìm tài liệu:**
- `f.tell() binary mode text mode meaning opaque number`
- `tell() text files opaque number binary files byte position`

**Context cuối:**
```text
[9c4ec9a68dac484801d37366b0214e51 | https://docs.python.org/3.14/tutorial/inputoutput.html | page python-3.14-ch07-u006]
f.tell() returns an integer giving the file object’s current position in the file represented as number of bytes from the beginning of the file when in binary mode and an opaque number when in text mode.

[e3dd727e9d10ff3ef55e9dda334b3b96 | https://docs.python.org/3.14/tutorial/inputoutput.html | page python-3.14-ch07-u005]
encoding when opening file in binary mode.

[5232afaeda65d6380749218d8b7fbbe6 | https://docs.python.org/3.14/tutorial/modules.html | page python-3.14-ch06-u003]
6.1.3. “Compiled” Python files
```

### D15 — answered

Trong try...except, khối else phải đặt sau phần nào và được dùng khi nào?

**Đáp án mong đợi:** Đặt sau tất cả các except; dùng cho code chỉ chạy khi khối try không phát sinh ngoại lệ.

**Đầu ra:**
Khối else là tùy chọn của câu lệnh try … except; khi có mặt, nó phải đặt sau tất cả các khối except. Nó hữu ích cho đoạn mã phải được thực thi nếu khối try không ném ra ngoại lệ — tức là else chạy khi không có ngoại lệ xảy ra [89cb0b58f013c40c3ef13c336fcb8792][e029e5d8abe70414636c4b8d53ae1e44].

**Query tìm tài liệu:**
- `try except else clause must follow which clause and when is it executed`
- `handling exceptions try statement else clause finally`

**Context cuối:**
```text
[89cb0b58f013c40c3ef13c336fcb8792 | https://docs.python.org/3.14/tutorial/errors.html | page python-3.14-ch08-u003]
The try … except statement has an optional else clause, which, when present, must follow all except clauses. It is useful for code that must be executed if the try clause does not raise an exception. For example:

[e029e5d8abe70414636c4b8d53ae1e44 | https://docs.python.org/3.14/tutorial/controlflow.html | page python-3.14-ch04-u003]
When used with a loop, the else clause has more in common with the else clause of a try statement than it does with that of if statements: a try statement’s else clause runs when no exception occurs, and a loop’s else clause runs when no break occurs. For more on the try statement and exceptions, see Handling Exceptions.
```

### D16 — abstain

Chỉ dựa trên tài liệu đã cung cấp, khi một task trong asyncio.TaskGroup lỗi, các task còn lại được hủy và chờ kết thúc như thế nào?

**Thiếu bằng chứng trong corpus:** Corpus không có phần giải thích asyncio hoặc TaskGroup. Các mục vòng lặp/ngoại lệ không quy định ngữ nghĩa hủy task bất đồng bộ.

**Đầu ra:**
Không đủ bằng chứng trong tài liệu để trả lời: context hiện có chỉ chứa nội dung về dùng Python như máy tính và câu lệnh pass, không có thông tin về asyncio.TaskGroup hay cách hủy/chờ các task còn lại khi một task lỗi.

**Query tìm tài liệu:**
- `asyncio.TaskGroup one task fails cancel remaining tasks wait for them to finish`
- `TaskGroup exception group cancel sibling tasks`
- `TaskGroup structured concurrency asyncio tasks cancelled when one raises exception`

**Context cuối:**
```text
[9ec7a9d833ea85692a48c6a45c56125a | https://docs.python.org/3.14/tutorial/introduction.html | page python-3.14-ch03-u001]
3.1. Using Python as a Calculator

Let’s try some simple Python commands. Start the interpreter and wait for the primary prompt, >>>. (It shouldn’t take long.)

[4e5eaa16aec75bdce7242ad5159c10d4 | https://docs.python.org/3.14/tutorial/controlflow.html | page python-3.14-ch04-u003]
4.6. pass Statements

The pass statement does nothing. It can be used when a statement is required syntactically but the program requires no action. For example:

>>> while True:
...     pass  # Busy-wait for keyboard interrupt (Ctrl+C)
...

This is commonly used for creating minimal classes:

>>> class MyEmptyClass:
...     pass
...
```

### D17 — abstain

Tài liệu đã cung cấp hướng dẫn dùng @dataclass(frozen=True) để ngăn gán lại thuộc tính như thế nào và phát sinh ngoại lệ gì khi cố gán?

**Thiếu bằng chứng trong corpus:** dataclasses chỉ được nhắc làm ví dụ lớp có thứ tự thuộc tính trong match; frozen xuất hiện trong tên built-in frozenset. Không có hướng dẫn frozen=True hoặc ngoại lệ khi gán.

**Đầu ra:**
Không đủ bằng chứng trong tài liệu để trả lời: context hiện có chỉ nói về except clause và tính bất biến của chuỗi, không có hướng dẫn dùng @dataclass(frozen=True) hay ngoại lệ phát sinh khi cố gán lại thuộc tính.

**Query tìm tài liệu:**
- `dataclass frozen=True prevent assignment attribute exception FrozenInstanceError`
- `dataclasses frozen immutable fields cannot assign raise exception`
- `dataclass decorator frozen parameter`

**Context cuối:**
```text
[508e7cdee72e393ecd43699da1396aee | https://docs.python.org/3.14/tutorial/errors.html | page python-3.14-ch08-u003]
The except clause may specify a variable after the exception name. The variable is bound to the exception instance which typically has an args attribute that stores the arguments. For convenience, builtin exception types define __str__() to print all the arguments without explicitly accessing .args.

[e00c977d03c6875555f83f0703e76d61 | https://docs.python.org/3.14/tutorial/introduction.html | page python-3.14-ch03-u005]
However, out of range slice indexes are handled gracefully when used for slicing:

>>> word[4:42]
'on'
>>> word[42:]
''

Python strings cannot be changed — they are immutable. Therefore, assigning to an indexed position in the string results in an error:
```

## hybrid

### D01 — answered

Muốn viết đường dẫn Windows mà các ký tự như \n và \t không bị hiểu là xuống dòng hoặc tab, tiền tố chuỗi nào được tài liệu hướng dẫn?

**Đáp án mong đợi:** Đặt tiền tố r trước dấu nháy để tạo raw string.

**Đầu ra:**
Tài liệu hướng dẫn dùng tiền tố r (raw string) trước dấu nháy đầu tiên, ví dụ r'C:\this\name', để các ký tự sau \ không bị hiểu là ký tự đặc biệt như \t (tab) hay \n (xuống dòng) [5046e99636180b57c2960fedf1d3566c]. Lưu ý: raw string không được kết thúc bằng số lẻ ký tự \ [5046e99636180b57c2960fedf1d3566c].

**Query tìm tài liệu:**
- `raw string prefix backslash not escape newline tab Windows path`
- `string literal prefix r raw strings`

**Context cuối:**
```text
[5046e99636180b57c2960fedf1d3566c | https://docs.python.org/3.14/tutorial/introduction.html | page python-3.14-ch03-u003]
If you don’t want characters prefaced by \ to be interpreted as special characters, you can use raw strings by adding an r before the first quote:

>>> print('C:\this\name')  # here \t means tab, \n means newline
C:      his
ame
>>> print(r'C:\this\name')  # note the r before the quote
C:\this\name

There is one subtle aspect to raw strings: a raw string may not end in an odd number of \ characters; see the FAQ entry for more information and workarounds.
```

### D02 — answered

Khi đánh chỉ số chuỗi từ phía cuối, -1 và -2 chỉ ký tự nào? Vì sao không bắt đầu bằng -0?

**Đáp án mong đợi:** -1 chỉ ký tự cuối, -2 chỉ ký tự áp cuối; -0 bằng 0 nên chỉ số âm bắt đầu từ -1.

**Đầu ra:**
Với chuỗi 'Python' trong ví dụ: word[-1] là ký tự cuối cùng ('n'), còn word[-2] là ký tự áp chót ('o') [07eab24fdef0d6f3c82bb56fb67407ce]. Không bắt đầu bằng -0 vì -0 bằng 0, nên các chỉ số âm bắt đầu từ -1 [07eab24fdef0d6f3c82bb56fb67407ce].

**Query tìm tài liệu:**
- `negative indices string -1 -2 last character why not -0`
- `indexing strings first character index 0 negative index from end`

**Context cuối:**
```text
[07eab24fdef0d6f3c82bb56fb67407ce | https://docs.python.org/3.14/tutorial/introduction.html | page python-3.14-ch03-u004]
>>> word[-1]  # last character
'n'
>>> word[-2]  # second-last character
'o'
>>> word[-6]
'P'

Note that since -0 is the same as 0, negative indices start from -1.

In addition to indexing, slicing is also supported. While indexing is used to obtain individual characters, slicing allows you to obtain a substring:

>>> word[0:2]  # characters from position 0 (included) to 2 (excluded)
'Py'
>>> word[2:5]  # characters from position 2 (included) to 5 (excluded)
'tho'
```

### D03 — answered

Ví dụ list(range(5, 10)) trong tài liệu cho ra danh sách nào?

**Đáp án mong đợi:** [5, 6, 7, 8, 9]; cận 10 không được lấy.

**Đầu ra:**
Theo tài liệu, `list(range(5, 10))` cho ra `[5, 6, 7, 8, 9]` [5b0389b2014ead261047a7ea77039951].

**Query tìm tài liệu:**
- `list(range(5, 10)) example output`
- `range function arguments start stop step examples`

**Context cuối:**
```text
[5b0389b2014ead261047a7ea77039951 | https://docs.python.org/3.14/tutorial/controlflow.html | page python-3.14-ch04-u002]
>>> list(range(5, 10))
[5, 6, 7, 8, 9]

>>> list(range(0, 10, 3))
[0, 3, 6, 9]

>>> list(range(-10, -100, -30))
[-10, -40, -70]

To iterate over the indices of a sequence, you can combine range() and len() as follows:

>>> a = ['Mary', 'had', 'a', 'little', 'lamb']
>>> for i in range(len(a)):
...     print(i, a[i])
...
0 Mary
1 had
2 a
3 little
4 lamb

In most such cases, however, it is convenient to use the enumerate() function, see Looping Techniques.
```

### D04 — error

Nếu có vòng lặp for lồng trong while, break nằm trong for sẽ thoát vòng nào theo quy tắc của tài liệu?

**Đáp án mong đợi:** Thoát vòng for ở trong cùng bao quanh break, không tự động thoát cả vòng while bên ngoài.

**Đầu ra:**
(không có câu trả lời được chấp nhận)

**Phản hồi model cuối — không được runner chấp nhận:**
```json
{"answer":"Không đủ bằng chứng trong tài liệu để trả lời: context hiện có chỉ nói về else clause đi kèm break trong for/while, không nêu quy tắc break trong for lồng trong while sẽ thoát vòng nào [e09df3f01953e055de669d3402d7ddac].","citations":["e09df3f01953e055de669d3402d7ddac"],"abstain":true}
```

**Query tìm tài liệu:**
- `break statement in for loop nested inside while loop which loop does it exit`
- `break statement terminates innermost enclosing for or while loop`
- `break statement breaks out of the innermost enclosing loop`

**Context cuối:**
```text
[e09df3f01953e055de669d3402d7ddac | https://docs.python.org/3.14/tutorial/controlflow.html | page python-3.14-ch04-u002]
4.5. else Clauses on Loops

In a for or while loop the break statement may be paired with an else clause. If the loop finishes without executing the break, the else clause executes.

In a for loop, the else clause is executed after the loop finishes its final iteration, that is, if no break occurred.

In a while loop, it’s executed after the loop’s condition becomes false.
```

### D05 — answered

Các đối số bổ sung được gom bởi *args trong định nghĩa hàm có kiểu cấu trúc dữ liệu gì?

**Đáp án mong đợi:** Một tuple chứa các đối số vị trí bổ sung.

**Đầu ra:**
Các đối số bổ sung được gom bởi *args sẽ được gói lại trong một tuple (xem phần Tuples and Sequences) [72ba98c7f88046b6519961423f685ff5].

**Query tìm tài liệu:**
- `*args arbitrary arguments tuple function definition`
- `arbitrary argument list packed into tuple keyword arguments dictionary`

**Context cuối:**
```text
[72ba98c7f88046b6519961423f685ff5 | https://docs.python.org/3.14/tutorial/controlflow.html | page python-3.14-ch04-u012]
4.9.4. Arbitrary Argument Lists

Finally, the least frequently used option is to specify that a function can be called with an arbitrary number of arguments. These arguments will be wrapped up in a tuple (see Tuples and Sequences). Before the variable number of arguments, zero or more normal arguments may occur.

def write_multiple_items(file, separator, *args):
    file.write(separator.join(args))
```

### D06 — error

Tham số **name nhận những đối số nào và lưu trong kiểu dữ liệu gì?

**Đáp án mong đợi:** Nhận các keyword arguments không ứng với tham số hình thức đã khai báo và lưu thành dictionary.

**Đầu ra:**
(không có câu trả lời được chấp nhận)

**Phản hồi model cuối — không được runner chấp nhận:**
```json
{"answer":"Không đủ bằng chứng trong tài liệu để trả lời: ngữ cảnh tìm được chỉ nói chung về đối số từ khóa trong lời gọi hàm (phải đứng sau đối số vị trí, phải khớp với đối số mà hàm chấp nhận, thứ tự không quan trọng, không đối số nào nhận giá trị quá một lần) [5c3e2cd2446561b62a1de5be9ec614ba], nhưng không nêu tham số `name` nhận những đối số nào hay được lưu trong kiểu dữ liệu gì.","citations":["5c3e2cd2446561b62a1de5be9ec614ba"],"abstain":true}
```

**Query tìm tài liệu:**
- `keyword argument name what values accepted type`
- `function parameter name argument type string`
- `def function definition name parameter default value type annotation`

**Context cuối:**
```text
[5c3e2cd2446561b62a1de5be9ec614ba | https://docs.python.org/3.14/tutorial/controlflow.html | page python-3.14-ch04-u009]
In a function call, keyword arguments must follow positional arguments. All the keyword arguments passed must match one of the arguments accepted by the function (e.g. actor is not a valid argument for the parrot function), and their order is not important. This also includes non-optional arguments (e.g. parrot(voltage=1000) is valid too). No argument may receive a value more than once. Here’s an example that fails due to this restriction:
```

### D07 — answered

Muốn tạo tuple chỉ chứa chuỗi hello thì chỉ viết ngoặc quanh giá trị có đủ không? Cú pháp cần thêm gì?

**Đáp án mong đợi:** Không đủ; phải có dấu phẩy sau giá trị, ví dụ ('hello',) hoặc 'hello',.

**Đầu ra:**
Không đủ. Theo tài liệu, chỉ đặt một giá trị trong ngoặc đơn là không đủ để tạo tuple một phần tử; cần thêm dấu phẩy sau giá trị (dấu phẩy ở cuối). Ví dụ: singleton = 'hello',  # chú ý dấu phẩy cuối — kết quả là ('hello',) với len bằng 1 [a14a0c62dbc9ade9275bb1cfd18bbc57].

**Query tìm tài liệu:**
- `tuple with one item single element trailing comma`
- `tuples parentheses special case singleton`

**Context cuối:**
```text
[a14a0c62dbc9ade9275bb1cfd18bbc57 | https://docs.python.org/3.14/tutorial/datastructures.html | page python-3.14-ch05-u005]
A special problem is the construction of tuples containing 0 or 1 items: the syntax has some extra quirks to accommodate these. Empty tuples are constructed by an empty pair of parentheses; a tuple with one item is constructed by following a value with a comma (it is not sufficient to enclose a single value in parentheses). Ugly, but effective. For example:

>>> empty = ()
>>> singleton = 'hello',    # <-- note trailing comma
>>> len(empty)
0
>>> len(singleton)
1
>>> singleton
('hello',)
```

### D08 — answered

a.pop() không truyền index sẽ xóa và trả về phần tử nào? Điều gì xảy ra nếu a rỗng?

**Đáp án mong đợi:** Xóa và trả về phần tử cuối; nếu list rỗng thì phát sinh IndexError.

**Đầu ra:**
a.pop() không truyền index sẽ xóa và trả về phần tử cuối cùng của list. Nếu list rỗng (hoặc index nằm ngoài phạm vi list), nó sẽ ném ra IndexError [e4976e7c8c03d1c6a37a18f46e14e9dd].

**Query tìm tài liệu:**
- `list.pop() remove and return last item empty list IndexError`
- `pop() without index default last element`

**Context cuối:**
```text
[e4976e7c8c03d1c6a37a18f46e14e9dd | https://docs.python.org/3.14/tutorial/datastructures.html | page python-3.14-ch05-u001]
Remove the item at the given position in the list, and return it. If no index is specified, a.pop() removes and returns the last item in the list. It raises an IndexError if the list is empty or the index is outside the list range.

list.clear()

Remove all items from the list. Similar to del a[:].

list.index(value[, start[, stop]])

Return zero-based index of the first occurrence of value in the list. Raises a ValueError if there is no such item.
```

### D09 — error

Khi duyệt dictionary, dùng phương thức nào để lấy đồng thời khóa và giá trị tương ứng?

**Đáp án mong đợi:** Dùng phương thức items(), ví dụ for k, v in d.items().

**Đầu ra:**
(không có câu trả lời được chấp nhận)

**Phản hồi model cuối — không được runner chấp nhận:**
```json
{"answer":"Không đủ bằng chứng trong tài liệu để trả lời: context hiện có chỉ mô tả dictionary là tập các cặp key: value và cách tạo/ghi dictionary, không nêu phương thức nào để lấy đồng thời khóa và giá trị khi duyệt dictionary [22d13ffc003595146adb41b1a1676227].","citations":["22d13ffc003595146adb41b1a1676227"],"abstain":true}
```

**Query tìm tài liệu:**
- `looping techniques dictionary items() key value pairs`
- `iterate over dictionary retrieve key and value simultaneously`
- `dictionary items method loop through keys and values at the same time`

**Context cuối:**
```text
[22d13ffc003595146adb41b1a1676227 | https://docs.python.org/3.14/tutorial/datastructures.html | page python-3.14-ch05-u006]
It is best to think of a dictionary as a set of key: value pairs, with the requirement that the keys are unique (within one dictionary). A pair of braces creates an empty dictionary: {}. Placing a comma-separated list of key:value pairs within the braces adds initial key:value pairs to the dictionary; this is also the way dictionaries are written on output.
```

### D10 — answered

Có hai sequence cần duyệt đồng thời thành từng cặp phần tử tương ứng. Tài liệu giới thiệu hàm nào?

**Đáp án mong đợi:** Dùng zip() để ghép các phần tử tương ứng khi duyệt hai hoặc nhiều sequence.

**Đầu ra:**
Tài liệu giới thiệu hàm zip(): để duyệt hai hoặc nhiều sequence cùng lúc, các phần tử có thể được ghép cặp bằng hàm zip(), ví dụ `for q, a in zip(questions, answers):` [d0465c0ebf1bcc71b35de11057f991e9].

**Query tìm tài liệu:**
- `loop over two sequences simultaneously pairs of elements zip`
- `zip function iterate two lists at the same time`

**Context cuối:**
```text
[d0465c0ebf1bcc71b35de11057f991e9 | https://docs.python.org/3.14/tutorial/datastructures.html | page python-3.14-ch05-u008]
To loop over two or more sequences at the same time, the entries can be paired with the zip() function.

>>> questions = ['name', 'quest', 'favorite color']
>>> answers = ['lancelot', 'the holy grail', 'blue']
>>> for q, a in zip(questions, answers):
...     print('What is your {0}?  It is {1}.'.format(q, a))
...
What is your name?  It is lancelot.
What is your quest?  It is the holy grail.
What is your favorite color?  It is blue.
```

### D11 — answered

dir() không truyền đối số liệt kê những tên nào? Nó có tự liệt kê tên hàm và biến built-in không?

**Đáp án mong đợi:** Liệt kê các tên đang được định nghĩa như biến, module và hàm; không liệt kê các tên hàm và biến built-in.

**Đầu ra:**
Khi không truyền đối số, dir() liệt kê các tên bạn đã định nghĩa hiện tại (mọi loại tên: biến, module, hàm, v.v.) [653c279748bae8969296f00bc2941191]. Tuy nhiên, dir() KHÔNG liệt kê tên của các hàm và biến built-in; muốn có danh sách đó thì chúng được định nghĩa trong module chuẩn builtins [653c279748bae8969296f00bc2941191].

**Query tìm tài liệu:**
- `dir() without arguments list names built-in functions variables`
- `built-in function dir returns sorted list of names in current local scope`

**Context cuối:**
```text
[653c279748bae8969296f00bc2941191 | https://docs.python.org/3.14/tutorial/modules.html | page python-3.14-ch06-u005]
Without arguments, dir() lists the names you have defined currently:

>>> a = [1, 2, 3, 4, 5]
>>> import fibo
>>> fib = fibo.fib
>>> dir()
['__builtins__', '__name__', 'a', 'fib', 'fibo', 'sys']

Note that it lists all types of names: variables, modules, functions, etc.

dir() does not list the names of built-in functions and variables. If you want a list of those, they are defined in the standard module builtins:

[6fab6ff982d8770e87310f8101a2f523 | https://docs.python.org/3.14/tutorial/modules.html | page python-3.14-ch06-u005]
6.3. The dir() Function

The built-in function dir() is used to find out which names a module defines. It returns a sorted list of strings:
```

### D12 — answered

Python dựa vào thông tin nào của file nguồn để quyết định module đã biên dịch có lỗi thời và cần biên dịch lại?

**Đáp án mong đợi:** So sánh ngày/giờ sửa đổi của mã nguồn với phiên bản đã biên dịch.

**Đầu ra:**
Python kiểm tra ngày sửa đổi (modification date) của file nguồn so với phiên bản đã biên dịch để xem module đã biên dịch có lỗi thời và cần biên dịch lại hay không; đây là quá trình hoàn toàn tự động [4b9311d6dabb880f0d9037d258d191b8].

**Query tìm tài liệu:**
- `how does Python decide a compiled module is out of date and needs recompiling source file information`
- `bytecode cache invalidation source mtime size check pyc`

**Context cuối:**
```text
[4b9311d6dabb880f0d9037d258d191b8 | https://docs.python.org/3.14/tutorial/modules.html | page python-3.14-ch06-u004]
Python checks the modification date of the source against the compiled version to see if it’s out of date and needs to be recompiled. This is a completely automatic process. Also, the compiled modules are platform-independent, so the same library can be shared among systems with different architectures.
```

### D13 — answered

Với file vừa mở để đọc và đang ở đầu file, bỏ size hoặc truyền size âm cho f.read(size) sẽ đọc bao nhiêu? Rủi ro bộ nhớ được tài liệu nhắc là gì?

**Đáp án mong đợi:** Đọc toàn bộ nội dung file; file quá lớn có thể vượt bộ nhớ máy.

**Đầu ra:**
Khi bỏ size hoặc truyền size âm cho f.read(size), toàn bộ nội dung file sẽ được đọc và trả về (dưới dạng chuỗi ở text mode hoặc bytes ở binary mode) [b2e4e2a1efb032538c84a9e87be3cfb4]. Rủi ro bộ nhớ mà tài liệu nhắc là: "it's your problem if the file is twice as large as your machine's memory" — tức nếu file lớn gấp đôi bộ nhớ máy thì đó là vấn đề của bạn [b2e4e2a1efb032538c84a9e87be3cfb4].

**Query tìm tài liệu:**
- `f.read(size) omit size or negative size read entire file memory risk`
- `reading and writing files read size negative memory`

**Context cuối:**
```text
[b2e4e2a1efb032538c84a9e87be3cfb4 | https://docs.python.org/3.14/tutorial/inputoutput.html | page python-3.14-ch07-u005]
To read a file’s contents, call f.read(size), which reads some quantity of data and returns it as a string (in text mode) or bytes object (in binary mode). size is an optional numeric argument. When size is omitted or negative, the entire contents of the file will be read and returned; it’s your problem if the file is twice as large as your machine’s memory. Otherwise, at most size characters (in text mode) or size bytes (in binary mode) are read and returned. If the end of the file has been 

[1dc34e861c5e5fadc4724e725df10931 | https://docs.python.org/3.14/tutorial/inputoutput.html | page python-3.14-ch07-u005]
reached, f.read() will return an empty string ('').
```

### D14 — answered

Giá trị f.tell() trong binary mode và text mode có ý nghĩa khác nhau thế nào?

**Đáp án mong đợi:** Binary mode: số byte tính từ đầu file. Text mode: một số opaque biểu diễn vị trí, không nên hiểu là số byte.

**Đầu ra:**
Trong binary mode, f.tell() trả về một số nguyên là vị trí hiện tại của file object, được biểu diễn bằng số byte tính từ đầu file; còn trong text mode, nó trả về một số "opaque" (không mang ý nghĩa trực tiếp là số byte) [9c4ec9a68dac484801d37366b0214e51].

**Query tìm tài liệu:**
- `f.tell() binary mode text mode meaning opaque number`
- `tell() text files opaque number binary files byte position`

**Context cuối:**
```text
[9c4ec9a68dac484801d37366b0214e51 | https://docs.python.org/3.14/tutorial/inputoutput.html | page python-3.14-ch07-u006]
f.tell() returns an integer giving the file object’s current position in the file represented as number of bytes from the beginning of the file when in binary mode and an opaque number when in text mode.

[e3dd727e9d10ff3ef55e9dda334b3b96 | https://docs.python.org/3.14/tutorial/inputoutput.html | page python-3.14-ch07-u005]
encoding when opening file in binary mode.
```

### D15 — answered

Trong try...except, khối else phải đặt sau phần nào và được dùng khi nào?

**Đáp án mong đợi:** Đặt sau tất cả các except; dùng cho code chỉ chạy khi khối try không phát sinh ngoại lệ.

**Đầu ra:**
Khối else là tùy chọn của câu lệnh try … except; khi có mặt, nó phải đặt sau tất cả các khối except. Nó hữu ích cho đoạn mã phải được thực thi nếu khối try không ném ra ngoại lệ — nói cách khác, else chạy khi không có ngoại lệ xảy ra [89cb0b58f013c40c3ef13c336fcb8792][e029e5d8abe70414636c4b8d53ae1e44].

**Query tìm tài liệu:**
- `try except else clause must follow which clause and when is it executed`
- `try statement else clause executed if no exception occurs`

**Context cuối:**
```text
[89cb0b58f013c40c3ef13c336fcb8792 | https://docs.python.org/3.14/tutorial/errors.html | page python-3.14-ch08-u003]
The try … except statement has an optional else clause, which, when present, must follow all except clauses. It is useful for code that must be executed if the try clause does not raise an exception. For example:

[e029e5d8abe70414636c4b8d53ae1e44 | https://docs.python.org/3.14/tutorial/controlflow.html | page python-3.14-ch04-u003]
When used with a loop, the else clause has more in common with the else clause of a try statement than it does with that of if statements: a try statement’s else clause runs when no exception occurs, and a loop’s else clause runs when no break occurs. For more on the try statement and exceptions, see Handling Exceptions.
```

### D16 — abstain

Chỉ dựa trên tài liệu đã cung cấp, khi một task trong asyncio.TaskGroup lỗi, các task còn lại được hủy và chờ kết thúc như thế nào?

**Thiếu bằng chứng trong corpus:** Corpus không có phần giải thích asyncio hoặc TaskGroup. Các mục vòng lặp/ngoại lệ không quy định ngữ nghĩa hủy task bất đồng bộ.

**Đầu ra:**
Không đủ bằng chứng trong tài liệu để trả lời: context hiện có chỉ chứa nội dung về dùng Python như máy tính và câu lệnh pass, không có thông tin về asyncio.TaskGroup hay cách hủy/chờ các task còn lại khi một task lỗi.

**Query tìm tài liệu:**
- `asyncio.TaskGroup one task fails cancel remaining tasks wait for them to finish`
- `TaskGroup exception group cancel sibling tasks`
- `TaskGroup asyncio concurrency task group error handling`

**Context cuối:**
```text
[9ec7a9d833ea85692a48c6a45c56125a | https://docs.python.org/3.14/tutorial/introduction.html | page python-3.14-ch03-u001]
3.1. Using Python as a Calculator

Let’s try some simple Python commands. Start the interpreter and wait for the primary prompt, >>>. (It shouldn’t take long.)

[4e5eaa16aec75bdce7242ad5159c10d4 | https://docs.python.org/3.14/tutorial/controlflow.html | page python-3.14-ch04-u003]
4.6. pass Statements

The pass statement does nothing. It can be used when a statement is required syntactically but the program requires no action. For example:

>>> while True:
...     pass  # Busy-wait for keyboard interrupt (Ctrl+C)
...

This is commonly used for creating minimal classes:

>>> class MyEmptyClass:
...     pass
...
```

### D17 — abstain

Tài liệu đã cung cấp hướng dẫn dùng @dataclass(frozen=True) để ngăn gán lại thuộc tính như thế nào và phát sinh ngoại lệ gì khi cố gán?

**Thiếu bằng chứng trong corpus:** dataclasses chỉ được nhắc làm ví dụ lớp có thứ tự thuộc tính trong match; frozen xuất hiện trong tên built-in frozenset. Không có hướng dẫn frozen=True hoặc ngoại lệ khi gán.

**Đầu ra:**
Không đủ bằng chứng trong tài liệu để trả lời: context hiện có chỉ nói về cơ chế raise ngoại lệ nói chung, không có hướng dẫn dùng @dataclass(frozen=True) để ngăn gán lại thuộc tính cũng như không nêu ngoại lệ cụ thể phát sinh khi cố gán.

**Query tìm tài liệu:**
- `dataclass frozen=True prevent assignment attribute raises exception`
- `frozen dataclass FrozenInstanceError cannot assign to field`
- `dataclasses module frozen dataclass fields cannot be assigned`

**Context cuối:**
```text
[eb1202071982afa8de740c2fa8c71a8f | https://docs.python.org/3.14/tutorial/errors.html | page python-3.14-ch08-u004]
The sole argument to raise indicates the exception to be raised. This must be either an exception instance or an exception class (a class that derives from BaseException, such as Exception or one of its subclasses). If an exception class is passed, it will be implicitly instantiated by calling its constructor with no arguments:

raise ValueError  # shorthand for 'raise ValueError()'

[22301843e855f993ff0daa2a245506d0 | https://docs.python.org/3.14/tutorial/errors.html | page python-3.14-ch08-u005]
    raise RuntimeError('Failed to open database') from exc
RuntimeError: Failed to open database
```

