#encoding:utf-8
__author__ = 'binpo'

from .base_do import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean, SmallInteger,Text,Float,Float

class Erp_Orders(Base):
    __tablename__ = 'orders'

    platform_type = Column(SmallInteger,doc='平台类型 1亚马逊；2速卖通；3敦煌等')
    user_id = Column(Integer,doc='用户ID')
    order_no = Column(String(64),doc='我们自己的订单编号')

    amazon_order_id = Column(String(64),doc='亚马逊定义的订单编号')
    seller_order_id = Column(String(64),doc='卖家所定义的订单编码 废弃 不用',default='')
    market_placeId = Column(String(64),doc='订单生成所在商城的匿名编码')#店铺id
    shop_id = Column(Integer,doc='店铺id和merchant_auth关联')

    #状态相关设置
    amazon_order_status = Column(String(64),doc='亚马逊的订单状态：生成未付款:Pending 付款并准备好发货:Unshipped 已发货:Shipped 取消:Canceled')

    #我们系统的状态
    order_status = Column(Integer,doc='我们库里订单状态 1待处理 2运单申请号 3待打单(未发货) 4已发货 5发货失败 默认待处理状态 6搁置',default=1)
    fillment_date =  Column(String(64),default='',doc='发货时间')
    feed_mission =  Column(String(64),default='',doc='feed_mission_id 发货返回id')

    print_express_bill_status = Column(Integer,doc='面单是否打印状态 1未打面单 2已打面单 默认1' ,default=1)
    print_pick_bill_status = Column(Integer,doc='拣单是否打印状态 是否打印 1未 2已',default=1)
    order_type = Column(Integer,doc='订单包裹类型  1单品单数(一个sku一件商品)  2单品多数（一个sku多个数）  3多品混包（多个sku在一个订单',default=1)
    is_remark = Column(Integer,doc='是否添加备注，1否 2是',default=1)
    order_remark = Column(String(250),doc='填写的拣货说明 即订单说明',default='')

    is_virtual_delivery = Column(Integer, default=1,doc='虚拟发货状态，是否向平台提交运单号： 1未提交 2已提交 3失败')

    #物流相关
    product_shortname = Column(String(128),doc='物流名称')
    express_type = Column(String(128),doc='物流公司类型编码')
    product_id = Column(String(128),doc='物流公司的ID，通过此id获取运单号等信息')

    express_no = Column(String(128),doc='物流单号 运单号',default='')
    express_status = Column(Integer,doc='运单号获取状态 1获取成功 2获取失败 默认为空即为失败状态')

    #费用
    total_amount = Column(Float,doc='订单总费用',default=0)
    currency_code = Column(String(128),doc='三位数的货币代码 格式为 ISO 4217 USD')
    payment_method = Column(String(128),doc='订单的主要付款方式 值: COD货到付款; Other COD和CVS之外的付款方式')

    #时间
    amazon_payment_time = Column(String(64),doc='付款时间')
    purchase_date = Column(String(64),doc='订单创建时间')

    #配送相关
    ful_fillment_channel = Column(String(128),doc='订单配送方式 亚马逊配送 (AFN) 或卖家自行配送 (MFN)')
    shipment_service_level_category = Column(String(64),doc='订单的配送服务级别分类 Expedited;FreeEconomy;NextDay;SameDay;SecondDay;Scheduled;Standard')
    shipping_address = Column(String(2048),doc='订单的配送地址 json字符串 {"Name":"","AddressLine1":"","AddressLine2":"","City":""}')
    number_of_items_shipped = Column(Integer,doc='已配送的商品数量',default=0)
    number_of_items_unshipped = Column(Integer,doc='未配送的商品数量',default=0)

    #配送仅适用于中国
    shipped_by_amazon_TFM = Column(Boolean,doc='指明订单配送方是否是亚马逊配送服务 仅适用于中国',default=0)
    TFM_shipment_status = Column(String(64),doc='亚马逊 TFM订单的状态。仅当ShippedByAmazonTFM = True时返回',default='')

    earliest_ship_date = Column(String(64),doc='承诺的订单发货时间范围的第一天 仅对MFN订单有效')
    latest_ship_date = Column(String(64),doc='承诺的订单发货时间范围的最后一天 仅对MFN订单有效')
    earliest_delivery_date = Column(String(64),doc='承诺的订单送达时间范围的第一天 仅对MFN订单有效')
    latest_delivery_date = Column(String(64),doc='承诺的订单送达时间范围的最后一天 仅对MFN订单有效')

    #买家相关
    buyer_email = Column(String(64),doc='买家的匿名电子邮件地址',default='')
    buyer_name = Column(String(64),doc='买家的姓名',default='')

    sales_channel = Column(String(64),doc='订单中第一件商品的销售渠道',default='')
    ship_service_level = Column(String(128),doc='货件服务水平',default='')

    purchase_status = Column(Boolean,doc='是否采购',default=False)
    purchase_no = Column(String(128), doc='采购单号', default='')
    is_recived = Column(Boolean,doc='是否已收货',default=False)
    order_items = Column(Text,doc='订单产品',default='')
    # is_send_mail = Column(Boolean,doc='是否发邮件',default=False)
    is_caculate = Column(Boolean,doc='是否已计算',default=False)
    delivery_amount = Column(String(32), doc='结算费用', default='')
    delivery_weight = Column(String(32), doc='称重', default='')

