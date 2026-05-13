# 2026-05-09 观察者模式学习笔记

## 今日主题

观察者模式

## 今日目标

- 理解观察者模式解决的问题。
- 知道什么时候适合用“通知多个对象更新”的方式组织代码。
- 能用 TypeScript 实现观察者模式。
- 能用 Python 实现观察者模式。
- 知道观察者模式适合和不适合的场景。

## 1. 观察者模式解决什么问题

观察者模式主要解决这种问题：

```text
一个对象状态变化后，需要自动通知多个依赖它的对象。
```

例如：

- 公众号发新文章后，所有订阅者都收到通知。
- 订单状态变化后，库存、通知、积分等模块都要联动更新。
- UI 状态变化后，多个视图组件需要同步刷新。
- 事件系统中，一个事件触发多个监听器执行。

如果把通知逻辑直接写死在一个对象里，就会出现强耦合。

## 2. 坏代码示例

假设订单支付成功后，要分别通知库存、短信、积分模块。

```ts
class OrderService {
  paySuccess(orderId: string) {
    console.log(`订单 ${orderId} 支付成功`);
    console.log(`更新库存: ${orderId}`);
    console.log(`发送短信通知: ${orderId}`);
    console.log(`发放积分: ${orderId}`);
  }
}
```

这段代码的问题是：

- 所有通知逻辑都挤在一个方法里。
- 新增一个通知模块时，必须修改 `OrderService`。
- 某个通知模块变复杂时，会污染主流程。
- 很难单独测试每个通知逻辑。

这类代码违反了开闭原则。

## 3. 观察者模式的核心思想

观察者模式的核心是：

```text
把“被观察者”和“观察者”解耦，状态变化时由被观察者统一通知观察者。
```

在订单场景里：

- 订单服务是被观察者。
- 库存服务、短信服务、积分服务是观察者。
- 订单状态变化时，被观察者通知所有观察者。

## 4. 生活类比

你关注了一个博主：

- 博主发布视频。
- 平台自动推送给所有关注者。
- 每个关注者收到通知后，执行自己的动作。

这里：

- 博主是被观察者。
- 关注者是观察者。
- 发布视频是状态变化。
- 推送通知是自动更新。

## 5. TypeScript 示例

```ts
interface Observer {
  update(message: string): void;
}

class Subject {
  private observers: Observer[] = [];

  attach(observer: Observer): void {
    this.observers.push(observer);
  }

  detach(observer: Observer): void {
    this.observers = this.observers.filter((item) => item !== observer);
  }

  notify(message: string): void {
    for (const observer of this.observers) {
      observer.update(message);
    }
  }
}

class InventoryObserver implements Observer {
  update(message: string): void {
    console.log(`库存系统收到通知: ${message}`);
  }
}

class SmsObserver implements Observer {
  update(message: string): void {
    console.log(`短信系统收到通知: ${message}`);
  }
}

class PointsObserver implements Observer {
  update(message: string): void {
    console.log(`积分系统收到通知: ${message}`);
  }
}

const subject = new Subject();
const inventory = new InventoryObserver();
const sms = new SmsObserver();
const points = new PointsObserver();

subject.attach(inventory);
subject.attach(sms);
subject.attach(points);

subject.notify("订单 A1001 支付成功");
```

### TypeScript 代码说明

- `Observer`：定义观察者必须实现的 `update` 方法。
- `Subject`：保存观察者列表，并在状态变化时统一通知。
- `InventoryObserver`：库存模块观察者。
- `SmsObserver`：短信模块观察者。
- `PointsObserver`：积分模块观察者。

新增一个通知模块时，只需要新增一个观察者类，然后订阅到 `Subject`，不需要改主流程。

## 6. Python 示例

```python
from abc import ABC, abstractmethod


class Observer(ABC):
    @abstractmethod
    def update(self, message: str) -> None:
        pass


class Subject:
    def __init__(self):
        self._observers = []

    def attach(self, observer: Observer) -> None:
        self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

    def notify(self, message: str) -> None:
        for observer in self._observers:
            observer.update(message)


class InventoryObserver(Observer):
    def update(self, message: str) -> None:
        print(f"库存系统收到通知: {message}")


class SmsObserver(Observer):
    def update(self, message: str) -> None:
        print(f"短信系统收到通知: {message}")


class PointsObserver(Observer):
    def update(self, message: str) -> None:
        print(f"积分系统收到通知: {message}")


subject = Subject()
inventory = InventoryObserver()
sms = SmsObserver()
points = PointsObserver()

subject.attach(inventory)
subject.attach(sms)
subject.attach(points)

subject.notify("订单 A1001 支付成功")
```

### Python 代码说明

- `Observer`：抽象基类，要求所有观察者实现 `update`。
- `Subject`：管理观察者列表，并负责通知。
- `InventoryObserver`：库存通知逻辑。
- `SmsObserver`：短信通知逻辑。
- `PointsObserver`：积分通知逻辑。

Python 也可以更轻量地直接传函数，但用类更容易表达“订阅者”这种角色关系。

## 7. TypeScript 和 Python 的区别

- TypeScript 更适合用 `interface` 约束观察者结构。
- Python 可以用抽象基类，也可以直接使用可调用对象。
- TypeScript 的类型约束更强，适合大型协作项目。
- Python 的写法更灵活，小型场景可以更简洁。

## 8. 适用场景

适合使用观察者模式的场景：

- 一个对象变化后，需要通知多个对象。
- 事件驱动系统。
- 消息订阅系统。
- UI 状态联动刷新。
- 订单状态变化后触发多个后续动作。

常见业务例子：

- 订单支付成功后通知库存、短信、积分、物流。
- 文章发布后通知订阅者。
- 配置更新后通知多个缓存或页面刷新。
- 业务事件总线中的监听器处理。

## 9. 不适用场景

不适合使用观察者模式的场景：

- 只有一个下游逻辑，直接调用更简单。
- 通知关系固定且不会变化。
- 观察者太多，调试和排查问题成本很高。
- 需要严格的执行顺序，但观察者之间又没有明确编排机制。

观察者模式不是所有“通知”场景都要上，简单直接调用有时更清晰。

## 10. 和相似模式的区别

- 策略模式关注“怎么做”，观察者模式关注“谁来被通知”。
- 责任链模式关注“沿链传递，谁处理算谁的”，观察者模式关注“一次变化通知多个订阅者”。
- 发布订阅模式和观察者模式很像，但发布订阅通常多了一个中间事件中心，观察者通常更强调主题和观察者之间的关系。

## 11. 今日练习

把下面的活动发布逻辑改造成观察者模式。

```ts
class EventService {
  publish(title: string) {
    console.log(`发布活动: ${title}`);
    console.log(`通知邮件系统: ${title}`);
    console.log(`通知推送系统: ${title}`);
    console.log(`通知统计系统: ${title}`);
  }
}
```

要求：

- 用 TypeScript 写一版。
- 用 Python 写一版。
- 新增一个通知模块时，尽量不要修改发布主流程。

## 12. 今日总结

观察者模式的重点不是“通知很多对象”，而是这句话：

```text
当一个对象变化后，有多个对象需要跟着变化时，把通知逻辑从主流程里拆出去。
```

以后看到类似代码时：

```text
状态变更后，顺手调用一堆下游模块
```

可以先思考：这里是不是适合使用观察者模式？
