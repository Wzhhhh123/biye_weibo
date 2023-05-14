import json
from pyecharts import options as opts
from pyecharts.charts import Sankey
from mysql_util import MysqlUtil
def sankey(title):


    sql_3 = f'SELECT * FROM weiboforword where title="{title}"'
    db = MysqlUtil()
    count_number = db.fetchall(sql_3)

    kk=[]
    # 数据库方式
    for row in count_number:
        kk.append(row["source"])
        kk.append(row["target"])
    kk = list(set(kk))
    import json

    # 数据库
    jsontext = {"nodes":[],"links":[]}
    for row in kk:
        jsontext["nodes"].append({"name":row})
    for row in count_number:
        if row['source'] in row['target']:
            continue
        jsontext["links"].append({"source":row["source"],"target":row["target"],"value":row["value"]})
    jsontext=json.dumps(jsontext)
    file = open(title+'.json', 'w')
    file.write(jsontext)
    file.close()

    with open(title+'.json', "r", encoding="utf-8") as f:
        j = json.load(f)

    c = (
        Sankey(
            init_opts=opts.InitOpts(width="1600px", height="800px")

        )
        .add(
            "转发关系",
            nodes=j["nodes"],
            links=j["links"],
            pos_top="10%",

            levels=[
                opts.SankeyLevelsOpts(
                    depth=0,
                    itemstyle_opts=opts.ItemStyleOpts(color="#fbb4ae"),
                    linestyle_opts=opts.LineStyleOpts(color="source", opacity=0.6),
                ),
                opts.SankeyLevelsOpts(
                    depth=1,
                    itemstyle_opts=opts.ItemStyleOpts(color="#b3cde3"),
                    linestyle_opts=opts.LineStyleOpts(color="source", opacity=0.6),
                ),
                opts.SankeyLevelsOpts(
                    depth=2,
                    itemstyle_opts=opts.ItemStyleOpts(color="#ccebc5"),
                    linestyle_opts=opts.LineStyleOpts(color="source", opacity=0.6),
                ),
                opts.SankeyLevelsOpts(
                    depth=3,
                    itemstyle_opts=opts.ItemStyleOpts(color="#decbe4"),
                    linestyle_opts=opts.LineStyleOpts(color="source", opacity=0.6),
                ),
            ],

            linestyle_opt=opts.LineStyleOpts(curve=0.5),
            label_opts=opts.LabelOpts(position="right"),
            focus_node_mode="adjacency",


        )
        .set_global_opts(

            title_opts=opts.TitleOpts(title="桑基关系图"),
            tooltip_opts=opts.TooltipOpts(trigger="item", trigger_on="mousemove"),

        )

    )

    return c
