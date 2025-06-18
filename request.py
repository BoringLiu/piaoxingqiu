import requests
import datetime
import logging
from config import token, sckey

# 根据项目id获取所有场次和在售状态
def get_sessions(show_id) -> list | None:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Mobile Safari/537.36',
        'Content-Type': 'application/json'
    }
    url = "https://m.piaoxingqiu.com/cyy_gatewayapi/show/pub/v3/show/" + show_id + "/sessions_dynamic_data"
    response = requests.get(url=url, headers=headers).json()
    if response["statusCode"] == 200:
        return response["data"]["sessionVOs"]
    else:
        logging.error("get_sessions异常: " + str(response))
    return None

# 根据场次id获取座位信息
def get_seat_plans(show_id, session_id) -> list:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Mobile Safari/537.36',
        'Content-Type': 'application/json'
    }
    url = "https://m.piaoxingqiu.com/cyy_gatewayapi/show/pub/v3/show/" + show_id + "/show_session/" + session_id + "/seat_plans_static_data"
    response = requests.get(url=url, headers=headers).json()
    if response["statusCode"] == 200:
        return response["data"]["seatPlans"]
    else:
        raise Exception("get_seat_plans异常: " + str(response))

# 获取座位余票
def get_seat_count(show_id, session_id) -> list:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Mobile Safari/537.36',
        'Content-Type': 'application/json'
    }
    url = "https://m.piaoxingqiu.com/cyy_gatewayapi/show/pub/v3/show/" + show_id + "/show_session/" + session_id + "/seat_plans_dynamic_data"
    response = requests.get(url=url, headers=headers).json()
    if response["statusCode"] == 200:
        return response["data"]["seatPlans"]
    else:
        raise Exception("get_seat_count异常: " + str(response))

def send_wechat_message(message):
    api_url = f"https://sctapi.ftqq.com/{sckey}.send"
    data = {
        'text': '抢票成功提醒',
        'desp': message
    }
    response = requests.post(api_url, data=data)
    return response.json()

# 获取门票类型（快递送票EXPRESS,电子票E_TICKET,现场取票VENUE,电子票或现场取票VENUE_E）
def get_deliver_method(show_id, session_id, seat_plan_id, price: int, qty: int) -> str:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Mobile Safari/537.36',
        'Content-Type': 'application/json',
        'access-token': token
    }
    data = {
        "items": [
            {
                "skus": [
                    {
                        "seatPlanId": seat_plan_id,  # 644fcf080f4f4e0001f1519d
                        "sessionId": session_id,  # 644fcb7dca916100017dda3d
                        "showId": show_id,  # 644fcb2aca916100017dcfef
                        "skuId": seat_plan_id,
                        "skuType": "SINGLE",
                        "ticketPrice": price,  # 388
                        "qty": qty  # 2
                    }
                ],
                "spu": {
                    "id": show_id,
                    "spuType": "SINGLE"
                }
            }
        ]
    }
    url = "https://m.piaoxingqiu.com/cyy_gatewayapi/trade/buyer/order/v3/pre_order"
    # logging.info(seat_plan_id)
    response = requests.post(url=url, headers=headers, json=data).json()
    if response["statusCode"] == 200:
        return response["data"]["supportDeliveries"][0]["name"]
    else:
        raise Exception("获取门票类型异常: " + str(response))

# 获取观演人信息
def get_audiences() -> list | None:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Mobile Safari/537.36',
        'Content-Type': 'application/json',
        'access-token': 'eyJ0eXAiOiJKV1QiLCJjdHkiOiJKV1QiLCJ6aXAiOiJERUYiLCJhbGciOiJSUzUxMiJ9.eNp8kU2PgjAQhv9Lzx76BQVuymokwWBYOXhqCgyRBIGUslnX-N-3VbN62uPMPO_MOzNXNKjZnJK-GVDUz123QPME-hFfUdn-xEMNKEKbbSp3aIGmuVz9JX3qCxVggJqSwONUBH5DeMgtZ5X50DloVRzXuc2cTVW41rUTeiH3KkFZo5qQYIwJhpoH-CF8YYKVARVMCQ-q0GGMhMJv0O3OZSNoZYb_WOJamstojRBrAXR1Ur15X_cL9NQOPYroAo1Km9bcI-RbIXyPrYZDe3Zy4WFGCbfOuUUrDcq8lSjz8LM0XSYD5-eJ4mUij4mM06z4kPdTyH2Rx9vl51ru0-Vhk-W7x6T3Eba_9dlD51Z7vaVXbpyLb78AAAD__w.HBkmpp4SvLtYFgZFpWTNHtcvCVH6sr_2dQ2IJCjKl7_kh8r1ZpOVEMoz_ytT9Mw8CQs96NkaC4WB0rczjk-ZLut0QtSR2NIn4jZDqgGC45B_97n_UQemhtHtzSeCbsiQ3y5HiCrsUGBdrWcCiZanfFb5N4tynyzkHsQ7XOTWb9s'
    }
    # url = "https://m.piaoxingqiu.com/cyy_gatewayapi/user/buyer/v3/user_audiences"
    url = "https://m.piaoxingqiu.com/cyy_gatewayapi/user/buyer/v3/user_audiences?idTypes=&lang=zh&length=500&offset=0&showId=&terminalSrc=WEB&utcOffset=480&ver=4.35.3&src=WEB"
    response = requests.get(url=url, headers=headers).json()
    if response["statusCode"] == 200:
        logging.info("get_audiences 通信正常")
        # logging.info(response)
        # return response["data"]["audiences"]
        return response["data"]
    else:
        logging.error("get_audiences异常: " + str(response))
    return None

