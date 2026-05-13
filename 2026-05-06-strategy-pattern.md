# 2026-05-06 策略模式学习笔记

## 今日主题

策略模式

## 今日目标

- 理解策略模式解决的问题。
- 知道为什么大量同类型 `if-else` 会让代码难维护。
- 能用 TypeScript 实现策略模式。
- 能用 Python 实现策略模式。
- 知道策略模式适合和不适合的场景。

## 1. 策略模式解决什么问题

策略模式主要解决这种问题：

```text
同一个业务动作，有多种不同算法或规则，而且这些规则可能经常变化。
```

例如：

- 不同会员等级有不同折扣规则。
- 不同支付方式有不同支付逻辑。
- 不同物流方式有不同运费计算规则。
- 不同登录方式有不同认证逻辑。

如果全部写在一个函数里，就很容易出现大量 `if-else` 或 `switch`。

## 2. 坏代码示例

假设我们要根据会员等级计算折扣。

```ts
function getDiscount(level: string): number {
  if (level === "normal") {
    return 1;
  }

  if (level === "vip") {
    return 0.9;
  }

  if (level === "svip") {
    return 0.8;
  }

  return 1;
}
```

这段代码的问题是：

- 每新增一种会员等级，都要修改 `getDiscount`。
- 折扣规则都挤在一个函数里，函数会越来越长。
- 修改旧函数时，可能影响已有逻辑。
- 每种折扣规则不方便单独测试。

这类代码违反了开闭原则。

开闭原则的意思是：

```text
对扩展开放，对修改关闭。
```

也就是说，新增功能时，尽量通过增加新代码完成，而不是频繁修改稳定的旧代码。

## 3. 策略模式的核心思想

策略模式的核心是：

```text
把一组可替换的算法封装起来，让它们可以互相替换。
```

在会员折扣场景里：

- 普通会员折扣是一种策略。
- VIP 会员折扣是一种策略。
- SVIP 会员折扣是一种策略。
- 新增会员等级时，只新增一个策略类或策略函数。

## 4. 生活类比

出门去公司，可以选择不同出行策略：

- 坐地铁
- 打车
- 骑车
- 步行

你的目标都是“到公司”，但具体路线和成本不同。

这里的“出行方式”就是策略。

## 5. TypeScript 示例

```ts
interface DiscountStrategy {
  calculate(): number;
}

class NormalDiscount implements DiscountStrategy {
  calculate(): number {
    return 1;
  }
}

class VipDiscount implements DiscountStrategy {
  calculate(): number {
    return 0.9;
  }
}

class SvipDiscount implements DiscountStrategy {
  calculate(): number {
    return 0.8;
  }
}

class DiscountContext {
  constructor(private strategy: DiscountStrategy) {}

  getDiscount(): number {
    return this.strategy.calculate();
  }
}

const context = new DiscountContext(new VipDiscount());
console.log(context.getDiscount());
```

### TypeScript 代码说明

- `DiscountStrategy`：定义所有折扣策略必须遵守的接口。
- `NormalDiscount`：普通会员折扣策略。
- `VipDiscount`：VIP 会员折扣策略。
- `SvipDiscount`：SVIP 会员折扣策略。
- `DiscountContext`：负责使用策略，但不关心具体是哪种策略。

新增黑金会员折扣时，只新增一个策略：

```ts
class BlackGoldDiscount implements DiscountStrategy {
  calculate(): number {
    return 0.7;
  }
}
```

## 6. Python 示例

```python
from abc import ABC, abstractmethod


class DiscountStrategy(ABC):
    @abstractmethod
    def calculate(self) -> float:
        pass


class NormalDiscount(DiscountStrategy):
    def calculate(self) -> float:
        return 1.0


class VipDiscount(DiscountStrategy):
    def calculate(self) -> float:
        return 0.9


class SvipDiscount(DiscountStrategy):
    def calculate(self) -> float:
        return 0.8


class DiscountContext:
    def __init__(self, strategy: DiscountStrategy):
        self.strategy = strategy

    def get_discount(self) -> float:
        return self.strategy.calculate()


context = DiscountContext(VipDiscount())
print(context.get_discount())
```

### Python 代码说明

- `DiscountStrategy`：抽象基类，要求所有策略实现 `calculate`。
- `NormalDiscount`：普通会员折扣策略。
- `VipDiscount`：VIP 会员折扣策略。
- `SvipDiscount`：SVIP 会员折扣策略。
- `DiscountContext`：负责调用策略，不负责判断具体规则。

Python 也可以更轻量地直接传函数：

```python
def normal_discount() -> float:
    return 1.0


def vip_discount() -> float:
    return 0.9


def get_discount(strategy) -> float:
    return strategy()


print(get_discount(vip_discount))
```

这种函数式写法更短，也更符合 Python 的灵活风格。

## 7. TypeScript 和 Python 的区别

- TypeScript 更适合用 `interface` 明确约束策略结构。
- Python 可以用抽象基类，也可以直接用函数或鸭子类型。
- TypeScript 的代码结构更清晰，适合多人协作和大型项目。
- Python 的代码更灵活，简单场景下可以不用类。

## 8. 适用场景

适合使用策略模式的场景：

- 有多种算法或规则可以互相替换。
- 代码里有大量同类型的 `if-else` 或 `switch`。
- 以后经常新增规则。
- 每种规则需要独立测试。
- 主流程稳定，但局部规则经常变化。

常见业务例子：

- 支付方式：支付宝、微信、银行卡、积分支付。
- 折扣规则：普通会员、VIP、SVIP、黑金会员。
- 物流计费：普通快递、顺丰、同城配送、国际配送。
- 登录方式：账号密码、短信验证码、第三方登录。

## 9. 不适用场景

不适合使用策略模式的场景：

- 规则很少，而且几乎不会变化。
- 简单 `if-else` 已经足够清晰。
- 业务逻辑还不稳定，过早抽象会增加理解成本。
- 使用策略模式后，类或函数数量明显变多，但收益很小。

设计模式不是越多越好。它的价值是控制变化，而不是制造复杂度。

## 10. 今日练习

把下面的支付逻辑改造成策略模式。

```ts
function pay(type: string, amount: number) {
  if (type === "alipay") {
    console.log(`支付宝支付 ${amount} 元`);
  } else if (type === "wechat") {
    console.log(`微信支付 ${amount} 元`);
  } else if (type === "bank") {
    console.log(`银行卡支付 ${amount} 元`);
  }
}
```

要求：

- 用 TypeScript 写一版。
- 用 Python 写一版。
- 新增一种支付方式时，尽量不要修改原来的支付上下文代码。

## 11. 今日总结

策略模式的重点不是类图，而是这句话：

```text
当一组规则经常变化时，把变化的部分拆出去，让主流程保持稳定。
```

以后看到类似代码时：

```text
if type == A 执行 A 规则
if type == B 执行 B 规则
if type == C 执行 C 规则
```

可以先思考：这里是不是适合使用策略模式？
