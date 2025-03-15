# data-analysis

## Graph
- 直方图(histogram)
    >适用于描述连续数据的集中趋势和离散程度,主要用来展示数据的分布情况,每个柱子表示一个区间内的数据频率
- 柱状图(bar)
    >适用于展示分类数据的计数、频率或其他度量,主要用来做差异比较，不同类别之间的数值大小

- 热力图(heatmap)
    >通过颜色变化展示数据密度、分布及变化趋势的可视化工具，有很高的空间利用率，色块可以紧凑排列，颜色的深度
    可以跨越较大数据范围，并且人类本身对颜色的理解要由于对数字的理解

<!--
小提琴图
箱线图
散点矩阵图
带边际分布的 Hexbin 图
-->

## Terms
- 虚拟变量（也称为独热编码，One-Hot Encoding）
    >一种将分类变量转换为数值变量的方法。每个分类变量的类别（category）会被转换为一个独立的列，列中只有有 0 和 1 两种值，表示该类别是否出现

- 多重共线性（Multicollinearity）
    >统计学和机器学习中一个重要的概念，指的是在回归模型中，两个或多个解释变量（自变量）之间存在高度相关性。这种相关性可能导致模型的估计结果不稳定，参数解释不准确，甚至影响模型的预测性能。

- VIF
    >检测多重共线性的常用指标。VIF 值越高，表示该变量与其他变量之间的共线性越强。



## Reference
- [sql join](https://learnsql.com/blog/sql-join-cheat-sheet/joins-cheat-sheet-a4.pdf)
- [统计学讲义](https://www.math.pku.edu.cn/teachers/lidf/course/probstathsy/probstathsy.pdf)



