# Đọc và kiểm tra 85 nhãn dev

AI-assisted; mọi nhãn hiện chờ người dùng xác nhận. Không có test trong tài liệu này. Context grade cho payload đã chuẩn bị; gặp lỗi provider thì không khẳng định model nhận payload.

## Dense 800 / arrival

### D01 — answered

Muốn viết đường dẫn Windows mà các ký tự như \n và \t không bị hiểu là xuống dòng hoặc tab, tiền tố chuỗi nào được tài liệu hướng dẫn?

**Nhãn đề xuất:** answer=2; context=2; abstention_correct=None

**Lý do:** Đúng tiền tố r và ý nghĩa giữ nguyên escape; ví dụ/giới hạn dấu backslash có trong nguồn.

**Đáp án mong đợi / giới hạn corpus:** Đặt tiền tố r trước dấu nháy để tạo raw string.

**Đầu ra được chấp nhận:**
Tài liệu hướng dẫn dùng tiền tố r để tạo raw string, đặt trước dấu nháy đầu tiên, nhờ đó các ký tự sau dấu \ không bị hiểu là ký tự đặc biệt (ví dụ \t là tab, \n là xuống dòng). Ví dụ: print(r'C:\this\name') in ra C:\this\name. Lưu ý: raw string không thể kết thúc bằng số lẻ ký tự \ [5046e99636180b57c2960fedf1d3566c].

**Citation đã đọc:**
- `5046e99636180b57c2960fedf1d3566c`: True — Đoạn raw strings nêu tiền tố r, ví dụ Windows path, escape và giới hạn backslash cuối.

<details><summary>Context đã chuẩn bị</summary>

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

</details>

### D02 — answered

Khi đánh chỉ số chuỗi từ phía cuối, -1 và -2 chỉ ký tự nào? Vì sao không bắt đầu bằng -0?

**Nhãn đề xuất:** answer=2; context=2; abstention_correct=None

**Lý do:** Đủ cả -1 là ký tự cuối, -2 áp cuối và -0 bằng 0.

**Đáp án mong đợi / giới hạn corpus:** -1 chỉ ký tự cuối, -2 chỉ ký tự áp cuối; -0 bằng 0 nên chỉ số âm bắt đầu từ -1.

**Đầu ra được chấp nhận:**
Theo tài liệu, với chuỗi 'Python' (word), word[-1] là ký tự cuối cùng ('n') và word[-2] là ký tự áp chót ('o'); tài liệu cũng lưu ý rằng vì -0 giống hệt 0 nên các chỉ số âm bắt đầu từ -1 [07eab24fdef0d6f3c82bb56fb67407ce].

**Citation đã đọc:**
- `07eab24fdef0d6f3c82bb56fb67407ce`: True — Ví dụ word[-1]/[-2] và câu -0 giống 0 hỗ trợ đủ điều kiện.

<details><summary>Context đã chuẩn bị</summary>

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

</details>

### D03 — answered

Ví dụ list(range(5, 10)) trong tài liệu cho ra danh sách nào?

**Nhãn đề xuất:** answer=2; context=2; abstention_correct=None

**Lý do:** Đúng toàn bộ danh sách [5, 6, 7, 8, 9].

**Đáp án mong đợi / giới hạn corpus:** [5, 6, 7, 8, 9]; cận 10 không được lấy.

**Đầu ra được chấp nhận:**
Theo tài liệu, `list(range(5, 10))` cho ra `[5, 6, 7, 8, 9]` [5b0389b2014ead261047a7ea77039951].

**Citation đã đọc:**
- `5b0389b2014ead261047a7ea77039951`: True — Ví dụ nguyên văn list(range(5,10)) và danh sách kết quả.

<details><summary>Context đã chuẩn bị</summary>

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

</details>

### D04 — abstain

Nếu có vòng lặp for lồng trong while, break nằm trong for sẽ thoát vòng nào theo quy tắc của tài liệu?

**Nhãn đề xuất:** answer=0; context=0; abstention_correct=None

**Lý do:** False refusal: context chỉ có loop else, thiếu quy tắc innermost dù các lượt tìm đã tìm thấy.

**Đáp án mong đợi / giới hạn corpus:** Thoát vòng for ở trong cùng bao quanh break, không tự động thoát cả vòng while bên ngoài.

**Đầu ra được chấp nhận:**
Không đủ bằng chứng trong tài liệu để trả lời: context hiện có chỉ nói về else clause của vòng lặp và break, không nêu quy tắc break trong for lồng trong while sẽ thoát vòng nào [e09df3f01953e055de669d3402d7ddac].

**Cờ citation ngoài mảng:** e09df3f01953e055de669d3402d7ddac

**Citation đã đọc:**

<details><summary>Context đã chuẩn bị</summary>

```text
[e09df3f01953e055de669d3402d7ddac | https://docs.python.org/3.14/tutorial/controlflow.html | page python-3.14-ch04-u002]
4.5. else Clauses on Loops

In a for or while loop the break statement may be paired with an else clause. If the loop finishes without executing the break, the else clause executes.

In a for loop, the else clause is executed after the loop finishes its final iteration, that is, if no break occurred.

In a while loop, it’s executed after the loop’s condition becomes false.
```

</details>

### D05 — answered

Các đối số bổ sung được gom bởi *args trong định nghĩa hàm có kiểu cấu trúc dữ liệu gì?

**Nhãn đề xuất:** answer=2; context=2; abstention_correct=None

**Lý do:** Xác định đúng *args được đóng gói thành tuple.

**Đáp án mong đợi / giới hạn corpus:** Một tuple chứa các đối số vị trí bổ sung.

**Đầu ra được chấp nhận:**
Theo tài liệu, các đối số bổ sung được gom bởi *args sẽ được "wrapped up in a tuple" — tức là gói lại trong một tuple (xem mục Tuples and Sequences) [72ba98c7f88046b6519961423f685ff5].

**Citation đã đọc:**
- `72ba98c7f88046b6519961423f685ff5`: True — Arbitrary Argument Lists nêu arguments wrapped up in tuple và ví dụ *args.

<details><summary>Context đã chuẩn bị</summary>

```text
[72ba98c7f88046b6519961423f685ff5 | https://docs.python.org/3.14/tutorial/controlflow.html | page python-3.14-ch04-u012]
4.9.4. Arbitrary Argument Lists

Finally, the least frequently used option is to specify that a function can be called with an arbitrary number of arguments. These arguments will be wrapped up in a tuple (see Tuples and Sequences). Before the variable number of arguments, zero or more normal arguments may occur.

def write_multiple_items(file, separator, *args):
    file.write(separator.join(args))
```

</details>

### D06 — answered

Tham số **name nhận những đối số nào và lưu trong kiểu dữ liệu gì?

**Nhãn đề xuất:** answer=2; context=2; abstention_correct=None

**Lý do:** Đủ keyword arguments dư, loại đối số đã khớp tham số hình thức, và kiểu dictionary.

**Đáp án mong đợi / giới hạn corpus:** Nhận các keyword arguments không ứng với tham số hình thức đã khai báo và lưu thành dictionary.

**Đầu ra được chấp nhận:**
Tham số cuối dạng **name nhận một dictionary (kiểu dict) chứa tất cả các keyword argument, trừ những đối số tương ứng với một tham số hình thức (formal parameter) đã có; nó có thể kết hợp với tham số dạng *name (nhận tuple các đối số vị trí vượt quá danh sách tham số hình thức), và *name phải đứng trước **name [a406cc7dac32b6727ecb688a6d3b9286].

**Citation đã đọc:**
- `a406cc7dac32b6727ecb688a6d3b9286`: True — Định nghĩa **name là dictionary chứa keyword arguments chưa khớp formal parameter; cũng hỗ trợ phần bổ sung *name.

<details><summary>Context đã chuẩn bị</summary>

```text
[a406cc7dac32b6727ecb688a6d3b9286 | https://docs.python.org/3.14/tutorial/controlflow.html | page python-3.14-ch04-u009]
When a final formal parameter of the form **name is present, it receives a dictionary (see Mapping Types — dict) containing all keyword arguments except for those corresponding to a formal parameter. This may be combined with a formal parameter of the form *name (described in the next subsection) which receives a tuple containing the positional arguments beyond the formal parameter list. (*name must occur before **name.) For example, if we define a function like this:
```

</details>

### D07 — error

Muốn tạo tuple chỉ chứa chuỗi hello thì chỉ viết ngoặc quanh giá trị có đủ không? Cú pháp cần thêm gì?

**Nhãn đề xuất:** answer=0; context=1; abstention_correct=None

**Lý do:** Context có tuple tổng quát (mức 1) nhưng không singleton; phản hồi từ chối kèm citations bị lỗi protocol, chấm all-case 0.

**Đáp án mong đợi / giới hạn corpus:** Không đủ; phải có dấu phẩy sau giá trị, ví dụ ('hello',) hoặc 'hello',.

**Đầu ra được chấp nhận:**
(không có)

**Lỗi:** protocol / ValueError

**Citation đã đọc:**

<details><summary>Context đã chuẩn bị</summary>

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

</details>

### D08 — answered

a.pop() không truyền index sẽ xóa và trả về phần tử nào? Điều gì xảy ra nếu a rỗng?

**Nhãn đề xuất:** answer=2; context=2; abstention_correct=None

**Lý do:** Đủ xóa/trả phần tử cuối và IndexError khi list rỗng.

**Đáp án mong đợi / giới hạn corpus:** Xóa và trả về phần tử cuối; nếu list rỗng thì phát sinh IndexError.

**Đầu ra được chấp nhận:**
a.pop() không truyền index sẽ xóa và trả về phần tử cuối cùng của list. Nếu list rỗng (hoặc index nằm ngoài phạm vi list), nó sẽ ném ra IndexError [e4976e7c8c03d1c6a37a18f46e14e9dd].

**Citation đã đọc:**
- `e4976e7c8c03d1c6a37a18f46e14e9dd`: True — Nêu pop không index xóa/trả phần tử cuối và IndexError với list rỗng.

<details><summary>Context đã chuẩn bị</summary>

```text
[e4976e7c8c03d1c6a37a18f46e14e9dd | https://docs.python.org/3.14/tutorial/datastructures.html | page python-3.14-ch05-u001]
Remove the item at the given position in the list, and return it. If no index is specified, a.pop() removes and returns the last item in the list. It raises an IndexError if the list is empty or the index is outside the list range.

list.clear()

Remove all items from the list. Similar to del a[:].

list.index(value[, start[, stop]])

Return zero-based index of the first occurrence of value in the list. Raises a ValueError if there is no such item.
```

</details>

### D09 — answered

Khi duyệt dictionary, dùng phương thức nào để lấy đồng thời khóa và giá trị tương ứng?

**Nhãn đề xuất:** answer=2; context=2; abstention_correct=None

**Lý do:** Đúng items() và lấy đồng thời key/value.

**Đáp án mong đợi / giới hạn corpus:** Dùng phương thức items(), ví dụ for k, v in d.items().

**Đầu ra được chấp nhận:**
Dùng phương thức items(): khi lặp qua dictionary, khóa và giá trị tương ứng có thể được lấy đồng thời bằng items(), ví dụ `for k, v in knights.items():` [fa52d5bbb11517433573b8febe0a1876].

**Citation đã đọc:**
- `fa52d5bbb11517433573b8febe0a1876`: True — Nêu items() lấy key/value đồng thời, có ví dụ for k,v.

<details><summary>Context đã chuẩn bị</summary>

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

</details>

### D10 — answered

Có hai sequence cần duyệt đồng thời thành từng cặp phần tử tương ứng. Tài liệu giới thiệu hàm nào?

**Nhãn đề xuất:** answer=2; context=2; abstention_correct=None

**Lý do:** Đúng zip() để ghép phần tử tương ứng của hai/nhiều sequence.

**Đáp án mong đợi / giới hạn corpus:** Dùng zip() để ghép các phần tử tương ứng khi duyệt hai hoặc nhiều sequence.

**Đầu ra được chấp nhận:**
Tài liệu giới thiệu hàm zip(). Để duyệt hai hoặc nhiều sequence cùng lúc, các phần tử có thể được ghép cặp bằng hàm zip(), ví dụ: for q, a in zip(questions, answers): ... [d0465c0ebf1bcc71b35de11057f991e9]

**Citation đã đọc:**
- `d0465c0ebf1bcc71b35de11057f991e9`: True — Nêu zip ghép entries của hai/nhiều sequence và ví dụ hai danh sách.

<details><summary>Context đã chuẩn bị</summary>

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

</details>

### D11 — answered

dir() không truyền đối số liệt kê những tên nào? Nó có tự liệt kê tên hàm và biến built-in không?

**Nhãn đề xuất:** answer=2; context=2; abstention_correct=None

**Lý do:** Đủ tên hiện tại gồm biến/module/hàm và không tự liệt kê các built-in.

**Đáp án mong đợi / giới hạn corpus:** Liệt kê các tên đang được định nghĩa như biến, module và hàm; không liệt kê các tên hàm và biến built-in.

**Đầu ra được chấp nhận:**
Khi không truyền đối số, dir() liệt kê các tên bạn đã định nghĩa hiện tại (mọi loại tên: biến, module, hàm, v.v.), ví dụ ['__builtins__', '__name__', 'a', 'fib', 'fibo', 'sys'] [653c279748bae8969296f00bc2941191]. Tuy nhiên dir() KHÔNG liệt kê tên của các hàm và biến built-in; muốn có danh sách đó thì chúng được định nghĩa trong module chuẩn builtins [653c279748bae8969296f00bc2941191].

**Citation đã đọc:**
- `653c279748bae8969296f00bc2941191`: True — Nêu tên hiện tại, mọi loại tên và loại trừ built-in; ví dụ dir().

<details><summary>Context đã chuẩn bị</summary>

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

</details>

### D12 — answered

Python dựa vào thông tin nào của file nguồn để quyết định module đã biên dịch có lỗi thời và cần biên dịch lại?

**Nhãn đề xuất:** answer=2; context=2; abstention_correct=None

**Lý do:** Đúng so sánh modification date của nguồn với bản đã biên dịch.

**Đáp án mong đợi / giới hạn corpus:** So sánh ngày/giờ sửa đổi của mã nguồn với phiên bản đã biên dịch.

**Đầu ra được chấp nhận:**
Python kiểm tra ngày sửa đổi (modification date) của file nguồn so với phiên bản đã biên dịch để xem module đã biên dịch có lỗi thời và cần biên dịch lại hay không; đây là quá trình hoàn toàn tự động [4b9311d6dabb880f0d9037d258d191b8].

**Citation đã đọc:**
- `4b9311d6dabb880f0d9037d258d191b8`: True — Nêu kiểm tra ngày sửa nguồn và compiled version để quyết định biên dịch lại.

<details><summary>Context đã chuẩn bị</summary>

```text
[4b9311d6dabb880f0d9037d258d191b8 | https://docs.python.org/3.14/tutorial/modules.html | page python-3.14-ch06-u004]
Python checks the modification date of the source against the compiled version to see if it’s out of date and needs to be recompiled. This is a completely automatic process. Also, the compiled modules are platform-independent, so the same library can be shared among systems with different architectures.
```

</details>

### D13 — answered

Với file vừa mở để đọc và đang ở đầu file, bỏ size hoặc truyền size âm cho f.read(size) sẽ đọc bao nhiêu? Rủi ro bộ nhớ được tài liệu nhắc là gì?

**Nhãn đề xuất:** answer=2; context=2; abstention_correct=None

**Lý do:** Đủ đọc toàn bộ khi bỏ size/size âm và cảnh báo file lớn hơn bộ nhớ.

**Đáp án mong đợi / giới hạn corpus:** Đọc toàn bộ nội dung file; file quá lớn có thể vượt bộ nhớ máy.

**Đầu ra được chấp nhận:**
Khi bỏ size hoặc truyền size âm cho f.read(size), toàn bộ nội dung file sẽ được đọc và trả về (chuỗi ở text mode, bytes ở binary mode) [b2e4e2a1efb032538c84a9e87be3cfb4]. Rủi ro bộ nhớ mà tài liệu nhắc là: "it's your problem if the file is twice as large as your machine's memory" — tức nếu file lớn gấp đôi bộ nhớ máy thì đó là vấn đề của bạn [b2e4e2a1efb032538c84a9e87be3cfb4].

**Citation đã đọc:**
- `b2e4e2a1efb032538c84a9e87be3cfb4`: True — Nêu text/bytes, trường hợp size omitted/negative, cảnh báo bộ nhớ và nhánh otherwise tối đa size.

<details><summary>Context đã chuẩn bị</summary>

```text
[b2e4e2a1efb032538c84a9e87be3cfb4 | https://docs.python.org/3.14/tutorial/inputoutput.html | page python-3.14-ch07-u005]
To read a file’s contents, call f.read(size), which reads some quantity of data and returns it as a string (in text mode) or bytes object (in binary mode). size is an optional numeric argument. When size is omitted or negative, the entire contents of the file will be read and returned; it’s your problem if the file is twice as large as your machine’s memory. Otherwise, at most size characters (in text mode) or size bytes (in binary mode) are read and returned. If the end of the file has been 
```

</details>

### D14 — answered

Giá trị f.tell() trong binary mode và text mode có ý nghĩa khác nhau thế nào?

**Nhãn đề xuất:** answer=2; context=2; abstention_correct=None

**Lý do:** Đủ byte offset trong binary và opaque position trong text.

**Đáp án mong đợi / giới hạn corpus:** Binary mode: số byte tính từ đầu file. Text mode: một số opaque biểu diễn vị trí, không nên hiểu là số byte.

**Đầu ra được chấp nhận:**
Trong binary mode, f.tell() trả về một số nguyên là vị trí hiện tại của file object, được biểu diễn bằng số byte tính từ đầu file. Trong text mode, f.tell() trả về một "opaque number" (con số không minh bạch về ý nghĩa byte) [9c4ec9a68dac484801d37366b0214e51]. Liên quan đến điều này, với text file (mở không có 'b' trong chuỗi mode), chỉ cho phép seek tương đối so với đầu file (ngoại lệ là seek tới cuối file với seek(0, 2)), và các giá trị offset hợp lệ duy nhất là những giá trị do f.tell() trả về, hoặc 0; mọi offset khác gây ra hành vi không xác định [dbb1c2a57f3bdb25359e5a45739375d9].

**Citation đã đọc:**
- `9c4ec9a68dac484801d37366b0214e51`: True — Nêu trực tiếp byte position ở binary và opaque number ở text.
- `dbb1c2a57f3bdb25359e5a45739375d9`: True — Hỗ trợ riêng phần bổ sung về các offset seek hợp lệ cho text.

