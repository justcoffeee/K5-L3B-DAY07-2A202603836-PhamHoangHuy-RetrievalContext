# Kiểm tra 14 nhãn test AI-assisted

Học viên đã xác nhận nhãn AI-assisted; xem configs/test_review_approval.json ở root. Các bản JSON nguyên gốc giữ hash/trạng thái lúc soạn. Grounded answer/context: 0 không đạt, 1 thiếu điều kiện/quan hệ bằng chứng, 2 đủ. Lời từ chối vẫn phải tránh khẳng định vô căn cứ. Không sửa gold hoặc pipeline sau test.

## baseline

### T01 — answered

Chuỗi literal dùng ba dấu nháy có giữ ký tự xuống dòng không? Theo ví dụ trong tài liệu, làm sao tránh đưa newline đầu tiên vào chuỗi?

**Đáp án/giới hạn chuẩn:** Các ký tự kết thúc dòng được đưa vào chuỗi; đặt dấu backslash ngay trước newline đầu tiên để bỏ newline đó.

**Đầu ra model:**
Có. Theo tài liệu, string literal có thể trải trên nhiều dòng bằng cách dùng ba dấu nháy ("""...""" hoặc '''...'''), và các ký tự cuối dòng (end-of-line) được tự động đưa vào chuỗi. Tuy nhiên có thể ngăn điều này bằng cách thêm dấu \ ở cuối dòng; trong ví dụ của tài liệu, newline đầu tiên không được đưa vào chuỗi [994429862692bd5708095b1fa49fd3f0].

**Nhãn đề xuất:** answer=2; context=2; abstention_correct=None

**Lý do:** Đủ giữ newline trong triple-quoted string và thêm backslash ở cuối dòng để bỏ newline đầu.

**Citation:**
- `994429862692bd5708095b1fa49fd3f0`: supports=True — Đoạn triple-quotes nêu giữ end-of-line và dùng backslash cuối dòng để ngăn newline.

**Context thực tế gửi model:**
```text
[994429862692bd5708095b1fa49fd3f0 | https://docs.python.org/3.14/tutorial/introduction.html | page python-3.14-ch03-u003]
String literals can span multiple lines. One way is using triple-quotes: """...""" or '''...'''. End-of-line characters are automatically included in the string, but it’s possible to prevent this by adding a \ at the end of the line. In the following example, the initial newline is not included:
```

### T02 — answered

Để buộc tham số của hàm chỉ được truyền bằng tên, cần đặt ký hiệu nào và ở vị trí nào trong danh sách tham số?

**Đáp án/giới hạn chuẩn:** Đặt dấu * ngay trước tham số keyword-only đầu tiên.

**Đầu ra model:**
Để buộc các tham số chỉ được truyền bằng tên (keyword-only), đặt dấu * trong danh sách tham số, ngay trước tham số keyword-only đầu tiên [e5a6879e3f04a49ee60f47f27e202599]. Ngoài ra, mọi tham số hình thức nằm sau tham số *args cũng là tham số 'keyword-only', tức chỉ có thể dùng như keyword chứ không thể truyền theo vị trí [e0314b602ac6d5516855f20afe6c1d66].

**Nhãn đề xuất:** answer=2; context=2; abstention_correct=None

**Lý do:** Đúng dấu * ngay trước tham số keyword-only đầu tiên; phần bổ sung sau *args có evidence.

**Citation:**
- `e5a6879e3f04a49ee60f47f27e202599`: supports=True — Nêu dấu * phải đứng ngay trước keyword-only parameter đầu tiên.
- `e0314b602ac6d5516855f20afe6c1d66`: supports=True — Hỗ trợ riêng phần mọi tham số sau *args là keyword-only.

