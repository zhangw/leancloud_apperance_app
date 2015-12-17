# coding: utf-8
"""
cloud function implementation
"""
from leancloud import Engine
from app import app
engine = Engine(app)

from libs.msxiaobing.post_msxiaobing import rating_apperance

@engine.define
def hello(**params):
  if 'name' in params:
    return 'Hello, {}!'.format(params['name'])
  else:
    return 'Hello, LeanCloud!'

@engine.after_save('Weibo')
def after_weibo_save(weibo):
  """
  在新的微博对象保存之后,读取pics中图片的URL并进行颜值计算,然后将计算结果更新回该对象
  """
  #照片可能是多张，marks按照照片的索引号，存放各自的得分
  marks = {}
  pics = weibo.get('pics')
  if len(pics) > 0:
    for pic in pics:
      index = pics.index(pic)
      apperance_mark = rating_apperance(pic, local=False)
      if apperance_mark is not None:
        marks[index] = apperance_mark
    #最低的得分
    def _sort_by_mark(key):
      return marks[key]
    if len(marks) > 0:
      min_mark_key = min(marks, key=_sort_by_mark)
      min_mark = marks[min_mark_key]
      try:
        weibo.set('mark', min_mark).set('marks', marks)
        weibo.save()
      except leancloud.LeanCloudError:
        raise leancloud.LeanEngineError(message='An error occurred while trying to update the Weibo object.')
