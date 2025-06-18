# 输入自己的token
token = 'eyJ0eXAiOiJKV1QiLCJjdHkiOiJKV1QiLCJ6aXAiOiJERUYiLCJhbGciOiJSUzUxMiJ9'
# 5865fa613ed5673f9c3a6419
# 项目id，必填
show_id = '68401819b7ce8000011e2df7'
# 68401819b7ce8000011e2df7    dys
# 681dbf710700d50001c877e1    fhcq
# 指定场次id，不指定则默认从第一场开始遍历
session_id = ''
# 684018422f092f00019ea136
# 购票数量，一定要看购票须知，不要超过    上限
buy_count = 1
# 指定观演人，观演人序号从0开始，人数需与票数保持一致
audience_idx = [0]

# 门票类型，不确定则可以不填，让系统自行判断。快递送票:EXPRESS,电子票:E_TICKET,现场取票:VENUE,电子票或现场取票:VENUE_E,目前只发现这四种，如有新发现可补充
# 新增,刷身份证: ID_CARD
deliver_method = 'E_TICKET'

# Server酱SCKEY
sckey = 'SCT266238TA-xALFKZRZyPQ8pkai4CW8B9cJ'