"""将 QQ 导出的 mht 文件转为 HTML文件"""

import os
from pathlib import Path
import re
from typing import List
from bs4 import BeautifulSoup

# 本人使用的昵称
MY_NICKNAME = ["dank", "木槿花"]


class QQMHTParse:
    def __init__(self, path: str) -> None:
        self.path = path
        self.__file = None
        self.bounder = None
        self.msg = []
        self.img = {}
        self.__re_compile = None
        self.role = ""

    def __enter__(self):
        # TODO
        pass

    def __exit__(self):
        # TODO
        pass

    def parse(self):
        self.__file = open(self.path, "r", encoding="utf-8")
        self.__parse_head()
        self.__parse_message()
        self.__parse_image()
        self.__deal_msg()
        self.__file.close()

    def __parse_head(self):
        line = self.__file.readline()

        while line:
            if "boundary=" in line:
                self.bounder = line.split('"')[1]
                self.__re_compile = re.compile(self.bounder)
                break
            line = self.__file.readline()

    def __parse_message(self):
        """
        msg-time: YY-MM-DD hh:mm:ss
        msg-content: "abscasx, {XX.dat}, as"

        Retrun: [msg]
        """
        start_part = False

        line = self.__file.readline()
        while line:
            line = line.strip()
            if not len(line):
                line = self.__file.readline()
                continue
            if start_part:
                if self.__re_compile.search(line):
                    break
                elif not line.startswith("Content"):
                    self.msg.append(line)
            elif not start_part and self.__re_compile.search(line):
                start_part = True

            line = self.__file.readline()

    def __parse_image(self):
        """
        img: {xx.dat}
        content: [XSSXS, SXSXS, ...]
        """
        file_name = ""
        img_code = []
        line = self.__file.readline()
        while line:
            line = line.strip()
            if not len(line):
                line = self.__file.readline()
                continue
            if line.startswith("Content-Location"):
                file_name = line.split(":")[1]
            elif line.startswith("Content-Type"):
                file_type = line.split(":")[1]
            elif self.__re_compile.search(line):
                # img part end
                self.img[file_name] = {"file_type": file_type, "file_code": img_code[:]}

                file_name = ""
                img_code.clear()
            elif file_name:
                img_code.append(line)
            line = self.__file.readline()

    def __deal_msg(self):
        """处理消息记录，将提取每一条消息

        "{time}" :
        {
            {"type":"text", "ctx":""}
            {"type":"img", "ctx":"{img_name}"}
        }
        """
        soup = BeautifulSoup("".join(self.msg), features="html.parser")
        self.msg.clear()
        data = ""
        cnt = 1
        for tr in soup.table:
            # 每一个td是一条消息 包括 发送人 时间 内容
            if cnt <= 4:
                if cnt == 3:
                    # if tr.td.text.startswith("消息对象:"):
                    # 第三行解析消息对象
                    self.role = tr.td.text.split(":")[1]
                cnt = cnt + 1
                continue

            for td in tr:
                div_time = td.div

                if not div_time:
                    # 没有子项，为日期栏
                    data = td.get_text().split(":")[1].strip()
                    # 可加入分界线
                    continue
                # 消息: [角色-时间, 内容]
                divs = [div for div in td]
                role_and_time = divs[0].get_text("_").split("_")
                
                if len(role_and_time) == 1:
                    role = "系统消息"
                    time = role_and_time[0]
                else:
                    role = role_and_time[0]
                    time = role_and_time[1]
                if role in MY_NICKNAME:
                    role = "抽穗的芒草"
                elif role.startswith("系统消息") or not role:
                    pass
                else:
                    role = self.role
                # time时间补齐2位
                time_list = time.split(":")
                for index in range(0, len(time_list)):
                    if len(time_list[index]) < 2:
                        time_list[index] = "0" + time_list[index]
                time = ":".join(time_list)
                # 时间戳做消息key去重 YY-MM-DD hh:mm:ss
                msg_key = "{} {} {}".format(role, data, time)
                msg_list = []
                # 此时间发送的消息 包括文字 图片
                for ctx in divs[1]:
                    if ctx.name == "img":
                        img_src = ctx["src"]
                        img_code = {
                            "file_type":"image/png",
                            "file_code":""
                        }
                        if img_src in self.img:
                            img_code = self.img[img_src]

                        msg_list.append(
                            {
                                "type": img_code["file_type"],
                                "ctx": img_code["file_code"],
                            }
                        )
                    else:
                        msg_list.append({"type": "text", "ctx": ctx.get_text()})
                self.msg.append({"msg_key": msg_key, "msg_ctx": msg_list})