<details><summary>Context đã chuẩn bị</summary>

```text
[9c4ec9a68dac484801d37366b0214e51 | https://docs.python.org/3.14/tutorial/inputoutput.html | page python-3.14-ch07-u006]
f.tell() returns an integer giving the file object’s current position in the file represented as number of bytes from the beginning of the file when in binary mode and an opaque number when in text mode.

[dbb1c2a57f3bdb25359e5a45739375d9 | https://docs.python.org/3.14/tutorial/inputoutput.html | page python-3.14-ch07-u006]
In text files (those opened without a b in the mode string), only seeks relative to the beginning of the file are allowed (the exception being seeking to the very file end with seek(0, 2)) and the only valid offset values are those returned from the f.tell(), or zero. Any other offset value produces undefined behaviour.
```

</details>

### D15 — answered

Trong try...except, khối else phải đặt sau phần nào và được dùng khi nào?

**Nhãn đề xuất:** answer=2; context=2; abstention_correct=None

**Lý do:** Đủ else sau tất cả except và chỉ chạy khi try không phát sinh ngoại lệ.

**Đáp án mong đợi / giới hạn corpus:** Đặt sau tất cả các except; dùng cho code chỉ chạy khi khối try không phát sinh ngoại lệ.

**Đầu ra được chấp nhận:**
Khối else là tùy chọn của câu lệnh try … except; khi có mặt, nó phải đặt sau tất cả các khối except. Nó hữu ích cho đoạn mã phải được thực thi nếu khối try không ném ra ngoại lệ (tức là chạy khi không có ngoại lệ xảy ra) [89cb0b58f013c40c3ef13c336fcb8792].

**Citation đã đọc:**
- `89cb0b58f013c40c3ef13c336fcb8792`: True — Hỗ trợ cả vị trí sau tất cả except và điều kiện try không có ngoại lệ.

<details><summary>Context đã chuẩn bị</summary>

```text
[89cb0b58f013c40c3ef13c336fcb8792 | https://docs.python.org/3.14/tutorial/errors.html | page python-3.14-ch08-u003]
The try … except statement has an optional else clause, which, when present, must follow all except clauses. It is useful for code that must be executed if the try clause does not raise an exception. For example:

[e029e5d8abe70414636c4b8d53ae1e44 | https://docs.python.org/3.14/tutorial/controlflow.html | page python-3.14-ch04-u003]
When used with a loop, the else clause has more in common with the else clause of a try statement than it does with that of if statements: a try statement’s else clause runs when no exception occurs, and a loop’s else clause runs when no break occurs. For more on the try statement and exceptions, see Handling Exceptions.
```

</details>

### D16 — abstain

Chỉ dựa trên tài liệu đã cung cấp, khi một task trong asyncio.TaskGroup lỗi, các task còn lại được hủy và chờ kết thúc như thế nào?

**Nhãn đề xuất:** answer=None; context=None; abstention_correct=True

**Lý do:** Đã đọc câu từ chối: giới hạn ở tài liệu/context, không nêu cơ chế kỹ thuật hay đoán ngoại lệ ngoài corpus; đúng theo absence audit của benchmark.

**Đáp án mong đợi / giới hạn corpus:** Corpus không có phần giải thích asyncio hoặc TaskGroup. Các mục vòng lặp/ngoại lệ không quy định ngữ nghĩa hủy task bất đồng bộ.

**Đầu ra được chấp nhận:**
Không đủ bằng chứng trong tài liệu để trả lời: context hiện tại chỉ chứa danh sách tên ngoại lệ/hàm tích hợp của Python, không có nội dung nào về asyncio.TaskGroup hay cách hủy và chờ các task còn lại khi một task lỗi.

**Citation đã đọc:**

<details><summary>Context đã chuẩn bị</summary>

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

</details>

### D17 — abstain

Tài liệu đã cung cấp hướng dẫn dùng @dataclass(frozen=True) để ngăn gán lại thuộc tính như thế nào và phát sinh ngoại lệ gì khi cố gán?

**Nhãn đề xuất:** answer=None; context=None; abstention_correct=True

**Lý do:** Đã đọc câu từ chối: giới hạn ở tài liệu/context, không nêu cơ chế kỹ thuật hay đoán ngoại lệ ngoài corpus; đúng theo absence audit của benchmark.

**Đáp án mong đợi / giới hạn corpus:** dataclasses chỉ được nhắc làm ví dụ lớp có thứ tự thuộc tính trong match; frozen xuất hiện trong tên built-in frozenset. Không có hướng dẫn frozen=True hoặc ngoại lệ khi gán.

**Đầu ra được chấp nhận:**
Không đủ bằng chứng trong tài liệu để trả lời: ngữ cảnh hiện có chỉ nói về xử lý ngoại lệ/chaining trong tutorial errors, không có nội dung về @dataclass(frozen=True) hay ngoại lệ khi cố gán lại thuộc tính.

**Citation đã đọc:**

<details><summary>Context đã chuẩn bị</summary>

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

</details>

## TF-IDF 800 / arrival

### D01 — answered

Muốn viết đường dẫn Windows mà các ký tự như \n và \t không bị hiểu là xuống dòng hoặc tab, tiền tố chuỗi nào được tài liệu hướng dẫn?

**Nhãn đề xuất:** answer=2; context=2; abstention_correct=None

**Lý do:** Đúng tiền tố r và ý nghĩa giữ nguyên escape; ví dụ/giới hạn dấu backslash có trong nguồn.

**Đáp án mong đợi / giới hạn corpus:** Đặt tiền tố r trước dấu nháy để tạo raw string.

**Đầu ra được chấp nhận:**
Tài liệu hướng dẫn dùng tiền tố r (raw string) trước dấu nháy đầu tiên, ví dụ r'C:\this\name', để các ký tự sau \ không bị hiểu là ký tự đặc biệt như \t (tab) hay \n (xuống dòng) [5046e99636180b57c2960fedf1d3566c]. Lưu ý: raw string không thể kết thúc bằng số lẻ ký tự \ [5046e99636180b57c2960fedf1d3566c].

**Citation đã đọc:**
- `5046e99636180b57c2960fedf1d3566c`: True — Đoạn raw strings nêu tiền tố r, ví dụ Windows path, escape và giới hạn backslash cuối.

<details><summary>Context đã chuẩn bị</summary>

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

</details>

### D02 — answered

Khi đánh chỉ số chuỗi từ phía cuối, -1 và -2 chỉ ký tự nào? Vì sao không bắt đầu bằng -0?

**Nhãn đề xuất:** answer=2; context=2; abstention_correct=None

**Lý do:** Đủ cả -1 là ký tự cuối, -2 áp cuối và -0 bằng 0.

**Đáp án mong đợi / giới hạn corpus:** -1 chỉ ký tự cuối, -2 chỉ ký tự áp cuối; -0 bằng 0 nên chỉ số âm bắt đầu từ -1.

**Đầu ra được chấp nhận:**
Theo tài liệu, với chuỗi 'Python' (word), word[-1] là ký tự cuối cùng ('n') và word[-2] là ký tự áp chót ('o'). Tài liệu giải thích rằng vì -0 giống hệt 0, nên các chỉ số âm bắt đầu từ -1 [07eab24fdef0d6f3c82bb56fb67407ce].

**Citation đã đọc:**
- `07eab24fdef0d6f3c82bb56fb67407ce`: True — Ví dụ word[-1]/[-2] và câu -0 giống 0 hỗ trợ đủ điều kiện.

<details><summary>Context đã chuẩn bị</summary>

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

</details>

### D03 — answered

Ví dụ list(range(5, 10)) trong tài liệu cho ra danh sách nào?

**Nhãn đề xuất:** answer=2; context=2; abstention_correct=None

**Lý do:** Đúng toàn bộ danh sách [5, 6, 7, 8, 9].

**Đáp án mong đợi / giới hạn corpus:** [5, 6, 7, 8, 9]; cận 10 không được lấy.

**Đầu ra được chấp nhận:**
Trong tài liệu, ví dụ `list(range(5, 10))` cho ra danh sách `[5, 6, 7, 8, 9]` [5b0389b2014ead261047a7ea77039951].

**Citation đã đọc:**
- `5b0389b2014ead261047a7ea77039951`: True — Ví dụ nguyên văn list(range(5,10)) và danh sách kết quả.

<details><summary>Context đã chuẩn bị</summary>

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

</details>

### D04 — error

Nếu có vòng lặp for lồng trong while, break nằm trong for sẽ thoát vòng nào theo quy tắc của tài liệu?

**Nhãn đề xuất:** answer=0; context=0; abstention_correct=None

**Lý do:** Thiếu evidence innermost trong context; từ chối kèm citations bị lỗi protocol.

**Đáp án mong đợi / giới hạn corpus:** Thoát vòng for ở trong cùng bao quanh break, không tự động thoát cả vòng while bên ngoài.

**Đầu ra được chấp nhận:**
(không có)

**Lỗi:** protocol / ValueError

**Citation đã đọc:**

<details><summary>Context đã chuẩn bị</summary>

```text
[e09df3f01953e055de669d3402d7ddac | https://docs.python.org/3.14/tutorial/controlflow.html | page python-3.14-ch04-u002]
4.5. else Clauses on Loops

In a for or while loop the break statement may be paired with an else clause. If the loop finishes without executing the break, the else clause executes.

In a for loop, the else clause is executed after the loop finishes its final iteration, that is, if no break occurred.

In a while loop, it’s executed after the loop’s condition becomes false.
```

</details>

### D05 — answered

Các đối số bổ sung được gom bởi *args trong định nghĩa hàm có kiểu cấu trúc dữ liệu gì?

**Nhãn đề xuất:** answer=2; context=2; abstention_correct=None

**Lý do:** Xác định đúng *args được đóng gói thành tuple.

**Đáp án mong đợi / giới hạn corpus:** Một tuple chứa các đối số vị trí bổ sung.

**Đầu ra được chấp nhận:**
Các đối số bổ sung được gom bởi *args sẽ được đóng gói (wrapped up) trong một tuple [72ba98c7f88046b6519961423f685ff5].

**Citation đã đọc:**
- `72ba98c7f88046b6519961423f685ff5`: True — Arbitrary Argument Lists nêu arguments wrapped up in tuple và ví dụ *args.

<details><summary>Context đã chuẩn bị</summary>

```text
[72ba98c7f88046b6519961423f685ff5 | https://docs.python.org/3.14/tutorial/controlflow.html | page python-3.14-ch04-u012]
4.9.4. Arbitrary Argument Lists

Finally, the least frequently used option is to specify that a function can be called with an arbitrary number of arguments. These arguments will be wrapped up in a tuple (see Tuples and Sequences). Before the variable number of arguments, zero or more normal arguments may occur.

def write_multiple_items(file, separator, *args):
    file.write(separator.join(args))

[563b2a10f1a146b6dabbe575bdc0c257 | https://docs.python.org/3.14/tutorial/controlflow.html | page python-3.14-ch04-u011]
TypeError: combined_example() got some positional-only arguments passed as keyword arguments: 'pos_only'
```

</details>

### D06 — abstain

Tham số **name nhận những đối số nào và lưu trong kiểu dữ liệu gì?

**Nhãn đề xuất:** answer=0; context=0; abstention_correct=None

**Lý do:** Context zip()/thông báo lỗi không hỗ trợ **name; false refusal.

**Đáp án mong đợi / giới hạn corpus:** Nhận các keyword arguments không ứng với tham số hình thức đã khai báo và lưu thành dictionary.

**Đầu ra được chấp nhận:**
Không đủ bằng chứng trong tài liệu để trả lời: context hiện tại chỉ nói về zip() và thông báo lỗi, không có nội dung về tham số **name hay kiểu dữ liệu mà nó lưu.

**Citation đã đọc:**

<details><summary>Context đã chuẩn bị</summary>

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

</details>

### D07 — answered

Muốn tạo tuple chỉ chứa chuỗi hello thì chỉ viết ngoặc quanh giá trị có đủ không? Cú pháp cần thêm gì?

**Nhãn đề xuất:** answer=2; context=2; abstention_correct=None

**Lý do:** Nêu rõ chỉ ngoặc không đủ, cần dấu phẩy sau giá trị và ví dụ tuple một phần tử.

**Đáp án mong đợi / giới hạn corpus:** Không đủ; phải có dấu phẩy sau giá trị, ví dụ ('hello',) hoặc 'hello',.

**Đầu ra được chấp nhận:**
Không đủ. Chỉ đặt ngoặc quanh một giá trị là không đủ để tạo tuple một phần tử; cần thêm dấu phẩy theo sau giá trị (trailing comma). Ví dụ: singleton = 'hello',  # chú ý dấu phẩy cuối, kết quả là ('hello',) với len bằng 1. Tuple rỗng thì tạo bằng cặp ngoặc rỗng (). [a14a0c62dbc9ade9275bb1cfd18bbc57]

**Citation đã đọc:**
- `a14a0c62dbc9ade9275bb1cfd18bbc57`: True — Nêu một phần tử phải có comma, ngoặc không đủ; có ví dụ singleton hello.

<details><summary>Context đã chuẩn bị</summary>

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

</details>

### D08 — answered

a.pop() không truyền index sẽ xóa và trả về phần tử nào? Điều gì xảy ra nếu a rỗng?

**Nhãn đề xuất:** answer=2; context=2; abstention_correct=None

**Lý do:** Đủ xóa/trả phần tử cuối và IndexError khi list rỗng.

**Đáp án mong đợi / giới hạn corpus:** Xóa và trả về phần tử cuối; nếu list rỗng thì phát sinh IndexError.

**Đầu ra được chấp nhận:**
a.pop() không truyền index sẽ xóa và trả về phần tử cuối cùng trong list. Nếu list rỗng (hoặc index nằm ngoài phạm vi list), nó sẽ ném ra IndexError [e4976e7c8c03d1c6a37a18f46e14e9dd].

**Citation đã đọc:**
- `e4976e7c8c03d1c6a37a18f46e14e9dd`: True — Nêu pop không index xóa/trả phần tử cuối và IndexError với list rỗng.

<details><summary>Context đã chuẩn bị</summary>

```text
[e4976e7c8c03d1c6a37a18f46e14e9dd | https://docs.python.org/3.14/tutorial/datastructures.html | page python-3.14-ch05-u001]
Remove the item at the given position in the list, and return it. If no index is specified, a.pop() removes and returns the last item in the list. It raises an IndexError if the list is empty or the index is outside the list range.

list.clear()

Remove all items from the list. Similar to del a[:].

list.index(value[, start[, stop]])

Return zero-based index of the first occurrence of value in the list. Raises a ValueError if there is no such item.
```

</details>

### D09 — error

Khi duyệt dictionary, dùng phương thức nào để lấy đồng thời khóa và giá trị tương ứng?

**Nhãn đề xuất:** answer=0; context=0; abstention_correct=None

**Lý do:** Context chỉ định nghĩa dictionary, không có items(); lỗi protocol do từ chối kèm citation.

**Đáp án mong đợi / giới hạn corpus:** Dùng phương thức items(), ví dụ for k, v in d.items().

**Đầu ra được chấp nhận:**
(không có)

**Lỗi:** protocol / ValueError

**Citation đã đọc:**

<details><summary>Context đã chuẩn bị</summary>

```text
[22d13ffc003595146adb41b1a1676227 | https://docs.python.org/3.14/tutorial/datastructures.html | page python-3.14-ch05-u006]
It is best to think of a dictionary as a set of key: value pairs, with the requirement that the keys are unique (within one dictionary). A pair of braces creates an empty dictionary: {}. Placing a comma-separated list of key:value pairs within the braces adds initial key:value pairs to the dictionary; this is also the way dictionaries are written on output.
```

</details>

### D10 — abstain

Có hai sequence cần duyệt đồng thời thành từng cặp phần tử tương ứng. Tài liệu giới thiệu hàm nào?

**Nhãn đề xuất:** answer=0; context=1; abstention_correct=None

**Lý do:** Context có zip(*matrix) nhưng thiếu giải thích duyệt hai sequence (mức 1); false refusal.

**Đáp án mong đợi / giới hạn corpus:** Dùng zip() để ghép các phần tử tương ứng khi duyệt hai hoặc nhiều sequence.

**Đầu ra được chấp nhận:**
Không đủ bằng chứng trong tài liệu để trả lời: context hiện có chỉ nhắc tới hàm zip trong ví dụ `list(zip(*matrix))` để chuyển vị ma trận, không có đoạn nào giới thiệu hàm dùng để duyệt đồng thời hai sequence thành từng cặp phần tử tương ứng.

**Citation đã đọc:**

<details><summary>Context đã chuẩn bị</summary>

```text
[22d13ffc003595146adb41b1a1676227 | https://docs.python.org/3.14/tutorial/datastructures.html | page python-3.14-ch05-u006]
It is best to think of a dictionary as a set of key: value pairs, with the requirement that the keys are unique (within one dictionary). A pair of braces creates an empty dictionary: {}. Placing a comma-separated list of key:value pairs within the braces adds initial key:value pairs to the dictionary; this is also the way dictionaries are written on output.

[05405500dec053b3c7600a61076a5941 | https://docs.python.org/3.14/tutorial/datastructures.html | page python-3.14-ch05-u004]
>>> list(zip(*matrix))
[(1, 5, 9), (2, 6, 10), (3, 7, 11), (4, 8, 12)]

See Unpacking Argument Lists for details on the asterisk in this line.
```

</details>

### D11 — answered

dir() không truyền đối số liệt kê những tên nào? Nó có tự liệt kê tên hàm và biến built-in không?

**Nhãn đề xuất:** answer=2; context=2; abstention_correct=None

**Lý do:** Đủ tên hiện tại gồm biến/module/hàm và không tự liệt kê các built-in.

**Đáp án mong đợi / giới hạn corpus:** Liệt kê các tên đang được định nghĩa như biến, module và hàm; không liệt kê các tên hàm và biến built-in.

**Đầu ra được chấp nhận:**
Khi không truyền đối số, dir() liệt kê các tên bạn đã định nghĩa hiện tại (ví dụ ['__builtins__', '__name__', 'a', 'fib', 'fibo', 'sys']), và nó liệt kê mọi loại tên: biến, module, hàm, v.v. [653c279748bae8969296f00bc2941191] Tuy nhiên, dir() KHÔNG liệt kê tên của các hàm và biến built-in; muốn có danh sách đó thì chúng được định nghĩa trong module chuẩn builtins [653c279748bae8969296f00bc2941191].

**Citation đã đọc:**
- `653c279748bae8969296f00bc2941191`: True — Nêu tên hiện tại, mọi loại tên và loại trừ built-in; ví dụ dir().

<details><summary>Context đã chuẩn bị</summary>

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

