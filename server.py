# coding: UTF-8
import sys
l11111ll_opy_ = sys.version_info [0] == 2
l1l1ll11_opy_ = 2048
l111lll1_opy_ = 7
def l11ll_opy_ (l11111_opy_):
    global l1l1llll_opy_
    l1l111ll_opy_ = ord (l11111_opy_ [-1])
    l1111l1l_opy_ = l11111_opy_ [:-1]
    l1llll11_opy_ = l1l111ll_opy_ % len (l1111l1l_opy_)
    l1ll1ll_opy_ = l1111l1l_opy_ [:l1llll11_opy_] + l1111l1l_opy_ [l1llll11_opy_:]
    if l11111ll_opy_:
        l1ll11_opy_ = unicode () .join ([unichr (ord (char) - l1l1ll11_opy_ - (l1l11_opy_ + l1l111ll_opy_) % l111lll1_opy_) for l1l11_opy_, char in enumerate (l1ll1ll_opy_)])
    else:
        l1ll11_opy_ = str () .join ([chr (ord (char) - l1l1ll11_opy_ - (l1l11_opy_ + l1l111ll_opy_) % l111lll1_opy_) for l1l11_opy_, char in enumerate (l1ll1ll_opy_)])
    return eval (l1ll11_opy_)
import web
import psycopg2
import urllib2
from PIL import Image
import io
import os
import json
import geojson
from PIL import ImageDraw
from shapely import wkb
# l1l1l111l_opy_ l11lll1ll_opy_ l11ll1lll_opy_
l1l1l11ll_opy_ = (
    l11ll_opy_ (u"࠭࠯ࡴࡶࡤࡸ࡮ࡹࡴࡪࡥࡶ࠳࠭࠴ࠪࠪࠩࡲ"), l11ll_opy_ (u"ࠧࡴࡶࡤࡸ࡮ࡹࡴࡪࡥࡶࠫࡳ"),
    l11ll_opy_ (u"ࠨ࠱ࡧ࡭ࡸࡶ࡬ࡢࡻ࠲ࠬ࠳࠰ࠩࠨࡴ"), l11ll_opy_ (u"ࠩࡧ࡭ࡸࡶ࡬ࡢࡻࠪࡵ"),
    l11ll_opy_ (u"ࠪ࠳࡫࡯࡮ࡥࠩࡶ"), l11ll_opy_ (u"ࠫ࡫࡯࡮ࡥࠩࡷ")
)
# l1ll1111l_opy_ cursor (l1ll1l11l_opy_ l11llllll_opy_)
cur = False
# l1ll111l1_opy_ the absolute path name
l1l1lll11_opy_ = os.path.dirname(__file__)
class display:
    def GET(self, id):
        data = web.input()
        web.header(l11ll_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡔࡺࡲࡨࠫࡸ"), l11ll_opy_ (u"࠭ࡩ࡮ࡣࡪࡩ࠴ࡰࡰࡦࡩࠪࡹ"))
        image = l1l1ll1ll_opy_(id)
        if image is not False:
            if l11ll_opy_ (u"ࠢࡰࡸࡨࡶࡱࡧࡹࠣࡺ") in data and data[l11ll_opy_ (u"ࠣࡱࡹࡩࡷࡲࡡࡺࠤࡻ")] == l11ll_opy_ (u"ࠤࡼࡩࡸࠨࡼ"):
                l1ll11l11_opy_(l11ll_opy_ (u"ࠥࡗࡊࡒࡅࡄࡖࠣࡴࡦࡸࡣࡦ࡮ࡢ࡫ࡪࡵࠬࠡࡤࡸ࡭ࡱࡪࡩ࡯ࡩࡢ࡫ࡪࡵࠬࠡ࡫ࡰࡥ࡬࡫࡟ࡣࡱࡸࡲࡩࡹࠠࡇࡔࡒࡑࠥࡶࡲࡰࡲࡨࡶࡹ࡯ࡥࡴ࡚ࠢࡌࡊࡘࡅࠡ࡫ࡧࠤࡂࠦࠥࡴࠤࡽ"), [id])
                row = cur.fetchone()
                l1ll1l111_opy_ = l11ll_opy_ (u"ࠦࡴࡸࡡ࡯ࡩࡨࠦࡾ")
                l11lll11l_opy_ = l11ll_opy_ (u"ࠧ࡭ࡲࡦࡧࡱࠦࡿ")
                if l11ll_opy_ (u"ࠨࡰࡢࡴࡦࡩࡱࠨࢀ") in data:
                    l1ll1l111_opy_ = data[l11ll_opy_ (u"ࠢࡱࡣࡵࡧࡪࡲࠢࢁ")]
                if l11ll_opy_ (u"ࠣࡤࡸ࡭ࡱࡪࡩ࡯ࡩࠥࢂ") in data:
                    l11lll11l_opy_ = data[l11ll_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡪࡰࡪࠦࢃ")]
                geom = wkb.loads(row[0], hex=True)
                l1ll1llll_opy_ = l1l11l1ll_opy_(image, row[2], geom, l1ll1l111_opy_)
                geom = wkb.loads(row[1], hex=True)
                l1ll1llll_opy_ = l1l11l1ll_opy_(l1ll1llll_opy_, row[2], geom, l11lll11l_opy_)
                return l1ll1llll_opy_.getvalue()
            return image
        return l1l11l11l_opy_()
class find:
    def POST(self):
        data = geojson.loads(web.data())
        web.header(l11ll_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱࡙ࡿࡰࡦࠩࢄ"), l11ll_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧࢅ"))
        web.header(l11ll_opy_ (u"ࠬࡇࡣࡤࡧࡶࡷ࠲ࡉ࡯࡯ࡶࡵࡳࡱ࠳ࡁ࡭࡮ࡲࡻ࠲ࡕࡲࡪࡩ࡬ࡲࠬࢆ"),l11ll_opy_ (u"࠭ࠪࠨࢇ"))
        web.header(l11ll_opy_ (u"ࠧࡂࡥࡦࡩࡸࡹ࠭ࡄࡱࡱࡸࡷࡵ࡬࠮ࡃ࡯ࡰࡴࡽ࠭ࡎࡧࡷ࡬ࡴࡪࡳࠨ࢈"), l11ll_opy_ (u"ࠨࡒࡒࡗ࡙࠭ࢉ"))
        l1ll11l11_opy_(l11ll_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡗࡊࡒࡅࡄࡖࠣ࡭ࡩ࠲ࠠࡔࡖࡢ࡜࠭࡭ࡥࡰࡥࡲࡨࡪࡥࡧࡦࡱ࠽࠾࡬࡫࡯࡮ࡧࡷࡶࡾ࠯ࠠࡂࡕࠣࡰࡴࡴࡧࡪࡶࡸࡨࡪ࠲ࠠࡔࡖࡢ࡝࠭࡭ࡥࡰࡥࡲࡨࡪࡥࡧࡦࡱ࠽࠾࡬࡫࡯࡮ࡧࡷࡶࡾ࠯ࠠࡂࡕࠣࡰࡦࡺࡩࡵࡷࡧࡩࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡊࡗࡕࡍࠡࡲࡵࡳࡵ࡫ࡲࡵ࡫ࡨࡷࠏࠦࠠࠡࠢࠣࠤ࡛ࠥࠦࠠࠡࠢࠣࡍࡋࡒࡆࠢࡖࡘࡤࡊࡩࡴࡶࡤࡲࡨ࡫࡟ࡔࡲ࡫ࡩࡷ࡫ࠨࡨࡧࡲࡧࡴࡪࡥࡠࡩࡨࡳ࠿ࡀࡧࡦࡱࡰࡩࡹࡸࡹ࠭ࠢࡖࡘࡤࡓࡡ࡬ࡧࡓࡳ࡮ࡴࡴࠩࠧࡶ࠰ࠥࠫࡳࠪࠫࠣࡀࡂࠦࠥࡴࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥࢊ"),
                 [data.geometry.coordinates[0], data.geometry.coordinates[1], data[l11ll_opy_ (u"ࠥࡼ࠲ࡪࡩࡴࡶࡤࡲࡨ࡫ࠢࢋ")]])
        return json.dumps([{l11ll_opy_ (u"ࠫࡵࡸ࡯ࡱࡧࡵࡸࡾࡏࡤࠨࢌ"):row[0],l11ll_opy_ (u"ࠬࡩ࡯ࡰࡴࡧ࡭ࡳࡧࡴࡦࡵࠪࢍ"):[row[1],row[2]]} for row in cur.fetchall()])
class statistics:
    def GET(self, id):
        data = web.input()
        distance = 0
        if l11ll_opy_ (u"ࠨࡤࡪࡵࡷࡥࡳࡩࡥࠣࢎ") in data and int(data[l11ll_opy_ (u"ࠢࡥ࡫ࡶࡸࡦࡴࡣࡦࠤ࢏")]) > 0:
            distance = data[l11ll_opy_ (u"ࠣࡦ࡬ࡷࡹࡧ࡮ࡤࡧࠥ࢐")]
        l1ll11l11_opy_(l11ll_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡗࡊࡒࡅࡄࡖࠣࡗ࡚ࡓࠨࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡕࡗࡣࡆࡸࡥࡢࠪࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࡙ࠥࡔࡠࡋࡱࡸࡪࡸࡳࡦࡥࡷ࡭ࡴࡴࠨࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡶࡡࡳࡥࡨࡰࡤ࡭ࡥࡰ࠮ࠣࡗ࡙ࡥࡂࡶࡨࡩࡩࡷ࠮ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠬࡘࡋࡌࡆࡅࡗࠤ࡬࡫࡯ࡤࡱࡧࡩࡤ࡭ࡥࡰࠢࡉࡖࡔࡓࠠࡱࡴࡲࡴࡪࡸࡴࡪࡧࡶࠤ࡜ࡎࡅࡓࡇࠣ࡭ࡩࠦ࠽ࠡࠧࡶ࠭࠱ࠦࠥࡴࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠩࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠭ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠯ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠯ࠠࡇࡔࡒࡑࠥࡶࡲࡰࡲࡨࡶࡹ࡯ࡥࡴ࠽ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦ࢑"),
                 [id, distance])
        l1l1ll1l1_opy_ = cur.fetchone()[0]
        l1ll11l11_opy_(l11ll_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡘࡋࡌࡆࡅࡗࠤࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࡙ࠥࡔࡠࡃࡵࡩࡦ࠮ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡖࡘࡤࡏ࡮ࡵࡧࡵࡷࡪࡩࡴࡪࡱࡱࠬࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡥࡹ࡮ࡲࡤࡪࡰࡪࡣ࡬࡫࡯࠭ࠢࡖࡘࡤࡈࡵࡧࡨࡨࡶ࠭ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠫࡗࡊࡒࡅࡄࡖࠣ࡫ࡪࡵࡣࡰࡦࡨࡣ࡬࡫࡯ࠡࡈࡕࡓࡒࠦࡰࡳࡱࡳࡩࡷࡺࡩࡦࡵ࡛ࠣࡍࡋࡒࡆࠢ࡬ࡨࠥࡃࠠࠦࡵࠬ࠰ࠥࠫࡳࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠯ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠬࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠮ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡋࡘࡏࡎࠢࡳࡶࡴࡶࡥࡳࡶ࡬ࡩࡸࡁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣ࢒"),
                 [id, distance])
        l1l1ll11l_opy_ = [row[0] for row in cur.fetchall()]
        l1ll11l11_opy_(l11ll_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࡙ࠥࡅࡍࡇࡆࡘࠥࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡓࡕࡡࡇ࡭ࡸࡺࡡ࡯ࡥࡨࠬࡧࡻࡩ࡭ࡦ࡬ࡲ࡬ࡥࡧࡦࡱ࠯ࠤ࡙࠭ࡅࡍࡇࡆࡘࠥ࡭ࡥࡰࡥࡲࡨࡪࡥࡧࡦࡱࠣࡊࡗࡕࡍࠡࡲࡵࡳࡵ࡫ࡲࡵ࡫ࡨࡷࠥ࡝ࡈࡆࡔࡈࠤ࡮ࡪࠠ࠾ࠢࠨࡷ࠮࠯ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡌࡒࡐࡏࠣࡴࡷࡵࡰࡦࡴࡷ࡭ࡪࡹ࠻ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤ࢓"),
                 [id])
        l1l11ll1l_opy_ = [row[0] for row in cur.fetchall()]
        l1ll11l11_opy_(l11ll_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡗࡊࡖࡋࠤࡽࠦࡁࡔࠢࠫࡗࡊࡒࡅࡄࡖࠣ࡫ࡪࡵࡣࡰࡦࡨࡣ࡬࡫࡯ࠡࡈࡕࡓࡒࠦࡰࡳࡱࡳࡩࡷࡺࡩࡦࡵ࡛ࠣࡍࡋࡒࡆࠢ࡬ࡨࠥࡃࠠࠦࡵࠬࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡖࡉࡑࡋࡃࡕࠢࠫࡗ࡚ࡓࠨࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡕࡗࡣࡆࡸࡥࡢࠪࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࡙ࠥࡔࡠࡋࡱࡸࡪࡸࡳࡦࡥࡷ࡭ࡴࡴࠨࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡨࡵࡪ࡮ࡧ࡭ࡳ࡭࡟ࡨࡧࡲ࠰࡙ࠥࡔࡠࡄࡸࡪ࡫࡫ࡲࠩࠪࡖࡉࡑࡋࡃࡕࠢࡪࡩࡴࡩ࡯ࡥࡧࡢ࡫ࡪࡵࠠࡇࡔࡒࡑࠥࡾࠩ࠭ࠢࠨࡷࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠬࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠩࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠫࠣ࠳࡙ࠥࡔࡠࡃࡵࡩࡦ࠮ࡓࡕࡡࡅࡹ࡫࡬ࡥࡳࠪࠫࡗࡊࡒࡅࡄࡖࠣ࡫ࡪࡵࡣࡰࡦࡨࡣ࡬࡫࡯ࠡࡈࡕࡓࡒࠦࡸࠪ࠮ࠣࠩࡸ࠯ࠩࠪࠢ࠭ࠤ࠶࠶࠰ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠩࠡࡈࡕࡓࡒࠦࡰࡳࡱࡳࡩࡷࡺࡩࡦࡵ࠾ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧ࢔"),
                 [id, distance, distance])
        l1l111ll1_opy_ = [row[0] for row in cur.fetchall()]
        return json.dumps({
            l11ll_opy_ (u"ࠨࡰࡢࡴࡦࡩࡱࡇࡲࡦࡣࠥ࢕"): l1l1ll1l1_opy_,
            l11ll_opy_ (u"ࠢࡣࡷ࡬ࡰࡩ࡯࡮ࡨࡃࡵࡩࡦࡹࠢ࢖"): l1l1ll11l_opy_,
            l11ll_opy_ (u"ࠣࡤࡸࡰࡩ࡯࡮ࡨࡆ࡬ࡷࡹࡧ࡮ࡤࡧࡶࠦࢗ"): l1l11ll1l_opy_,
            l11ll_opy_ (u"ࠤࡽࡳࡳ࡫࡟ࡥࡧࡱࡷ࡮ࡺࡹࠣ࢘"): l1l111ll1_opy_
        })
# l1l1l1lll_opy_ a l1l11llll_opy_ (u"ࠪࡷࠥࡩ࡯ࡰࡴࡧ࡭ࡳࡧࡴࡦࡵࠣࡳࡳࠦࡴࡰࡲࠣࡳ࡫ࠦࡡ࡯ࠢ࡬ࡱࡦ࡭ࡥࠡࡩ࡬ࡺࡪࡴࠠࡪࡶ࢙ࠪ")s l1l11ll11_opy_ l1l1llll1_opy_ and with the l1ll11lll_opy_ color
def l1l11l1ll_opy_(image, l11llll11_opy_, geom, color):
    l1ll111ll_opy_ = Image.open(image)
    l11lllll1_opy_ = l1ll111ll_opy_.size[0] / (l11llll11_opy_[2] - l11llll11_opy_[0])
    l11llll1l_opy_ = l1ll111ll_opy_.size[1] / (l11llll11_opy_[3] - l11llll11_opy_[1])
    x = []
    for l1l1lllll_opy_ in geom.exterior.xy[0]:
        x.append((l1l1lllll_opy_ - l11llll11_opy_[0]) * l11lllll1_opy_)
    y = []
    for l1ll11111_opy_ in geom.exterior.xy[1]:
        y.append((l11llll11_opy_[3] - l1ll11111_opy_) * l11llll1l_opy_)
    l1ll1l1ll_opy_ = l1ll111ll_opy_.copy()
    draw = ImageDraw.Draw(l1ll1l1ll_opy_)
    draw.polygon(zip(x, y), fill=color)
    l1ll1l1l1_opy_ = Image.blend(l1ll111ll_opy_, l1ll1l1ll_opy_, 0.5)
    l1l1111ll_opy_ = io.BytesIO()
    l1ll1l1l1_opy_.save(l1l1111ll_opy_, format=l11ll_opy_ (u"ࠫࡏࡖࡅࡈ࢚ࠩ"))
    return l1l1111ll_opy_
# l1l1l1ll1_opy_ and l11ll1ll1_opy_ image from l1l11111l_opy_
def l1l1ll1ll_opy_(id):
    l1ll11l11_opy_(l11ll_opy_ (u"ࠧࠨࠢࡔࡇࡏࡉࡈ࡚ࠠࡪ࡯ࡤ࡫ࡪࡥࡵࡳ࡮ࠣࡊࡗࡕࡍࠡࡲࡵࡳࡵ࡫ࡲࡵ࡫ࡨࡷࠥ࡝ࡈࡆࡔࡈࠤ࡮ࡪࠠ࠾ࠢࠨࡷࠧࠨ࢛ࠢ"), [id])
    l11lll1l1_opy_ = cur.fetchone()
    if l11lll1l1_opy_ is not None:
        l1l11l1l1_opy_ = l11ll_opy_ (u"ࠨࡳࡵࡱࡵࡥ࡬࡫࠯ࡤࡣࡦ࡬ࡪ࠵ࡩ࡮ࡣࡪࡩࡸ࠵ࠢ࢜") + id
        l1l111l11_opy_ = os.path.join(l1l1lll11_opy_, l1l11l1l1_opy_)
        if os.path.exists(l1l111l11_opy_):
            l1l111lll_opy_ = open(l1l111l11_opy_, l11ll_opy_ (u"ࠢࡳࠤ࢝"))
            return l1l111lll_opy_
        l11lll1l1_opy_ = l11lll1l1_opy_[0]
        l1l1l1l11_opy_ = urllib2.urlopen(l11lll1l1_opy_)
        if l1l1l1l11_opy_.getcode() == 200:
            l1l1ll111_opy_ = l1l1l1l11_opy_.read()
            l1l11lll1_opy_ = io.BytesIO(l1l1ll111_opy_)
            l1ll1lll1_opy_ = io.BytesIO()
            l1l1l11l1_opy_ = Image.open(l1l11lll1_opy_)
            l1l1l11l1_opy_.save(l1ll1lll1_opy_, format=l11ll_opy_ (u"ࠨࡌࡓࡉࡌ࠭࢞"))
            l1l11l1l1_opy_ = l11ll_opy_ (u"ࠤࡶࡸࡴࡸࡡࡨࡧ࠲ࡧࡦࡩࡨࡦ࠱࡬ࡱࡦ࡭ࡥࡴ࠱ࠥ࢟") + id
            l1l111l11_opy_ = os.path.join(l1l1lll11_opy_, l1l11l1l1_opy_)
            l1l111lll_opy_ = open(l1l111l11_opy_, l11ll_opy_ (u"ࠥࡻࠧࢠ"))
            l1l111lll_opy_.write(l1ll1lll1_opy_.getvalue())
            l1l111lll_opy_.close()
            return l1ll1lll1_opy_
    return False
# l1l111111_opy_ method for running l11lll111_opy_ (l1l111l1l_opy_: add exception l1l1111l1_opy_)
def l1ll11l11_opy_(sql, args):
    return l1ll1ll1l_opy_().execute(sql, args);
# l1ll11ll1_opy_ load database connection
def l1ll1ll1l_opy_():
    global cur
    if not cur:
        conn = psycopg2.connect(host=l11ll_opy_ (u"ࠦࡵࡵࡳࡵࡩࡵࡩࡸࡷ࡬ࠣࢡ"), port=l11ll_opy_ (u"ࠧ࠻࠴࠴࠴ࠥࢢ"), database=l11ll_opy_ (u"ࠨࡺࡦࡵࡷࡽࠧࢣ"), user=l11ll_opy_ (u"ࠢࡱࡱࡶࡸ࡬ࡸࡥࡴࠤࢤ"),
                                password=l11ll_opy_ (u"ࠣࡧࡱ࡫࡮ࡴࡥࡕࡧࡶࡸ࠽࠾࠸ࠣࢥ"))
        cur = conn.cursor()
    return cur
# l1l1l1ll1_opy_ and l1l1lll1l_opy_ the 404 image from l1l1l1111_opy_ (l1l111l1l_opy_: l1l1l1l1l_opy_ as redirect l1l11l111_opy_)
def l1l11l11l_opy_():
    l1l11l1l1_opy_ = l11ll_opy_ (u"ࠤࡶࡸࡴࡸࡡࡨࡧ࠲ࡲࡴࡺ࠭ࡧࡱࡸࡲࡩ࠴ࡪࡱࡩࠥࢦ")
    l1l111l11_opy_ = os.path.join(l1l1lll11_opy_, l1l11l1l1_opy_)
    fp = open(l1l111l11_opy_, l11ll_opy_ (u"ࠪࡶ࠰࠭ࢧ"));
    return fp
# l1ll11l1l_opy_ the l11lll1ll_opy_
if __name__ == l11ll_opy_ (u"ࠦࡤࡥ࡭ࡢ࡫ࡱࡣࡤࠨࢨ"):
    app = web.application(l1l1l11ll_opy_, globals())
    app.run()
