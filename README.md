# 调用示例：
根据需求可分别调用标题、时间、作者，也可以调用together返回包含三者的字典，若没有取到相应value为null。构建对象时需要传入html，response中的 Last-Modified（此参数可不传）

    from tdaExtract.dtObtain import Document
    import requests
    
    # 获取 HTML
    url = 'http://news.163.com/18/0305/09/DC4I8HRC0001875N.html'
    response = requests.get(url)
    
    # 获取response中的 Last-Modified
    header_time = response.headers["Last-Modified"]
    
    # 构建对象，传入html和header_time, header_time作为一个准确性参考，若没有可不传
    item = Document(html, header_time)
    
    # 获取title,date,author， 返回类型：dict
    tda_dict = item.together()
    
    # 可分别获取title,date,author, 返回类型：dict
    title_dict = item.title()
    date_dict = item.date()
    author_dict = item.author()


# 说明
1、Date提取：基于正则匹配文章时间，然后进行加权计分得出最佳时间。
		  self._html()初始化函数对HTML进行不必要的标签过滤，降低提取噪点，提高正则匹配速度。
		  get_date()方法对时间进行加权计分，返回时间格式化和时间戳的字典
		  
2、title提取：参照readability启发式提取方式，self._parse()初始化函数构建dom树、对html设置编码和去噪点。get_title()方法进行标题的提取。

3、author和source提取：是根据查看网页的规律来用正则手动去匹配一些个通用的规则去提取信息放到AS_INFO，对于特殊的网站直接把对应的正则添加到config配置文件里的AS_INFO里就行。