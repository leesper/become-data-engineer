# 优达学城Git提交消息样式指南

## 消息结构

提交消息由3个部分组成，每个部分由一个空白行隔开：标题，可选的消息体和可选的脚注。例如：

```
type: subject

body

footer
```

标题由消息类型和主题组成。

## 类型

标题中的“类型”可以有以下几种：

* feat：新特性
* fix：bug修复
* docs：文档修改
* style：格式化，添加缺失的分号等等，代码不变
* refactor：重构产品代码
* test：添加测试，重构测试，产品代码不变
* chore：例行事务，例如更新构建任务，包管理器配置等等，产品代码不变

## 主题

主题不多于50个字符，以大写开头，没有句号。使用命令式的语气来描述一个提交做了什么，比如使用`change`而不是`changed`或者`changes`。

## 消息体

不是所有的提交都复杂到需要详述，所以消息体不是必选项。只有当提交需要一点解释或者上下文时才提供消息体。使用消息体来解释提交**做了什么**和**为什么这么做**，不解释如何做。编写消息体时标题和消息体之间的空白行是必须的，消息体的每行不要超过72个字符。

## 脚注

脚注也是可选的，用来引用问题追踪记录ID号。

## 例子

```
feat: Summarize changes in around 50 characters or less

More detailed explanatory text, if necessary. Wrap it to about 72
characters or so. In some contexts, the first line is treated as the
subject of the commit and the rest of the text as the body. The
blank line separating the summary from the body is critical (unless
you omit the body entirely); various tools like `log`, `shortlog`
and `rebase` can get confused if you run the two together.

Explain the problem that this commit is solving. Focus on why you
are making this change as opposed to how (the code explains that).
Are there side effects or other unintuitive consequenses of this
change? Here's the place to explain them.

Further paragraphs come after blank lines.

 - Bullet points are okay, too

 - Typically a hyphen or asterisk is used for the bullet, preceded
   by a single space, with blank lines in between, but conventions
   vary here

If you use an issue tracker, put references to them at the bottom,
like this:

Resolves: #123
See also: #456, #789
```