# 获取收货地址
def get_address() -> dict | None:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Mobile Safari/537.36',
        'Content-Type': 'application/json',
        'access-token': token
    }
    url = "https://m.piaoxingqiu.com/cyy_gatewayapi/user/buyer/v5/user/addresses/default"
    response = requests.get(url=url, headers=headers).json()
    if response["statusCode"] == 200:
        return response["data"]
    else:
        logging.error("get_address异常: " + str(response))
    return None

# 获取快递费
def get_express_fee(show_id, session_id, seat_plan_id, price: int, qty: int, location_city_id: str) -> dict:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Mobile Safari/537.36',
        'Content-Type': 'application/json',
        'access-token': token
    }
    data = {
        "items": [
            {
                "skus": [
                    {
                        "seatPlanId": seat_plan_id,  # 644fcf080f4f4e0001f1519d
                        "sessionId": session_id,  # 644fcb7dca916100017dda3d
                        "showId": show_id,  # 644fcb2aca916100017dcfef
                        "skuId": seat_plan_id,
                        "skuType": "SINGLE",
                        "ticketPrice": price,  # 388
                        "qty": qty,  # 2
                        "deliverMethod": "EXPRESS"
                    }
                ],
                "spu": {
                    "id": show_id,
                    "spuType": "SINGLE"
                }
            }
        ],
        "locationCityId": location_city_id  # 460102
    }
    url = "https://m.piaoxingqiu.com/cyy_gatewayapi/trade/buyer/order/v3/price_items"
    response = requests.post(url=url, headers=headers, json=data).json()
    if response["statusCode"] == 200:
        return response["data"][0]
    else:
        raise Exception("获取快递费异常: " + str(response))

# 获取当前时间戳并生成1000001的id
def generate_timestamp_id():
    # 获取当前时间的 datetime 对象
    now = datetime.datetime.now()
    # 转换为时间戳，毫秒为单位
    timestamp_ms = int(now.timestamp() * 1000)
    # 加上常数 10000001
    return timestamp_ms

