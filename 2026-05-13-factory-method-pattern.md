# 2026-05-13 工厂方法模式学习笔记

## 今日主题

工厂方法模式

## 今日目标

- 理解工厂方法模式解决的问题。
- 知道对象创建逻辑为什么不应该到处散落。
- 能用 TypeScript 实现工厂方法模式。
- 能用 Python 实现工厂方法模式。
- 能区分工厂方法模式和策略模式。
- 知道什么时候不应该为了“消灭 if-else”而强行上模式。

## 1. 工厂方法模式解决什么问题

工厂方法模式主要解决这种问题：

```text
创建对象的逻辑比较复杂，或者经常变化，不适合散落在业务代码里。
```

例如：

- 根据通知类型创建短信、邮件、站内信通知器。
- 根据文件类型创建 PDF、Excel、CSV 导出器。
- 根据支付渠道创建微信、支付宝、银行卡支付对象。
- 根据不同环境创建本地缓存、Redis 缓存、内存缓存。

如果业务代码里到处直接 `new` 具体类，后续新增类型时就容易到处改。

## 2. 坏代码示例

假设系统需要根据通知类型发送消息。

```ts
class EmailNotifier {
  send(message: string): void {
    console.log(`发送邮件: ${message}`);
  }
}

class SmsNotifier {
  send(message: string): void {
    console.log(`发送短信: ${message}`);
  }
}

function notify(type: string, message: string): void {
  if (type === "email") {
    const notifier = new EmailNotifier();
    notifier.send(message);
  }

  if (type === "sms") {
    const notifier = new SmsNotifier();
    notifier.send(message);
  }
}
```

这段代码的问题是：

- `notify` 同时负责业务流程和对象创建。
- 新增通知渠道时，必须修改 `notify`。
- 创建逻辑一旦变复杂，会污染主流程。
- 如果多个地方都要创建通知器，判断逻辑会重复。

这里的问题不只是有 `if-else`，而是创建具体对象的职责放错了地方。

## 3. 工厂方法模式的核心思想

工厂方法模式的核心是：

```text
把对象创建这件事交给工厂，让业务代码依赖抽象，而不是直接依赖具体类。
```

在通知场景里：

- `Notifier` 是产品接口。
- `EmailNotifier` 和 `SmsNotifier` 是具体产品。
- `NotifierFactory` 是工厂接口。
- `EmailNotifierFactory` 和 `SmsNotifierFactory` 是具体工厂。

业务代码只使用工厂创建出来的 `Notifier`，不直接关心具体创建细节。

## 4. 生活类比

你去咖啡店点咖啡。

你不会自己去磨豆、控制水温、打奶泡。你只需要说：

```text
我要一杯拿铁。
```

咖啡店负责创建咖啡。你负责喝咖啡。

在这个类比里：

- 咖啡是产品。
- 拿铁、美式、摩卡是具体产品。
- 咖啡店是工厂。
- 你不关心咖啡怎么被创建，只关心拿到能喝的咖啡。

## 5. TypeScript 示例

```ts
interface Notifier {
  send(message: string): void;
}

class EmailNotifier implements Notifier {
  send(message: string): void {
    console.log(`发送邮件: ${message}`);
  }
}

class SmsNotifier implements Notifier {
  send(message: string): void {
    console.log(`发送短信: ${message}`);
  }
}

interface NotifierFactory {
  createNotifier(): Notifier;
}

class EmailNotifierFactory implements NotifierFactory {
  createNotifier(): Notifier {
    return new EmailNotifier();
  }
}

class SmsNotifierFactory implements NotifierFactory {
  createNotifier(): Notifier {
    return new SmsNotifier();
  }
}

function notifyUser(factory: NotifierFactory, message: string): void {
  const notifier = factory.createNotifier();
  notifier.send(message);
}

notifyUser(new EmailNotifierFactory(), "订单已支付");
notifyUser(new SmsNotifierFactory(), "验证码是 123456");
```

### TypeScript 代码说明

- `Notifier`：定义通知器必须具备 `send` 方法。
- `EmailNotifier`：邮件通知器。
- `SmsNotifier`：短信通知器。
- `NotifierFactory`：定义创建通知器的方法。
- `EmailNotifierFactory`：负责创建邮件通知器。
- `SmsNotifierFactory`：负责创建短信通知器。
- `notifyUser`：只负责使用通知器，不负责判断具体创建哪一种通知器。