</details>

### D12 — answered

Python dựa vào thông tin nào của file nguồn để quyết định module đã biên dịch có lỗi thời và cần biên dịch lại?

**Nhãn đề xuất:** answer=2; context=2; abstention_correct=None

**Lý do:** Đúng so sánh modification date của nguồn với bản đã biên dịch.

**Đáp án mong đợi / giới hạn corpus:** So sánh ngày/giờ sửa đổi của mã nguồn với phiên bản đã biên dịch.

**Đầu ra được chấp nhận:**
Python kiểm tra ngày sửa đổi (modification date) của file nguồn so với phiên bản đã biên dịch để xem module đã biên dịch có lỗi thời và cần biên dịch lại hay không; đây là quá trình hoàn toàn tự động [4b9311d6dabb880f0d9037d258d191b8].

**Citation đã đọc:**
- `4b9311d6dabb880f0d9037d258d191b8`: True — Nêu kiểm tra ngày sửa nguồn và compiled version để quyết định biên dịch lại.

<details><summary>Context đã chuẩn bị</summary>

```text
[4b9311d6dabb880f0d9037d258d191b8 | https://docs.python.org/3.14/tutorial/modules.html | page python-3.14-ch06-u004]
Python checks the modification date of the source against the compiled version to see if it’s out of date and needs to be recompiled. This is a completely automatic process. Also, the compiled modules are platform-independent, so the same library can be shared among systems with different architectures.

[5232afaeda65d6380749218d8b7fbbe6 | https://docs.python.org/3.14/tutorial/modules.html | page python-3.14-ch06-u003]
6.1.3. “Compiled” Python files
```

</details>

### D13 — answered

Với file vừa mở để đọc và đang ở đầu file, bỏ size hoặc truyền size âm cho f.read(size) sẽ đọc bao nhiêu? Rủi ro bộ nhớ được tài liệu nhắc là gì?

**Nhãn đề xuất:** answer=2; context=2; abstention_correct=None

**Lý do:** Đủ đọc toàn bộ khi bỏ size/size âm và cảnh báo file lớn hơn bộ nhớ.

**Đáp án mong đợi / giới hạn corpus:** Đọc toàn bộ nội dung file; file quá lớn có thể vượt bộ nhớ máy.

**Đầu ra được chấp nhận:**
Khi bỏ size hoặc truyền size âm cho f.read(size), toàn bộ nội dung của file sẽ được đọc và trả về (dưới dạng chuỗi ở text mode hoặc bytes ở binary mode) [b2e4e2a1efb032538c84a9e87be3cfb4]. Rủi ro bộ nhớ mà tài liệu nhắc là: "it's your problem if the file is twice as large as your machine's memory" — tức là nếu file lớn gấp đôi bộ nhớ máy thì đó là vấn đề của bạn [b2e4e2a1efb032538c84a9e87be3cfb4].

**Citation đã đọc:**
- `b2e4e2a1efb032538c84a9e87be3cfb4`: True — Nêu text/bytes, trường hợp size omitted/negative, cảnh báo bộ nhớ và nhánh otherwise tối đa size.

<details><summary>Context đã chuẩn bị</summary>

```text
[b2e4e2a1efb032538c84a9e87be3cfb4 | https://docs.python.org/3.14/tutorial/inputoutput.html | page python-3.14-ch07-u005]
To read a file’s contents, call f.read(size), which reads some quantity of data and returns it as a string (in text mode) or bytes object (in binary mode). size is an optional numeric argument. When size is omitted or negative, the entire contents of the file will be read and returned; it’s your problem if the file is twice as large as your machine’s memory. Otherwise, at most size characters (in text mode) or size bytes (in binary mode) are read and returned. If the end of the file has been 

[1dc34e861c5e5fadc4724e725df10931 | https://docs.python.org/3.14/tutorial/inputoutput.html | page python-3.14-ch07-u005]
reached, f.read() will return an empty string ('').
```

</details>

### D14 — answered

Giá trị f.tell() trong binary mode và text mode có ý nghĩa khác nhau thế nào?

**Nhãn đề xuất:** answer=2; context=2; abstention_correct=None

**Lý do:** Đủ byte offset trong binary và opaque position trong text.

**Đáp án mong đợi / giới hạn corpus:** Binary mode: số byte tính từ đầu file. Text mode: một số opaque biểu diễn vị trí, không nên hiểu là số byte.

**Đầu ra được chấp nhận:**
Theo tài liệu: f.tell() trả về một số nguyên cho biết vị trí hiện tại của file object trong file — ở binary mode đó là số byte tính từ đầu file, còn ở text mode đó là một "opaque number" (con số không mang ý nghĩa trực tiếp, không phải số byte) [9c4ec9a68dac484801d37366b0214e51].

**Citation đã đọc:**
- `9c4ec9a68dac484801d37366b0214e51`: True — Nêu trực tiếp byte position ở binary và opaque number ở text.

<details><summary>Context đã chuẩn bị</summary>

```text
[9c4ec9a68dac484801d37366b0214e51 | https://docs.python.org/3.14/tutorial/inputoutput.html | page python-3.14-ch07-u006]
f.tell() returns an integer giving the file object’s current position in the file represented as number of bytes from the beginning of the file when in binary mode and an opaque number when in text mode.

[e3dd727e9d10ff3ef55e9dda334b3b96 | https://docs.python.org/3.14/tutorial/inputoutput.html | page python-3.14-ch07-u005]
encoding when opening file in binary mode.

[5232afaeda65d6380749218d8b7fbbe6 | https://docs.python.org/3.14/tutorial/modules.html | page python-3.14-ch06-u003]
6.1.3. “Compiled” Python files
```

</details>

### D15 — answered

Trong try...except, khối else phải đặt sau phần nào và được dùng khi nào?

**Nhãn đề xuất:** answer=2; context=2; abstention_correct=None

**Lý do:** Đủ else sau tất cả except và chỉ chạy khi try không phát sinh ngoại lệ.

**Đáp án mong đợi / giới hạn corpus:** Đặt sau tất cả các except; dùng cho code chỉ chạy khi khối try không phát sinh ngoại lệ.

**Đầu ra được chấp nhận:**
Khối else là tùy chọn của câu lệnh try … except; khi có mặt, nó phải đặt sau tất cả các khối except. Nó hữu ích cho đoạn mã phải được thực thi nếu khối try không ném ra ngoại lệ — tức là else chạy khi không có ngoại lệ xảy ra [89cb0b58f013c40c3ef13c336fcb8792][e029e5d8abe70414636c4b8d53ae1e44].

**Citation đã đọc:**
- `89cb0b58f013c40c3ef13c336fcb8792`: True — Hỗ trợ cả vị trí sau tất cả except và điều kiện try không có ngoại lệ.
- `e029e5d8abe70414636c4b8d53ae1e44`: True — Hỗ trợ riêng mệnh đề else của try chạy khi không có ngoại lệ; vị trí except được citation khác hỗ trợ.

<details><summary>Context đã chuẩn bị</summary>

```text
[89cb0b58f013c40c3ef13c336fcb8792 | https://docs.python.org/3.14/tutorial/errors.html | page python-3.14-ch08-u003]
The try … except statement has an optional else clause, which, when present, must follow all except clauses. It is useful for code that must be executed if the try clause does not raise an exception. For example:

[e029e5d8abe70414636c4b8d53ae1e44 | https://docs.python.org/3.14/tutorial/controlflow.html | page python-3.14-ch04-u003]
When used with a loop, the else clause has more in common with the else clause of a try statement than it does with that of if statements: a try statement’s else clause runs when no exception occurs, and a loop’s else clause runs when no break occurs. For more on the try statement and exceptions, see Handling Exceptions.
```

</details>

### D16 — abstain

Chỉ dựa trên tài liệu đã cung cấp, khi một task trong asyncio.TaskGroup lỗi, các task còn lại được hủy và chờ kết thúc như thế nào?

**Nhãn đề xuất:** answer=None; context=None; abstention_correct=True

**Lý do:** Đã đọc câu từ chối: giới hạn ở tài liệu/context, không nêu cơ chế kỹ thuật hay đoán ngoại lệ ngoài corpus; đúng theo absence audit của benchmark.

**Đáp án mong đợi / giới hạn corpus:** Corpus không có phần giải thích asyncio hoặc TaskGroup. Các mục vòng lặp/ngoại lệ không quy định ngữ nghĩa hủy task bất đồng bộ.

**Đầu ra được chấp nhận:**
Không đủ bằng chứng trong tài liệu để trả lời: context hiện có chỉ chứa nội dung về dùng Python như máy tính và câu lệnh pass, không có thông tin về asyncio.TaskGroup hay cách hủy/chờ các task còn lại khi một task lỗi.

**Citation đã đọc:**

<details><summary>Context đã chuẩn bị</summary>

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

</details>

### D17 — abstain

Tài liệu đã cung cấp hướng dẫn dùng @dataclass(frozen=True) để ngăn gán lại thuộc tính như thế nào và phát sinh ngoại lệ gì khi cố gán?

**Nhãn đề xuất:** answer=None; context=None; abstention_correct=True

**Lý do:** Đã đọc câu từ chối: giới hạn ở tài liệu/context, không nêu cơ chế kỹ thuật hay đoán ngoại lệ ngoài corpus; đúng theo absence audit của benchmark.

**Đáp án mong đợi / giới hạn corpus:** dataclasses chỉ được nhắc làm ví dụ lớp có thứ tự thuộc tính trong match; frozen xuất hiện trong tên built-in frozenset. Không có hướng dẫn frozen=True hoặc ngoại lệ khi gán.

**Đầu ra được chấp nhận:**
Không đủ bằng chứng trong tài liệu để trả lời: context hiện có chỉ nói về except clause và tính bất biến của chuỗi, không có hướng dẫn dùng @dataclass(frozen=True) hay ngoại lệ phát sinh khi cố gán lại thuộc tính.

**Citation đã đọc:**

<details><summary>Context đã chuẩn bị</summary>

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

</details>

## Hybrid 800 / arrival

### D01 — answered

Muốn viết đường dẫn Windows mà các ký tự như \n và \t không bị hiểu là xuống dòng hoặc tab, tiền tố chuỗi nào được tài liệu hướng dẫn?

**Nhãn đề xuất:** answer=2; context=2; abstention_correct=None

**Lý do:** Đúng tiền tố r và ý nghĩa giữ nguyên escape; ví dụ/giới hạn dấu backslash có trong nguồn.

**Đáp án mong đợi / giới hạn corpus:** Đặt tiền tố r trước dấu nháy để tạo raw string.

**Đầu ra được chấp nhận:**
Tài liệu hướng dẫn dùng tiền tố r (raw string) trước dấu nháy đầu tiên, ví dụ r'C:\this\name', để các ký tự sau \ không bị hiểu là ký tự đặc biệt như \t (tab) hay \n (xuống dòng) [5046e99636180b57c2960fedf1d3566c]. Lưu ý: raw string không được kết thúc bằng số lẻ ký tự \ [5046e99636180b57c2960fedf1d3566c].

**Citation đã đọc:**
- `5046e99636180b57c2960fedf1d3566c`: True — Đoạn raw strings nêu tiền tố r, ví dụ Windows path, escape và giới hạn backslash cuối.

<details><summary>Context đã chuẩn bị</summary>

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

</details>

### D02 — answered

Khi đánh chỉ số chuỗi từ phía cuối, -1 và -2 chỉ ký tự nào? Vì sao không bắt đầu bằng -0?

**Nhãn đề xuất:** answer=2; context=2; abstention_correct=None

**Lý do:** Đủ cả -1 là ký tự cuối, -2 áp cuối và -0 bằng 0.

**Đáp án mong đợi / giới hạn corpus:** -1 chỉ ký tự cuối, -2 chỉ ký tự áp cuối; -0 bằng 0 nên chỉ số âm bắt đầu từ -1.

**Đầu ra được chấp nhận:**
Với chuỗi 'Python' trong ví dụ: word[-1] là ký tự cuối cùng ('n'), còn word[-2] là ký tự áp chót ('o') [07eab24fdef0d6f3c82bb56fb67407ce]. Không bắt đầu bằng -0 vì -0 bằng 0, nên các chỉ số âm bắt đầu từ -1 [07eab24fdef0d6f3c82bb56fb67407ce].

**Citation đã đọc:**
- `07eab24fdef0d6f3c82bb56fb67407ce`: True — Ví dụ word[-1]/[-2] và câu -0 giống 0 hỗ trợ đủ điều kiện.

<details><summary>Context đã chuẩn bị</summary>

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

</details>

### D03 — answered

Ví dụ list(range(5, 10)) trong tài liệu cho ra danh sách nào?

**Nhãn đề xuất:** answer=2; context=2; abstention_correct=None

**Lý do:** Đúng toàn bộ danh sách [5, 6, 7, 8, 9].

**Đáp án mong đợi / giới hạn corpus:** [5, 6, 7, 8, 9]; cận 10 không được lấy.

**Đầu ra được chấp nhận:**
Theo tài liệu, `list(range(5, 10))` cho ra `[5, 6, 7, 8, 9]` [5b0389b2014ead261047a7ea77039951].

**Citation đã đọc:**
- `5b0389b2014ead261047a7ea77039951`: True — Ví dụ nguyên văn list(range(5,10)) và danh sách kết quả.

<details><summary>Context đã chuẩn bị</summary>

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

</details>

### D04 — error

Nếu có vòng lặp for lồng trong while, break nằm trong for sẽ thoát vòng nào theo quy tắc của tài liệu?

**Nhãn đề xuất:** answer=0; context=0; abstention_correct=None

**Lý do:** Context loop else thiếu innermost; lỗi protocol do từ chối kèm citation.

**Đáp án mong đợi / giới hạn corpus:** Thoát vòng for ở trong cùng bao quanh break, không tự động thoát cả vòng while bên ngoài.

**Đầu ra được chấp nhận:**
(không có)

**Lỗi:** protocol / ValueError

**Citation đã đọc:**

<details><summary>Context đã chuẩn bị</summary>

```text
[e09df3f01953e055de669d3402d7ddac | https://docs.python.org/3.14/tutorial/controlflow.html | page python-3.14-ch04-u002]
4.5. else Clauses on Loops

In a for or while loop the break statement may be paired with an else clause. If the loop finishes without executing the break, the else clause executes.

In a for loop, the else clause is executed after the loop finishes its final iteration, that is, if no break occurred.

In a while loop, it’s executed after the loop’s condition becomes false.
```

</details>

### D05 — answered

Các đối số bổ sung được gom bởi *args trong định nghĩa hàm có kiểu cấu trúc dữ liệu gì?

**Nhãn đề xuất:** answer=2; context=2; abstention_correct=None

**Lý do:** Xác định đúng *args được đóng gói thành tuple.

**Đáp án mong đợi / giới hạn corpus:** Một tuple chứa các đối số vị trí bổ sung.

**Đầu ra được chấp nhận:**
Các đối số bổ sung được gom bởi *args sẽ được gói lại trong một tuple (xem phần Tuples and Sequences) [72ba98c7f88046b6519961423f685ff5].

**Citation đã đọc:**
- `72ba98c7f88046b6519961423f685ff5`: True — Arbitrary Argument Lists nêu arguments wrapped up in tuple và ví dụ *args.

<details><summary>Context đã chuẩn bị</summary>

```text
[72ba98c7f88046b6519961423f685ff5 | https://docs.python.org/3.14/tutorial/controlflow.html | page python-3.14-ch04-u012]
4.9.4. Arbitrary Argument Lists

Finally, the least frequently used option is to specify that a function can be called with an arbitrary number of arguments. These arguments will be wrapped up in a tuple (see Tuples and Sequences). Before the variable number of arguments, zero or more normal arguments may occur.

def write_multiple_items(file, separator, *args):
    file.write(separator.join(args))
```

</details>

### D06 — error

Tham số **name nhận những đối số nào và lưu trong kiểu dữ liệu gì?

**Nhãn đề xuất:** answer=0; context=0; abstention_correct=None

**Lý do:** Context chỉ có quy tắc keyword arguments chung, thiếu **name/dictionary; lỗi protocol.

**Đáp án mong đợi / giới hạn corpus:** Nhận các keyword arguments không ứng với tham số hình thức đã khai báo và lưu thành dictionary.

**Đầu ra được chấp nhận:**
(không có)

**Lỗi:** protocol / ValueError

**Citation đã đọc:**

<details><summary>Context đã chuẩn bị</summary>

```text
[5c3e2cd2446561b62a1de5be9ec614ba | https://docs.python.org/3.14/tutorial/controlflow.html | page python-3.14-ch04-u009]
In a function call, keyword arguments must follow positional arguments. All the keyword arguments passed must match one of the arguments accepted by the function (e.g. actor is not a valid argument for the parrot function), and their order is not important. This also includes non-optional arguments (e.g. parrot(voltage=1000) is valid too). No argument may receive a value more than once. Here’s an example that fails due to this restriction:
```

</details>

### D07 — answered

Muốn tạo tuple chỉ chứa chuỗi hello thì chỉ viết ngoặc quanh giá trị có đủ không? Cú pháp cần thêm gì?

**Nhãn đề xuất:** answer=2; context=2; abstention_correct=None

**Lý do:** Nêu rõ chỉ ngoặc không đủ, cần dấu phẩy sau giá trị và ví dụ tuple một phần tử.

**Đáp án mong đợi / giới hạn corpus:** Không đủ; phải có dấu phẩy sau giá trị, ví dụ ('hello',) hoặc 'hello',.

**Đầu ra được chấp nhận:**
Không đủ. Theo tài liệu, chỉ đặt một giá trị trong ngoặc đơn là không đủ để tạo tuple một phần tử; cần thêm dấu phẩy sau giá trị (dấu phẩy ở cuối). Ví dụ: singleton = 'hello',  # chú ý dấu phẩy cuối — kết quả là ('hello',) với len bằng 1 [a14a0c62dbc9ade9275bb1cfd18bbc57].

**Citation đã đọc:**
- `a14a0c62dbc9ade9275bb1cfd18bbc57`: True — Nêu một phần tử phải có comma, ngoặc không đủ; có ví dụ singleton hello.

<details><summary>Context đã chuẩn bị</summary>

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

</details>

### D08 — answered

a.pop() không truyền index sẽ xóa và trả về phần tử nào? Điều gì xảy ra nếu a rỗng?

**Nhãn đề xuất:** answer=2; context=2; abstention_correct=None

**Lý do:** Đủ xóa/trả phần tử cuối và IndexError khi list rỗng.

**Đáp án mong đợi / giới hạn corpus:** Xóa và trả về phần tử cuối; nếu list rỗng thì phát sinh IndexError.