# 提交订单（快递送票EXPRESS,电子票E_TICKET,现场取票VENUE,电子票或现场取票VENUE_E, 刷身份证ID_CARD）
def create_order(show_id, session_id, seat_plan_id, price: int, qty: int, deliver_method, express_fee: int, receiver,
                 cellphone,
                 address_id, detail_address, location_city_id, audience_ids: list):
    # headers = {
    #     'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Mobile Safari/537.36',
    #     'Content-Type': 'application/json',
    #     'access-token': 'eyJ0eXAiOiJKV1QiLCJjdHkiOiJKV1QiLCJ6aXAiOiJERUYiLCJhbGciOiJSUzUxMiJ9'
    # }
    headers = {
        "Accept": "*/*",
        "Accept-Language": "zh-HK,zh-TW;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6,zh-CN;q=0.5",
        "Angry-dog": "N2YxOWMzZjg4YWJlMDJjZDk0NWEzYzRjZTAwYzI3NzUyNDMzZWRiNjljNDhjNTQ4NjI2Yjc5Y2JmMWY4NjI0YTpkYTIwYTUxNTA4N2UzMjA2NTAyOWRkN2QxZGMyZTE4NDJjMTI2ZGFmM2Y5MWYxN2I1ZjkwYzdjOTM5ODJlMTFmMjEwZWQwY2NiM2M0YjMyY2E3MmI0MjBiYThiMWIyYmM4MzEwOGRiNTdjYzdlMTJlYTM2OThmMTMxNDEyY2VjODkzNTkwN2UzODU0OGRjOWNlZGY1YWMxYzk1YzMwYTcwM2VkOWQ3MGI4ZTQzNDU2NTA4MTUyZDBiOTFlYmRjMDE6MTc1MDI0NjgwODA0MQ",
        "Content-Type": "application/json",
        "Origin": "https://m.piaoxingqiu.com",
        "Referer": "https://m.piaoxingqiu.com/order/confirm?cpId=local_319b3a930eea4de6b6f71c95&whiteTagsSeatPlanIds=",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)...",
        "access-token": "eyJ0eXAiOiJKV1QiLCJjdHkiOiJKV1QiLCJ6aXAiOiJERUYiLCJhbGciOiJSUzUxMiJ9",
        "src": "WEB",
        "terminal-src": "WEB",
        "utc-offset": "480",
        "ver": "4.35.3",
    }

    if deliver_method == "EXPRESS":
        data = {
            "priceItemParam": [
                {
                    "applyTickets": [],
                    "priceItemName": "票款总额",
                    "priceItemVal": price * qty,
                    "priceItemType": "TICKET_FEE",
                    "priceItemSpecies": "SEAT_PLAN",
                    "direction": "INCREASE",
                    "priceDisplay": "￥" + str(price * qty)
                },
                {
                    "applyTickets": [],
                    "priceItemName": "快递费",
                    "priceItemVal": express_fee,
                    "priceItemId": show_id,
                    "priceItemSpecies": "SEAT_PLAN",
                    "priceItemType": "EXPRESS_FEE",
                    "direction": "INCREASE",
                    "priceDisplay": "￥" + str(express_fee)
                }
            ],
            "items": [
                {
                    "skus": [
                        {
                            "seatPlanId": seat_plan_id,
                            "sessionId": session_id,
                            "showId": show_id,
                            "skuId": seat_plan_id,
                            "skuType": "SINGLE",
                            "ticketPrice": price,
                            "qty": qty,
                            "deliverMethod": deliver_method
                        }
                    ],
                    "spu": {
                        "id": show_id,
                        "spuType": "SINGLE"
                    }
                }
            ],
            "contactParam": {
                "receiver": receiver,  # 张三
                "cellphone": cellphone  # 13812345678
            },

            "one2oneAudiences": [{"audienceId": i, "sessionId": session_id} for i in audience_ids],
            "addressParam": {
                "address": detail_address,
                "district": location_city_id[4:],
                "city": location_city_id[2:4],
                "province": location_city_id[0:2],
                "addressId": address_id
            }
        }
    elif deliver_method == "E_TICKET":
        # data = {
        #     "priceItemParam": [
        #         {
        #             "applyTickets": [],
        #             "priceItemName": "票款总额",
        #             "priceItemVal": price * qty,
        #             "priceItemType": "TICKET_FEE",
        #             "priceItemSpecies": "SEAT_PLAN",
        #             "direction": "INCREASE",
        #             "priceDisplay": "￥" + str(price * qty)
        #         }
        #     ],
        #     "items": [
        #         {
        #             "deliverMethod": deliver_method,
        #             "sku": [
        #                 {
        #                     # "seatPlanId": seat_plan_id,
        #                     # "sessionId": session_id,
        #                     # "showId": show_id,
        #                     "skuId": seat_plan_id,
        #                     "skuType": "SINGLE",
        #                     "ticketPrice": price,
        #                     "qty": qty,
        #                     # "deliverMethod": deliver_method,
        #                     "ticketItems": [
        #                         {
        #                             # "id": str(uuid.uuid4()),  # 或抓包里的 id，临时随机填
        #                             "id": '1750241734743100000003',
        #                             "audienceId": audience_id
        #                         }
        #                         for audience_id in audience_ids
        #                     ]
        #                 }
        #             ],
        #             "spu": {
        #                 "id": show_id,
        #                 "session_Id": session_id,
        #                 "spuType": "SINGLE",
        #                 "addPromoVersionHash": "EMPTY_PROMOTION_HASH",
        #                 "promotionVersionHash": "EMPTY_PROMOTION_HASH"
        #             }
        #         }
        #     ],
        #
        #     "locationParam":[
        #         {
        #          "locationCityId": "BL1173",
        #          "bsCityId": "BL1173"
        #          }],
        #     "many2OneAudience": {
        #     #     "audienceId": '67e6ac7b03a32d0001155cec',
        #     # # audience_ids[0]
        #     #     "sessionIds": [
        #     #         session_id
        #     #     ]
        #     },
        #     "orderSource": "COMMON",
        #     "paymentParam": [{
        #         "totalAmount": f"{price * qty:.2f}",
        #         "payAmount": f"{price * qty:.2f}"
        #     }],
        #     "priorityId":"",
        #     "scene":"",
        #     "sourceOrderId":""
        # }
        data = {
            "src": "WEB",
            "ver": "4.35.3",
            "addressParam": {},
            "locationParam": {
                "locationCityId": "BL1173",
                "bsCityId": "BL1173"
            },
            "paymentParam": {
                "totalAmount": f"{price * qty:.2f}",
                "payAmount": f"{price * qty:.2f}"
            },
            "priceItemParam": [
                {
                    "applyTickets": [],
                    "priceItemName": "票款总额",
                    "priceItemVal": price * qty,
                    "priceItemType": "TICKET_FEE",
                    "priceItemSpecies": "SEAT_PLAN",
                    "direction": "INCREASE",
                    "priceDisplay": "￥" + str(price * qty)
                }
            ],
            "items": [
                {
                    "sku": {
                        "skuId": seat_plan_id,
                        "skuType": "SINGLE",
                        "ticketPrice": price,
                        "qty": qty,
                        "ticketItems": [
                            {
                                "id": "1750246847613100000003",
                                "audienceId": audience_id,
                            }
                            for audience_id in audience_ids
                        ]
                    },
                    "spu": {
                        "showId": show_id,
                        "sessionId": session_id,
                        "promotionVersionHash": "EMPTY_PROMOTION_HASH",
                        "addPromoVersionHash": "EMPTY_PROMOTION_HASH"
                    },
                    "deliverMethod": "E_TICKET"
                }
            ],
            "priorityId": "",
            "sourceOrderId": "",
            "addPurchasePromotionId": "",
            "scene": "",
            "many2OneAudience": {},
            "orderSource": "COMMON"
        }
    elif deliver_method == "VENUE":
        data = {
            "priceItemParam": [
                {
                    "applyTickets": [],
                    "priceItemName": "票款总额",
                    "priceItemVal": price * qty,
                    "priceItemType": "TICKET_FEE",
                    "priceItemSpecies": "SEAT_PLAN",
                    "direction": "INCREASE",
                    "priceDisplay": "￥" + str(price * qty)
                }
            ],
            "items": [
                {
                    "skus": [
                        {
                            "seatPlanId": seat_plan_id,
                            "sessionId": session_id,
                            "showId": show_id,
                            "skuId": seat_plan_id,
                            "skuType": "SINGLE",
                            "ticketPrice": price,
                            "qty": qty,
                            "deliverMethod": deliver_method
                        }
                    ],
                    "spu": {
                        "id": show_id,
                        "spuType": "SINGLE"
                    }
                }
            ],
            "one2oneAudiences": [{"audienceId": i, "sessionId": session_id} for i in audience_ids]
        }
    elif deliver_method == "VENUE_E":
        data = {
            "priceItemParam": [
                {
                    "applyTickets": [],
                    "priceItemName": "票款总额",
                    "priceItemVal": price * qty,
                    "priceItemType": "TICKET_FEE",
                    "priceItemSpecies": "SEAT_PLAN",
                    "direction": "INCREASE",
                    "priceDisplay": "￥" + str(price * qty)
                }
            ],
            "items": [
                {
                    "skus": [
                        {
                            "seatPlanId": seat_plan_id,
                            "sessionId": session_id,
                            "showId": show_id,
                            "skuId": seat_plan_id,
                            "skuType": "SINGLE",
                            "ticketPrice": price,
                            "qty": qty,
                            "deliverMethod": deliver_method
                        }
                    ],
                    "spu": {
                        "id": show_id,
                        "spuType": "SINGLE"
                    }
                }
            ]
        }
    elif deliver_method == "ID_CARD":
        data = {
            "priceItemParam": [
                {
                    "applyTickets": [],
                    "priceItemName": "票款总额",
                    "priceItemVal": price * qty,
                    "priceItemType": "TICKET_FEE",
                    "priceItemSpecies": "SEAT_PLAN",
                    "direction": "INCREASE",
                    "priceDisplay": "￥" + str(price * qty)
                }
            ],
            "items": [
                {
                    "sku": [
                        {
                            "seatPlanId": seat_plan_id,
                            "showId": show_id,
                            "skuId": seat_plan_id,
                            "skuType": "SINGLE",
                            "ticketPrice": price,
                            "qty": qty,
                            "deliverMethod": deliver_method
                        }
                    ],
                    "spu": {
                        "id": show_id,
                        "sessionId": session_id,
                        "spuType": "SINGLE"
                    }
                }
            ],
            "one2oneAudiences": [{"audienceId": 0, "sessionId": session_id} for i in audience_ids]
        }
    else:
        raise Exception("不支持的deliver_method: " + str(deliver_method))
    # print(data)
    url = "https://m.piaoxingqiu.com/cyy_gatewayapi/trade/buyer/order/v5/create_order?lang=zh&terminalSrc=WEB&utcOffset=480&ver=4.35.3"
    # response = requests.post(url=url, headers=headers, json=data).json()
    response = requests.post(url = url, headers=headers, data=data)
    logging.info(response.json()['statusCode'])
    logging.info("已尝试下单")
    if response["statusCode"] == 200:
        logging.info("下单成功！请尽快支付！")
        if sckey:
            result = send_wechat_message("你的订单已成功创建，快去支付吧！")
            logging.info(result)  # 输出推送结果
    else:
        raise Exception("下单异常: " + str(response))