# Bản nháp benchmark để kiểm tra

24 câu, AI-assisted; nhãn chưa được người dùng xác nhận. Chưa chạy retrieval/model hoặc chấm điểm.

Chỉ dùng dev để cải tiến. Phần test ở cuối dành cho kiểm tra nhãn trước khi đóng băng; sau khi bắt đầu chạy dev, không dùng test để chỉnh cấu hình.

## DEV

### D01 — Có đáp án

Muốn viết đường dẫn Windows mà các ký tự như \n và \t không bị hiểu là xuống dòng hoặc tab, tiền tố chuỗi nào được tài liệu hướng dẫn?

**Đáp án mong đợi:** Đặt tiền tố r trước dấu nháy để tạo raw string.

**Nguồn:** [python-3.14-ch03](https://docs.python.org/3.14/tutorial/introduction.html); đơn vị `python-3.14-ch03-u003`; chunk `5046e99636180b57c2960fedf1d3566c`.

**Bằng chứng:**

```text
If you don’t want characters prefaced by \ to be interpreted as special characters, you can use raw strings by adding an r before the first quote:
```

### D02 — Có đáp án

Khi đánh chỉ số chuỗi từ phía cuối, -1 và -2 chỉ ký tự nào? Vì sao không bắt đầu bằng -0?

**Đáp án mong đợi:** -1 chỉ ký tự cuối, -2 chỉ ký tự áp cuối; -0 bằng 0 nên chỉ số âm bắt đầu từ -1.

**Nguồn:** [python-3.14-ch03](https://docs.python.org/3.14/tutorial/introduction.html); đơn vị `python-3.14-ch03-u004`; chunk `07eab24fdef0d6f3c82bb56fb67407ce`.

**Bằng chứng:**

```text
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

### D03 — Có đáp án

Ví dụ list(range(5, 10)) trong tài liệu cho ra danh sách nào?

**Đáp án mong đợi:** [5, 6, 7, 8, 9]; cận 10 không được lấy.

**Nguồn:** [python-3.14-ch04](https://docs.python.org/3.14/tutorial/controlflow.html); đơn vị `python-3.14-ch04-u002`; chunk `5b0389b2014ead261047a7ea77039951`.

**Bằng chứng:**

```text
>>> list(range(5, 10))
[5, 6, 7, 8, 9]
```

### D04 — Có đáp án

Nếu có vòng lặp for lồng trong while, break nằm trong for sẽ thoát vòng nào theo quy tắc của tài liệu?

**Đáp án mong đợi:** Thoát vòng for ở trong cùng bao quanh break, không tự động thoát cả vòng while bên ngoài.

**Nguồn:** [python-3.14-ch04](https://docs.python.org/3.14/tutorial/controlflow.html); đơn vị `python-3.14-ch04-u002`; chunk `6f16320109f4a36189eb5033ecbb89b2`.

**Bằng chứng:**

```text
The break statement breaks out of the innermost enclosing for or while loop:
```

### D05 — Có đáp án

Các đối số bổ sung được gom bởi *args trong định nghĩa hàm có kiểu cấu trúc dữ liệu gì?

**Đáp án mong đợi:** Một tuple chứa các đối số vị trí bổ sung.

**Nguồn:** [python-3.14-ch04](https://docs.python.org/3.14/tutorial/controlflow.html); đơn vị `python-3.14-ch04-u012`; chunk `72ba98c7f88046b6519961423f685ff5`.

**Bằng chứng:**

```text
Finally, the least frequently used option is to specify that a function can be called with an arbitrary number of arguments. These arguments will be wrapped up in a tuple (see Tuples and Sequences).
```

### D06 — Có đáp án

Tham số **name nhận những đối số nào và lưu trong kiểu dữ liệu gì?

**Đáp án mong đợi:** Nhận các keyword arguments không ứng với tham số hình thức đã khai báo và lưu thành dictionary.

**Nguồn:** [python-3.14-ch04](https://docs.python.org/3.14/tutorial/controlflow.html); đơn vị `python-3.14-ch04-u009`; chunk `a406cc7dac32b6727ecb688a6d3b9286`.

**Bằng chứng:**

```text
When a final formal parameter of the form **name is present, it receives a dictionary (see Mapping Types — dict) containing all keyword arguments except for those corresponding to a formal parameter.
```

### D07 — Có đáp án

Muốn tạo tuple chỉ chứa chuỗi hello thì chỉ viết ngoặc quanh giá trị có đủ không? Cú pháp cần thêm gì?

**Đáp án mong đợi:** Không đủ; phải có dấu phẩy sau giá trị, ví dụ ('hello',) hoặc 'hello',.

**Nguồn:** [python-3.14-ch05](https://docs.python.org/3.14/tutorial/datastructures.html); đơn vị `python-3.14-ch05-u005`; chunk `a14a0c62dbc9ade9275bb1cfd18bbc57`.

**Bằng chứng:**

```text
a tuple with one item is constructed by following a value with a comma (it is not sufficient to enclose a single value in parentheses).
```

### D08 — Có đáp án

a.pop() không truyền index sẽ xóa và trả về phần tử nào? Điều gì xảy ra nếu a rỗng?

**Đáp án mong đợi:** Xóa và trả về phần tử cuối; nếu list rỗng thì phát sinh IndexError.

**Nguồn:** [python-3.14-ch05](https://docs.python.org/3.14/tutorial/datastructures.html); đơn vị `python-3.14-ch05-u001`; chunk `e4976e7c8c03d1c6a37a18f46e14e9dd`.

**Bằng chứng:**

```text
If no index is specified, a.pop() removes and returns the last item in the list. It raises an IndexError if the list is empty or the index is outside the list range.
```

### D09 — Có đáp án

Khi duyệt dictionary, dùng phương thức nào để lấy đồng thời khóa và giá trị tương ứng?

**Đáp án mong đợi:** Dùng phương thức items(), ví dụ for k, v in d.items().

**Nguồn:** [python-3.14-ch05](https://docs.python.org/3.14/tutorial/datastructures.html); đơn vị `python-3.14-ch05-u007`; chunk `fa52d5bbb11517433573b8febe0a1876`.

**Bằng chứng:**

```text
When looping through dictionaries, the key and corresponding value can be retrieved at the same time using the items() method.
```

### D10 — Có đáp án

Có hai sequence cần duyệt đồng thời thành từng cặp phần tử tương ứng. Tài liệu giới thiệu hàm nào?

**Đáp án mong đợi:** Dùng zip() để ghép các phần tử tương ứng khi duyệt hai hoặc nhiều sequence.

**Nguồn:** [python-3.14-ch05](https://docs.python.org/3.14/tutorial/datastructures.html); đơn vị `python-3.14-ch05-u008`; chunk `d0465c0ebf1bcc71b35de11057f991e9`.

**Bằng chứng:**

```text
To loop over two or more sequences at the same time, the entries can be paired with the zip() function.
```

### D11 — Có đáp án

dir() không truyền đối số liệt kê những tên nào? Nó có tự liệt kê tên hàm và biến built-in không?

**Đáp án mong đợi:** Liệt kê các tên đang được định nghĩa như biến, module và hàm; không liệt kê các tên hàm và biến built-in.

**Nguồn:** [python-3.14-ch06](https://docs.python.org/3.14/tutorial/modules.html); đơn vị `python-3.14-ch06-u005`; chunk `653c279748bae8969296f00bc2941191`.

**Bằng chứng:**

```text
Without arguments, dir() lists the names you have defined currently:

>>> a = [1, 2, 3, 4, 5]
>>> import fibo
>>> fib = fibo.fib
>>> dir()
['__builtins__', '__name__', 'a', 'fib', 'fibo', 'sys']

Note that it lists all types of names: variables, modules, functions, etc.

dir() does not list the names of built-in functions and variables. If you want a list of those, they are defined in the standard module builtins:
```

### D12 — Có đáp án

Python dựa vào thông tin nào của file nguồn để quyết định module đã biên dịch có lỗi thời và cần biên dịch lại?

**Đáp án mong đợi:** So sánh ngày/giờ sửa đổi của mã nguồn với phiên bản đã biên dịch.

**Nguồn:** [python-3.14-ch06](https://docs.python.org/3.14/tutorial/modules.html); đơn vị `python-3.14-ch06-u004`; chunk `4b9311d6dabb880f0d9037d258d191b8`.

**Bằng chứng:**

```text
Python checks the modification date of the source against the compiled version to see if it’s out of date and needs to be recompiled.
```

### D13 — Có đáp án

Với file vừa mở để đọc và đang ở đầu file, bỏ size hoặc truyền size âm cho f.read(size) sẽ đọc bao nhiêu? Rủi ro bộ nhớ được tài liệu nhắc là gì?

**Đáp án mong đợi:** Đọc toàn bộ nội dung file; file quá lớn có thể vượt bộ nhớ máy.

**Nguồn:** [python-3.14-ch07](https://docs.python.org/3.14/tutorial/inputoutput.html); đơn vị `python-3.14-ch07-u005`; chunk `b2e4e2a1efb032538c84a9e87be3cfb4`.

**Bằng chứng:**

```text
When size is omitted or negative, the entire contents of the file will be read and returned; it’s your problem if the file is twice as large as your machine’s memory.
```

### D14 — Có đáp án

Giá trị f.tell() trong binary mode và text mode có ý nghĩa khác nhau thế nào?

**Đáp án mong đợi:** Binary mode: số byte tính từ đầu file. Text mode: một số opaque biểu diễn vị trí, không nên hiểu là số byte.

**Nguồn:** [python-3.14-ch07](https://docs.python.org/3.14/tutorial/inputoutput.html); đơn vị `python-3.14-ch07-u006`; chunk `9c4ec9a68dac484801d37366b0214e51`.

**Bằng chứng:**

```text
f.tell() returns an integer giving the file object’s current position in the file represented as number of bytes from the beginning of the file when in binary mode and an opaque number when in text mode.
```

### D15 — Có đáp án

Trong try...except, khối else phải đặt sau phần nào và được dùng khi nào?

**Đáp án mong đợi:** Đặt sau tất cả các except; dùng cho code chỉ chạy khi khối try không phát sinh ngoại lệ.

**Nguồn:** [python-3.14-ch08](https://docs.python.org/3.14/tutorial/errors.html); đơn vị `python-3.14-ch08-u003`; chunk `89cb0b58f013c40c3ef13c336fcb8792`.

**Bằng chứng:**

```text
The try … except statement has an optional else clause, which, when present, must follow all except clauses. It is useful for code that must be executed if the try clause does not raise an exception.
```

### D16 — Thiếu bằng chứng

Chỉ dựa trên tài liệu đã cung cấp, khi một task trong asyncio.TaskGroup lỗi, các task còn lại được hủy và chờ kết thúc như thế nào?

**Hành vi mong đợi:** Tìm tài liệu rồi nói rõ không đủ bằng chứng trong corpus; không điền đáp án từ kiến thức bên ngoài.

**Lý do:** Corpus không có phần giải thích asyncio hoặc TaskGroup. Các mục vòng lặp/ngoại lệ không quy định ngữ nghĩa hủy task bất đồng bộ.

### D17 — Thiếu bằng chứng

Tài liệu đã cung cấp hướng dẫn dùng @dataclass(frozen=True) để ngăn gán lại thuộc tính như thế nào và phát sinh ngoại lệ gì khi cố gán?

**Hành vi mong đợi:** Tìm tài liệu rồi nói rõ không đủ bằng chứng trong corpus; không điền đáp án từ kiến thức bên ngoài.

**Lý do:** dataclasses chỉ được nhắc làm ví dụ lớp có thứ tự thuộc tính trong match; frozen xuất hiện trong tên built-in frozenset. Không có hướng dẫn frozen=True hoặc ngoại lệ khi gán.

## TEST

### T01 — Có đáp án

Chuỗi literal dùng ba dấu nháy có giữ ký tự xuống dòng không? Theo ví dụ trong tài liệu, làm sao tránh đưa newline đầu tiên vào chuỗi?

**Đáp án mong đợi:** Các ký tự kết thúc dòng được đưa vào chuỗi; đặt dấu backslash ngay trước newline đầu tiên để bỏ newline đó.

**Nguồn:** [python-3.14-ch03](https://docs.python.org/3.14/tutorial/introduction.html); đơn vị `python-3.14-ch03-u003`; chunk `994429862692bd5708095b1fa49fd3f0`.

**Bằng chứng:**

```text
String literals can span multiple lines. One way is using triple-quotes: """...""" or '''...'''. End-of-line characters are automatically included in the string, but it’s possible to prevent this by adding a \ at the end of the line. In the following example, the initial newline is not included:
```

### T02 — Có đáp án

Để buộc tham số của hàm chỉ được truyền bằng tên, cần đặt ký hiệu nào và ở vị trí nào trong danh sách tham số?

**Đáp án mong đợi:** Đặt dấu * ngay trước tham số keyword-only đầu tiên.

**Nguồn:** [python-3.14-ch04](https://docs.python.org/3.14/tutorial/controlflow.html); đơn vị `python-3.14-ch04-u010`; chunk `e5a6879e3f04a49ee60f47f27e202599`.

**Bằng chứng:**

```text
To mark parameters as keyword-only, indicating the parameters must be passed by keyword argument, place an * in the arguments list just before the first keyword-only parameter.
```

### T03 — Có đáp án

Nếu cần xóa phần tử theo index hoặc xóa một slice của list mà không lấy giá trị trả về, tài liệu hướng dẫn dùng câu lệnh nào? Nó khác pop() ở điểm gì?

**Đáp án mong đợi:** Dùng del; có thể xóa phần tử theo index hoặc slice, còn pop() xóa và trả về một giá trị.

**Nguồn:** [python-3.14-ch05](https://docs.python.org/3.14/tutorial/datastructures.html); đơn vị `python-3.14-ch05-u004`; chunk `e12d5e0b102af3fb583cc06e854db00b`.

**Bằng chứng:**

```text
5.2. The del statement

There is a way to remove an item from a list given its index instead of its value: the del statement. This differs from the pop() method which returns a value. The del statement can also be used to remove slices from a list or clear the entire list (which we did earlier by assignment of an empty list to the slice). For example:
```

### T04 — Có đáp án

Vì sao nên mở file bằng with? Nếu trong khối with phát sinh exception thì file có được đóng không?

**Đáp án mong đợi:** with bảo đảm file được đóng đúng khi khối kết thúc, kể cả khi có ngoại lệ.

**Nguồn:** [python-3.14-ch07](https://docs.python.org/3.14/tutorial/inputoutput.html); đơn vị `python-3.14-ch07-u005`; chunk `d85bd86a93a6322c8c4ebab07194dbdb`.

**Bằng chứng:**

```text
It is good practice to use the with keyword when dealing with file objects. The advantage is that the file is properly closed after its suite finishes, even if an exception is raised at some point.
```

### T05 — Có đáp án

Khi raise một ngoại lệ mới trong except, cú pháp nào được tài liệu dùng để tắt automatic exception chaining?

**Đáp án mong đợi:** Dùng raise ... from None, ví dụ raise RuntimeError from None.

**Nguồn:** [python-3.14-ch08](https://docs.python.org/3.14/tutorial/errors.html); đơn vị `python-3.14-ch08-u005`; chunk `ff3919a7aecf66d4113ecfab1a1fe6b0`.

**Bằng chứng:**

```text
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

### T06 — Thiếu bằng chứng

Theo corpus này, cấu hình sqlite3 PRAGMA busy_timeout bằng câu lệnh nào và thời gian chờ có đơn vị gì?

**Hành vi mong đợi:** Tìm tài liệu rồi nói rõ không đủ bằng chứng trong corpus; không điền đáp án từ kiến thức bên ngoài.

**Lý do:** database.sqlite chỉ là tên file trong ví dụ open() và exception chaining. Không có API sqlite3, PRAGMA hay thiết lập busy_timeout.

### T07 — Thiếu bằng chứng

Chỉ dựa trên các tài liệu này, covariant=True và contravariant=True của typing.TypeVar khác nhau thế nào khi khai báo kiểu generic?

**Hành vi mong đợi:** Tìm tài liệu rồi nói rõ không đủ bằng chứng trong corpus; không điền đáp án từ kiến thức bên ngoài.

**Lý do:** Mục function annotations chỉ giới thiệu metadata, __annotations__ và cú pháp :/->. Không giải thích TypeVar, generic variance hoặc hai cờ được hỏi.