**Context thực tế gửi model:**
```text
[e5a6879e3f04a49ee60f47f27e202599 | https://docs.python.org/3.14/tutorial/controlflow.html | page python-3.14-ch04-u010]
4.9.3.3. Keyword-Only Arguments

To mark parameters as keyword-only, indicating the parameters must be passed by keyword argument, place an * in the arguments list just before the first keyword-only parameter.

[e0314b602ac6d5516855f20afe6c1d66 | https://docs.python.org/3.14/tutorial/controlflow.html | page python-3.14-ch04-u012]
Normally, these variadic arguments will be last in the list of formal parameters, because they scoop up all remaining input arguments that are passed to the function. Any formal parameters which occur after the *args parameter are ‘keyword-only’ arguments, meaning that they can only be used as keywords rather than positional arguments.
```

### T03 — answered

Nếu cần xóa phần tử theo index hoặc xóa một slice của list mà không lấy giá trị trả về, tài liệu hướng dẫn dùng câu lệnh nào? Nó khác pop() ở điểm gì?

**Đáp án/giới hạn chuẩn:** Dùng del; có thể xóa phần tử theo index hoặc slice, còn pop() xóa và trả về một giá trị.

**Đầu ra model:**
Tài liệu hướng dẫn dùng câu lệnh del: có một cách để xóa một phần tử khỏi list dựa theo index thay vì theo giá trị, đó là câu lệnh del. Điểm khác với pop() là del không trả về giá trị ("This differs from the pop() method which returns a value"). Ngoài ra, del còn có thể dùng để xóa các slice khỏi list hoặc xóa toàn bộ list [e12d5e0b102af3fb583cc06e854db00b].

**Nhãn đề xuất:** answer=2; context=2; abstention_correct=None

**Lý do:** Đủ del xóa theo index/slice không trả giá trị, khác pop trả phần tử bị xóa.

**Citation:**
- `e12d5e0b102af3fb583cc06e854db00b`: supports=True — Đủ del theo index, xóa slice/clear list và sự khác biệt với pop trả giá trị.

**Context thực tế gửi model:**
```text
[e12d5e0b102af3fb583cc06e854db00b | https://docs.python.org/3.14/tutorial/datastructures.html | page python-3.14-ch05-u004]
5.2. The del statement

There is a way to remove an item from a list given its index instead of its value: the del statement. This differs from the pop() method which returns a value. The del statement can also be used to remove slices from a list or clear the entire list (which we did earlier by assignment of an empty list to the slice). For example:
```

### T04 — answered

Vì sao nên mở file bằng with? Nếu trong khối with phát sinh exception thì file có được đóng không?

**Đáp án/giới hạn chuẩn:** with bảo đảm file được đóng đúng khi khối kết thúc, kể cả khi có ngoại lệ.

**Đầu ra model:**
Nên mở file bằng with vì sau khi khối lệnh được thực thi, file f luôn được đóng, kể cả khi gặp sự cố trong quá trình xử lý các dòng — tức là nếu trong khối with phát sinh exception thì file vẫn được đóng [af4e9b992542a8f255a34c2e182dc1f8]. Các đối tượng, giống như file, cung cấp các hành động dọn dẹp (clean-up) được định trước sẽ ghi rõ điều này trong tài liệu của chúng [af4e9b992542a8f255a34c2e182dc1f8].

**Nhãn đề xuất:** answer=1; context=1; abstention_correct=None

**Lý do:** Đáp án đúng theo nguồn đầy đủ nhưng context gửi model thiếu antecedent cho the statement trong af4. Chunk còn lại chỉ có open() thông thường, không gắn hành vi đóng file khi exception với with. Chấm bảo thủ answer=1/context=1; citation chưa hỗ trợ đủ mệnh đề with/exception. Không bổ sung antecedent hoặc thay gold sau khi xem test.

**Citation:**
- `af4e9b992542a8f255a34c2e182dc1f8`: supports=False — Nêu đóng file ngay cả khi có vấn đề và predefined cleanup. Trong I1, f75 thiết lập quan hệ với with; baseline thiếu antecedent nên nguồn này chưa đủ cho khẳng định with/exception hoàn chỉnh.