**Đầu ra được chấp nhận:**
a.pop() không truyền index sẽ xóa và trả về phần tử cuối cùng của list. Nếu list rỗng (hoặc index nằm ngoài phạm vi list), nó sẽ ném ra IndexError [e4976e7c8c03d1c6a37a18f46e14e9dd].

**Citation đã đọc:**
- `e4976e7c8c03d1c6a37a18f46e14e9dd`: True — Nêu pop không index xóa/trả phần tử cuối và IndexError với list rỗng.

<details><summary>Context đã chuẩn bị</summary>

```text
[e4976e7c8c03d1c6a37a18f46e14e9dd | https://docs.python.org/3.14/tutorial/datastructures.html | page python-3.14-ch05-u001]
Remove the item at the given position in the list, and return it. If no index is specified, a.pop() removes and returns the last item in the list. It raises an IndexError if the list is empty or the index is outside the list range.

list.clear()

Remove all items from the list. Similar to del a[:].

list.index(value[, start[, stop]])

Return zero-based index of the first occurrence of value in the list. Raises a ValueError if there is no such item.
```

</details>

### D09 — error

Khi duyệt dictionary, dùng phương thức nào để lấy đồng thời khóa và giá trị tương ứng?

**Nhãn đề xuất:** answer=0; context=0; abstention_correct=None

**Lý do:** Context định nghĩa dictionary, không có phương thức items(); lỗi protocol.

**Đáp án mong đợi / giới hạn corpus:** Dùng phương thức items(), ví dụ for k, v in d.items().

**Đầu ra được chấp nhận:**
(không có)

**Lỗi:** protocol / ValueError

**Citation đã đọc:**

<details><summary>Context đã chuẩn bị</summary>

```text
[22d13ffc003595146adb41b1a1676227 | https://docs.python.org/3.14/tutorial/datastructures.html | page python-3.14-ch05-u006]
It is best to think of a dictionary as a set of key: value pairs, with the requirement that the keys are unique (within one dictionary). A pair of braces creates an empty dictionary: {}. Placing a comma-separated list of key:value pairs within the braces adds initial key:value pairs to the dictionary; this is also the way dictionaries are written on output.
```

</details>

### D10 — answered

Có hai sequence cần duyệt đồng thời thành từng cặp phần tử tương ứng. Tài liệu giới thiệu hàm nào?

**Nhãn đề xuất:** answer=2; context=2; abstention_correct=None

**Lý do:** Đúng zip() để ghép phần tử tương ứng của hai/nhiều sequence.

**Đáp án mong đợi / giới hạn corpus:** Dùng zip() để ghép các phần tử tương ứng khi duyệt hai hoặc nhiều sequence.

**Đầu ra được chấp nhận:**
Tài liệu giới thiệu hàm zip(): để duyệt hai hoặc nhiều sequence cùng lúc, các phần tử có thể được ghép cặp bằng hàm zip(), ví dụ `for q, a in zip(questions, answers):` [d0465c0ebf1bcc71b35de11057f991e9].

**Citation đã đọc:**
- `d0465c0ebf1bcc71b35de11057f991e9`: True — Nêu zip ghép entries của hai/nhiều sequence và ví dụ hai danh sách.

<details><summary>Context đã chuẩn bị</summary>

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

</details>

### D11 — answered

dir() không truyền đối số liệt kê những tên nào? Nó có tự liệt kê tên hàm và biến built-in không?

**Nhãn đề xuất:** answer=2; context=2; abstention_correct=None

**Lý do:** Đủ tên hiện tại gồm biến/module/hàm và không tự liệt kê các built-in.

**Đáp án mong đợi / giới hạn corpus:** Liệt kê các tên đang được định nghĩa như biến, module và hàm; không liệt kê các tên hàm và biến built-in.

**Đầu ra được chấp nhận:**
Khi không truyền đối số, dir() liệt kê các tên bạn đã định nghĩa hiện tại (mọi loại tên: biến, module, hàm, v.v.) [653c279748bae8969296f00bc2941191]. Tuy nhiên, dir() KHÔNG liệt kê tên của các hàm và biến built-in; muốn có danh sách đó thì chúng được định nghĩa trong module chuẩn builtins [653c279748bae8969296f00bc2941191].

**Citation đã đọc:**
- `653c279748bae8969296f00bc2941191`: True — Nêu tên hiện tại, mọi loại tên và loại trừ built-in; ví dụ dir().

<details><summary>Context đã chuẩn bị</summary>

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

</details>

### D12 — answered

Python dựa vào thông tin nào của file nguồn để quyết định module đã biên dịch có lỗi thời và cần biên dịch lại?

**Nhãn đề xuất:** answer=2; context=2; abstention_correct=None

**Lý do:** Đúng so sánh modification date của nguồn với bản đã biên dịch.

**Đáp án mong đợi / giới hạn corpus:** So sánh ngày/giờ sửa đổi của mã nguồn với phiên bản đã biên dịch.

**Đầu ra được chấp nhận:**
Python kiểm tra ngày sửa đổi (modification date) của file nguồn so với phiên bản đã biên dịch để xem module đã biên dịch có lỗi thời và cần biên dịch lại hay không; đây là quá trình hoàn toàn tự động [4b9311d6dabb880f0d9037d258d191b8].

**Citation đã đọc:**
- `4b9311d6dabb880f0d9037d258d191b8`: True — Nêu kiểm tra ngày sửa nguồn và compiled version để quyết định biên dịch lại.

<details><summary>Context đã chuẩn bị</summary>

```text
[4b9311d6dabb880f0d9037d258d191b8 | https://docs.python.org/3.14/tutorial/modules.html | page python-3.14-ch06-u004]
Python checks the modification date of the source against the compiled version to see if it’s out of date and needs to be recompiled. This is a completely automatic process. Also, the compiled modules are platform-independent, so the same library can be shared among systems with different architectures.
```

</details>

### D13 — answered

Với file vừa mở để đọc và đang ở đầu file, bỏ size hoặc truyền size âm cho f.read(size) sẽ đọc bao nhiêu? Rủi ro bộ nhớ được tài liệu nhắc là gì?

**Nhãn đề xuất:** answer=2; context=2; abstention_correct=None

**Lý do:** Đủ đọc toàn bộ khi bỏ size/size âm và cảnh báo file lớn hơn bộ nhớ.

**Đáp án mong đợi / giới hạn corpus:** Đọc toàn bộ nội dung file; file quá lớn có thể vượt bộ nhớ máy.

**Đầu ra được chấp nhận:**
Khi bỏ size hoặc truyền size âm cho f.read(size), toàn bộ nội dung file sẽ được đọc và trả về (dưới dạng chuỗi ở text mode hoặc bytes ở binary mode) [b2e4e2a1efb032538c84a9e87be3cfb4]. Rủi ro bộ nhớ mà tài liệu nhắc là: "it's your problem if the file is twice as large as your machine's memory" — tức nếu file lớn gấp đôi bộ nhớ máy thì đó là vấn đề của bạn [b2e4e2a1efb032538c84a9e87be3cfb4].

**Citation đã đọc:**
- `b2e4e2a1efb032538c84a9e87be3cfb4`: True — Nêu text/bytes, trường hợp size omitted/negative, cảnh báo bộ nhớ và nhánh otherwise tối đa size.

<details><summary>Context đã chuẩn bị</summary>

```text
[b2e4e2a1efb032538c84a9e87be3cfb4 | https://docs.python.org/3.14/tutorial/inputoutput.html | page python-3.14-ch07-u005]
To read a file’s contents, call f.read(size), which reads some quantity of data and returns it as a string (in text mode) or bytes object (in binary mode). size is an optional numeric argument. When size is omitted or negative, the entire contents of the file will be read and returned; it’s your problem if the file is twice as large as your machine’s memory. Otherwise, at most size characters (in text mode) or size bytes (in binary mode) are read and returned. If the end of the file has been 

[1dc34e861c5e5fadc4724e725df10931 | https://docs.python.org/3.14/tutorial/inputoutput.html | page python-3.14-ch07-u005]
reached, f.read() will return an empty string ('').
```

</details>

### D14 — answered

Giá trị f.tell() trong binary mode và text mode có ý nghĩa khác nhau thế nào?

**Nhãn đề xuất:** answer=2; context=2; abstention_correct=None

**Lý do:** Đủ byte offset trong binary và opaque position trong text.

**Đáp án mong đợi / giới hạn corpus:** Binary mode: số byte tính từ đầu file. Text mode: một số opaque biểu diễn vị trí, không nên hiểu là số byte.

**Đầu ra được chấp nhận:**
Trong binary mode, f.tell() trả về một số nguyên là vị trí hiện tại của file object, được biểu diễn bằng số byte tính từ đầu file; còn trong text mode, nó trả về một số "opaque" (không mang ý nghĩa trực tiếp là số byte) [9c4ec9a68dac484801d37366b0214e51].

**Citation đã đọc:**
- `9c4ec9a68dac484801d37366b0214e51`: True — Nêu trực tiếp byte position ở binary và opaque number ở text.

<details><summary>Context đã chuẩn bị</summary>

```text
[9c4ec9a68dac484801d37366b0214e51 | https://docs.python.org/3.14/tutorial/inputoutput.html | page python-3.14-ch07-u006]
f.tell() returns an integer giving the file object’s current position in the file represented as number of bytes from the beginning of the file when in binary mode and an opaque number when in text mode.

[e3dd727e9d10ff3ef55e9dda334b3b96 | https://docs.python.org/3.14/tutorial/inputoutput.html | page python-3.14-ch07-u005]
encoding when opening file in binary mode.
```

</details>

### D15 — answered

Trong try...except, khối else phải đặt sau phần nào và được dùng khi nào?

**Nhãn đề xuất:** answer=2; context=2; abstention_correct=None

**Lý do:** Đủ else sau tất cả except và chỉ chạy khi try không phát sinh ngoại lệ.

**Đáp án mong đợi / giới hạn corpus:** Đặt sau tất cả các except; dùng cho code chỉ chạy khi khối try không phát sinh ngoại lệ.

**Đầu ra được chấp nhận:**
Khối else là tùy chọn của câu lệnh try … except; khi có mặt, nó phải đặt sau tất cả các khối except. Nó hữu ích cho đoạn mã phải được thực thi nếu khối try không ném ra ngoại lệ — nói cách khác, else chạy khi không có ngoại lệ xảy ra [89cb0b58f013c40c3ef13c336fcb8792][e029e5d8abe70414636c4b8d53ae1e44].

**Citation đã đọc:**
- `89cb0b58f013c40c3ef13c336fcb8792`: True — Hỗ trợ cả vị trí sau tất cả except và điều kiện try không có ngoại lệ.
- `e029e5d8abe70414636c4b8d53ae1e44`: True — Hỗ trợ riêng mệnh đề else của try chạy khi không có ngoại lệ; vị trí except được citation khác hỗ trợ.

<details><summary>Context đã chuẩn bị</summary>

```text
[89cb0b58f013c40c3ef13c336fcb8792 | https://docs.python.org/3.14/tutorial/errors.html | page python-3.14-ch08-u003]
The try … except statement has an optional else clause, which, when present, must follow all except clauses. It is useful for code that must be executed if the try clause does not raise an exception. For example:

[e029e5d8abe70414636c4b8d53ae1e44 | https://docs.python.org/3.14/tutorial/controlflow.html | page python-3.14-ch04-u003]
When used with a loop, the else clause has more in common with the else clause of a try statement than it does with that of if statements: a try statement’s else clause runs when no exception occurs, and a loop’s else clause runs when no break occurs. For more on the try statement and exceptions, see Handling Exceptions.
```

</details>

### D16 — abstain

Chỉ dựa trên tài liệu đã cung cấp, khi một task trong asyncio.TaskGroup lỗi, các task còn lại được hủy và chờ kết thúc như thế nào?

**Nhãn đề xuất:** answer=None; context=None; abstention_correct=True

**Lý do:** Đã đọc câu từ chối: giới hạn ở tài liệu/context, không nêu cơ chế kỹ thuật hay đoán ngoại lệ ngoài corpus; đúng theo absence audit của benchmark.

**Đáp án mong đợi / giới hạn corpus:** Corpus không có phần giải thích asyncio hoặc TaskGroup. Các mục vòng lặp/ngoại lệ không quy định ngữ nghĩa hủy task bất đồng bộ.

**Đầu ra được chấp nhận:**
Không đủ bằng chứng trong tài liệu để trả lời: context hiện có chỉ chứa nội dung về dùng Python như máy tính và câu lệnh pass, không có thông tin về asyncio.TaskGroup hay cách hủy/chờ các task còn lại khi một task lỗi.

**Citation đã đọc:**

<details><summary>Context đã chuẩn bị</summary>

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

</details>

### D17 — abstain

Tài liệu đã cung cấp hướng dẫn dùng @dataclass(frozen=True) để ngăn gán lại thuộc tính như thế nào và phát sinh ngoại lệ gì khi cố gán?

**Nhãn đề xuất:** answer=None; context=None; abstention_correct=True

**Lý do:** Đã đọc câu từ chối: giới hạn ở tài liệu/context, không nêu cơ chế kỹ thuật hay đoán ngoại lệ ngoài corpus; đúng theo absence audit của benchmark.

**Đáp án mong đợi / giới hạn corpus:** dataclasses chỉ được nhắc làm ví dụ lớp có thứ tự thuộc tính trong match; frozen xuất hiện trong tên built-in frozenset. Không có hướng dẫn frozen=True hoặc ngoại lệ khi gán.

**Đầu ra được chấp nhận:**
Không đủ bằng chứng trong tài liệu để trả lời: context hiện có chỉ nói về cơ chế raise ngoại lệ nói chung, không có hướng dẫn dùng @dataclass(frozen=True) để ngăn gán lại thuộc tính cũng như không nêu ngoại lệ cụ thể phát sinh khi cố gán.

**Citation đã đọc:**

<details><summary>Context đã chuẩn bị</summary>

```text
[eb1202071982afa8de740c2fa8c71a8f | https://docs.python.org/3.14/tutorial/errors.html | page python-3.14-ch08-u004]
The sole argument to raise indicates the exception to be raised. This must be either an exception instance or an exception class (a class that derives from BaseException, such as Exception or one of its subclasses). If an exception class is passed, it will be implicitly instantiated by calling its constructor with no arguments:

raise ValueError  # shorthand for 'raise ValueError()'

[22301843e855f993ff0daa2a245506d0 | https://docs.python.org/3.14/tutorial/errors.html | page python-3.14-ch08-u005]
    raise RuntimeError('Failed to open database') from exc
RuntimeError: Failed to open database
```

</details>

## Dense 2000 / arrival

### D01 — answered

Muốn viết đường dẫn Windows mà các ký tự như \n và \t không bị hiểu là xuống dòng hoặc tab, tiền tố chuỗi nào được tài liệu hướng dẫn?

**Nhãn đề xuất:** answer=2; context=2; abstention_correct=None

**Lý do:** Đúng tiền tố r và ý nghĩa giữ nguyên escape; ví dụ/giới hạn dấu backslash có trong nguồn.

**Đáp án mong đợi / giới hạn corpus:** Đặt tiền tố r trước dấu nháy để tạo raw string.

**Đầu ra được chấp nhận:**
Tài liệu hướng dẫn dùng chuỗi raw (raw strings) bằng cách thêm tiền tố r trước dấu nháy đầu tiên, ví dụ print(r'C:\this\name') sẽ in ra C:\this\name thay vì hiểu \t là tab và \n là xuống dòng [5046e99636180b57c2960fedf1d3566c]. Lưu ý: chuỗi raw không được kết thúc bằng số lẻ ký tự \ [5046e99636180b57c2960fedf1d3566c].

**Citation đã đọc:**
- `5046e99636180b57c2960fedf1d3566c`: True — Đoạn raw strings nêu tiền tố r, ví dụ Windows path, escape và giới hạn backslash cuối.

<details><summary>Context đã chuẩn bị</summary>

```text
[5046e99636180b57c2960fedf1d3566c | https://docs.python.org/3.14/tutorial/introduction.html | page python-3.14-ch03-u003]
If you don’t want characters prefaced by \ to be interpreted as special characters, you can use raw strings by adding an r before the first quote:

>>> print('C:\this\name')  # here \t means tab, \n means newline
C:      his
ame
>>> print(r'C:\this\name')  # note the r before the quote
C:\this\name

There is one subtle aspect to raw strings: a raw string may not end in an odd number of \ characters; see the FAQ entry for more information and workarounds.

[fe2016a8e160f971dbbd874c33e966ae | https://docs.python.org/3.14/tutorial/introduction.html | page python-3.14-ch03-u003]
>>> prefix = 'Py'
>>> prefix 'thon'  # can't concatenate a variable and a string literal
  File "<stdin>", line 1
    prefix 'thon'
           ^^^^^^
SyntaxError: invalid syntax
>>> ('un' * 3) 'ium'
  File "<stdin>", line 1
    ('un' * 3) 'ium'
               ^^^^^
SyntaxError: invalid syntax

[5c1c637fc4b007260e53d8163375a998 | https://docs.python.org/3.14/tutorial/inputoutput.html | page python-3.14-ch07-u005]
In text mode, the default when reading is to convert platform-specific line endings (\n on Unix, \r\n on Windows) to just \n. When writing in text mode, the default is to convert occurrences of \n back to platform-specific line endings. This behind-the-scenes modification to file data is fine for text files, but will corrupt binary data like that in JPEG or EXE files. Be very careful to use binary mode when reading and writing such files.
```

</details>

### D02 — answered

Khi đánh chỉ số chuỗi từ phía cuối, -1 và -2 chỉ ký tự nào? Vì sao không bắt đầu bằng -0?

**Nhãn đề xuất:** answer=2; context=2; abstention_correct=None

**Lý do:** Đủ cả -1 là ký tự cuối, -2 áp cuối và -0 bằng 0.

**Đáp án mong đợi / giới hạn corpus:** -1 chỉ ký tự cuối, -2 chỉ ký tự áp cuối; -0 bằng 0 nên chỉ số âm bắt đầu từ -1.

**Đầu ra được chấp nhận:**
Với chuỗi 'Python', word[-1] là ký tự cuối cùng ('n') và word[-2] là ký tự áp chót ('o') [07eab24fdef0d6f3c82bb56fb67407ce]. Không bắt đầu bằng -0 vì -0 bằng 0, nên các chỉ số âm bắt đầu từ -1 [07eab24fdef0d6f3c82bb56fb67407ce].

**Citation đã đọc:**
- `07eab24fdef0d6f3c82bb56fb67407ce`: True — Ví dụ word[-1]/[-2] và câu -0 giống 0 hỗ trợ đủ điều kiện.