新增站内信通知时，可以新增一个具体产品和一个具体工厂：

```ts
class SiteMessageNotifier implements Notifier {
  send(message: string): void {
    console.log(`发送站内信: ${message}`);
  }
}

class SiteMessageNotifierFactory implements NotifierFactory {
  createNotifier(): Notifier {
    return new SiteMessageNotifier();
  }
}
```

## 6. Python 示例

```python
from abc import ABC, abstractmethod


class Notifier(ABC):
    @abstractmethod
    def send(self, message: str) -> None:
        pass


class EmailNotifier(Notifier):
    def send(self, message: str) -> None:
        print(f"发送邮件: {message}")


class SmsNotifier(Notifier):
    def send(self, message: str) -> None:
        print(f"发送短信: {message}")


class NotifierFactory(ABC):
    @abstractmethod
    def create_notifier(self) -> Notifier:
        pass


class EmailNotifierFactory(NotifierFactory):
    def create_notifier(self) -> Notifier:
        return EmailNotifier()


class SmsNotifierFactory(NotifierFactory):
    def create_notifier(self) -> Notifier:
        return SmsNotifier()


def notify_user(factory: NotifierFactory, message: str) -> None:
    notifier = factory.create_notifier()
    notifier.send(message)


notify_user(EmailNotifierFactory(), "订单已支付")
notify_user(SmsNotifierFactory(), "验证码是 123456")
```

### Python 代码说明

- `Notifier`：抽象基类，要求具体通知器实现 `send`。
- `EmailNotifier`：邮件通知器。
- `SmsNotifier`：短信通知器。
- `NotifierFactory`：抽象工厂基类，定义 `create_notifier`。
- `EmailNotifierFactory`：负责创建邮件通知器。
- `SmsNotifierFactory`：负责创建短信通知器。
- `notify_user`：只依赖工厂抽象，不直接依赖具体通知器。

Python 中如果创建逻辑很简单，也可以使用更轻量的简单工厂函数：

```python
def create_notifier(kind: str) -> Notifier:
    if kind == "email":
        return EmailNotifier()

    if kind == "sms":
        return SmsNotifier()

    raise ValueError(f"未知通知类型: {kind}")
```

这个写法不是严格的工厂方法模式，但在小项目里经常更实用。

## 7. TypeScript 和 Python 的区别

- TypeScript 更适合用 `interface` 明确约束产品和工厂结构。
- Python 可以用抽象基类，也可以直接依赖鸭子类型。
- TypeScript 的类型约束更强，适合多人协作时维护扩展点。
- Python 简单场景下不一定需要工厂类，一个工厂函数就够了。
- 两种语言都不应该为了展示模式而强行增加类数量。

## 8. 适用场景

适合使用工厂方法模式的场景：

- 创建对象的过程比较复杂。
- 业务代码不应该知道具体类的创建细节。
- 不同产品有统一接口，但具体实现不同。
- 未来经常新增产品类型。
- 创建逻辑需要单独测试或复用。

常见业务例子：

- 支付渠道：微信支付、支付宝支付、银行卡支付。
- 通知渠道：短信、邮件、站内信、App 推送。
- 文件导出：PDF、Excel、CSV。
- 日志输出：控制台日志、文件日志、远程日志。
- 缓存实现：内存缓存、Redis 缓存、本地文件缓存。

## 9. 不适用场景

不适合使用工厂方法模式的场景：

- 只有一个具体类，没有变化点。
- 创建对象只是简单 `new` 一下。
- 类型很少，而且几乎不会扩展。
- 一个简单映射表或简单工厂函数已经足够清楚。
- 引入工厂后，代码文件变多，但业务收益很小。

例如：

```ts
const user = new User(name);
```

这种代码没有必要专门写一个 `UserFactory`。

设计模式不是为了隐藏 `new`，而是为了管理复杂的创建逻辑。

## 10. 和策略模式的区别

工厂方法模式和策略模式都可能减少 `if-else`，但它们解决的问题不同。

| 对比点 | 工厂方法模式 | 策略模式 |
| --- | --- | --- |
| 关注点 | 创建哪个对象 | 使用哪种行为 |
| 解决的问题 | 创建逻辑复杂或散落 | 算法、规则、行为经常变化 |
| 常见方法名 | `create`、`make`、`build` | `execute`、`calculate`、`pay`、`send` |
| 替代的判断 | 判断 `new` 哪个类 | 判断执行哪段业务逻辑 |
| 输出结果 | 返回一个对象 | 执行动作或返回计算结果 |

