# coding:utf-8

from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class AssetCategory(models.Model):
    # 资产类别
    CategoryName = models.CharField(max_length=50)

    def __unicode__(self):
        return self.CategoryName


class UsageStatus(models.Model):
    # 正常使用状态
    StatusName = models.CharField(max_length=50)

    def __unicode__(self):
        return self.StatusName


class DiscardStatus(models.Model):
    # 报废状态
    # 未处理；已处理
    StatusName = models.CharField(max_length=50)

    def __unicode__(self):
        return self.StatusName


class Information(models.Model):
    # 正常使用资产表
    Department = models.CharField(max_length=50, null=True)  # 使用部门
    UserName = models.CharField(max_length=50, null=True)  # 使用人
    AssetBrand = models.CharField(max_length=50)  # 品牌
    AssetType = models.CharField(max_length=50)  # 型号
    SerialNumber = models.CharField(max_length=100)  # 序列号
    # SerialNumber_Pic = models.ImageField(upload_to='SerialNumber_PIC', null=True)
    Buy_Time = models.DateField()  # 采购时间
    Buy_Channel = models.CharField(max_length=50)  # 采购渠道
    Buy_Price = models.CharField(max_length=50)  # 采购价格
    Buyer = models.CharField(max_length=50)  # 采购人
    AssetCategory = models.ForeignKey(AssetCategory)  # 类别
    UsageStatus = models.ForeignKey(UsageStatus)  # 正常使用状态
    Place = models.TextField(null=True)  # 放置位置
    Remark = models.TextField(null=True)  # 备注
    Discard = models.IntegerField(default=0)  # 0正常使用；1报废


class DiscardAsset(models.Model):
    # 报废资产表
    DiscardAssetID = models.ForeignKey(Information)  # 关联资产ID
    Discard_time = models.DateTimeField(auto_now_add=True)  # 报废时间
    DiscardReason = models.TextField()  # 报废原因
    Dispose_Status = models.ForeignKey(DiscardStatus)  # 处理状态
    Dispose_time = models.DateTimeField(null=True)  # 处理时间
    Dispose_Remark = models.TextField(null=True)  # 处理备注


class Log(models.Model):
    # 操作日志
    datetime = models.DateTimeField()  # 操作时间
    user = models.ForeignKey(User)  # 操作人
    action = models.TextField()  # 操作详细
