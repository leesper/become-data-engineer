# A Free World in Github

# Project Scope

This capstone project focuses on the open source software hosted in Github. It will do some interesting analysis about the data of them. I will first collect related datasets, extract some samples and do some EDAs locally in order to understand the data and find some insights. Second, I will upload the datasets into AWS S3 bucket, using Apache Airflow to create a pipeline using Spark on EMR to load them into staging tables on redshift and perform ETLs forming a series of target tables. 

The end case of this project will be a data visualization dashboard showing the results, with the help of some front-end and backend techniques.

# Gather Data

I find the public dataset from [awesome public datasets](https://github.com/awesomedata/awesome-public-datasets) in the portion of **Software**. The datasets are of 13GB and in CSV format and come from [Libraries.io Open Source Repository and Dependency Metadata](https://zenodo.org/record/1068916). This data is collected from GitLab, Github and BitBucket. Considering that this project only interests in repositories on Github, we also take the [Github Developer API](https://developer.github.com/v3/) as a supplement.

# Explore & Assess Data

通过探索性数据分析对数据样本进行初步研究

对数据进行质量检查，文档记录数据清洗加工的处理过程

通过对数据的研究确认要从Github API获取和采集哪些数据（JSON格式）

# Conceptual Data Model

解释所选择数据模型的合理性

根据数据模型进行数据管道概念设计

# ETL Data Modeling

数据管道编排
    从Github API采集目标数据
    在数据管道中进行数据质量检查
        完整性检查
        单元测试代码
        source/count检查

提供最终数据的数据字典

notes:
1. 使用S3存储原始文件，使用Redshift做数据仓库，用EMR的Spark集群做计算，用Airflow做管道编排
2. Redshift集群要attach一个role来访问S3，同样EMR也要attach一个role访问Redshift，Airflow要通过IAM user访问EMR和Redshift

# Applications Architecture

项目应用的目标（根据上面对数据的研究确定最终产品形态）
    为什么选择这个数据模型
进行项目架构设计
    架构设计
    技术选型合理性
    性能指标
        SLA
        数据量增大100x怎么办
        100+DB访问量如何处理
    解释数据的更新频率
    每日七点定时运行如何实现
    后端开发
        运行哪些查询？
    前端开发
    云端部署

整理成博客并附上链接