更直观地说：

```text
工厂方法模式关心“对象从哪里来”。
策略模式关心“拿到对象后怎么做”。
```

判断方式：

```text
如果 if-else 是为了决定 new 哪个类，优先考虑工厂方法。
如果 if-else 是为了决定执行哪种规则，优先考虑策略模式。
```

它们也经常一起使用：

```ts
const strategy = PayStrategyFactory.create("wechat");
strategy.pay(100);
```

这里：

- 工厂负责创建 `PayStrategy`。
- 策略负责执行具体支付逻辑。

### 同一个支付场景里的区别

先看一段常见坏代码：

```ts
function pay(type: string, amount: number): void {
  if (type === "wechat") {
    console.log(`微信支付 ${amount}`);
  }

  if (type === "alipay") {
    console.log(`支付宝支付 ${amount}`);
  }
}
```

这段代码里其实混了两类变化：

- 选择哪种支付对象。
- 执行哪种支付行为。

策略模式负责拆出支付行为：

```ts
interface PayStrategy {
  pay(amount: number): void;
}

class WechatPayStrategy implements PayStrategy {
  pay(amount: number): void {
    console.log(`微信支付 ${amount}`);
  }
}

class AlipayStrategy implements PayStrategy {
  pay(amount: number): void {
    console.log(`支付宝支付 ${amount}`);
  }
}
```

工厂方法负责创建具体策略：

```ts
interface PayStrategyFactory {
  create(): PayStrategy;
}

class WechatPayStrategyFactory implements PayStrategyFactory {
  create(): PayStrategy {
    return new WechatPayStrategy();
  }
}

class AlipayStrategyFactory implements PayStrategyFactory {
  create(): PayStrategy {
    return new AlipayStrategy();
  }
}
```

使用时：

```ts
function checkout(factory: PayStrategyFactory, amount: number): void {
  const strategy = factory.create();
  strategy.pay(amount);
}

checkout(new WechatPayStrategyFactory(), 100);
```

这里的职责边界是：

- `PayStrategyFactory`：负责创建哪个策略。
- `PayStrategy`：负责具体怎么支付。
- `checkout`：负责主业务流程。

如果只是支付规则不同，但对象创建很简单，可以只用策略模式，不一定需要工厂方法。

如果创建策略时还要读取配置、初始化 SDK、设置密钥、选择环境，就可以考虑再引入工厂。

## 11. 容易混淆的模式对比

工厂方法模式还容易和简单工厂、抽象工厂、建造者模式混淆。

### 和简单工厂的区别

简单工厂通常是一个函数或一个类，根据参数返回不同对象。

```ts
function createNotifier(type: string): Notifier {
  if (type === "email") {
    return new EmailNotifier();
  }

  if (type === "sms") {
    return new SmsNotifier();
  }

  throw new Error("未知通知类型");
}
```

工厂方法则是把创建动作放到不同的具体工厂里。

```ts
interface NotifierFactory {
  createNotifier(): Notifier;
}

class EmailNotifierFactory implements NotifierFactory {
  createNotifier(): Notifier {
    return new EmailNotifier();
  }
}
```

区别：

| 对比点 | 简单工厂 | 工厂方法 |
| --- | --- | --- |
| 是否是 GoF 经典设计模式 | 不是严格的 GoF 模式 | 是 |
| 创建逻辑位置 | 集中在一个函数或类里 | 分散到多个具体工厂里 |
| 新增产品 | 通常要修改工厂判断 | 新增一个具体工厂 |
| 代码复杂度 | 低 | 更高 |
| 适合场景 | 类型少，创建简单 | 类型多，创建逻辑复杂，扩展频繁 |

实用建议：

```text
能用简单工厂清楚表达，就不要急着升级成工厂方法。
```

### 和抽象工厂的区别

工厂方法通常创建一种产品。

抽象工厂通常创建一组相关产品。

例如 UI 主题系统：

```text
浅色主题工厂创建：浅色按钮、浅色输入框、浅色弹窗。
深色主题工厂创建：深色按钮、深色输入框、深色弹窗。
```

这就不是只创建一个对象，而是创建一整套相关对象。

对比：

| 对比点 | 工厂方法 | 抽象工厂 |
| --- | --- | --- |
| 创建对象数量 | 通常是一类产品 | 一组相关产品 |
| 关注点 | 某个产品如何创建 | 某个产品族如何创建 |
| 例子 | 创建一个通知器 | 创建一整套 UI 组件 |
| 复杂度 | 较低 | 更高 |

