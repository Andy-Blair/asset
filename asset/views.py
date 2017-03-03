# _*_ coding:utf-8 _*_
from django.shortcuts import render_to_response, HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import forms
import models
import json
import xlrd
import xlwt
import StringIO
import sys,datetime

reload(sys)
sys.setdefaultencoding('utf-8')

# Create your views here.


def login_view(request):
    # 登陆验证
    loginform = forms.LoginForm()
    if request.method == 'POST':
        username = request.POST.get('username')
        passwd = request.POST.get('password')
        user = authenticate(username=username, password=passwd)
        if user is not None and user.is_active:
            login(request,user)
            return HttpResponseRedirect('/asset/index/')
    return render_to_response('login.html', {'loginform': loginform})


@login_required(login_url="/asset/login/")
def logout_view(request):
    # 退出登陆
    logout(request)
    return HttpResponseRedirect('/')


@login_required(login_url="/asset/login/")
def index(request):
    # 首页
    super_admin = False  # 超级管理员标识符，True代表超级管理员
    admin = False
    user = User.objects.get(id=request.session['_auth_user_id'])  # 从数据库查询登陆用户信息
    try:
        # 获取用户组，判断是否具有超级管理员权限
        perm = user.groups.values()[0]['name']
        # 把用户组传递到模板，在模板中判断是否显示操作按钮
        if perm:
            super_admin = perm
    except:
        pass
    upload = forms.UploadFile()  # 实例化上传的表单类
    return render_to_response('index.html', {'importfile': upload, 'super_admin': super_admin, 'login_user': user.username})


@login_required(login_url="/asset/login/")
def dataimport(request):
    # 导入数据
    # 待优化：上传同名文件时，不能保存前一个文件（是否需要保留多个文件？）
    if request.method == 'POST':
        import_file = request.FILES.get('upload_file', None)
        write_file = open('./uploadfile/%s' %import_file.name, 'wb')
        for i in import_file.chunks():
            write_file.write(i)
        write_file.close()
        work_book = xlrd.open_workbook('./uploadfile/%s' % import_file.name)
        work_sheet = work_book.sheets()[0]
        for line in range(1, work_sheet.nrows):
            line_data = work_sheet.row_values(line)
            # 转换导入文件中的日期格式为存储所需格式“YYYY-MM-DD”
            try:
                t = str(line_data[5])
                d = datetime.datetime.strptime(t,'%Y-%m-%d')
            except:
                t = "9999-01-01"
            # to_localtime = time.localtime(time.mktime(time.strptime(t,"%Y-%m-%d")))
            # insert_time = time.strftime("%Y-%m-%d", to_localtime)
            #  获取外键表的实例（外键直接赋值时，值必须是外键表的实例），此处不可使用filter方法
            try:
                category_id = models.AssetCategory.objects.get(CategoryName=line_data[9])
            except:
                category_id = models.AssetCategory.objects.get(id=1)
            try:
                usagestatus_id = models.UsageStatus.objects.get(StatusName=line_data[10])
            except:
                usagestatus_id = models.UsageStatus.objects.get(id=1)
            # 插入数据
            insert_data = models.Information(Department=line_data[0], UserName=line_data[1], AssetBrand=line_data[2],
                                             AssetType=line_data[3], SerialNumber=line_data[4], Buy_Time=t,
                                             Buy_Channel=line_data[6], Buy_Price=line_data[7], Buyer=line_data[8],
                                             AssetCategory=category_id, UsageStatus=usagestatus_id, Place=line_data[11],
                                             Remark=line_data[12])
            insert_data.save()
    return HttpResponseRedirect('/asset/index/')


@login_required(login_url="/asset/login/")
def dataexport(request):
    # 导出数据到 EXCEL
    # StringIO模块在3.0将取消
    # excel导出后内容的格式待优化
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment;filename=AssetInformation_export.xls'  # 指定生成的文件名
    filter_data = models.Information.objects.filter(Discard=0)  # 查询正常在用的资产
    # 使用xlwt模块生成 EXCEL
    excel_file = xlwt.Workbook(encoding='utf-8')
    sheet = excel_file.add_sheet('sheet1')
    excel_file_head = ['使用部门', '使用人','品牌(必填)','型号(必填)','序列号(必填)','采购时间(必填)',
                       '采购渠道(必填)','采购价格(必填)','采购人(必填)', '类别(必填)', '使用状态(必填)','放置位置','备注']
    line = 1
    col = 0
    for i in excel_file_head:
        sheet.write(0, col, i)
        col += 1
    for i in filter_data:
        col = 0
        data = [i.Department, i.UserName, i.AssetBrand, i.AssetType, i.SerialNumber, i.Buy_Time.strftime("%Y-%m-%d"),
                i.Buy_Channel, i.Buy_Price, i.Buyer, i.AssetCategory.CategoryName, i.UsageStatus.StatusName, i.Place, i.Remark]
        for item in data:
            sheet.write(line, col, item)
            col += 1
        line += 1
    output = StringIO.StringIO()
    excel_file.save(output)
    output.seek(0)
    response.write(output.getvalue())
    return response


