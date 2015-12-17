# coding: utf-8
from leancloud import Object
from leancloud import Query
from leancloud import LeanCloudError
from flask import Blueprint
from flask import request
from flask import redirect
from flask import url_for
from flask import render_template
import sys
sys.path.insert(0,'../')
from utils import JsonDict
import logging
import json

class Weibo(Object):
    pass

weibos_handler = Blueprint('weibos', __name__)

@weibos_handler.route('', methods=['GET'])
def show():
    try:
      weibos = Query(Weibo).descending('createdAt').find()
    except LeanCloudError, e:
      #服务端还没有Weibo这个Class
      if e.code == 101:
        weibos = []
      else:
        raise e
    return render_template('weibos.html', weibos=weibos)
    """
    try:
        todos = Query(Todo).descending('createdAt').find()
    except LeanCloudError, e:
        if e.code == 101:  # 服务端对应的 Class 还没创建
            todos = []
        else:
            raise e
    return render_template('todos.html', todos=todos)
    """

@weibos_handler.route('', methods=['POST'])
def add():
    #获取搜索出来的某一页里的微博数据
    weibos = request.json['weibos']
    #将这些微博数据存到leancloud
    new_mid_list = []
    for _weibo in weibos:
      _weibo = JsonDict(_weibo)
      #判断这条微博是否已经保存过
      _weibo_is_saved  = len(Query(Weibo).equal_to('mid',_weibo.mid).find()) > 0
      if not _weibo_is_saved:
        #parse it to leancloud object
        weibo = Weibo(mid=_weibo.mid, nickname=_weibo.user_nick_name, timestamp = _weibo.timestamp, topic = _weibo.topic, pics = _weibo.pics)
        weibo.save()
        new_mid_list.append(_weibo.mid)
    return u'话题#%s#新增了%s条微博:%s' % (_weibo.topic, len(new_mid_list), ",".join(new_mid_list))
    """
    todo = Todo(content=content)
    todo.save()
    return redirect(url_for('todos.show'))
    """
