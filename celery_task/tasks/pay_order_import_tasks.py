#!/usr/bin/env python
# encoding: utf-8
'''
@author: qiuyan
@contact: winston@peipeiyun.com
@file: location_update_tasks.py
@time: 2019/8/8 5:35 PM
@desc:
'''
from celery_task.base import DatabaseTasks
from celery_task.celery import app
from loguru import logger as operaton_log
operaton_log.add("log/task/user_operation_logs.log",format="{time} {level} {message}",rotation="50 MB")

import traceback
from conn.redis_conn import getRedisConn
from celery_task.config import REDIS
import json
from ..models.orders_do import*
from models.user_do import *
from models.orders_do import *
from models.item_do import ItemSKU
from ..base import erp_coon
@app.task(base=DatabaseTasks)
def pay_order_import_operation():
    rdb = getRedisConn(host=REDIS.get('host'), port=REDIS.get('port'), db=REDIS.get('db'))
    order_no_dumps = rdb.rpop('pay_order')
    if order_no_dumps:
        order_no_json = json.loads(order_no_dumps)
        session = pay_order_import_operation.db
        # # 订单详情
        orders = session.query(Orders).filter(Orders.deleted == 0,Orders.order_no == order_no_json.get("order_num")).scalar()
        order_items = session.query(OrderItems).filter(OrderItems.deleted == 0,OrderItems.order_id == orders.id)
        address = session.query(UserAddress).filter(UserAddress.deleted==0,UserAddress.id==int(orders.recevie_address_id)).scalar()
        address_info = {
            "City":{"value":address.city},
            "Name":{"value":address.email},
            "CountryCode":{"value":address.country_code},
            "Phone":{"value":address.phone},
            "StateOrRegion":{"value":address.province},
            "AddressLine1":{"value":address.address},
            "PostalCode":{"value":address.zipcode}}

        session.close()
        # erp_orders=erp_coon().query(Erp_Orders).filter(Erp_Orders.id == 1,).scalar()
        # print(erp_orders.order_no)
        erp_session = erp_coon()

        erp_order=Erp_Orders()
        # 平台类型(1,亚马逊)
        erp_order.platform_type=1
        # 用户id
        erp_order.user_id=0
        # 外贸系统编号
        erp_order.order_no=orders.order_no
        # 亚马逊编号
        erp_order.amazon_order_id = orders.order_no
        #
        erp_order.market_placeId = ""
        #店铺
        erp_order.shop_id=0
        #订单状态
        erp_order.amazon_order_status = "Unshipped"
        erp_order.order_status=1
        #物流名称
        erp_order.product_shortname = orders.transport_name
        # 物流编码
        erp_order.express_type = ""
        # 物流id
        erp_order.product_id=1
        # 物流状态
        erp_order.express_status=1
        # 总费用
        erp_order.total_amount=orders.real_amount

        erp_order.currency_code = "ISO"
        erp_order.payment_method = "Other"

        # 付款时间
        erp_order.amazon_payment_time = orders.pay_time
        # 订单创建时间
        erp_order.purchase_date = orders.gmt_created

        # 配送相关
        erp_order.ful_fillment_channel = "MFN"
        # 配送级别
        erp_order.shipment_service_level_category = "FreeEconomy"
        # 货币代码
        # 配送地址
        erp_order.shipping_address = str(address_info)

        # erp_order.earliest_ship_date ="2017-09-20T22:59:59Z"
        # erp_order.latest_ship_date ="2017-09-20T22:59:59Z"
        # erp_order.earliest_delivery_date ="2017-09-20T22:59:59Z"
        # erp_order.latest_delivery_date ="2017-09-20T22:59:59Z"
        erp_session.add(erp_order)
        erp_session.flush()
        orders_item_info=[]
        order_simple_info={}
        for i in order_items:
            # 找到子商品信息
            orders_item = session.query(ItemSKU).filter(ItemSKU.deleted == 0,
                                                  ItemSKU.id==i.sku_id).scalar()
            erp_order_items=Erp_OrderItems()
            erp_order_items.order_id=erp_order.id
            erp_order_items.buy_nums=i.buy_nums
            erp_order_items.order_no=erp_order.order_no
            erp_order_items.item_price=i.item_price
            erp_order_items.shipping_price=orders.transport_anmount
            erp_order_items.total_price=i.total_amount
            erp_order_items.parent_sku= orders_item.parent_item_no
            erp_order_items.seller_sku= orders_item.item_no
            erp_order_items.profile=i.item_img
            erp_order_items.title=i.item_title
            erp_order_items.product_id=orders.transport_id
            erp_order_items.product_shortname=orders.transport_name
            erp_order_items.order_no=orders.order_no
            erp_session.add(erp_order_items)
            order_simple_info={
                "sku":orders_item.item_no,
                "asin":orders_item.id,
                "num":i.buy_nums,
                "image":orders_item.color_img
            }
        orders_item_info.append(order_simple_info)
        erp_order.order_items= json.dumps(orders_item_info)
        erp_session.commit()
        erp_session.close()
    else:
        print("无新订单")
    # data = {
    #     "order":{"num":123321,
    #              "statue":"代发货"},
    #     "items":{
    #         "sku":1231,
    #         "num":"ewqeq",
    #         "price":"2e21e",
    #         "pic":12313
    #     }
    # }

    # operaton_log.info(log)
    # while log:
    #     try:
    #         p = ujson.loads(log)
    #         agent = p.get('user_type','admin')
            # logs = OperationLogs()
            # logs.user_id = get_id_by_show_id(p.get('show_id'))
            # if agent=='agent':
            #     agent = AgentMerchant.get(AgentMerchant.id==get_id_by_show_id(p.get('show_id')))
            #     logs.username = agent.agent_company
            # else:
            #     if not p.get('show_id') in users:
            #         admin = Admins.get(Admins.id==get_id_by_show_id(p.get('show_id')))
            #         if admin:
            #             users[p.get('show_id')] = admin.nickname
            #     logs.username = users.get(p.get('show_id'),'')
            # logs.user_type = agent
            # logs.name = p.get('name')
            # logs.args = p.get('args')
            # logs.is_success = p.get('is_success')
            # logs.operation = p.get('operation')
            # logs.url=p.get('url','')
            # logs.create_time = p.get('datetime')
            # logs.error = p.get('error')
            # logs.save()
            # log = rdb.rpop('pay_order')
        # except:
        #     operaton_log.error(traceback.format_exc())
        #     break
    # db.close()

