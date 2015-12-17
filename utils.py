# coding: utf-8

class JsonDict(dict):
  'general json object that allows attributes to be bound to and also behaves like a dict '
  def __getattr__(self, attr):
    try:
      return self[attr]
    except KeyError:
      raise AttributeError(r"'JsonDict' object has no attribute '%s'" % attr)

  def __setattr__(self, attr, value):
    self[attr] = value