判断方式：

```text
只创建一个产品，优先考虑工厂方法。
要创建一组必须搭配使用的产品，才考虑抽象工厂。
```

### 和建造者模式的区别

工厂方法关注“创建哪一种对象”。

建造者模式关注“一个复杂对象如何一步步组装”。

例如：

```text
工厂方法：创建 PDF 导出器还是 Excel 导出器。
建造者模式：一步步构建一份复杂报表，包括标题、表格、图表、页脚。
```

对比：

| 对比点 | 工厂方法 | 建造者模式 |
| --- | --- | --- |
| 关注点 | 选择具体产品类型 | 分步骤构造复杂对象 |
| 创建过程 | 通常一步返回对象 | 通常多步骤配置和组装 |
| 适合对象 | 多种同类对象 | 一个对象结构复杂 |
| 常见方法 | `create()` | `setTitle()`、`addSection()`、`build()` |

判断方式：

```text
如果问题是“要哪个类”，更像工厂方法。
如果问题是“这个对象参数很多、组装步骤复杂”，更像建造者模式。
```

## 12. 对比小结

看到对象创建相关代码时，可以这样判断：

| 问题 | 更可能的选择 |
| --- | --- |
| 根据类型创建一个对象 | 简单工厂或工厂方法 |
| 创建逻辑简单，类型不多 | 简单工厂 |
| 创建逻辑复杂，类型扩展频繁 | 工厂方法 |
| 要创建一组配套对象 | 抽象工厂 |
| 一个对象有很多构建步骤 | 建造者模式 |
| 对象创建后，要切换不同算法或规则 | 策略模式 |

最重要的是：不要只因为看到 `if-else` 就套模式。先判断这个 `if-else` 到底是在处理创建问题，还是行为问题。

## 13. 今日练习

把下面的文件导出逻辑改造成工厂方法模式。

```ts
function exportFile(type: string, data: string): void {
  if (type === "pdf") {
    console.log(`导出 PDF: ${data}`);
  }

  if (type === "excel") {
    console.log(`导出 Excel: ${data}`);
  }

  if (type === "csv") {
    console.log(`导出 CSV: ${data}`);
  }
}
```

要求：

- 定义一个 `Exporter` 接口。
- 实现 `PdfExporter`、`ExcelExporter`、`CsvExporter`。
- 定义一个工厂接口。
- 每种导出器有自己的具体工厂。
- 用 TypeScript 写一版。
- 用 Python 写一版。

思考题：

- 如果只是这三个简单分支，用工厂方法会不会有点重？
- 什么时候用简单工厂函数反而更合适？

## 14. 参考答案

如果导出逻辑很简单，一个简单工厂函数可能更合适。

```ts
type ExportType = "pdf" | "excel" | "csv";

interface Exporter {
  export(data: string): void;
}

class PdfExporter implements Exporter {
  export(data: string): void {
    console.log(`导出 PDF: ${data}`);
  }
}

class ExcelExporter implements Exporter {
  export(data: string): void {
    console.log(`导出 Excel: ${data}`);
  }
}

class CsvExporter implements Exporter {
  export(data: string): void {
    console.log(`导出 CSV: ${data}`);
  }
}

function createExporter(type: ExportType): Exporter {
  const exporterMap: Record<ExportType, Exporter> = {
    pdf: new PdfExporter(),
    excel: new ExcelExporter(),
    csv: new CsvExporter(),
  };

  return exporterMap[type];
}

const exporter = createExporter("pdf");
exporter.export("订单数据");
```

这段代码严格来说更接近简单工厂，而不是工厂方法。

如果每种导出器的创建过程都很复杂，比如 PDF 需要模板配置，Excel 需要表头配置，CSV 需要编码配置，再升级成工厂方法会更合理。

## 15. 今日总结

工厂方法模式的重点不是“少写 `new`”，而是这句话：

```text
把复杂或易变的对象创建逻辑，从业务流程中拆出去。
```

以后看到类似代码时：

```text
if type == A 就 new A
if type == B 就 new B
if type == C 就 new C
```

可以先思考：这里是不是对象创建逻辑已经开始影响业务代码了？

如果创建逻辑简单，直接写或用简单工厂就够了。只有当创建过程真的复杂、扩展频繁时，工厂方法模式才更有价值。