@login_required(login_url="/asset/login/")
def add(request):
    # 新增固定资产
    user = User.objects.get(id=request.session['_auth_user_id'])
    assetaddform = forms.AssetAddForm()
    if request.method == 'GET':
        return render_to_response('add.html', {'assetform':assetaddform, 'login_user': user.username})
    if request.method == 'POST':
        assetadddata = forms.AssetAddForm(request.POST)
        if assetadddata.is_valid():
            data = assetadddata.clean()
            categoy = models.AssetCategory.objects.get(CategoryName=data['assetcategory'])
            use = models.UsageStatus.objects.get(StatusName=data['usagestatus'])
            db = models.Information(Department=data['department'], UserName=data['username'], AssetBrand=data['assetbrand'],
                                    AssetType=data['assettype'], SerialNumber=data['serialnumber'], Buy_Time=data['buytime'],
                                    Buy_Channel=data['buychannel'], Buy_Price=data['buyprice'], Buyer=data['buyer'],
                                    AssetCategory=categoy, UsageStatus=use, Place=data['place'],
                                    Remark=data['remark'])
            db.save()
            return HttpResponseRedirect('/asset/index/')


@login_required(login_url="/asset/login/")
def modify(request, dataid):
    # 资产信息修改
    user = User.objects.get(id=request.session['_auth_user_id'])
    datas = models.Information.objects.get(id=dataid)
    if request.method == 'GET':
        # if datas.SerialNumber:
        #     soc_serial = datas.SerialNumber.name.split('/')[1]
        # else:
        #     soc_serial = None
        data = {'username': datas.UserName, 'department': datas.Department, 'assetbrand': datas.AssetBrand,
                'assettype': datas.AssetType, 'serialnumber': datas.SerialNumber, 'buytime': datas.Buy_Time.strftime("%Y-%m-%d"),
                'buychannel':datas.Buy_Channel, 'buyprice':datas.Buy_Price, 'buyer': datas.Buyer,
                'assetcategory': datas.AssetCategory.CategoryName, 'usagestatus': datas.UsageStatus.StatusName,
                'place': datas.Place, 'remark': datas.Remark}
        assetaddform = forms.AssetAddForm(data)
        return render_to_response('modify.html', {'assetform': assetaddform, 'login_user': user.username})
    if request.method == 'POST':
        assetadddata = forms.AssetAddForm(request.POST, request.FILES)
        if assetadddata.is_valid():
            data = assetadddata.clean()
            datas.UserName = data['username']
            datas.Department = data['department']
            datas.AssetBrand = data['assetbrand']
            datas.AssetType = data['assettype']
            datas.SerialNumber = data['serialnumber']
            datas.Buy_Time = data['buytime']
            datas.Buy_Channel = data['buychannel']
            datas.Buy_Price = data['buyprice']
            datas.Buyer = data['buyer']
            datas.AssetCategory = models.AssetCategory.objects.get(CategoryName=data['assetcategory'])
            datas.UsageStatus = models.UsageStatus.objects.get(StatusName=data['usagestatus'])
            datas.Place = data['place']
            datas.Remark = data['remark']
            # if data['serianumber']:
            #     datas.SerialNumber = data['serianumber']
            datas.save()
            return HttpResponseRedirect('/asset/index/')
        else:
            return HttpResponse('faile')


@login_required(login_url="/asset/login/")
def copyadd(request, dataid):
    # 复制新增资产
    if request.method == 'GET':
        user = User.objects.get(id=request.session['_auth_user_id'])
        datas = models.Information.objects.filter(id=dataid)
        data = {}
        for i in datas:
            data = {'username': i.UserName, 'department': i.Department, 'assetbrand': i.AssetBrand,
                    'assettype': i.AssetType, 'serialnumber': i.SerialNumber, 'buytime': i.Buy_Time.strftime("%Y-%m-%d"),
                    'buychannel': i.Buy_Channel, 'buyprice': i.Buy_Price, 'buyer': i.Buyer,
                    'assetcategory': i.AssetCategory, 'usagestatus': i.UsageStatus, 'place': i.Place,
                    'remark': i.Remark}
        assetaddform = forms.AssetAddForm(data)
        return render_to_response('add.html', {'assetform': assetaddform, 'login_user': user.username})
    if request.method == 'POST':
        assetadddata = forms.AssetAddForm(request.POST, request.FILES)
        if assetadddata.is_valid():
            data = assetadddata.clean()
            categoy = models.AssetCategory.objects.get(CategoryName=data['assetcategory'])
            use = models.UsageStatus.objects.get(StatusName=data['usagestatus'])
            db = models.Information(UserName=data['username'], Department=data['department'], AssetBrand=data['assetbrand'],
                                    AssetType=data['assettype'], SerialNumber=data['serialnumber'], Buy_Time=data['buytime'],
                                    Buy_Channel=data['buychannel'], Buy_Price=data['buyprice'], Buyer=data['buyer'],
                                    AssetCategory=categoy, UsageStatus=use, Place=data['place'],
                                    Remark=data['remark'])
            db.save()
            return HttpResponseRedirect('/asset/index/')
        else:
            return HttpResponse('upload faile')


