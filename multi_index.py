# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np

'''
在传统的索引中，每个数据点只有一个标签（即索引值）。
而在 MultiIndex 中，每个数据点可以有多个标签，这些标签分层存储，形成一个分层的索引结构。
这种结构类似于数据库中的复合键，可以更高效地组织和查询数据。

### 概念理解
1. index指的就是GDP数据对应的索引,这里是两层, Country, Year
2. tag标签,指的就是index中的子索引, 这里就是 USA, 2018等
3. level,指的就是索引的某一层,Country,或者是 Year一层
               GDP
Country   Year     
USA       2018  1000
          2019  1200
          2020  1300
Canada    2018  1100
          2019  1400
          2020  1500
Mexico    2018  1600
          2019  1700


### 价值和优势
1. 数据组织：
MultiIndex 允许你在一个索引中存储多个维度的数据，使得数据结构更加清晰和有层次。
2. 高效查询：
通过多级索引，你可以快速访问特定维度的数据，而不需要进行复杂的筛选操作。
3. 灵活性：
MultiIndex 支持多种操作，如切片、交叉选择等，使得数据操作更加灵活。
4. 数据完整性：
多级索引可以帮助你保持数据的完整性，避免数据丢失或重复。

### 使用场景
1. 时间序列数据：
分析不同时间点的数据，例如股票价格、经济指标等。
2. 面板数据：
分析多个实体在不同时间点的数据，例如不同国家的经济数据。
3. 多维度数据：
分析具有多个分类维度的数据，例如不同产品在不同地区的销售数据。

### 构造方法
返回一个 MultiIndex 对象，该对象可以用作 DataFrame 或 Series 的多层次行或列索引
class pandas.MultiIndex(levels=None, 
                        codes=None, 
                        sortorder=None, 
                        names=None, 
                        dtype=None, 
                        copy=False, 
                        name=None, 
                        verify_integrity=True)
levels：序列或列表，包含每个索引级别的唯一标签值。它定义了每个层级的可能值。
codes：序列或列表，包含每个级别对应的整数索引。它对应 levels 中的标签值的编码。
sortorder：整数或 None，表示索引应按第几个级别进行排序。如果没有设置则保持默认顺序。
names：序列或列表，指定每个级别的名称。通常是每个索引层级的标签。
dtype：索引的数据类型，默认为 object。
copy：布尔型，表示是否复制输入数据。默认为 False。
name：索引名称，与 names 类似，但只适用于单一名称。
verify_integrity：布尔型，默认为 True，表示是否检查 codes 是否与 levels 一致，以确保 MultiIndex 的有效性。

MultiIndex 的属性
levels：返回每个层级的标签值。
codes：返回每个层级的整数索引编码。
names：返回索引每个层级的名称。
nlevels：返回层级的数量。
size：返回 MultiIndex 的大小，即行数。
is_unique：返回索引是否唯一。
has_duplicates：返回索引中是否存在重复值。

MultiIndex 的方法
from_arrays：从多个数组创建 MultiIndex。
from_tuples：从元组列表创建 MultiIndex。
from_product：从笛卡尔积创建 MultiIndex。
from_frame：从 DataFrame 创建 MultiIndex。
to_frame：将 MultiIndex 转换为 DataFrame。
get_level_values：获取指定层级的值。
droplevel：删除指定层级。
'''
def multiIndex():
    # 创建一个示例数据集
    data = {
        'GDP': [1000, 1200, 1300, 1100, 1400, 1500, 1600, 1700]
    }

    # 创建 MultiIndex
    index = pd.MultiIndex.from_tuples([
        ('USA', 2018), ('USA', 2019), ('USA', 2020),('Canada', 2018), 
        ('Canada', 2019), ('Canada', 2020),('Mexico', 2018), ('Mexico', 2019)
    ], names=['Country', 'Year'])

    # 创建 DataFrame
    df = pd.DataFrame(data, index=index)

    # 查看 DataFrame
    print(df)

    # 访问特定国家的数据
    usa_data = df.loc['USA']
    print(usa_data)

    # 访问特定年份的数据
    year_2018_data = df.xs(2018, level='Year')
    print(year_2018_data)

    # 访问特定年份的数据
    year_2018_data = df.xs(2018, level='Year')
    print(year_2018_data)

    # 检查索引是否为多级索引
    if isinstance(df.index, pd.MultiIndex):
        print("索引是 MultiIndex")
    else:
        print("索引不是 MultiIndex")

    print(df)
    # 获取 MultiIndex 的所有级别
    levels = df.index.levels
    # 打印每个级别的所有唯一值
    for i, level in enumerate(levels):
        print(f"Level {i} ({df.index.names[i]}): {list(level)}")


    return

def main():
    multiIndex()
    return

if __name__ == '__main__':
    main()