class Erp_OrderItems(Base):
    '''商品订单'''
    __tablename__ = 'order_items'

    user_id = Column(Integer,doc='用户ID')
    item_id = Column(Integer,doc='匹配商品ID',default=0)
    item_sku = Column(String(64),doc='商品',default='')
    #-------------------亚马逊属性-------------------
    amazon_asin = Column(String(64),doc='商品的亚马逊标准识别号')
    parent_sku = Column(String(256),doc='父SKU',default='')
    seller_sku = Column(String(64),doc='亚马逊商品的卖家 SKU',default='')
    amazon_order_id = Column(String(128),doc='亚马逊定义的订单号',default='')#订单号
    #亚马逊商品价格相关
    item_price = Column(Float,doc='商品单价',default=0)
    buy_nums = Column(Integer,doc='商品购买数量')
    total_price = Column(Float,doc='商品总价',default=0)
    # item_img = Column(String(1924),doc='图片链接',default=0)

    item_tax = Column(Float,doc='商品价格的税费',default=0)
    shipping_price = Column(Float,doc='运费',default=0)
    shipping_tax = Column(Float,doc='运费税费',default=0)
    shipping_discount = Column(Float,doc='运费的折扣',default=0)
    currency_code = Column(String(64),doc='运费货币类型')
    promotion_discount = Column(Float,doc='报价中的全部促销折扣总计',default=0)
    #买家服务相关
    gift_message_text = Column(String(512),doc='买家提供的礼品消息',default='')
    gift_wrap_level = Column(String(128),doc='买家指定的礼品包装等级',default='')

    #发票相关
    invoice_data = Column(String(2048),doc='发票信息 JSON字符串{"InvoiceRequirement":"","BuyerSelectedInvoiceCategory":"","InvoiceTitle":"","InvoiceInformation":""}',default='')
    product_shortname = Column(String(128),doc='物流名称')
    express_type = Column(String(128),doc='物流公司类型编码')
    product_id = Column(String(128),doc='物流公司的ID，通过此id获取运单号等信息')

    #亚马逊商品相关
    title = Column(String(512),doc='亚马逊商品名称',default='')
    condition_note = Column(String(512),doc='卖家描述的商品状况',default='')
    condition_id = Column(String(64),doc='商品的状况 New Used Collectible Refurbished Preorder Club')
    condition_sub_typeId = Column(String(64),doc='商品的子状况')

    profile = Column(String(256),doc='商品图片',default='')

    #-------------------我们自己的属性-------------------
    # item_id = Column(Integer,doc='产品的id')
    order_id = Column(Integer,doc='订单id')
    order_no = Column(String(64),doc='订单序号')

    #报关信息
    invoice_amount = Column(String(128),doc="申报总价值，必填",default=0)
    invoice_pcs = Column(String(128),doc="件数，必填")
    invoice_title = Column(String(512),doc="英文品名，必填")
    invoice_weight = Column(String(128),doc="单件重")

    order_item_id = Column(String(256),doc="",default='') #OrderItemId 42919851216074
    item_transactionid = Column(String(128),doc="",default=0)
    sku = Column(String(256),doc="中文品名",default='')
    sku_code = Column(String(256),doc="配货信息",default='')
    is_match=Column(Boolean,default=0,doc='是否配对')