@login_required(login_url="/asset/login/")
def discard(request, dataid):
    # 点击报废自动添加报废时间，报废原因必须写
    if request.method == "POST":
        get_asset = models.Information.objects.get(id=dataid)
        get_asset.Discard = 1
        d = models.DiscardAsset(DiscardAssetID=get_asset, DiscardReason=request.POST['discardreason'], Dispose_Status=models.DiscardStatus.objects.get(id=1))
        get_asset.save()
        d.save()
        return HttpResponseRedirect('/asset/index')


@login_required(login_url="/asset/login/")
def discard_index(request):
    super_admin = False  # 超级管理员标识符，True代表超级管理员
    admin = False  # 管理员标识符，True代表管理员
    user = User.objects.get(id=request.session['_auth_user_id'])  # 从数据库查询登陆用户信息
    try:
        # 获取用户组，判断是否具有超级管理员权限
        perm = user.groups.values()[0]['name']
        # 把用户组传递到模板，在模板中判断是否显示操作按钮
        if perm:
            super_admin = perm
    except:
        pass
    return render_to_response('discard.html', {'super_admin': super_admin, 'login_user': user.username})


@login_required(login_url="/asset/login/")
def indexdata(request):
    # 首页bootstrap-table数据
    data = []
    # ↓此处待优化，如果一次把所有数据都查询出来，当数据量过大的时候，内存不够用会导致内存溢出
    data_value = models.Information.objects.filter(Discard=0)
    for i in data_value:
        d = {'ID': i.id, 'department': i.Department, 'username': i.UserName, 'assetbrand': i.AssetBrand,
             'assettype': i.AssetType, 'serianumber': i.SerialNumber, 'buytime': i.Buy_Time.strftime("%Y-%m-%d"),
             'buychannel': i.Buy_Channel, 'buyprice': i.Buy_Price, 'buyer': i.Buyer, 'assetcategory': i.AssetCategory.CategoryName,
             'usagestatus':i.UsageStatus.StatusName, 'place': i.Place, 'remark': i.Remark}
        data.append(d)
    return HttpResponse(json.dumps(data), content_type="application/json")


@login_required(login_url="/asset/login/")
def discarddata(requst):
    # 报废列表bootstrap-table数据
    data = []
    data_value = models.Information.objects.filter(Discard=1)
    for i in data_value:
        data_value2 = models.DiscardAsset.objects.get(DiscardAssetID=i)
        dis_time = None
        if data_value2.Dispose_time:
            dis_time = data_value2.Dispose_time.strftime("%Y-%m-%d")
        d = {'ID': i.id, 'assetbrand': i.AssetBrand, 'assettype': i.AssetType, 'serianumber': i.SerialNumber,
             'buytime': i.Buy_Time.strftime("%Y-%m-%d"), 'buyprice': i.Buy_Price,
             'assetcategory': i.AssetCategory.CategoryName, 'discardtime': data_value2.Discard_time.strftime("%Y-%m-%d"),
             'discardreason':data_value2.DiscardReason, 'disposestatus':data_value2.Dispose_Status.StatusName,
             'disposetime':dis_time, 'disposeremark':data_value2.Dispose_Remark}
        data.append(d)
    return HttpResponse(json.dumps(data), content_type="application/json")


# 统计
@login_required(login_url="/asset/login/")
def statistical(request):
    sum_data = {}
    categrys = models.AssetCategory.objects.filter(id__gt=1)
    use = models.UsageStatus.objects.filter(id__gt=1)
    for i in categrys:
        u_sums = []
        t = {}
        sums = models.Information.objects.filter(AssetCategory=i, Discard=0).count()
        t['总计'] = sums
        u_sums.append(t)
        for u in use:
            u_sum = models.Information.objects.filter(AssetCategory=i, Discard=0, UsageStatus=u).count()
            t1 = {}
            t1[u.StatusName] = u_sum
            u_sums.append(t1)
        sum_data[i.CategoryName] = u_sums
    return HttpResponse(json.dumps(sum_data), content_type="application/json")