**Context thực tế gửi model:**
```text
[af4e9b992542a8f255a34c2e182dc1f8 | https://docs.python.org/3.14/tutorial/errors.html | page python-3.14-ch08-u007]
After the statement is executed, the file f is always closed, even if a problem was encountered while processing the lines. Objects which, like files, provide predefined clean-up actions will indicate this in their documentation.

[165ec1af75ea093488f0707786df1509 | https://docs.python.org/3.14/tutorial/inputoutput.html | page python-3.14-ch07-u004]
7.2. Reading and Writing Files

open() returns a file object, and is most commonly used with two positional arguments and one keyword argument: open(filename, mode, encoding=None)

>>> f = open('workfile', 'w', encoding="utf-8")
```

### T05 — answered

Khi raise một ngoại lệ mới trong except, cú pháp nào được tài liệu dùng để tắt automatic exception chaining?

**Đáp án/giới hạn chuẩn:** Dùng raise ... from None, ví dụ raise RuntimeError from None.

**Đầu ra model:**
Tài liệu dùng idiom `from None` để tắt automatic exception chaining khi raise ngoại lệ mới trong `except`, ví dụ: `raise RuntimeError from None` [ff3919a7aecf66d4113ecfab1a1fe6b0].

**Nhãn đề xuất:** answer=2; context=2; abstention_correct=None

**Lý do:** Đúng cú pháp raise ... from None để tắt automatic exception chaining.

**Citation:**
- `ff3919a7aecf66d4113ecfab1a1fe6b0`: supports=True — Nêu from None tắt automatic exception chaining và ví dụ raise RuntimeError from None.