def dedupe(items, key=None):
    """Eliminate duplicate elements and keep order

    Args:
        items (iterable)
        key (function, optional): Convert sequence elements to hashable type. Defaults to None.

    Yields:
        _type_: sequence item
    """
    seen = set()
    for item in items:
        val = item if key is None else key(item)
        if val not in seen:
            yield item
            seen.add(val)


class QQMHT2HTML:
    def __init__(self, path: str) -> None:
        self.path = path
        self._html = ""
        self.__parse_result: List[QQMHTParse] = []
        self.role = ""
        self.role_id = ""
        self.__msg = []

    def dump(self, path: str):
        with open(path, "w", encoding="utf-8") as f:
            f.write(self._html)

    def __parse_mht(self):
        is_file = os.path.isfile(self.path)
        if is_file:
            files = [self.path]
        else:
            files = [file for file in os.listdir(self.path) if file.endswith(".mht")]
        role_info = Path(files[0]).name.split("(")
        self.role = role_info[0]
        self.role_id = role_info[1].split(")")[0]
        for file in files:
            if is_file:
                qq_parse = QQMHTParse(self.path)
            else:
                qq_parse = QQMHTParse(os.path.join(self.path, file))
            qq_parse.parse()
            self.__parse_result.append(qq_parse)

    def __merge_mht_parse(self):
        msg_list = []
        for data in self.__parse_result:
            msg_list.extend(data.msg)
        
        self.__msg.extend(list(dedupe(msg_list, lambda x: x["msg_key"])))

    def to_html(self):
        self.__parse_mht()
        self.__merge_mht_parse()
        html_temp = """
        <html>
        <head>
            <title></title>
            <style type="text/css">
                body {
                    font-size: 14px;
                    line-height: 22px;
                    margin: 2px;
                }
                td {
                    font-size: 14px;
                    line-height: 22px;
                }
            </style>
        </head>
        <body>
            <table width=100% cellspacing=0>
                <tr>
                    <td>
                        <div style=padding-left:10px;><br><b></b></div>
                    </td>
                </tr>
                <tr>
                    <td>
                        <div style=padding-left:10px;>&nbsp;</div>
                    </td>
                </tr>
            </table>
        </body>
        </html>
        """
        role_info = "{} ({})".format(self.role, self.role_id)
        date_flg = ""
        soup = BeautifulSoup(html_temp, "html.parser")
        soup.title.string = role_info
        table = soup.table

        base_info = table.tr.td.div.b
        base_info.string = "消息对象:" + role_info
        base_info["style"] = "font-size: 18px;"

        for msg in self.__msg:
            msg_name = msg["msg_key"]
            msg_ctx = msg["msg_ctx"]
            # 加横线区分日期
            date = msg_name.split(" ")[1]
            if date != date_flg:
                tr = soup.new_tag("tr")
                td = soup.new_tag("td")
                td.string = date
                td.attrs[
                    "style"
                ] = "border-bottom-width:2px;border-bottom-color:#8EC3EB;border-bottom-style:solid;color:#3568BB;font-weight:bold;font-size:16px;height:24px;line-height:24px;padding-left:10px;margin-bottom:5px;"
                tr.append(td)
                table.append(tr)
                date_flg = date

            tr = soup.new_tag("tr")
            td = soup.new_tag("td")

            # 消息发送人和时间
            div_msg_name = soup.new_tag("div")
            div_msg_name.string = msg_name
            if msg_name.startswith(self.role):
                div_msg_name.attrs["style"] = "color:#006EFE;padding-left:10px;"
            elif msg_name.startswith("抽穗的芒草"):
                div_msg_name.attrs["style"] = "color:#42B475;padding-left:10px;"
            elif msg_name.startswith("系统消息"):
                div_msg_name.attrs["style"] = "color:#FFA500;padding-left:10px;"
            else:
                raise ValueError("角色错误")

            # 消息内容
            div_msg_ctx = soup.new_tag("div")
            div_msg_ctx.attrs["style"] = "padding-left:20px;"
            for ctx in msg_ctx:
                type_ctx = ctx["type"]
                ctx_line = ctx["ctx"]
                if type_ctx.startswith("image"):
                    img = soup.new_tag("img")
                    img.attrs["src"] = "data:{};base64,{}".format(type_ctx, "".join(ctx_line))
                    div_msg_ctx.append(img)
                elif type_ctx.startswith("text"):
                    txt = soup.new_tag("font")
                    txt.string = ctx_line
                    div_msg_ctx.append(ctx_line)
                else:
                    raise ValueError("消息内容格式错误")
            td.append(div_msg_name)
            td.append(div_msg_ctx)
            tr.append(td)
            table.append(tr)
        self._html = str(soup)
        return self._html


def run():
    root = "QQMSG"
    mht2html = QQMHT2HTML(root)
    mht2html.to_html()
    mht2html.dump("{} ({}).html".format(mht2html.role, mht2html.role_id))


if __name__ == "__main__":
    run()
