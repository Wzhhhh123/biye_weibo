from pyecharts import options as opts
from pyecharts.charts import Radar


def radar(count_number):
    number_list=[]
    data_list=[]
    c_schema = []
    for i in range(len(count_number)):
        if count_number[i]['zhong'] != None and count_number[i]['zhong'] != "":
            number_list.append(count_number[i]['zhong'])
            data_list.append(count_number[i]['t'])
    for i in range(len(number_list)):
        a = {"name": number_list[i], "max": 10, "min": 0}
        c_schema.append(a)
    data = [{"value": data_list, "name": "微博热搜种类画像"}]
    sss=zip(number_list,data_list)
    global ppp
    kk=dict(sss)
    entity_dict_1 = sorted(kk.items(), key=lambda x: x[1])
    ppp="今天类型最多的是"+entity_dict_1[-1][0]+"所以可见今天人们更倾向于讨论"+entity_dict_1[-1][0]
    c = (
        Radar()
        .set_colors(["#4587E7"])
        .add_schema(
            schema=c_schema,
            shape="circle",
            center=["50%", "50%"],
            radius="80%",
            angleaxis_opts=opts.AngleAxisOpts(
                min_=0,
                max_=360,
                is_clockwise=False,
                interval=5,
                axistick_opts=opts.AxisTickOpts(is_show=False),
                axislabel_opts=opts.LabelOpts(is_show=False),
                axisline_opts=opts.AxisLineOpts(is_show=False),
                splitline_opts=opts.SplitLineOpts(is_show=False),
            ),
            radiusaxis_opts=opts.RadiusAxisOpts(
                min_=0,
                max_=10,
                interval=2,
                splitarea_opts=opts.SplitAreaOpts(
                    is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
                ),
            ),
            polar_opts=opts.PolarOpts(),
            splitarea_opt=opts.SplitAreaOpts(is_show=False),
            splitline_opt=opts.SplitLineOpts(is_show=False),
        )
        .add(
            series_name="种类画像",
            data=data,

            areastyle_opts=opts.AreaStyleOpts(opacity=0.3 ),
            linestyle_opts=opts.LineStyleOpts(width=2),
        )

    )
    return c