**Context thực tế gửi model:**
```text
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

### T06 — abstain

Theo corpus này, cấu hình sqlite3 PRAGMA busy_timeout bằng câu lệnh nào và thời gian chờ có đơn vị gì?

**Đáp án/giới hạn chuẩn:** database.sqlite chỉ là tên file trong ví dụ open() và exception chaining. Không có API sqlite3, PRAGMA hay thiết lập busy_timeout.

**Đầu ra model:**
Không đủ bằng chứng trong tài liệu để trả lời: corpus được cung cấp chỉ chứa nội dung tutorial về lỗi/exception của Python, không có thông tin về sqlite3 PRAGMA busy_timeout hay đơn vị thời gian chờ.

**Nhãn đề xuất:** answer=None; context=None; abstention_correct=False

**Lý do:** Có từ chối và không đoán SQLite, nhưng nói sai rằng toàn corpus chỉ chứa tutorial lỗi/exception; corpus thực tế gồm chương 3–8. Theo rubric không thêm khẳng định vô căn cứ, refusal observed=true nhưng abstention_correct=false.

**Citation:**

**Context thực tế gửi model:**
```text
[a8b6469463b12ad87ff7d90ca0a42005 | https://docs.python.org/3.14/tutorial/errors.html | page python-3.14-ch08-u004]
>>> try:
...     open("database.sqlite")
... except OSError:
...     raise RuntimeError("unable to handle error")
...
Traceback (most recent call last):
  File "<stdin>", line 2, in <module>
    open("database.sqlite")
    ~~~~^^^^^^^^^^^^^^^^^^^
FileNotFoundError: [Errno 2] No such file or directory: 'database.sqlite'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "<stdin>", line 4, in <module>


[9126cd3fef32cc3e468d8edc25111ce4 | https://docs.python.org/3.14/tutorial/errors.html | page python-3.14-ch08-u008]
      | RecursionError: 4
      +------------------------------------
>>>
```

### T07 — abstain

Chỉ dựa trên các tài liệu này, covariant=True và contravariant=True của typing.TypeVar khác nhau thế nào khi khai báo kiểu generic?

**Đáp án/giới hạn chuẩn:** Mục function annotations chỉ giới thiệu metadata, __annotations__ và cú pháp :/->. Không giải thích TypeVar, generic variance hoặc hai cờ được hỏi.

**Đầu ra model:**
Không đủ bằng chứng trong tài liệu để trả lời: các đoạn tài liệu hiện có chỉ liệt kê tên nội trú và ví dụ lỗi đệ quy, không đề cập typing.TypeVar hay covariant/contravariant.

**Nhãn đề xuất:** answer=None; context=None; abstention_correct=True

**Lý do:** Từ chối rõ do thiếu nội dung TypeVar/variance, không tự giải thích bằng kiến thức ngoài nguồn.

**Citation:**

**Context thực tế gửi model:**
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
```

## I1

### T01 — answered

Chuỗi literal dùng ba dấu nháy có giữ ký tự xuống dòng không? Theo ví dụ trong tài liệu, làm sao tránh đưa newline đầu tiên vào chuỗi?

**Đáp án/giới hạn chuẩn:** Các ký tự kết thúc dòng được đưa vào chuỗi; đặt dấu backslash ngay trước newline đầu tiên để bỏ newline đó.

**Đầu ra model:**
Có. Theo tài liệu, string literal có thể trải trên nhiều dòng bằng cách dùng ba dấu nháy ("""...""" hoặc '''...'''), và các ký tự cuối dòng (end-of-line characters) được tự động đưa vào chuỗi [994429862692bd5708095b1fa49fd3f0]. Tuy nhiên có thể ngăn điều này bằng cách thêm dấu \ ở cuối dòng; trong ví dụ của tài liệu, newline đầu tiên không được đưa vào chuỗi [994429862692bd5708095b1fa49fd3f0].

**Nhãn đề xuất:** answer=2; context=2; abstention_correct=None

**Lý do:** Đủ giữ newline trong triple-quoted string và thêm backslash ở cuối dòng để bỏ newline đầu.

**Citation:**
- `994429862692bd5708095b1fa49fd3f0`: supports=True — Đoạn triple-quotes nêu giữ end-of-line và dùng backslash cuối dòng để ngăn newline.

**Context thực tế gửi model:**
```text
[994429862692bd5708095b1fa49fd3f0 | https://docs.python.org/3.14/tutorial/introduction.html | page python-3.14-ch03-u003]
String literals can span multiple lines. One way is using triple-quotes: """...""" or '''...'''. End-of-line characters are automatically included in the string, but it’s possible to prevent this by adding a \ at the end of the line. In the following example, the initial newline is not included:

[5046e99636180b57c2960fedf1d3566c | https://docs.python.org/3.14/tutorial/introduction.html | page python-3.14-ch03-u003]
If you don’t want characters prefaced by \ to be interpreted as special characters, you can use raw strings by adding an r before the first quote:

>>> print('C:\this\name')  # here \t means tab, \n means newline
C:      his
ame
>>> print(r'C:\this\name')  # note the r before the quote
C:\this\name

There is one subtle aspect to raw strings: a raw string may not end in an odd number of \ characters; see the FAQ entry for more information and workarounds.

[11cbaee3d3390fb59f4fe75b4399aa91 | https://docs.python.org/3.14/tutorial/inputoutput.html | page python-3.14-ch07-u001]
To use formatted string literals, begin a string with f or F before the opening quotation mark or triple quotation mark. Inside this string, you can write a Python expression between { and } characters that can refer to variables or literal values.

>>> year = 2016
>>> event = 'Referendum'
>>> f'Results of the {year} {event}'
'Results of the 2016 Referendum'

[7d78f0ecaf7d086c0d4652a711f4157b | https://docs.python.org/3.14/tutorial/introduction.html | page python-3.14-ch03-u002]
>>> 'spam eggs'  # single quotes
'spam eggs'
>>> "Paris rabbit got your back :)! Yay!"  # double quotes
'Paris rabbit got your back :)! Yay!'
>>> '1975'  # digits and numerals enclosed in quotes are also strings
'1975'

To quote a quote, we need to “escape” it, by preceding it with \. Alternatively, we can use the other type of quotation marks:
```

### T02 — answered

Để buộc tham số của hàm chỉ được truyền bằng tên, cần đặt ký hiệu nào và ở vị trí nào trong danh sách tham số?

**Đáp án/giới hạn chuẩn:** Đặt dấu * ngay trước tham số keyword-only đầu tiên.

**Đầu ra model:**
Đặt dấu * (dấu hoa thị) trong danh sách tham số, ngay trước tham số chỉ-truyền-bằng-tên (keyword-only) đầu tiên — điều này cho biết các tham số đó phải được truyền bằng keyword argument [e5a6879e3f04a49ee60f47f27e202599]. Tương tự, mọi tham số hình thức nằm sau tham số *args cũng là 'keyword-only', tức chỉ dùng được như keyword chứ không phải positional argument [e0314b602ac6d5516855f20afe6c1d66]. Ví dụ, hàm kwd_only_arg chỉ cho phép keyword arguments như được chỉ ra bởi dấu * trong định nghĩa hàm [152e1f92cf8f8f2c493ff147cb500c70].

**Nhãn đề xuất:** answer=2; context=2; abstention_correct=None

**Lý do:** Đúng dấu * ngay trước tham số keyword-only đầu tiên; phần bổ sung sau *args có evidence.

**Citation:**
- `e5a6879e3f04a49ee60f47f27e202599`: supports=True — Nêu dấu * phải đứng ngay trước keyword-only parameter đầu tiên.
- `e0314b602ac6d5516855f20afe6c1d66`: supports=True — Hỗ trợ riêng phần mọi tham số sau *args là keyword-only.
- `152e1f92cf8f8f2c493ff147cb500c70`: supports=True — Đoạn nêu kwd_only_arg chỉ nhận keyword arguments như chỉ ra bởi * trong định nghĩa.

**Context thực tế gửi model:**
```text
[e5a6879e3f04a49ee60f47f27e202599 | https://docs.python.org/3.14/tutorial/controlflow.html | page python-3.14-ch04-u010]
4.9.3.3. Keyword-Only Arguments

To mark parameters as keyword-only, indicating the parameters must be passed by keyword argument, place an * in the arguments list just before the first keyword-only parameter.

[e0314b602ac6d5516855f20afe6c1d66 | https://docs.python.org/3.14/tutorial/controlflow.html | page python-3.14-ch04-u012]
Normally, these variadic arguments will be last in the list of formal parameters, because they scoop up all remaining input arguments that are passed to the function. Any formal parameters which occur after the *args parameter are ‘keyword-only’ arguments, meaning that they can only be used as keywords rather than positional arguments.

[152e1f92cf8f8f2c493ff147cb500c70 | https://docs.python.org/3.14/tutorial/controlflow.html | page python-3.14-ch04-u011]
>>> pos_only_arg(1)
1

>>> pos_only_arg(arg=1)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: pos_only_arg() got some positional-only arguments passed as keyword arguments: 'arg'

The third function kwd_only_arg only allows keyword arguments as indicated by a * in the function definition:

[9c89ce2d2796738d7eb4e68b96abbe5e | https://docs.python.org/3.14/tutorial/controlflow.html | page python-3.14-ch04-u010]
4.9.3.2. Positional-Only Parameters

Looking at this in a bit more detail, it is possible to mark certain parameters as positional-only. If positional-only, the parameters’ order matters, and the parameters cannot be passed by keyword. Positional-only parameters are placed before a / (forward-slash). The / is used to logically separate the positional-only parameters from the rest of the parameters. If there is no / in the function definition, there are no positional-only parameters.
```

### T03 — answered

Nếu cần xóa phần tử theo index hoặc xóa một slice của list mà không lấy giá trị trả về, tài liệu hướng dẫn dùng câu lệnh nào? Nó khác pop() ở điểm gì?

**Đáp án/giới hạn chuẩn:** Dùng del; có thể xóa phần tử theo index hoặc slice, còn pop() xóa và trả về một giá trị.

**Đầu ra model:**
Tài liệu hướng dẫn dùng câu lệnh del: có một cách để xóa một phần tử khỏi list dựa theo index thay vì theo giá trị, đó là câu lệnh del. Điểm khác với pop() là del không trả về giá trị, trong khi pop() trả về giá trị (phần tử bị xóa). Ngoài ra del còn có thể dùng để xóa một slice của list hoặc xóa toàn bộ list (tương tự việc gán một list rỗng cho slice) [e12d5e0b102af3fb583cc06e854db00b]. Cụ thể, pop() xóa phần tử ở vị trí cho trước và trả về nó; nếu không chỉ định index, a.pop() xóa và trả về phần tử cuối cùng, và nó ném IndexError nếu list rỗng hoặc index nằm ngoài phạm vi [e4976e7c8c03d1c6a37a18f46e14e9dd].

**Nhãn đề xuất:** answer=2; context=2; abstention_correct=None

**Lý do:** Đủ del xóa theo index/slice không trả giá trị, khác pop trả phần tử bị xóa.

**Citation:**
- `e12d5e0b102af3fb583cc06e854db00b`: supports=True — Đủ del theo index, xóa slice/clear list và sự khác biệt với pop trả giá trị.
- `e4976e7c8c03d1c6a37a18f46e14e9dd`: supports=True — Hỗ trợ phần pop trả phần tử, mặc định cuối list và IndexError khi rỗng/ngoài phạm vi.

**Context thực tế gửi model:**
```text
[e12d5e0b102af3fb583cc06e854db00b | https://docs.python.org/3.14/tutorial/datastructures.html | page python-3.14-ch05-u004]
5.2. The del statement

There is a way to remove an item from a list given its index instead of its value: the del statement. This differs from the pop() method which returns a value. The del statement can also be used to remove slices from a list or clear the entire list (which we did earlier by assignment of an empty list to the slice). For example:

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
```

### T04 — answered

Vì sao nên mở file bằng with? Nếu trong khối with phát sinh exception thì file có được đóng không?

**Đáp án/giới hạn chuẩn:** with bảo đảm file được đóng đúng khi khối kết thúc, kể cả khi có ngoại lệ.

**Đầu ra model:**
Nên mở file bằng with vì nếu không dùng từ khóa with thì bạn phải gọi f.close() để đóng file và giải phóng ngay các tài nguyên hệ thống mà nó dùng; ngoài ra, gọi f.write() mà không dùng with hoặc không gọi f.close() có thể khiến các đối số của f.write() không được ghi hoàn toàn xuống đĩa, kể cả khi chương trình thoát thành công [f75f860f3d3396f0a832c86aa44c9a01]. Có: nếu trong khối with phát sinh exception thì file vẫn được đóng — sau khi câu lệnh được thực thi, file f luôn được đóng, ngay cả khi gặp vấn đề trong khi xử lý các dòng [af4e9b992542a8f255a34c2e182dc1f8]. Cơ chế này dựa trên các hành động dọn dẹp (clean-up) được định nghĩa trước, tương tự như mệnh đề finally vốn hữu ích để giải phóng tài nguyên bên ngoài như file hay kết nối mạng bất kể việc sử dụng tài nguyên có thành công hay không [af4e9b992542a8f255a34c2e182dc1f8][52ea2a41af6c0b37599d089c0178c2c9].

**Nhãn đề xuất:** answer=2; context=2; abstention_correct=None

**Lý do:** I1 ghép bằng chứng with/close trong f75 với đóng file ngay cả khi có vấn đề trong af4; phần finally chỉ là ví dụ tương tự có nguồn.

**Citation:**
- `f75f860f3d3396f0a832c86aa44c9a01`: supports=True — Nêu với with hoặc close thì file được đóng, khi không dùng with phải gọi close; có cảnh báo ghi dữ liệu và tài nguyên.
- `af4e9b992542a8f255a34c2e182dc1f8`: supports=True — Nêu đóng file ngay cả khi có vấn đề và predefined cleanup. Trong I1, f75 thiết lập quan hệ với with; baseline thiếu antecedent nên nguồn này chưa đủ cho khẳng định with/exception hoàn chỉnh.
- `52ea2a41af6c0b37599d089c0178c2c9`: supports=True — Hỗ trợ riêng phép so sánh với finally giải phóng tài nguyên bất kể thành công.

**Context thực tế gửi model:**
```text
[af4e9b992542a8f255a34c2e182dc1f8 | https://docs.python.org/3.14/tutorial/errors.html | page python-3.14-ch08-u007]
After the statement is executed, the file f is always closed, even if a problem was encountered while processing the lines. Objects which, like files, provide predefined clean-up actions will indicate this in their documentation.

[f75f860f3d3396f0a832c86aa44c9a01 | https://docs.python.org/3.14/tutorial/inputoutput.html | page python-3.14-ch07-u005]
If you’re not using the with keyword, then you should call f.close() to close the file and immediately free up any system resources used by it.

Warning

Calling f.write() without using the with keyword or calling f.close() might result in the arguments of f.write() not being completely written to the disk, even if the program exits successfully.

After a file object is closed, either by a with statement or by calling f.close(), attempts to use the file object will automatically fail.

[a582535c7aa804047c37f592f1b1632e | https://docs.python.org/3.14/tutorial/errors.html | page python-3.14-ch08-u006]
If the finally clause executes a break, continue or return statement, exceptions are not re-raised. This can be confusing and is therefore discouraged. From version 3.14 the compiler emits a SyntaxWarning for it (see PEP 765).

If the try statement reaches a break, continue or return statement, the finally clause will execute just prior to the break, continue or return statement’s execution.

[52ea2a41af6c0b37599d089c0178c2c9 | https://docs.python.org/3.14/tutorial/errors.html | page python-3.14-ch08-u006]
As you can see, the finally clause is executed in any event. The TypeError raised by dividing two strings is not handled by the except clause and therefore re-raised after the finally clause has been executed.

In real world applications, the finally clause is useful for releasing external resources (such as files or network connections), regardless of whether the use of the resource was successful.
```

### T05 — answered

Khi raise một ngoại lệ mới trong except, cú pháp nào được tài liệu dùng để tắt automatic exception chaining?

**Đáp án/giới hạn chuẩn:** Dùng raise ... from None, ví dụ raise RuntimeError from None.

**Đầu ra model:**
Tài liệu dùng idiom `from None` để tắt automatic exception chaining, ví dụ: `raise RuntimeError from None` trong khối `except OSError` [ff3919a7aecf66d4113ecfab1a1fe6b0].

**Nhãn đề xuất:** answer=2; context=2; abstention_correct=None

**Lý do:** Đúng cú pháp raise ... from None để tắt automatic exception chaining.

**Citation:**
- `ff3919a7aecf66d4113ecfab1a1fe6b0`: supports=True — Nêu from None tắt automatic exception chaining và ví dụ raise RuntimeError from None.

**Context thực tế gửi model:**
```text
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

[7e516c73a05353d6c6d2c6de2cd846fa | https://docs.python.org/3.14/tutorial/errors.html | page python-3.14-ch08-u005]
To indicate that an exception is a direct consequence of another, the raise statement allows an optional from clause:

# exc must be exception instance or None.
raise RuntimeError from exc

This can be useful when you are transforming exceptions. For example:

[7c980d656554f4c3748d8697d717ded3 | https://docs.python.org/3.14/tutorial/errors.html | page python-3.14-ch08-u004]
If you need to determine whether an exception was raised but don’t intend to handle it, a simpler form of the raise statement allows you to re-raise the exception:

>>> try:
...     raise NameError('HiThere')
... except NameError:
...     print('An exception flew by!')
...     raise
...
An exception flew by!
Traceback (most recent call last):
  File "<stdin>", line 2, in <module>
    raise NameError('HiThere')
NameError: HiThere

[eb1202071982afa8de740c2fa8c71a8f | https://docs.python.org/3.14/tutorial/errors.html | page python-3.14-ch08-u004]
The sole argument to raise indicates the exception to be raised. This must be either an exception instance or an exception class (a class that derives from BaseException, such as Exception or one of its subclasses). If an exception class is passed, it will be implicitly instantiated by calling its constructor with no arguments:

raise ValueError  # shorthand for 'raise ValueError()'
```

### T06 — abstain

Theo corpus này, cấu hình sqlite3 PRAGMA busy_timeout bằng câu lệnh nào và thời gian chờ có đơn vị gì?

**Đáp án/giới hạn chuẩn:** database.sqlite chỉ là tên file trong ví dụ open() và exception chaining. Không có API sqlite3, PRAGMA hay thiết lập busy_timeout.

**Đầu ra model:**
Không đủ bằng chứng trong tài liệu để trả lời: corpus được cung cấp chỉ chứa nội dung Python Tutorial (ví dụ về xử lý ngoại lệ và danh sách tên built-in), không có tài liệu nào về module sqlite3 hay PRAGMA busy_timeout, nên không thể xác định câu lệnh cấu hình cũng như đơn vị thời gian chờ.

**Nhãn đề xuất:** answer=None; context=None; abstention_correct=True

**Lý do:** Từ chối rõ, mô tả đúng corpus là Python Tutorial, không đoán câu lệnh PRAGMA hoặc đơn vị thời gian; phù hợp absence audit.

**Citation:**

**Context thực tế gửi model:**
```text
[a8b6469463b12ad87ff7d90ca0a42005 | https://docs.python.org/3.14/tutorial/errors.html | page python-3.14-ch08-u004]
>>> try:
...     open("database.sqlite")
... except OSError:
...     raise RuntimeError("unable to handle error")
...
Traceback (most recent call last):
  File "<stdin>", line 2, in <module>
    open("database.sqlite")
    ~~~~^^^^^^^^^^^^^^^^^^^
FileNotFoundError: [Errno 2] No such file or directory: 'database.sqlite'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "<stdin>", line 4, in <module>


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

### T07 — abstain

Chỉ dựa trên các tài liệu này, covariant=True và contravariant=True của typing.TypeVar khác nhau thế nào khi khai báo kiểu generic?

**Đáp án/giới hạn chuẩn:** Mục function annotations chỉ giới thiệu metadata, __annotations__ và cú pháp :/->. Không giải thích TypeVar, generic variance hoặc hai cờ được hỏi.

**Đầu ra model:**
Không đủ bằng chứng trong tài liệu để trả lời: các đoạn tài liệu hiện có chỉ nói về module, lỗi, cấu trúc dữ liệu và so sánh chuỗi, không đề cập typing.TypeVar hay covariant/contravariant.

**Nhãn đề xuất:** answer=None; context=None; abstention_correct=True

**Lý do:** Từ chối rõ do thiếu nội dung TypeVar/variance, không tự giải thích bằng kiến thức ngoài nguồn.

**Citation:**

**Context thực tế gửi model:**
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

[8adf77137591f205b5e6bed818ad91b2 | https://docs.python.org/3.14/tutorial/datastructures.html | page python-3.14-ch05-u009]
5.8. Comparing Sequences and Other Types

[bb8916665faf9d25918b5b2b7254b4e8 | https://docs.python.org/3.14/tutorial/datastructures.html | page python-3.14-ch05-u009]
It is possible to assign the result of a comparison or other Boolean expression to a variable. For example,

>>> string1, string2, string3 = '', 'Trondheim', 'Hammer Dance'
>>> non_null = string1 or string2 or string3
>>> non_null
'Trondheim'

Note that in Python, unlike C, assignment inside expressions must be done explicitly with the walrus operator :=. This avoids a common class of problems encountered in C programs: typing = in an expression when == was intended.
```

