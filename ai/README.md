# python for AI

## 定制化训练大模型
1. 选择基座模型，安装，加载[OpenCompass](https://rank.opencompass.org.cn/home)
2. 配置前端展示
   1. [Gradio](https://www.gradio.app/guides/quickstart)
   2. [streamlit](https://streamlit.io)
3. 低成本部署考虑
   1. 模型量化
   2. CPU,GPU部署调整，多卡部署
4. 微调
   1. 准备数据，训练集，测试集
   2. 使用训练工具,提升训练效率和扩展性  
        1. 加速训练效率
        [DeepSpeed](https://github.com/deepspeedai/DeepSpeed)
        [DeepSpeed介绍](https://developer.aliyun.com/article/1606813)
        2. 用于摘要文本评分
        [ROUGE,Recall-Oriented Understudy for Gisting Evaluation](https://pypi.org/project/rouge-chinese/)
        3. 自然语言处理
        [NLTK,Natural Language Toolkit](https://github.com/nltk/nltk)
        [jieba](https://github.com/fxsjy/jieba),中文分词
        [datasets](https://pypi.org/project/datasets/)
    3. 定制化训练参数，训练
    4. 监督微调
 5. 部署


## 术语及概念
### 模型架构分类
1. 深度神经网络（DNNs，Deep Neural Networks）
    >一种模拟人脑神经元的工作方式的计算模型，深度神经网络的“深度”指的是网络中神经元的层数。具有多个隐藏层的神经网络，通常用于处理复杂的非线性关系。它是所有深度学习模型的基础。  
    包括多层感知机（MLPs）、卷积神经网络（CNNs）、循环神经网络（RNNs）、长短期记忆网络（LSTMs）和门控循环单元（GRUs）。 

2. Transformer模型
    >Transformer是一种基于自注意力机制的模型。它主要由两个部分组成：编码器和解码器。编码器负责将输入的数据（如一段文本或一段语音）转换成一种内部表示，而解码器则使用这种内部表示来生成输出在Transformer中，每个位置的输出并不只依赖于其输入，而是依赖于输入序列中的所有位置。这种“自注意力”机制使得模型能够捕捉到输入数据中的复杂模式和依赖关系。  
    与深度神经网络相比，Transformer的一个显著优点是它不需要像循环神经网络（RNN）那样处理序列数据，因此它可以避免RNN在处理长序列时遇到的梯度消失问题。这使得Transformer在处理自然语言处理等序列数据任务时具有优越性

3. 图神经网络（GNNs，Graph Neural Networks）
    >一种基于图结构的深度学习模型，专门用于处理图数据。适用于处理图结构数据，如社交网络、知识图谱等。

### 模型应用
自然语言处理（NLP，Natural Language Processing）：如机器翻译、文本摘要、情感分析等。
计算机视觉（CV，Computer Vision）：如图像识别、目标检测、图像生成等。
语音识别（ASR，Automatic Speech Recognition）：如语音到文本转换、说话人识别等。
推荐系统（Recommendation System）：如电子商务、视频流媒体平台的个性化推荐

### 参数规模
小型模型：参数量在百万以下，通常用于移动设备和边缘计算。
中型模型：参数量在百万到十亿之间，适用于服务器和云计算。
大型模型：参数量超过十亿，如GPT-3、Switch Transformer等，需要大量的计算资源进行训练和使用

### 大模型训练三个阶段
1. 预训练（Pretraining）
>   预训练是指在大量无标签数据上进行训练，使模型学习到一些基础的语言表示和知识。常见的预训练方法包括自回归语言模型（如GPT系列）、自编码器等。这些方法通过在大规模语料库上训练，使模型能够理解语言的语法、语义和上下文信息。在预训练阶段，模型通常会学习到一些通用的语言特征，这些特征可以用于各种自然语言处理任务。
2. 微调（Fine-tuning）
>   微调是指在预训练模型的基础上，针对特定任务进行训练的过程。在微调阶段，模型会根据具体任务的标注数据进行训练，使模型能够更好地适应特定任务的需求。通过微调，模型可以学习到一些特定任务的语义信息和特征，从而提高任务的性能。在微调阶段，通常会使用一些优化算法和技巧，如学习率衰减、早停等，来加速模型的收敛和提高模型的性能。
3. 人类反馈强化学习（Reinforcement Learning from Human Feedback）
>   人类反馈强化学习是指通过人类提供的反馈来训练模型的方法。这种方法通常涉及到与人类互动的过程，通过让人类对模型生成的输出进行评价和打分，来指导模型的训练和优化。与监督学习和无监督学习不同，人类反馈强化学习更加注重人类的参与和反馈，从而使得模型能够更好地适应人类的意图和需求。在人类反馈强化学习阶段通常会使用一些强化学习算法和技巧，如Q-learning、SARSA等，来优化模型的性能和提升用户体验。

## 数学基础
### 卷积（convolution）
>   这个概念的理解还是不要试图从“图形化的翻转，平移”或者是“像毛巾一样卷”的这种概念去理解。翻译本身上就带了一些语义的歧义进来。从本质上的信号处理原理或者数学定义去理解更能明白含义。
>   卷积的重要的物理意义是：一个函数（如：单位响应）在另一个函数（如：输入信号）上的加权叠加。  
>   对于线性时不变系统，如果知道该系统的单位响应，那么将单位响应和输入信号求卷积，就相当于把输入
>   号的各个时间点的单位响应 加权叠加，就直接得到了输出信号。
>   f(x)和g(x)的卷积，定义为： 
>   $$ (f*g)(x) = \int_{-\infty}^{\infty} f(\alpha)g(x-\alpha)d\alpha $$