<details><summary>Context đã chuẩn bị</summary>

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

[ac9fccfaf2dfa153a59f7efd2c111d51 | https://docs.python.org/3.14/tutorial/introduction.html | page python-3.14-ch03-u004]
The first row of numbers gives the position of the indices 0…6 in the string; the second row gives the corresponding negative indices. The slice from i to j consists of all characters between the edges labeled i and j, respectively.

For non-negative indices, the length of a slice is the difference of the indices, if both are within bounds. For example, the length of word[1:3] is 2.

Attempting to use an index that is too large will result in an error:

[50e8eec209f93683350b16b44dd4cb79 | https://docs.python.org/3.14/tutorial/introduction.html | page python-3.14-ch03-u004]
>>> word[:2] + word[2:]
'Python'
>>> word[:4] + word[4:]
'Python'

One way to remember how slices work is to think of the indices as pointing between characters, with the left edge of the first character numbered 0. Then the right edge of the last character of a string of n characters has index n, for example:

 +---+---+---+---+---+---+
 | P | y | t | h | o | n |
 +---+---+---+---+---+---+
 0   1   2   3   4   5   6
-6  -5  -4  -3  -2  -1
```

</details>

### D03 — answered

Ví dụ list(range(5, 10)) trong tài liệu cho ra danh sách nào?

**Nhãn đề xuất:** answer=2; context=2; abstention_correct=None

**Lý do:** Đúng toàn bộ danh sách [5, 6, 7, 8, 9].

**Đáp án mong đợi / giới hạn corpus:** [5, 6, 7, 8, 9]; cận 10 không được lấy.

**Đầu ra được chấp nhận:**
Theo tài liệu, `list(range(5, 10))` cho ra `[5, 6, 7, 8, 9]` [5b0389b2014ead261047a7ea77039951].

**Citation đã đọc:**
- `5b0389b2014ead261047a7ea77039951`: True — Ví dụ nguyên văn list(range(5,10)) và danh sách kết quả.

<details><summary>Context đã chuẩn bị</summary>

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

[a40e04bdcbe4d88c4ee0527d01776073 | https://docs.python.org/3.14/tutorial/controlflow.html | page python-3.14-ch04-u012]
>>> list(range(3, 6))            # normal call with separate arguments
[3, 4, 5]
>>> args = [3, 6]
>>> list(range(*args))            # call with arguments unpacked from a list
[3, 4, 5]

In the same fashion, dictionaries can deliver keyword arguments with the **-operator:

[887a6a1782d1e358b353296859c4b6bc | https://docs.python.org/3.14/tutorial/datastructures.html | page python-3.14-ch05-u003]
For example, assume we want to create a list of squares, like:

>>> squares = []
>>> for x in range(10):
...     squares.append(x**2)
...
>>> squares
[0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

Note that this creates (or overwrites) a variable named x that still exists after the loop completes. We can calculate the list of squares without any side effects using:

squares = list(map(lambda x: x**2, range(10)))

or, equivalently:

squares = [x**2 for x in range(10)]

which is more concise and readable.
```

</details>

### D04 — answered

Nếu có vòng lặp for lồng trong while, break nằm trong for sẽ thoát vòng nào theo quy tắc của tài liệu?

**Nhãn đề xuất:** answer=2; context=2; abstention_correct=None

**Lý do:** Áp dụng đúng quy tắc innermost: thoát for bên trong, không tự thoát while bên ngoài.

**Đáp án mong đợi / giới hạn corpus:** Thoát vòng for ở trong cùng bao quanh break, không tự động thoát cả vòng while bên ngoài.

**Đầu ra được chấp nhận:**
Theo tài liệu, câu lệnh break chỉ thoát khỏi vòng lặp for hoặc while gần nhất bao quanh nó ("breaks out of the innermost enclosing for or while loop"). Vì vậy, với for lồng trong while, break nằm trong for sẽ chỉ thoát vòng for bên trong, không thoát vòng while bên ngoài [6f16320109f4a36189eb5033ecbb89b2].

**Citation đã đọc:**
- `6f16320109f4a36189eb5033ecbb89b2`: True — Nêu break thoát innermost enclosing for/while, hỗ trợ suy luận vòng lặp lồng nhau.

<details><summary>Context đã chuẩn bị</summary>

```text
[e09df3f01953e055de669d3402d7ddac | https://docs.python.org/3.14/tutorial/controlflow.html | page python-3.14-ch04-u002]
4.5. else Clauses on Loops

In a for or while loop the break statement may be paired with an else clause. If the loop finishes without executing the break, the else clause executes.

In a for loop, the else clause is executed after the loop finishes its final iteration, that is, if no break occurred.

In a while loop, it’s executed after the loop’s condition becomes false.

[2df57e0bc5ea73bc55a3cee76070ef4f | https://docs.python.org/3.14/tutorial/controlflow.html | page python-3.14-ch04-u003]
(Yes, this is the correct code. Look closely: the else clause belongs to the for loop, not the if statement.)

One way to think of the else clause is to imagine it paired with the if inside the loop. As the loop executes, it will run a sequence like if/if/if/else. The if is inside the loop, encountered a number of times. If the condition is ever true, a break will happen. If the condition is never true, the else clause outside the loop will execute.

[6f16320109f4a36189eb5033ecbb89b2 | https://docs.python.org/3.14/tutorial/controlflow.html | page python-3.14-ch04-u002]
4.4. break and continue Statements

The break statement breaks out of the innermost enclosing for or while loop:

>>> for n in range(2, 10):
...     for x in range(2, n):
...         if n % x == 0:
...             print(f"{n} equals {x} * {n//x}")
...             break
...
4 equals 2 * 2
6 equals 2 * 3
8 equals 2 * 4
9 equals 3 * 3

The continue statement continues with the next iteration of the loop:
```

</details>

### D05 — answered

Các đối số bổ sung được gom bởi *args trong định nghĩa hàm có kiểu cấu trúc dữ liệu gì?

**Nhãn đề xuất:** answer=2; context=2; abstention_correct=None

**Lý do:** Xác định đúng *args được đóng gói thành tuple.

**Đáp án mong đợi / giới hạn corpus:** Một tuple chứa các đối số vị trí bổ sung.

**Đầu ra được chấp nhận:**
Các đối số bổ sung được gom bởi *args sẽ được gói lại (wrapped up) trong một tuple — tức kiểu cấu trúc dữ liệu là tuple [72ba98c7f88046b6519961423f685ff5].

**Citation đã đọc:**
- `72ba98c7f88046b6519961423f685ff5`: True — Arbitrary Argument Lists nêu arguments wrapped up in tuple và ví dụ *args.

<details><summary>Context đã chuẩn bị</summary>

```text
[72ba98c7f88046b6519961423f685ff5 | https://docs.python.org/3.14/tutorial/controlflow.html | page python-3.14-ch04-u012]
4.9.4. Arbitrary Argument Lists

Finally, the least frequently used option is to specify that a function can be called with an arbitrary number of arguments. These arguments will be wrapped up in a tuple (see Tuples and Sequences). Before the variable number of arguments, zero or more normal arguments may occur.

def write_multiple_items(file, separator, *args):
    file.write(separator.join(args))

[6dd006f402ad41bfbb1f2f1338540f52 | https://docs.python.org/3.14/tutorial/controlflow.html | page python-3.14-ch04-u012]
>>> def concat(*args, sep="/"):
...     return sep.join(args)
...
>>> concat("earth", "mars", "venus")
'earth/mars/venus'
>>> concat("earth", "mars", "venus", sep=".")
'earth.mars.venus'

[a40e04bdcbe4d88c4ee0527d01776073 | https://docs.python.org/3.14/tutorial/controlflow.html | page python-3.14-ch04-u012]
>>> list(range(3, 6))            # normal call with separate arguments
[3, 4, 5]
>>> args = [3, 6]
>>> list(range(*args))            # call with arguments unpacked from a list
[3, 4, 5]

In the same fashion, dictionaries can deliver keyword arguments with the **-operator:

[a7e8e4c36fffdd57a7d21decbf80e7a1 | https://docs.python.org/3.14/tutorial/controlflow.html | page python-3.14-ch04-u012]
4.9.5. Unpacking Argument Lists

The reverse situation occurs when the arguments are already in a list or tuple but need to be unpacked for a function call requiring separate positional arguments. For instance, the built-in range() function expects separate start and stop arguments. If they are not available separately, write the function call with the *-operator to unpack the arguments out of a list or tuple:
```

</details>

### D06 — answered

Tham số **name nhận những đối số nào và lưu trong kiểu dữ liệu gì?

**Nhãn đề xuất:** answer=2; context=2; abstention_correct=None

**Lý do:** Đủ keyword arguments dư, loại đối số đã khớp tham số hình thức, và kiểu dictionary.

**Đáp án mong đợi / giới hạn corpus:** Nhận các keyword arguments không ứng với tham số hình thức đã khai báo và lưu thành dictionary.

**Đầu ra được chấp nhận:**
Khi tham số hình thức cuối cùng có dạng **name, nó nhận một dictionary (kiểu dict — Mapping Types) chứa tất cả các đối số từ khóa, trừ những đối số tương ứng với một tham số hình thức khác. Nó có thể được kết hợp với tham số dạng *name (nhận tuple các đối số vị trí vượt quá danh sách tham số hình thức), và *name phải đứng trước **name [a406cc7dac32b6727ecb688a6d3b9286].

**Citation đã đọc:**
- `a406cc7dac32b6727ecb688a6d3b9286`: True — Định nghĩa **name là dictionary chứa keyword arguments chưa khớp formal parameter; cũng hỗ trợ phần bổ sung *name.

<details><summary>Context đã chuẩn bị</summary>

```text
[ae0fc3e74e7c0bae057391fca74c3eeb | https://docs.python.org/3.14/tutorial/controlflow.html | page python-3.14-ch04-u008]
4.9.2. Keyword Arguments

Functions can also be called using keyword arguments of the form kwarg=value. For instance, the following function:

def parrot(voltage, state='a stiff', action='voom', type='Norwegian Blue'):
    print("-- This parrot wouldn't", action, end=' ')
    print("if you put", voltage, "volts through it.")
    print("-- Lovely plumage, the", type)
    print("-- It's", state, "!")

[a406cc7dac32b6727ecb688a6d3b9286 | https://docs.python.org/3.14/tutorial/controlflow.html | page python-3.14-ch04-u009]
When a final formal parameter of the form **name is present, it receives a dictionary (see Mapping Types — dict) containing all keyword arguments except for those corresponding to a formal parameter. This may be combined with a formal parameter of the form *name (described in the next subsection) which receives a tuple containing the positional arguments beyond the formal parameter list. (*name must occur before **name.) For example, if we define a function like this:

[13bcbe39fcbdc1244143ca0ef6b8e4cc | https://docs.python.org/3.14/tutorial/controlflow.html | page python-3.14-ch04-u010]
4.9.3.1. Positional-or-Keyword Arguments

If / and * are not present in the function definition, arguments may be passed to a function by position or by keyword.

[a40e04bdcbe4d88c4ee0527d01776073 | https://docs.python.org/3.14/tutorial/controlflow.html | page python-3.14-ch04-u012]
>>> list(range(3, 6))            # normal call with separate arguments
[3, 4, 5]
>>> args = [3, 6]
>>> list(range(*args))            # call with arguments unpacked from a list
[3, 4, 5]

In the same fashion, dictionaries can deliver keyword arguments with the **-operator:
```

</details>

### D07 — error

Muốn tạo tuple chỉ chứa chuỗi hello thì chỉ viết ngoặc quanh giá trị có đủ không? Cú pháp cần thêm gì?

**Nhãn đề xuất:** answer=0; context=0; abstention_correct=None

**Lý do:** Lỗi provider không có mã HTTP; không có final answer được chấp nhận. Giữ lỗi và chấm answer all-case bằng 0; không tự suy diễn đáp án. Chưa có context agent để đánh giá bằng chứng.

**Đáp án mong đợi / giới hạn corpus:** Không đủ; phải có dấu phẩy sau giá trị, ví dụ ('hello',) hoặc 'hello',.

**Đầu ra được chấp nhận:**
(không có)

**Lỗi:** provider / ProviderError

**Citation đã đọc:**

<details><summary>Context đã chuẩn bị</summary>

```text
(rỗng)
```

</details>

### D08 — answered

a.pop() không truyền index sẽ xóa và trả về phần tử nào? Điều gì xảy ra nếu a rỗng?

**Nhãn đề xuất:** answer=2; context=2; abstention_correct=None

**Lý do:** Đủ xóa/trả phần tử cuối và IndexError khi list rỗng.

**Đáp án mong đợi / giới hạn corpus:** Xóa và trả về phần tử cuối; nếu list rỗng thì phát sinh IndexError.

**Đầu ra được chấp nhận:**
Nếu không truyền index, a.pop() sẽ xóa và trả về phần tử cuối cùng trong danh sách (tương ứng với index mặc định -1) [e4976e7c8c03d1c6a37a18f46e14e9dd][6713445f8d29820661a5d0f210010c7a]. Nếu danh sách rỗng (hoặc index nằm ngoài phạm vi danh sách), nó sẽ ném ra IndexError [e4976e7c8c03d1c6a37a18f46e14e9dd].

**Citation đã đọc:**
- `e4976e7c8c03d1c6a37a18f46e14e9dd`: True — Nêu pop không index xóa/trả phần tử cuối và IndexError với list rỗng.
- `6713445f8d29820661a5d0f210010c7a`: True — Chữ ký list.pop(index=-1, /) hỗ trợ riêng phần index mặc định; hành vi/ngoại lệ do đoạn pop kế tiếp hỗ trợ.

<details><summary>Context đã chuẩn bị</summary>

```text
[e4976e7c8c03d1c6a37a18f46e14e9dd | https://docs.python.org/3.14/tutorial/datastructures.html | page python-3.14-ch05-u001]
Remove the item at the given position in the list, and return it. If no index is specified, a.pop() removes and returns the last item in the list. It raises an IndexError if the list is empty or the index is outside the list range.

list.clear()

Remove all items from the list. Similar to del a[:].

list.index(value[, start[, stop]])

Return zero-based index of the first occurrence of value in the list. Raises a ValueError if there is no such item.

[6713445f8d29820661a5d0f210010c7a | https://docs.python.org/3.14/tutorial/datastructures.html | page python-3.14-ch05-u001]
Insert an item at a given position. The first argument is the index of the element before which to insert, so a.insert(0, x) inserts at the front of the list, and a.insert(len(a), x) is equivalent to a.append(x).

list.remove(value, /)

Remove the first item from the list whose value is equal to value. It raises a ValueError if there is no such item.

list.pop(index=-1, /)

[e12d5e0b102af3fb583cc06e854db00b | https://docs.python.org/3.14/tutorial/datastructures.html | page python-3.14-ch05-u004]
5.2. The del statement

There is a way to remove an item from a list given its index instead of its value: the del statement. This differs from the pop() method which returns a value. The del statement can also be used to remove slices from a list or clear the entire list (which we did earlier by assignment of an empty list to the slice). For example:

[08cc1a23a50cfe385721826ae05c568c | https://docs.python.org/3.14/tutorial/controlflow.html | page python-3.14-ch04-u002]
Later we will see more functions that return iterables and take iterables as arguments. In chapter Data Structures, we will discuss list() in more detail.
```

</details>

### D09 — answered

Khi duyệt dictionary, dùng phương thức nào để lấy đồng thời khóa và giá trị tương ứng?

**Nhãn đề xuất:** answer=2; context=2; abstention_correct=None

**Lý do:** Đúng items() và lấy đồng thời key/value.

**Đáp án mong đợi / giới hạn corpus:** Dùng phương thức items(), ví dụ for k, v in d.items().

**Đầu ra được chấp nhận:**
Khi duyệt dictionary, bạn dùng phương thức items() để lấy đồng thời khóa và giá trị tương ứng, ví dụ: `for k, v in knights.items(): print(k, v)` [fa52d5bbb11517433573b8febe0a1876].

**Citation đã đọc:**
- `fa52d5bbb11517433573b8febe0a1876`: True — Nêu items() lấy key/value đồng thời, có ví dụ for k,v.

<details><summary>Context đã chuẩn bị</summary>

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

[ac6c1afbbdfdef051c6c2d881e0c8b5b | https://docs.python.org/3.14/tutorial/datastructures.html | page python-3.14-ch05-u007]
The dict() constructor builds dictionaries directly from sequences of key-value pairs:

>>> dict([('sape', 4139), ('guido', 4127), ('jack', 4098)])
{'sape': 4139, 'guido': 4127, 'jack': 4098}

In addition, dict comprehensions can be used to create dictionaries from arbitrary key and value expressions:

>>> {x: x**2 for x in (2, 4, 6)}
{2: 4, 4: 16, 6: 36}

When the keys are simple strings, it is sometimes easier to specify pairs using keyword arguments:

[6a283703bc3b7d5deaceb4053de6cb12 | https://docs.python.org/3.14/tutorial/datastructures.html | page python-3.14-ch05-u007]
The main operations on a dictionary are storing a value with some key and extracting the value given the key. It is also possible to delete a key:value pair with del. If you store using a key that is already in use, the old value associated with that key is forgotten.
```

</details>

### D10 — answered

Có hai sequence cần duyệt đồng thời thành từng cặp phần tử tương ứng. Tài liệu giới thiệu hàm nào?

**Nhãn đề xuất:** answer=2; context=2; abstention_correct=None

**Lý do:** Đúng zip() để ghép phần tử tương ứng của hai/nhiều sequence.

**Đáp án mong đợi / giới hạn corpus:** Dùng zip() để ghép các phần tử tương ứng khi duyệt hai hoặc nhiều sequence.

**Đầu ra được chấp nhận:**
Tài liệu giới thiệu hàm zip(). Cụ thể: "To loop over two or more sequences at the same time, the entries can be paired with the zip() function." — để duyệt hai hay nhiều sequence đồng thời, các phần tử có thể được ghép cặp bằng hàm zip(), ví dụ `for q, a in zip(questions, answers):` [d0465c0ebf1bcc71b35de11057f991e9].

**Citation đã đọc:**
- `d0465c0ebf1bcc71b35de11057f991e9`: True — Nêu zip ghép entries của hai/nhiều sequence và ví dụ hai danh sách.

<details><summary>Context đã chuẩn bị</summary>

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

[3ae984dcd6ea0fd56b8d4818aede35d0 | https://docs.python.org/3.14/tutorial/datastructures.html | page python-3.14-ch05-u005]
This is called, appropriately enough, sequence unpacking and works for any sequence on the right-hand side. Sequence unpacking requires that there are as many variables on the left side of the equals sign as there are elements in the sequence. Note that multiple assignment is really just a combination of tuple packing and sequence unpacking.

[05405500dec053b3c7600a61076a5941 | https://docs.python.org/3.14/tutorial/datastructures.html | page python-3.14-ch05-u004]
>>> list(zip(*matrix))
[(1, 5, 9), (2, 6, 10), (3, 7, 11), (4, 8, 12)]

See Unpacking Argument Lists for details on the asterisk in this line.

[08cc1a23a50cfe385721826ae05c568c | https://docs.python.org/3.14/tutorial/controlflow.html | page python-3.14-ch04-u002]
Later we will see more functions that return iterables and take iterables as arguments. In chapter Data Structures, we will discuss list() in more detail.
```

</details>

### D11 — answered

dir() không truyền đối số liệt kê những tên nào? Nó có tự liệt kê tên hàm và biến built-in không?

**Nhãn đề xuất:** answer=2; context=2; abstention_correct=None

**Lý do:** Đủ tên hiện tại gồm biến/module/hàm và không tự liệt kê các built-in.

**Đáp án mong đợi / giới hạn corpus:** Liệt kê các tên đang được định nghĩa như biến, module và hàm; không liệt kê các tên hàm và biến built-in.

**Đầu ra được chấp nhận:**
Khi không truyền đối số, dir() liệt kê những tên bạn đã định nghĩa hiện tại (ví dụ sau khi gán a, import fibo, fib = fibo.fib thì dir() trả về ['__builtins__', '__name__', 'a', 'fib', 'fibo', 'sys']); nó liệt kê mọi loại tên: biến, module, hàm, v.v. [653c279748bae8969296f00bc2941191] Tuy nhiên dir() KHÔNG liệt kê tên của các hàm và biến built-in; nếu muốn danh sách đó, chúng được định nghĩa trong module chuẩn builtins [653c279748bae8969296f00bc2941191].

**Citation đã đọc:**
- `653c279748bae8969296f00bc2941191`: True — Nêu tên hiện tại, mọi loại tên và loại trừ built-in; ví dụ dir().

<details><summary>Context đã chuẩn bị</summary>

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

[72ba98c7f88046b6519961423f685ff5 | https://docs.python.org/3.14/tutorial/controlflow.html | page python-3.14-ch04-u012]
4.9.4. Arbitrary Argument Lists

Finally, the least frequently used option is to specify that a function can be called with an arbitrary number of arguments. These arguments will be wrapped up in a tuple (see Tuples and Sequences). Before the variable number of arguments, zero or more normal arguments may occur.

def write_multiple_items(file, separator, *args):
    file.write(separator.join(args))

[15f965a58ca6a4984f1e4003047b0497 | https://docs.python.org/3.14/tutorial/datastructures.html | page python-3.14-ch05-u001]
The optional arguments start and end are interpreted as in the slice notation and are used to limit the search to a particular subsequence of the list. The returned index is computed relative to the beginning of the full sequence rather than the start argument.

list.count(value, /)

Return the number of times value appears in the list.

list.sort(*, key=None, reverse=False)
```

</details>

### D12 — answered

Python dựa vào thông tin nào của file nguồn để quyết định module đã biên dịch có lỗi thời và cần biên dịch lại?

**Nhãn đề xuất:** answer=2; context=2; abstention_correct=None

**Lý do:** Đúng so sánh modification date của nguồn với bản đã biên dịch.

**Đáp án mong đợi / giới hạn corpus:** So sánh ngày/giờ sửa đổi của mã nguồn với phiên bản đã biên dịch.

**Đầu ra được chấp nhận:**
Python kiểm tra ngày sửa đổi (modification date) của file nguồn so với phiên bản đã biên dịch để xem module đã biên dịch có lỗi thời và cần biên dịch lại hay không; đây là quá trình hoàn toàn tự động [4b9311d6dabb880f0d9037d258d191b8]. Ngoài ra, Python không kiểm tra cache trong hai trường hợp: module được nạp trực tiếp từ dòng lệnh (luôn biên dịch lại và không lưu kết quả), và khi không có file nguồn (để hỗ trợ phân phối chỉ có bản biên dịch) [2710a5930f78e76bbaa16236576d8562].

**Citation đã đọc:**
- `4b9311d6dabb880f0d9037d258d191b8`: True — Nêu kiểm tra ngày sửa nguồn và compiled version để quyết định biên dịch lại.
- `2710a5930f78e76bbaa16236576d8562`: True — Hỗ trợ phần bổ sung về hai trường hợp không kiểm tra cache.

<details><summary>Context đã chuẩn bị</summary>

```text
[4b9311d6dabb880f0d9037d258d191b8 | https://docs.python.org/3.14/tutorial/modules.html | page python-3.14-ch06-u004]
Python checks the modification date of the source against the compiled version to see if it’s out of date and needs to be recompiled. This is a completely automatic process. Also, the compiled modules are platform-independent, so the same library can be shared among systems with different architectures.

[2710a5930f78e76bbaa16236576d8562 | https://docs.python.org/3.14/tutorial/modules.html | page python-3.14-ch06-u004]
Python does not check the cache in two circumstances. First, it always recompiles and does not store the result for the module that’s loaded directly from the command line. Second, it does not check the cache if there is no source module. To support a non-source (compiled only) distribution, the compiled module must be in the source directory, and there must not be a source module.

Some tips for experts:

[74e8ed7f7867f0561346780737e8de24 | https://docs.python.org/3.14/tutorial/modules.html | page python-3.14-ch06-u003]
To speed up loading modules, Python caches the compiled version of each module in the __pycache__ directory under the name module.version.pyc, where the version encodes the format of the compiled file; it generally contains the Python version number. For example, in CPython release 3.3 the compiled version of spam.py would be cached as __pycache__/spam.cpython-33.pyc. This naming convention allows compiled modules from different releases and different versions of Python to coexist.
```

</details>

### D13 — answered

Với file vừa mở để đọc và đang ở đầu file, bỏ size hoặc truyền size âm cho f.read(size) sẽ đọc bao nhiêu? Rủi ro bộ nhớ được tài liệu nhắc là gì?

**Nhãn đề xuất:** answer=2; context=2; abstention_correct=None

**Lý do:** Đủ đọc toàn bộ khi bỏ size/size âm và cảnh báo file lớn hơn bộ nhớ. Cụm ngược lại được hiểu là nhánh size còn lại; cách viết size không âm sẽ rõ hơn.

**Đáp án mong đợi / giới hạn corpus:** Đọc toàn bộ nội dung file; file quá lớn có thể vượt bộ nhớ máy.

**Đầu ra được chấp nhận:**
Khi gọi f.read(size) mà bỏ size hoặc truyền size âm, toàn bộ nội dung file sẽ được đọc và trả về (dưới dạng chuỗi ở text mode hoặc bytes ở binary mode) [b2e4e2a1efb032538c84a9e87be3cfb4]. Rủi ro bộ nhớ mà tài liệu nhắc là: "it's your problem if the file is twice as large as your machine's memory" — tức nếu file lớn gấp đôi bộ nhớ máy thì đó là vấn đề của bạn [b2e4e2a1efb032538c84a9e87be3cfb4]. Ngược lại, nếu truyền size, tối đa size ký tự (text mode) hoặc size byte (binary mode) được đọc và trả về [b2e4e2a1efb032538c84a9e87be3cfb4].

**Citation đã đọc:**
- `b2e4e2a1efb032538c84a9e87be3cfb4`: True — Nêu text/bytes, trường hợp size omitted/negative, cảnh báo bộ nhớ và nhánh otherwise tối đa size.

<details><summary>Context đã chuẩn bị</summary>

```text
[b2e4e2a1efb032538c84a9e87be3cfb4 | https://docs.python.org/3.14/tutorial/inputoutput.html | page python-3.14-ch07-u005]
To read a file’s contents, call f.read(size), which reads some quantity of data and returns it as a string (in text mode) or bytes object (in binary mode). size is an optional numeric argument. When size is omitted or negative, the entire contents of the file will be read and returned; it’s your problem if the file is twice as large as your machine’s memory. Otherwise, at most size characters (in text mode) or size bytes (in binary mode) are read and returned. If the end of the file has been 

[88e5cfa94339c9566fd9682ea7f267f0 | https://docs.python.org/3.14/tutorial/inputoutput.html | page python-3.14-ch07-u006]
>>> f.read()
'This is the entire file.\n'
>>> f.read()
''

f.readline() reads a single line from the file; a newline character (\n) is left at the end of the string, and is only omitted on the last line of the file if the file doesn’t end in a newline. This makes the return value unambiguous; if f.readline() returns an empty string, the end of the file has been reached, while a blank line is represented by '\n', a string containing only a single newline.

[802e02440bfa7459cfee4a49c6ca69c3 | https://docs.python.org/3.14/tutorial/inputoutput.html | page python-3.14-ch07-u005]
>>> f.close()
>>> f.read()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ValueError: I/O operation on closed file.
```

</details>

### D14 — answered

Giá trị f.tell() trong binary mode và text mode có ý nghĩa khác nhau thế nào?

**Nhãn đề xuất:** answer=2; context=2; abstention_correct=None

**Lý do:** Đủ byte offset trong binary và opaque position trong text.

**Đáp án mong đợi / giới hạn corpus:** Binary mode: số byte tính từ đầu file. Text mode: một số opaque biểu diễn vị trí, không nên hiểu là số byte.

**Đầu ra được chấp nhận:**
Theo tài liệu: f.tell() trả về một số nguyên cho biết vị trí hiện tại của file object trong file — ở binary mode đó là số byte tính từ đầu file, còn ở text mode đó là một "opaque number" (con số không mang ý nghĩa byte cụ thể) [9c4ec9a68dac484801d37366b0214e51]. Liên quan đến điều này, với text file (mở không có 'b' trong mode string) chỉ cho phép seek tương đối so với đầu file (ngoại lệ là seek tới cuối file bằng seek(0, 2)), và các giá trị offset hợp lệ chỉ là những giá trị do f.tell() trả về hoặc 0; offset khác sẽ gây hành vi không xác định [dbb1c2a57f3bdb25359e5a45739375d9].

**Citation đã đọc:**
- `9c4ec9a68dac484801d37366b0214e51`: True — Nêu trực tiếp byte position ở binary và opaque number ở text.
- `dbb1c2a57f3bdb25359e5a45739375d9`: True — Hỗ trợ riêng phần bổ sung về các offset seek hợp lệ cho text.

<details><summary>Context đã chuẩn bị</summary>

```text
[9c4ec9a68dac484801d37366b0214e51 | https://docs.python.org/3.14/tutorial/inputoutput.html | page python-3.14-ch07-u006]
f.tell() returns an integer giving the file object’s current position in the file represented as number of bytes from the beginning of the file when in binary mode and an opaque number when in text mode.

[dbb1c2a57f3bdb25359e5a45739375d9 | https://docs.python.org/3.14/tutorial/inputoutput.html | page python-3.14-ch07-u006]
In text files (those opened without a b in the mode string), only seeks relative to the beginning of the file are allowed (the exception being seeking to the very file end with seek(0, 2)) and the only valid offset values are those returned from the f.tell(), or zero. Any other offset value produces undefined behaviour.

[6fbf000a89c6f543bce38bbfb2905520 | https://docs.python.org/3.14/tutorial/inputoutput.html | page python-3.14-ch07-u006]
f.write(string) writes the contents of string to the file, returning the number of characters written.

>>> f.write('This is a test\n')
15

Other types of objects need to be converted – either to a string (in text mode) or a bytes object (in binary mode) – before writing them:

>>> value = ('the answer', 42)
>>> s = str(value)  # convert the tuple to string
>>> f.write(s)
18

[e3dd727e9d10ff3ef55e9dda334b3b96 | https://docs.python.org/3.14/tutorial/inputoutput.html | page python-3.14-ch07-u005]
encoding when opening file in binary mode.
```

</details>

### D15 — answered

Trong try...except, khối else phải đặt sau phần nào và được dùng khi nào?

**Nhãn đề xuất:** answer=2; context=2; abstention_correct=None

**Lý do:** Đủ else sau tất cả except và chỉ chạy khi try không phát sinh ngoại lệ.

**Đáp án mong đợi / giới hạn corpus:** Đặt sau tất cả các except; dùng cho code chỉ chạy khi khối try không phát sinh ngoại lệ.

**Đầu ra được chấp nhận:**
Khối else là tùy chọn của câu lệnh try … except; khi có mặt, nó phải đặt sau tất cả các khối except. Nó hữu ích cho đoạn mã phải được thực thi nếu khối try không gây ra ngoại lệ — nói cách khác, else chạy khi không có ngoại lệ xảy ra [89cb0b58f013c40c3ef13c336fcb8792][e029e5d8abe70414636c4b8d53ae1e44].

**Citation đã đọc:**
- `89cb0b58f013c40c3ef13c336fcb8792`: True — Hỗ trợ cả vị trí sau tất cả except và điều kiện try không có ngoại lệ.
- `e029e5d8abe70414636c4b8d53ae1e44`: True — Hỗ trợ riêng mệnh đề else của try chạy khi không có ngoại lệ; vị trí except được citation khác hỗ trợ.

<details><summary>Context đã chuẩn bị</summary>

```text
[89cb0b58f013c40c3ef13c336fcb8792 | https://docs.python.org/3.14/tutorial/errors.html | page python-3.14-ch08-u003]
The try … except statement has an optional else clause, which, when present, must follow all except clauses. It is useful for code that must be executed if the try clause does not raise an exception. For example:

[40d1dc8b383841d91bf6c0ecd6174cf5 | https://docs.python.org/3.14/tutorial/errors.html | page python-3.14-ch08-u002]
If an exception occurs during execution of the try clause, the rest of the clause is skipped. Then, if its type matches the exception named after the except keyword, the except clause is executed, and then execution continues after the try/except block.

If an exception occurs which does not match the exception named in the except clause, it is passed on to outer try statements; if no handler is found, it is an unhandled exception and execution stops with an error message.

[a9b61cae10de6e45674d2656e1ff3c38 | https://docs.python.org/3.14/tutorial/errors.html | page python-3.14-ch08-u006]
If an exception occurs during execution of the try clause, the exception may be handled by an except clause. If the exception is not handled by an except clause, the exception is re-raised after the finally clause has been executed.

An exception could occur during execution of an except or else clause. Again, the exception is re-raised after the finally clause has been executed.

[e029e5d8abe70414636c4b8d53ae1e44 | https://docs.python.org/3.14/tutorial/controlflow.html | page python-3.14-ch04-u003]
When used with a loop, the else clause has more in common with the else clause of a try statement than it does with that of if statements: a try statement’s else clause runs when no exception occurs, and a loop’s else clause runs when no break occurs. For more on the try statement and exceptions, see Handling Exceptions.
```

</details>

### D16 — abstain

Chỉ dựa trên tài liệu đã cung cấp, khi một task trong asyncio.TaskGroup lỗi, các task còn lại được hủy và chờ kết thúc như thế nào?

**Nhãn đề xuất:** answer=None; context=None; abstention_correct=True

**Lý do:** Đã đọc lời từ chối và context: không bổ sung cơ chế kỹ thuật hoặc đoán ngoại lệ; phù hợp corpus absence audit.

**Đáp án mong đợi / giới hạn corpus:** Corpus không có phần giải thích asyncio hoặc TaskGroup. Các mục vòng lặp/ngoại lệ không quy định ngữ nghĩa hủy task bất đồng bộ.

**Đầu ra được chấp nhận:**
Không đủ bằng chứng trong tài liệu để trả lời: context hiện tại chỉ chứa nội dung về danh sách built-in names và xử lý lỗi/ExceptionGroup trong tutorial, không có mô tả cơ chế asyncio.TaskGroup hủy và chờ các task còn lại khi một task lỗi.

**Citation đã đọc:**

<details><summary>Context đã chuẩn bị</summary>

```text
[f56f1b83badcd52d685382d45a8001a6 | https://docs.python.org/3.14/tutorial/modules.html | page python-3.14-ch06-u006]
 'StopIteration', 'SyntaxError', 'SyntaxWarning', 'SystemError',
 'SystemExit', 'TabError', 'TimeoutError', 'True', 'TypeError',
 'UnboundLocalError', 'UnicodeDecodeError', 'UnicodeEncodeError',
 'UnicodeError', 'UnicodeTranslateError', 'UnicodeWarning', 'UserWarning',
 'ValueError', 'Warning', 'ZeroDivisionError', '_', '__build_class__',
 '__debug__', '__doc__', '__import__', '__name__', '__package__', 'abs',
 'all', 'any', 'ascii', 'bin', 'bool', 'bytearray', 'bytes', 'callable',


[9126cd3fef32cc3e468d8edc25111ce4 | https://docs.python.org/3.14/tutorial/errors.html | page python-3.14-ch08-u008]
      | RecursionError: 4
      +------------------------------------
>>>

[f43fbe7ecf4d366d1ff0de508196dc46 | https://docs.python.org/3.14/tutorial/errors.html | page python-3.14-ch08-u008]
    |     ~^^
    |   File "<stdin>", line 2, in f
    |     raise OSError('operation failed')
    | OSError: operation failed
    | Happened in Iteration 2
    +---------------- 3 ----------------
    | Traceback (most recent call last):
    |   File "<stdin>", line 3, in <module>
    |     f()
    |     ~^^
    |   File "<stdin>", line 2, in f
    |     raise OSError('operation failed')
    | OSError: operation failed
    | Happened in Iteration 3
    +------------------------------------
>>>

[50a02bfe09cbf31193dec2537ce7cbd3 | https://docs.python.org/3.14/tutorial/errors.html | page python-3.14-ch08-u007]
    +---------------- 2 ----------------
    | SystemError: error 2
    +------------------------------------
>>> try:
...     f()
... except Exception as e:
...     print(f'caught {type(e)}: {e}')
...
caught <class 'ExceptionGroup'>: there were problems (2 sub-exceptions)
>>>
```

</details>

### D17 — abstain

Tài liệu đã cung cấp hướng dẫn dùng @dataclass(frozen=True) để ngăn gán lại thuộc tính như thế nào và phát sinh ngoại lệ gì khi cố gán?

**Nhãn đề xuất:** answer=None; context=None; abstention_correct=True

**Lý do:** Đã đọc lời từ chối và context: không bổ sung cơ chế kỹ thuật hoặc đoán ngoại lệ; phù hợp corpus absence audit.

**Đáp án mong đợi / giới hạn corpus:** dataclasses chỉ được nhắc làm ví dụ lớp có thứ tự thuộc tính trong match; frozen xuất hiện trong tên built-in frozenset. Không có hướng dẫn frozen=True hoặc ngoại lệ khi gán.

**Đầu ra được chấp nhận:**
Không đủ bằng chứng trong tài liệu để trả lời: context hiện có chỉ nói về xử lý ngoại lệ và danh sách tên ngoại lệ tích hợp, không có nội dung nào về @dataclass(frozen=True), cách ngăn gán lại thuộc tính, hay ngoại lệ phát sinh khi cố gán.

**Citation đã đọc:**

<details><summary>Context đã chuẩn bị</summary>

```text
[22301843e855f993ff0daa2a245506d0 | https://docs.python.org/3.14/tutorial/errors.html | page python-3.14-ch08-u005]
    raise RuntimeError('Failed to open database') from exc
RuntimeError: Failed to open database

[f56f1b83badcd52d685382d45a8001a6 | https://docs.python.org/3.14/tutorial/modules.html | page python-3.14-ch06-u006]
 'StopIteration', 'SyntaxError', 'SyntaxWarning', 'SystemError',
 'SystemExit', 'TabError', 'TimeoutError', 'True', 'TypeError',
 'UnboundLocalError', 'UnicodeDecodeError', 'UnicodeEncodeError',
 'UnicodeError', 'UnicodeTranslateError', 'UnicodeWarning', 'UserWarning',
 'ValueError', 'Warning', 'ZeroDivisionError', '_', '__build_class__',
 '__debug__', '__doc__', '__import__', '__name__', '__package__', 'abs',
 'all', 'any', 'ascii', 'bin', 'bool', 'bytearray', 'bytes', 'callable',


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

[fede68f1763fa2d54f86aa447d416fc2 | https://docs.python.org/3.14/tutorial/modules.html | page python-3.14-ch06-u006]
 'FutureWarning', 'GeneratorExit', 'IOError', 'ImportError',
 'ImportWarning', 'IndentationError', 'IndexError', 'InterruptedError',
 'IsADirectoryError', 'KeyError', 'KeyboardInterrupt', 'LookupError',
 'MemoryError', 'NameError', 'None', 'NotADirectoryError', 'NotImplemented',
 'NotImplementedError', 'OSError', 'OverflowError',
 'PendingDeprecationWarning', 'PermissionError', 'ProcessLookupError',
 'ReferenceError', 'ResourceWarning', 'RuntimeError', 'RuntimeWarning',

```

</details>

## Dense 2000 / latest

### D01 — error

Muốn viết đường dẫn Windows mà các ký tự như \n và \t không bị hiểu là xuống dòng hoặc tab, tiền tố chuỗi nào được tài liệu hướng dẫn?

**Nhãn đề xuất:** answer=0; context=0; abstention_correct=None

**Lý do:** Lỗi provider không có mã HTTP; không có final answer được chấp nhận. Giữ lỗi và chấm answer all-case bằng 0; không tự suy diễn đáp án. Chưa có context agent để đánh giá bằng chứng.

**Đáp án mong đợi / giới hạn corpus:** Đặt tiền tố r trước dấu nháy để tạo raw string.

**Đầu ra được chấp nhận:**
(không có)

**Lỗi:** provider / ProviderError

**Citation đã đọc:**

<details><summary>Context đã chuẩn bị</summary>

```text
(rỗng)
```

</details>

### D02 — error

Khi đánh chỉ số chuỗi từ phía cuối, -1 và -2 chỉ ký tự nào? Vì sao không bắt đầu bằng -0?

**Nhãn đề xuất:** answer=0; context=0; abstention_correct=None

**Lý do:** Lỗi provider không có mã HTTP; không có final answer được chấp nhận. Giữ lỗi và chấm answer all-case bằng 0; không tự suy diễn đáp án. Chưa có context agent để đánh giá bằng chứng.

**Đáp án mong đợi / giới hạn corpus:** -1 chỉ ký tự cuối, -2 chỉ ký tự áp cuối; -0 bằng 0 nên chỉ số âm bắt đầu từ -1.

**Đầu ra được chấp nhận:**
(không có)

**Lỗi:** provider / ProviderError

**Citation đã đọc:**

<details><summary>Context đã chuẩn bị</summary>

```text
(rỗng)
```

</details>

### D03 — error

Ví dụ list(range(5, 10)) trong tài liệu cho ra danh sách nào?

**Nhãn đề xuất:** answer=0; context=0; abstention_correct=None

**Lý do:** Lỗi provider không có mã HTTP; không có final answer được chấp nhận. Giữ lỗi và chấm answer all-case bằng 0; không tự suy diễn đáp án. Chưa có context agent để đánh giá bằng chứng.

**Đáp án mong đợi / giới hạn corpus:** [5, 6, 7, 8, 9]; cận 10 không được lấy.

**Đầu ra được chấp nhận:**
(không có)

**Lỗi:** provider / ProviderError

**Citation đã đọc:**

<details><summary>Context đã chuẩn bị</summary>

```text
(rỗng)
```

</details>

### D04 — error

Nếu có vòng lặp for lồng trong while, break nằm trong for sẽ thoát vòng nào theo quy tắc của tài liệu?

**Nhãn đề xuất:** answer=0; context=2; abstention_correct=None

**Lý do:** Lỗi provider không có mã HTTP; không có final answer được chấp nhận. Giữ lỗi và chấm answer all-case bằng 0; không tự suy diễn đáp án. Context đã chuẩn bị có đủ evidence nhưng request sinh câu trả lời lỗi; không xác nhận model nhận được context.

**Đáp án mong đợi / giới hạn corpus:** Thoát vòng for ở trong cùng bao quanh break, không tự động thoát cả vòng while bên ngoài.

**Đầu ra được chấp nhận:**
(không có)

**Lỗi:** provider / ProviderError

**Citation đã đọc:**

<details><summary>Context đã chuẩn bị</summary>

```text
[6f16320109f4a36189eb5033ecbb89b2 | https://docs.python.org/3.14/tutorial/controlflow.html | page python-3.14-ch04-u002]
4.4. break and continue Statements

The break statement breaks out of the innermost enclosing for or while loop:

>>> for n in range(2, 10):
...     for x in range(2, n):
...         if n % x == 0:
...             print(f"{n} equals {x} * {n//x}")
...             break
...
4 equals 2 * 2
6 equals 2 * 3
8 equals 2 * 4
9 equals 3 * 3

The continue statement continues with the next iteration of the loop:

[e09df3f01953e055de669d3402d7ddac | https://docs.python.org/3.14/tutorial/controlflow.html | page python-3.14-ch04-u002]
4.5. else Clauses on Loops

In a for or while loop the break statement may be paired with an else clause. If the loop finishes without executing the break, the else clause executes.

In a for loop, the else clause is executed after the loop finishes its final iteration, that is, if no break occurred.

In a while loop, it’s executed after the loop’s condition becomes false.

[2df57e0bc5ea73bc55a3cee76070ef4f | https://docs.python.org/3.14/tutorial/controlflow.html | page python-3.14-ch04-u003]
(Yes, this is the correct code. Look closely: the else clause belongs to the for loop, not the if statement.)

One way to think of the else clause is to imagine it paired with the if inside the loop. As the loop executes, it will run a sequence like if/if/if/else. The if is inside the loop, encountered a number of times. If the condition is ever true, a break will happen. If the condition is never true, the else clause outside the loop will execute.
```

</details>

### D05 — error

Các đối số bổ sung được gom bởi *args trong định nghĩa hàm có kiểu cấu trúc dữ liệu gì?

**Nhãn đề xuất:** answer=0; context=0; abstention_correct=None

**Lý do:** Lỗi provider không có mã HTTP; không có final answer được chấp nhận. Giữ lỗi và chấm answer all-case bằng 0; không tự suy diễn đáp án. Chưa có context agent để đánh giá bằng chứng.

**Đáp án mong đợi / giới hạn corpus:** Một tuple chứa các đối số vị trí bổ sung.

**Đầu ra được chấp nhận:**
(không có)

**Lỗi:** provider / ProviderError

**Citation đã đọc:**

<details><summary>Context đã chuẩn bị</summary>

```text
(rỗng)
```

</details>

### D06 — answered

Tham số **name nhận những đối số nào và lưu trong kiểu dữ liệu gì?

**Nhãn đề xuất:** answer=2; context=2; abstention_correct=None

**Lý do:** Đủ keyword arguments dư, loại đối số đã khớp tham số hình thức, và kiểu dictionary.

**Đáp án mong đợi / giới hạn corpus:** Nhận các keyword arguments không ứng với tham số hình thức đã khai báo và lưu thành dictionary.

**Đầu ra được chấp nhận:**
Khi tham số hình thức cuối cùng có dạng **name, nó nhận một dictionary (kiểu Mapping — dict) chứa tất cả các đối số từ khóa (keyword arguments) ngoại trừ những đối số tương ứng với một tham số hình thức khác. Nó có thể được kết hợp với tham số dạng *name (nhận tuple các đối số vị trí vượt quá danh sách tham số hình thức), và *name phải đứng trước **name [a406cc7dac32b6727ecb688a6d3b9286].

**Citation đã đọc:**
- `a406cc7dac32b6727ecb688a6d3b9286`: True — Định nghĩa **name là dictionary chứa keyword arguments chưa khớp formal parameter; cũng hỗ trợ phần bổ sung *name.

<details><summary>Context đã chuẩn bị</summary>

```text
[a406cc7dac32b6727ecb688a6d3b9286 | https://docs.python.org/3.14/tutorial/controlflow.html | page python-3.14-ch04-u009]
When a final formal parameter of the form **name is present, it receives a dictionary (see Mapping Types — dict) containing all keyword arguments except for those corresponding to a formal parameter. This may be combined with a formal parameter of the form *name (described in the next subsection) which receives a tuple containing the positional arguments beyond the formal parameter list. (*name must occur before **name.) For example, if we define a function like this:

[a40e04bdcbe4d88c4ee0527d01776073 | https://docs.python.org/3.14/tutorial/controlflow.html | page python-3.14-ch04-u012]
>>> list(range(3, 6))            # normal call with separate arguments
[3, 4, 5]
>>> args = [3, 6]
>>> list(range(*args))            # call with arguments unpacked from a list
[3, 4, 5]

In the same fashion, dictionaries can deliver keyword arguments with the **-operator:

[16ce190fe7ecb304045bc7fd1a403985 | https://docs.python.org/3.14/tutorial/controlflow.html | page python-3.14-ch04-u011]
But using / (positional only arguments), it is possible since it allows name as a positional argument and 'name' as a key in the keyword arguments:

>>> def foo(name, /, **kwds):
...     return 'name' in kwds
...
>>> foo(1, **{'name': 2})
True

In other words, the names of positional-only parameters can be used in **kwds without ambiguity.

[ae0fc3e74e7c0bae057391fca74c3eeb | https://docs.python.org/3.14/tutorial/controlflow.html | page python-3.14-ch04-u008]
4.9.2. Keyword Arguments

Functions can also be called using keyword arguments of the form kwarg=value. For instance, the following function:

def parrot(voltage, state='a stiff', action='voom', type='Norwegian Blue'):
    print("-- This parrot wouldn't", action, end=' ')
    print("if you put", voltage, "volts through it.")
    print("-- Lovely plumage, the", type)
    print("-- It's", state, "!")
```

</details>

### D07 — error

Muốn tạo tuple chỉ chứa chuỗi hello thì chỉ viết ngoặc quanh giá trị có đủ không? Cú pháp cần thêm gì?

**Nhãn đề xuất:** answer=0; context=2; abstention_correct=None

**Lý do:** Lỗi provider không có mã HTTP; không có final answer được chấp nhận. Giữ lỗi và chấm answer all-case bằng 0; không tự suy diễn đáp án. Context đã chuẩn bị có đủ evidence nhưng request sinh câu trả lời lỗi; không xác nhận model nhận được context.

**Đáp án mong đợi / giới hạn corpus:** Không đủ; phải có dấu phẩy sau giá trị, ví dụ ('hello',) hoặc 'hello',.

**Đầu ra được chấp nhận:**
(không có)

**Lỗi:** provider / ProviderError

**Citation đã đọc:**

<details><summary>Context đã chuẩn bị</summary>

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

[271c4db72dfc9ab3cc659e83ef58fa06 | https://docs.python.org/3.14/tutorial/datastructures.html | page python-3.14-ch05-u005]
As you see, on output tuples are always enclosed in parentheses, so that nested tuples are interpreted correctly; they may be input with or without surrounding parentheses, although often parentheses are necessary anyway (if the tuple is part of a larger expression). It is not possible to assign to the individual items of a tuple, however it is possible to create tuples which contain mutable objects, such as lists.

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

</details>

### D08 — answered

a.pop() không truyền index sẽ xóa và trả về phần tử nào? Điều gì xảy ra nếu a rỗng?

**Nhãn đề xuất:** answer=2; context=2; abstention_correct=None

**Lý do:** Đủ xóa/trả phần tử cuối và IndexError khi list rỗng.

**Đáp án mong đợi / giới hạn corpus:** Xóa và trả về phần tử cuối; nếu list rỗng thì phát sinh IndexError.

**Đầu ra được chấp nhận:**
a.pop() không truyền index sẽ xóa và trả về phần tử cuối cùng của list ("If no index is specified, a.pop() removes and returns the last item in the list") [e4976e7c8c03d1c6a37a18f46e14e9dd]. Nếu list rỗng, nó sẽ ném ra IndexError ("It raises an IndexError if the list is empty or the index is outside the list range") [e4976e7c8c03d1c6a37a18f46e14e9dd]. Điều này cũng nhất quán với cách dùng list như stack: pop() không có index lấy phần tử ở đỉnh stack [e8d023727367b0f20a7c3b6060eee5e1].

**Citation đã đọc:**
- `e4976e7c8c03d1c6a37a18f46e14e9dd`: True — Nêu pop không index xóa/trả phần tử cuối và IndexError với list rỗng.
- `e8d023727367b0f20a7c3b6060eee5e1`: True — Hỗ trợ phần bổ sung list là stack LIFO và pop() không index lấy phần tử đỉnh.

<details><summary>Context đã chuẩn bị</summary>

```text
[e8d023727367b0f20a7c3b6060eee5e1 | https://docs.python.org/3.14/tutorial/datastructures.html | page python-3.14-ch05-u002]
5.1.1. Using Lists as Stacks

The list methods make it very easy to use a list as a stack, where the last element added is the first element retrieved (“last-in, first-out”). To add an item to the top of the stack, use append(). To retrieve an item from the top of the stack, use pop() without an explicit index. For example:

[08cc1a23a50cfe385721826ae05c568c | https://docs.python.org/3.14/tutorial/controlflow.html | page python-3.14-ch04-u002]
Later we will see more functions that return iterables and take iterables as arguments. In chapter Data Structures, we will discuss list() in more detail.

[847870e76b53277ae6eb98a917b193c0 | https://docs.python.org/3.14/tutorial/datastructures.html | page python-3.14-ch05-u002]
5.1.2. Using Lists as Queues

It is also possible to use a list as a queue, where the first element added is the first element retrieved (“first-in, first-out”); however, lists are not efficient for this purpose. While appends and pops from the end of list are fast, doing inserts or pops from the beginning of a list is slow (because all of the other elements have to be shifted by one). See Time complexity of operations on built-in types for more information.

[e4976e7c8c03d1c6a37a18f46e14e9dd | https://docs.python.org/3.14/tutorial/datastructures.html | page python-3.14-ch05-u001]
Remove the item at the given position in the list, and return it. If no index is specified, a.pop() removes and returns the last item in the list. It raises an IndexError if the list is empty or the index is outside the list range.

list.clear()

Remove all items from the list. Similar to del a[:].

list.index(value[, start[, stop]])

Return zero-based index of the first occurrence of value in the list. Raises a ValueError if there is no such item.
```

</details>

### D09 — error

Khi duyệt dictionary, dùng phương thức nào để lấy đồng thời khóa và giá trị tương ứng?

**Nhãn đề xuất:** answer=0; context=2; abstention_correct=None

**Lý do:** Lỗi provider không có mã HTTP; không có final answer được chấp nhận. Giữ lỗi và chấm answer all-case bằng 0; không tự suy diễn đáp án. Context đã chuẩn bị có đủ evidence nhưng request sinh câu trả lời lỗi; không xác nhận model nhận được context.

**Đáp án mong đợi / giới hạn corpus:** Dùng phương thức items(), ví dụ for k, v in d.items().

**Đầu ra được chấp nhận:**
(không có)

**Lỗi:** provider / ProviderError

**Citation đã đọc:**

<details><summary>Context đã chuẩn bị</summary>

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

[6a283703bc3b7d5deaceb4053de6cb12 | https://docs.python.org/3.14/tutorial/datastructures.html | page python-3.14-ch05-u007]
The main operations on a dictionary are storing a value with some key and extracting the value given the key. It is also possible to delete a key:value pair with del. If you store using a key that is already in use, the old value associated with that key is forgotten.

[ac6c1afbbdfdef051c6c2d881e0c8b5b | https://docs.python.org/3.14/tutorial/datastructures.html | page python-3.14-ch05-u007]
The dict() constructor builds dictionaries directly from sequences of key-value pairs:

>>> dict([('sape', 4139), ('guido', 4127), ('jack', 4098)])
{'sape': 4139, 'guido': 4127, 'jack': 4098}

In addition, dict comprehensions can be used to create dictionaries from arbitrary key and value expressions:

>>> {x: x**2 for x in (2, 4, 6)}
{2: 4, 4: 16, 6: 36}

When the keys are simple strings, it is sometimes easier to specify pairs using keyword arguments:
```

</details>

### D10 — answered

Có hai sequence cần duyệt đồng thời thành từng cặp phần tử tương ứng. Tài liệu giới thiệu hàm nào?

**Nhãn đề xuất:** answer=2; context=2; abstention_correct=None

**Lý do:** Đúng zip() để ghép phần tử tương ứng của hai/nhiều sequence.

**Đáp án mong đợi / giới hạn corpus:** Dùng zip() để ghép các phần tử tương ứng khi duyệt hai hoặc nhiều sequence.

**Đầu ra được chấp nhận:**
Tài liệu giới thiệu hàm zip(). Để duyệt hai hoặc nhiều sequence đồng thời, các phần tử có thể được ghép cặp bằng hàm zip(), ví dụ: for q, a in zip(questions, answers): ... [d0465c0ebf1bcc71b35de11057f991e9]

**Citation đã đọc:**
- `d0465c0ebf1bcc71b35de11057f991e9`: True — Nêu zip ghép entries của hai/nhiều sequence và ví dụ hai danh sách.

<details><summary>Context đã chuẩn bị</summary>

```text
[05405500dec053b3c7600a61076a5941 | https://docs.python.org/3.14/tutorial/datastructures.html | page python-3.14-ch05-u004]
>>> list(zip(*matrix))
[(1, 5, 9), (2, 6, 10), (3, 7, 11), (4, 8, 12)]

See Unpacking Argument Lists for details on the asterisk in this line.

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

[08cc1a23a50cfe385721826ae05c568c | https://docs.python.org/3.14/tutorial/controlflow.html | page python-3.14-ch04-u002]
Later we will see more functions that return iterables and take iterables as arguments. In chapter Data Structures, we will discuss list() in more detail.

[3ae984dcd6ea0fd56b8d4818aede35d0 | https://docs.python.org/3.14/tutorial/datastructures.html | page python-3.14-ch05-u005]
This is called, appropriately enough, sequence unpacking and works for any sequence on the right-hand side. Sequence unpacking requires that there are as many variables on the left side of the equals sign as there are elements in the sequence. Note that multiple assignment is really just a combination of tuple packing and sequence unpacking.
```

</details>

### D11 — error

dir() không truyền đối số liệt kê những tên nào? Nó có tự liệt kê tên hàm và biến built-in không?

**Nhãn đề xuất:** answer=0; context=0; abstention_correct=None

**Lý do:** Lỗi provider không có mã HTTP; không có final answer được chấp nhận. Giữ lỗi và chấm answer all-case bằng 0; không tự suy diễn đáp án. Chưa có context agent để đánh giá bằng chứng.

**Đáp án mong đợi / giới hạn corpus:** Liệt kê các tên đang được định nghĩa như biến, module và hàm; không liệt kê các tên hàm và biến built-in.

**Đầu ra được chấp nhận:**
(không có)

**Lỗi:** provider / ProviderError

**Citation đã đọc:**

<details><summary>Context đã chuẩn bị</summary>

```text
(rỗng)
```

</details>

### D12 — answered

Python dựa vào thông tin nào của file nguồn để quyết định module đã biên dịch có lỗi thời và cần biên dịch lại?

**Nhãn đề xuất:** answer=2; context=2; abstention_correct=None

**Lý do:** Đúng so sánh modification date của nguồn với bản đã biên dịch.

**Đáp án mong đợi / giới hạn corpus:** So sánh ngày/giờ sửa đổi của mã nguồn với phiên bản đã biên dịch.

**Đầu ra được chấp nhận:**
Python kiểm tra ngày sửa đổi (modification date) của file nguồn so với phiên bản đã biên dịch để xem module đã biên dịch có lỗi thời và cần biên dịch lại hay không; đây là quá trình hoàn toàn tự động [4b9311d6dabb880f0d9037d258d191b8].

**Citation đã đọc:**
- `4b9311d6dabb880f0d9037d258d191b8`: True — Nêu kiểm tra ngày sửa nguồn và compiled version để quyết định biên dịch lại.

<details><summary>Context đã chuẩn bị</summary>

```text
[4b9311d6dabb880f0d9037d258d191b8 | https://docs.python.org/3.14/tutorial/modules.html | page python-3.14-ch06-u004]
Python checks the modification date of the source against the compiled version to see if it’s out of date and needs to be recompiled. This is a completely automatic process. Also, the compiled modules are platform-independent, so the same library can be shared among systems with different architectures.

[2710a5930f78e76bbaa16236576d8562 | https://docs.python.org/3.14/tutorial/modules.html | page python-3.14-ch06-u004]
Python does not check the cache in two circumstances. First, it always recompiles and does not store the result for the module that’s loaded directly from the command line. Second, it does not check the cache if there is no source module. To support a non-source (compiled only) distribution, the compiled module must be in the source directory, and there must not be a source module.

Some tips for experts:

[dfa958b48abdf6dbd7a440377512c745 | https://docs.python.org/3.14/tutorial/modules.html | page python-3.14-ch06-u004]
A program doesn’t run any faster when it is read from a .pyc file than when it is read from a .py file; the only thing that’s faster about .pyc files is the speed with which they are loaded.

The module compileall can create .pyc files for all modules in a directory.

There is more detail on this process, including a flow chart of the decisions, in PEP 3147.

[3e7ab623ba54a8d3e2bc09914534e6a1 | https://docs.python.org/3.14/tutorial/modules.html | page python-3.14-ch06-u005]
 'getfilesystemencodeerrors', 'getfilesystemencoding', 'getprofile',
 'getrecursionlimit', 'getrefcount', 'getsizeof', 'getswitchinterval',
 'gettrace', 'hash_info', 'hexversion', 'implementation', 'int_info',
 'intern', 'is_finalizing', 'last_traceback', 'last_type', 'last_value',
 'maxsize', 'maxunicode', 'meta_path', 'modules', 'path', 'path_hooks',
 'path_importer_cache', 'platform', 'prefix', 'ps1', 'ps2', 'pycache_prefix',

```

</details>

### D13 — answered

Với file vừa mở để đọc và đang ở đầu file, bỏ size hoặc truyền size âm cho f.read(size) sẽ đọc bao nhiêu? Rủi ro bộ nhớ được tài liệu nhắc là gì?

**Nhãn đề xuất:** answer=2; context=2; abstention_correct=None

**Lý do:** Đủ đọc toàn bộ khi bỏ size/size âm và cảnh báo file lớn hơn bộ nhớ.

**Đáp án mong đợi / giới hạn corpus:** Đọc toàn bộ nội dung file; file quá lớn có thể vượt bộ nhớ máy.

**Đầu ra được chấp nhận:**
Khi bỏ size hoặc truyền size âm cho f.read(size), toàn bộ nội dung file sẽ được đọc và trả về [b2e4e2a1efb032538c84a9e87be3cfb4]. Tài liệu cảnh báo rằng "it's your problem if the file is twice as large as your machine's memory" — tức là rủi ro là file có thể lớn gấp đôi bộ nhớ của máy, và việc này do bạn tự chịu trách nhiệm [b2e4e2a1efb032538c84a9e87be3cfb4].

**Citation đã đọc:**
- `b2e4e2a1efb032538c84a9e87be3cfb4`: True — Nêu text/bytes, trường hợp size omitted/negative, cảnh báo bộ nhớ và nhánh otherwise tối đa size.

<details><summary>Context đã chuẩn bị</summary>

```text
[b2e4e2a1efb032538c84a9e87be3cfb4 | https://docs.python.org/3.14/tutorial/inputoutput.html | page python-3.14-ch07-u005]
To read a file’s contents, call f.read(size), which reads some quantity of data and returns it as a string (in text mode) or bytes object (in binary mode). size is an optional numeric argument. When size is omitted or negative, the entire contents of the file will be read and returned; it’s your problem if the file is twice as large as your machine’s memory. Otherwise, at most size characters (in text mode) or size bytes (in binary mode) are read and returned. If the end of the file has been 

[88e5cfa94339c9566fd9682ea7f267f0 | https://docs.python.org/3.14/tutorial/inputoutput.html | page python-3.14-ch07-u006]
>>> f.read()
'This is the entire file.\n'
>>> f.read()
''

f.readline() reads a single line from the file; a newline character (\n) is left at the end of the string, and is only omitted on the last line of the file if the file doesn’t end in a newline. This makes the return value unambiguous; if f.readline() returns an empty string, the end of the file has been reached, while a blank line is represented by '\n', a string containing only a single newline.

[5c1c637fc4b007260e53d8163375a998 | https://docs.python.org/3.14/tutorial/inputoutput.html | page python-3.14-ch07-u005]
In text mode, the default when reading is to convert platform-specific line endings (\n on Unix, \r\n on Windows) to just \n. When writing in text mode, the default is to convert occurrences of \n back to platform-specific line endings. This behind-the-scenes modification to file data is fine for text files, but will corrupt binary data like that in JPEG or EXE files. Be very careful to use binary mode when reading and writing such files.
```

</details>

### D14 — answered

Giá trị f.tell() trong binary mode và text mode có ý nghĩa khác nhau thế nào?

**Nhãn đề xuất:** answer=2; context=2; abstention_correct=None

**Lý do:** Đủ byte offset trong binary và opaque position trong text.

**Đáp án mong đợi / giới hạn corpus:** Binary mode: số byte tính từ đầu file. Text mode: một số opaque biểu diễn vị trí, không nên hiểu là số byte.

**Đầu ra được chấp nhận:**
Theo tài liệu: f.tell() trả về một số nguyên cho biết vị trí hiện tại của file object — ở binary mode đó là số byte tính từ đầu file, còn ở text mode đó là một "opaque number" (con số không mang ý nghĩa byte cụ thể) [9c4ec9a68dac484801d37366b0214e51]. Liên quan đến điều này, với text file (mở không có 'b' trong mode), chỉ cho phép seek tương đối so với đầu file (ngoại lệ là seek tới cuối file bằng seek(0, 2)) và các giá trị offset hợp lệ duy nhất là những giá trị do f.tell() trả về, hoặc 0; mọi offset khác gây hành vi không xác định [dbb1c2a57f3bdb25359e5a45739375d9].

**Citation đã đọc:**
- `9c4ec9a68dac484801d37366b0214e51`: True — Nêu trực tiếp byte position ở binary và opaque number ở text.
- `dbb1c2a57f3bdb25359e5a45739375d9`: True — Hỗ trợ riêng phần bổ sung về các offset seek hợp lệ cho text.

<details><summary>Context đã chuẩn bị</summary>

```text
[9c4ec9a68dac484801d37366b0214e51 | https://docs.python.org/3.14/tutorial/inputoutput.html | page python-3.14-ch07-u006]
f.tell() returns an integer giving the file object’s current position in the file represented as number of bytes from the beginning of the file when in binary mode and an opaque number when in text mode.

[dbb1c2a57f3bdb25359e5a45739375d9 | https://docs.python.org/3.14/tutorial/inputoutput.html | page python-3.14-ch07-u006]
In text files (those opened without a b in the mode string), only seeks relative to the beginning of the file are allowed (the exception being seeking to the very file end with seek(0, 2)) and the only valid offset values are those returned from the f.tell(), or zero. Any other offset value produces undefined behaviour.

[e3dd727e9d10ff3ef55e9dda334b3b96 | https://docs.python.org/3.14/tutorial/inputoutput.html | page python-3.14-ch07-u005]
encoding when opening file in binary mode.

[6fbf000a89c6f543bce38bbfb2905520 | https://docs.python.org/3.14/tutorial/inputoutput.html | page python-3.14-ch07-u006]
f.write(string) writes the contents of string to the file, returning the number of characters written.

>>> f.write('This is a test\n')
15

Other types of objects need to be converted – either to a string (in text mode) or a bytes object (in binary mode) – before writing them:

>>> value = ('the answer', 42)
>>> s = str(value)  # convert the tuple to string
>>> f.write(s)
18
```

</details>

### D15 — answered

Trong try...except, khối else phải đặt sau phần nào và được dùng khi nào?

**Nhãn đề xuất:** answer=2; context=2; abstention_correct=None

**Lý do:** Đủ else sau tất cả except và chỉ chạy khi try không phát sinh ngoại lệ.

**Đáp án mong đợi / giới hạn corpus:** Đặt sau tất cả các except; dùng cho code chỉ chạy khi khối try không phát sinh ngoại lệ.

**Đầu ra được chấp nhận:**
Khối else là tùy chọn trong câu lệnh try … except; khi có mặt, nó phải đặt sau tất cả các khối except. Nó hữu ích cho đoạn mã cần được thực thi nếu khối try không gây ra ngoại lệ [89cb0b58f013c40c3ef13c336fcb8792].

**Citation đã đọc:**
- `89cb0b58f013c40c3ef13c336fcb8792`: True — Hỗ trợ cả vị trí sau tất cả except và điều kiện try không có ngoại lệ.

<details><summary>Context đã chuẩn bị</summary>

```text
[a9b61cae10de6e45674d2656e1ff3c38 | https://docs.python.org/3.14/tutorial/errors.html | page python-3.14-ch08-u006]
If an exception occurs during execution of the try clause, the exception may be handled by an except clause. If the exception is not handled by an except clause, the exception is re-raised after the finally clause has been executed.

An exception could occur during execution of an except or else clause. Again, the exception is re-raised after the finally clause has been executed.

[6b8205431dca57f8309581db45ed672e | https://docs.python.org/3.14/tutorial/errors.html | page python-3.14-ch08-u002]
A try statement may have more than one except clause, to specify handlers for different exceptions. At most one handler will be executed. Handlers only handle exceptions that occur in the corresponding try clause, not in other handlers of the same try statement. An except clause may name multiple exceptions, for example:

... except RuntimeError, TypeError, NameError:
...     pass

[74e63b1a1f4e5a3cc37ae4c983f65dde | https://docs.python.org/3.14/tutorial/errors.html | page python-3.14-ch08-u005]
If a finally clause is present, the finally clause will execute as the last task before the try statement completes. The finally clause runs whether or not the try statement produces an exception. The following points discuss more complex cases when an exception occurs:

[89cb0b58f013c40c3ef13c336fcb8792 | https://docs.python.org/3.14/tutorial/errors.html | page python-3.14-ch08-u003]
The try … except statement has an optional else clause, which, when present, must follow all except clauses. It is useful for code that must be executed if the try clause does not raise an exception. For example:
```

</details>

### D16 — error

Chỉ dựa trên tài liệu đã cung cấp, khi một task trong asyncio.TaskGroup lỗi, các task còn lại được hủy và chờ kết thúc như thế nào?

**Nhãn đề xuất:** answer=None; context=None; abstention_correct=False

**Lý do:** Lỗi provider không có mã HTTP; không có final answer được chấp nhận. Giữ lỗi và chấm answer all-case bằng 0; không tự suy diễn đáp án. Lỗi không được tính là từ chối đúng.

**Đáp án mong đợi / giới hạn corpus:** Corpus không có phần giải thích asyncio hoặc TaskGroup. Các mục vòng lặp/ngoại lệ không quy định ngữ nghĩa hủy task bất đồng bộ.

**Đầu ra được chấp nhận:**
(không có)

**Lỗi:** provider / ProviderError

**Citation đã đọc:**

<details><summary>Context đã chuẩn bị</summary>

```text
[d7935416e6a4422454632df7af21d446 | https://docs.python.org/3.14/tutorial/errors.html | page python-3.14-ch08-u008]
...     print("There were SystemErrors")
...
There were OSErrors
There were SystemErrors
  + Exception Group Traceback (most recent call last):
  |   File "<stdin>", line 2, in <module>
  |     f()
  |     ~^^
  |   File "<stdin>", line 2, in f
  |     raise ExceptionGroup(
  |     ...<12 lines>...
  |     )
  | ExceptionGroup: group1 (1 sub-exception)
  +-+---------------- 1 ----------------
    | ExceptionGroup: group2 (1 sub-exception)
    +-+---------------- 1 ----------------


[b1a08e0d1d99f8cd3598859d0523c3be | https://docs.python.org/3.14/tutorial/errors.html | page python-3.14-ch08-u008]
>>> def f():
...     raise ExceptionGroup(
...         "group1",
...         [
...             OSError(1),
...             SystemError(2),
...             ExceptionGroup(
...                 "group2",
...                 [
...                     OSError(3),
...                     RecursionError(4)
...                 ]
...             )
...         ]
...     )
...
>>> try:
...     f()
... except* OSError as e:
...     print("There were OSErrors")
... except* SystemError as e:


[dfe29fdd1b1fc2c1e55a629f7499f668 | https://docs.python.org/3.14/tutorial/errors.html | page python-3.14-ch08-u007]
The builtin ExceptionGroup wraps a list of exception instances so that they can be raised together. It is an exception itself, so it can be caught like any other exception.

[9126cd3fef32cc3e468d8edc25111ce4 | https://docs.python.org/3.14/tutorial/errors.html | page python-3.14-ch08-u008]
      | RecursionError: 4
      +------------------------------------
>>>
```

</details>

### D17 — abstain

Tài liệu đã cung cấp hướng dẫn dùng @dataclass(frozen=True) để ngăn gán lại thuộc tính như thế nào và phát sinh ngoại lệ gì khi cố gán?

**Nhãn đề xuất:** answer=None; context=None; abstention_correct=True

**Lý do:** Đã đọc lời từ chối và context: không bổ sung cơ chế kỹ thuật hoặc đoán ngoại lệ; phù hợp corpus absence audit.

**Đáp án mong đợi / giới hạn corpus:** dataclasses chỉ được nhắc làm ví dụ lớp có thứ tự thuộc tính trong match; frozen xuất hiện trong tên built-in frozenset. Không có hướng dẫn frozen=True hoặc ngoại lệ khi gán.

**Đầu ra được chấp nhận:**
Không đủ bằng chứng trong tài liệu để trả lời: các đoạn tài liệu hiện có chỉ nói về cơ chế raise ngoại lệ nói chung và danh sách tên ngoại lệ, không có nội dung nào về @dataclass(frozen=True) hay ngoại lệ phát sinh khi cố gán lại thuộc tính.

**Citation đã đọc:**

<details><summary>Context đã chuẩn bị</summary>

```text
[22301843e855f993ff0daa2a245506d0 | https://docs.python.org/3.14/tutorial/errors.html | page python-3.14-ch08-u005]
    raise RuntimeError('Failed to open database') from exc
RuntimeError: Failed to open database

[f56f1b83badcd52d685382d45a8001a6 | https://docs.python.org/3.14/tutorial/modules.html | page python-3.14-ch06-u006]
 'StopIteration', 'SyntaxError', 'SyntaxWarning', 'SystemError',
 'SystemExit', 'TabError', 'TimeoutError', 'True', 'TypeError',
 'UnboundLocalError', 'UnicodeDecodeError', 'UnicodeEncodeError',
 'UnicodeError', 'UnicodeTranslateError', 'UnicodeWarning', 'UserWarning',
 'ValueError', 'Warning', 'ZeroDivisionError', '_', '__build_class__',
 '__debug__', '__doc__', '__import__', '__name__', '__package__', 'abs',
 'all', 'any', 'ascii', 'bin', 'bool', 'bytearray', 'bytes', 'callable',


[eb1202071982afa8de740c2fa8c71a8f | https://docs.python.org/3.14/tutorial/errors.html | page python-3.14-ch08-u004]
The sole argument to raise indicates the exception to be raised. This must be either an exception instance or an exception class (a class that derives from BaseException, such as Exception or one of its subclasses). If an exception class is passed, it will be implicitly instantiated by calling its constructor with no arguments:

raise ValueError  # shorthand for 'raise ValueError()'

[9126cd3fef32cc3e468d8edc25111ce4 | https://docs.python.org/3.14/tutorial/errors.html | page python-3.14-ch08-u008]
      | RecursionError: 4
      +------------------------------------
>>>
```

</details>

